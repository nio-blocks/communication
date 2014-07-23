from nio.configuration import Configuration
from nioext.extensions.components.communication.manager import CommManager
from nio.core.context import InitContext
from communication.publisher import Publisher
from communication.subscriber import Subscriber
from nio.modules.communication.zmq.tests import OPEN_CLOSE_SLEEP_WAIT
from nio.modules.threading import sleep
from nio.util.attribute_dict import AttributeDict
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.modules.communication import CommunicationModule


MATCHING = 'nio.modules.communication.matching.default.DefaultMatching'


class TestPubSub(NIOBlockTestCase):
    def setUp(self):
        super().setUp()
        self._comm_manager = CommManager()
        self._comm_manager.configure(InitContext([], Configuration.empty()))
        self._comm_manager.start()
        sleep(OPEN_CLOSE_SLEEP_WAIT)
        self._configuration = AttributeDict(
            {"communication": "zmq",
             "matching": MATCHING,
             "xpub_url": self._comm_manager.xpub_url,
             "xsub_url": self._comm_manager.xsub_url,
             "ZMQ_MAX_IO_THREAD_COUNT": 1})

    def tearDown(self):
        self._comm_manager.stop()
        super().tearDown()

    def test_pub_sub(self):
        pub = Publisher()
        sub = Subscriber()

        self.configure_block(pub, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['foobar']}
            ]
        })

        self.configure_block(sub, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['foobar']}
            ]
        })

        CommunicationModule.module_init(self._configuration)
        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub.start()
        sub.start()
        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub.process_signals([1, 2, 3, 4])
        sleep(0.1)

        self.assert_num_signals_notified(4, sub)

        pub.stop()
        sub.stop()
        CommunicationModule.module_finalize()

    def test_ignore_other_types(self):
        pub1 = Publisher()
        pub2 = Publisher()
        sub = Subscriber()

        self.configure_block(pub1, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['bazqux']}
            ]
        })
        self.configure_block(pub2, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['foobar']}
            ]
        })
        self.configure_block(sub, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['bazqux']}
            ]
        })

        CommunicationModule.module_init(self._configuration)
        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub1.start()
        pub2.start()
        sub.start()
        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub1.process_signals([1, 2, 3, 4])
        pub2.process_signals(['a', 'b', 'c', 'd'])
        sleep(0.1)

        self.assert_num_signals_notified(4, sub)

        pub1.stop()
        pub2.stop()
        sub.stop()

        CommunicationModule.module_finalize()

    def test_subscribe_partial_match(self):
        pub = Publisher()
        sub1 = Subscriber()
        sub2 = Subscriber()
        sub3 = Subscriber()

        self.configure_block(pub, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['foobar']},
                {"keyword": "source",
                 "rule": ['A']}
            ]
        })

        self.configure_block(sub1, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['foobar', 'bazqux']}
            ]
        })

        self.configure_block(sub2, {
            "criteria": [
                {"keyword": "source",
                 "rule": ['A']}
            ]
        })

        self.configure_block(sub3, {
            "criteria": [
                {"keyword": "type",
                 "rule": ['fail']},
                {"keyword": "source",
                 "rule": ['B']}
            ]
        })

        CommunicationModule.module_init(self._configuration)
        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub.start()
        sub1.start()
        sub2.start()
        sub3.start()
        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub.process_signals([1, 2, 3, 4])
        sleep(0.1)

        self.assert_num_signals_notified(4, sub1)
        self.assert_num_signals_notified(4, sub2)
        self.assert_num_signals_notified(0, sub3)

        pub.stop()
        sub1.stop()
        sub2.stop()
        sub3.stop()
        CommunicationModule.module_finalize()
