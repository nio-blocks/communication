from ..publisher import Publisher
from ..subscriber import Subscriber
from nio.modules.threading import sleep
from nio.util.attribute_dict import AttributeDict
from nioext.util.support.block_test_case import NIOExtBlockTestCase


OPEN_CLOSE_SLEEP_WAIT = 1


class TestMatching(NIOExtBlockTestCase):

    def get_test_modules(self):
        return super().get_test_modules() + ['communication']
    
    def setUp(self):
        super().setUp()
        sleep(OPEN_CLOSE_SLEEP_WAIT)
        self._configuration = AttributeDict(
            {"xpub_port": 9000,
             "xsub_port": 9001})

    def test_loose_matching_override(self):
        """ asserts that matching algorithm can be specified as a
        subscriber property, and thus it is applied accordingly.

        It does so by having two subscribers with different matching
        algorithms
        """
        pub = Publisher()
        sub_loose = Subscriber()
        sub_default = Subscriber()

        self.configure_block(pub, {
            "criteria": [
                {"keyword": "type", "rule": ['A']},
                {"keyword": "source", "rule": ['C', 'G']}
            ]
        })

        # the criteria above is the same for both subscribers, the
        # difference resides int he matching algorithm

        # loose matching satisfied criteria
        self.configure_block(sub_loose, {
            "criteria": [
                {"keyword": "type", "rule": ['A']},
                {"keyword": "source", "rule": ['C', 'D']}
            ],
            "matching_provider": "nio.modules.communication.matching."
                                 "loose.LooseMatching"
        })

        # default not-matching satisfied criteria
        self.configure_block(sub_default, {
            "criteria": [
                {"keyword": "type", "rule": ['A']},
                {"keyword": "source", "rule": ['C', 'D']}
            ]
        })

        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub.start()
        sub_loose.start()
        sub_default.start()
        sleep(OPEN_CLOSE_SLEEP_WAIT)

        pub.process_signals([1, 2, 3, 4])
        sleep(0.1)

        # assert that subscriber with loose algorithm received events
        self.assert_num_signals_notified(4, sub_loose)
        # assert that subscriber with default algorithm did NOT receive events
        self.assert_num_signals_notified(0, sub_default)

        pub.stop()
        sub_loose.stop()
        sub_default.stop()
