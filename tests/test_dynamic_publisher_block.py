from unittest.mock import patch, Mock

from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase

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
        publisher = DynamicPublisher()
        topic = "topic.{{ $sig }}"

        foo_pub = Mock()
        bar_pub = Mock()
        baz_pub = Mock()

        with patch(DynamicPublisher.__module__ + '.Publisher', side_effect=[foo_pub, bar_pub, baz_pub]) as pub:
            self.configure_block(publisher, {"topic": topic})
            publisher.start()

            signals = [
                Signal(dict(sig="foo", val=1)),
                Signal(dict(sig="bar", val=2)),
                Signal(dict(sig="baz", val=3)),
                Signal(dict(sig="foo", val=4)),
                Signal(dict(sig="bar", val=5)),
                Signal(dict(sig="foo", val=6)),
            ]
            publisher.process_signals(signals)

            pub.assert_any_call(topic="topic.foo")
            pub.assert_any_call(topic="topic.bar")
            pub.assert_any_call(topic="topic.baz")

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
