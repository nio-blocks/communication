from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.modules.communication.imports import Publisher as NIOPublisher
from nio.common.block.criteria import CriteriaBlock


@Discoverable(DiscoverableType.block)
class Publisher(CriteriaBlock):
    """ A block for publishing to a NIO communication channel.

    Functions regardless of communication module implementation.

    Properties:
        signal_type (str): Subscribers will receive published messages
            if their specified signal type matches.

    """
    def __init__(self):
        super().__init__()
        self._publisher = None

    def configure(self, context):
        super().configure(context)
        self._publisher = NIOPublisher(**self._flatten_criteria())

    def start(self):
        """ Start the block by opening the underlying publisher

        """
        super().start()
        self._publisher.open()

    def stop(self):
        """ Stop the block by closing the underlying publisher

        """
        self._publisher.close()
        super().stop()

    def process_signals(self, signals):
        """ Publisher block doesn't do any real processing, just publishes
        the signals it processes.

        """
        self._publisher.send(signals)
