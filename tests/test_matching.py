from unittest.mock import patch
from ..subscriber import Subscriber
from nio.testing.block_test_case import NIOBlockTestCase


class TestMatching(NIOBlockTestCase):

    def test_loose_matching_override(self):
        """ asserts that matching algorithm can be specified as a
        subscriber property, and thus it is applied accordingly.

        It does so by having two subscribers with different matching
        algorithms
        """
        sub_loose = Subscriber()
        sub_default = Subscriber()

        with patch("{}.NIOSubscriber".format(Subscriber.__module__)) as sub:
            # loose matching satisfied criteria
            loose_matching = ("nio.modules.communication"
                              ".matching.loose.LooseMatching")
            self.configure_block(sub_loose, {
                "criteria": [
                    {"keyword": "type", "rule": ['A']},
                    {"keyword": "source", "rule": ['C', 'D']}
                ],
                "matching_provider": loose_matching
            })
            self.assertEqual(sub.call_args[1]['matching_provider'],
                             loose_matching)
            sub.reset_mock()

            # default not-matching satisfied criteria
            self.configure_block(sub_default, {
                "criteria": [
                    {"keyword": "type", "rule": ['A']},
                    {"keyword": "source", "rule": ['C', 'D']}
                ]
            })
            # Matching shouldn't be provided
            self.assertEqual(sub.call_args[1]['matching_provider'], '')
