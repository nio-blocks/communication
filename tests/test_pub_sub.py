from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..publisher import Publisher as Publisher
from ..subscriber import Subscriber as Subscriber


class TestPubSub(NIOBlockTestCase):

    def get_test_modules(self):
        return super().get_test_modules() | {'communication'}

    def test_publisher(self):
        publisher = Publisher()

        # assert that it needs to be configured
        with self.assertRaises(AttributeError):
            publisher.process_signals([Signal()])

        topic = "test_topic"
        self.configure_block(publisher, {"topic": topic})
        # assert that topic property value is now available
        self.assertEqual(publisher.topic(), topic)

        publisher.start()
        # now it can process signals
        publisher.process_signals([Signal()])
        publisher.stop()

    def test_subscriber(self):
        subscriber = Subscriber()

        topic = "test_topic"
        self.configure_block(subscriber, {"topic": topic})
        # assert that topic property value is now available
        self.assertEqual(subscriber.topic(), topic)

        subscriber.start()
        subscriber.stop()
