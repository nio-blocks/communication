from collections import defaultdict
from unittest.mock import patch, Mock
from threading import Event

from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from nio.util.discovery import not_discoverable

from ..dynamic_publisher import DynamicPublisher


class TestDynamicPublisher(NIOBlockTestCase):

    def test_creating_a_publisher(self):
        publisher = DynamicPublisher()
        topic = "topic.{{ $sig }}"

        with patch(DynamicPublisher.__module__ + '.Publisher') as pub:
            self.configure_block(publisher, {"topic": topic})
            publisher.start()

            pub.assert_not_called()

            signals = [Signal(dict(sig="foo"))]
            publisher.process_signals(signals)

            pub.assert_called_once_with(topic="topic.foo")
            self.assertEqual(pub.return_value.open.call_count, 1)
            pub.return_value.send.assert_called_once_with(signals)

            publisher.stop()
            pub.return_value.close.assert_called_once_with()

    def test_creating_multiple_publishers(self):
        publisher = DynamicPublisher()
        topic = "topic.{{ $sig }}"

        with patch(DynamicPublisher.__module__ + '.Publisher') as pub:
            self.configure_block(publisher, {"topic": topic})
            publisher.start()

            pub.assert_not_called()

            signals = [Signal(dict(sig="foo"))]
            publisher.process_signals(signals)

            pub.assert_called_once_with(topic="topic.foo")
            self.assertEqual(pub.return_value.open.call_count, 1)
            pub.return_value.send.assert_called_once_with(signals)

            pub.reset_mock()

            signals = [Signal(dict(sig="bar"))]
            publisher.process_signals(signals)

            pub.assert_called_once_with(topic="topic.bar")
            self.assertEqual(pub.return_value.open.call_count, 1)
            pub.return_value.send.assert_called_once_with(signals)

            publisher.stop()
            self.assertEqual(pub.return_value.close.call_count, 2)

    def test_reusing_pubs(self):
        publisher = DynamicPublisher()
        topic = "topic.{{ $sig }}"

        with patch(DynamicPublisher.__module__ + '.Publisher') as pub:
            self.configure_block(publisher, {"topic": topic})
            publisher.start()

            pub.assert_not_called()

            signals = [Signal(dict(sig="foo", val=1))]
            publisher.process_signals(signals)

            pub.assert_called_once_with(topic="topic.foo")
            self.assertEqual(pub.return_value.open.call_count, 1)
            pub.return_value.send.assert_called_with(signals)

            signals = [Signal(dict(sig="foo", val=2))]
            publisher.process_signals(signals)

            self.assertEqual(pub.return_value.open.call_count, 1)
            pub.return_value.send.assert_called_with(signals)

    def test_partitioning(self):
        block = DynamicPublisher()

        publishers = defaultdict(lambda: Mock())
        with patch(DynamicPublisher.__module__ + '.Publisher', side_effect=lambda topic: publishers[topic]) as pub:
            self.configure_block(block, {"topic": "topic.{{ $sig }}"})
            block.start()

            signals = [
                Signal(dict(sig="foo", val=1)),
                Signal(dict(sig="bar", val=2)),
                Signal(dict(sig="baz", val=3)),
                Signal(dict(sig="foo", val=4)),
                Signal(dict(sig="bar", val=5)),
                Signal(dict(sig="foo", val=6)),
            ]
            block.process_signals(signals)

            self.assertEqual(pub.call_count, 3)
            pub.assert_any_call(topic="topic.foo")
            pub.assert_any_call(topic="topic.bar")
            pub.assert_any_call(topic="topic.baz")

            foo_pub = publishers.get("topic.foo")
            bar_pub = publishers.get("topic.bar")
            baz_pub = publishers.get("topic.baz")

            foo_pub.send.assert_called_once_with([
                Signal(dict(sig="foo", val=1)),
                Signal(dict(sig="foo", val=4)),
                Signal(dict(sig="foo", val=6)),
            ])

            bar_pub.send.assert_called_once_with([
                Signal(dict(sig="bar", val=2)),
                Signal(dict(sig="bar", val=5)),
            ])

            baz_pub.send.assert_called_once_with([
                Signal(dict(sig="baz", val=3)),
            ])

    @not_discoverable
    class EventDynamicPublisher(DynamicPublisher):

        def __init__(self, event):
            super().__init__()
            self._event = event

        def emit(self, reset=False):
            super().emit(reset)
            self._event.set()
            self._event.clear()

    def test_closing(self):
        event = Event()
        with patch(DynamicPublisher.__module__ + '.Publisher') as pub:
            block = TestDynamicPublisher.EventDynamicPublisher(event)
            self.configure_block(block, dict(
                topic="topic.{{ $sig }}",
                ttl=dict(milliseconds=200),
            ))

            block.start()
            block.process_signals([Signal(dict(sig="foo"))])
            pub.assert_called_once_with(topic="topic.foo")
            pub.return_value.close.assert_not_called()

            event.wait(.3)

            self.assertEqual(pub.return_value.close.call_count, 1)

    @patch(DynamicPublisher.__module__ + '.Publisher')
    def test_never_expiring(self, publisher):
        block = DynamicPublisher()
        topic = "topic.{{ $sig }}"

        self.configure_block(block, dict(
            topic=topic,
            ttl=dict(seconds=-1),
        ))

        block.start()
        self.assertEqual(publisher.call_count, 0)
        block.process_signals([Signal(dict(sig="foo"))])

        # should create the correct topic
        publisher.assert_called_once_with(topic="topic.foo")

        _, job = block._cache["topic.foo"]
        self.assertIsNone(job)
