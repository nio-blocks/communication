from nio import Block
from nio import discoverable
from nio.modules.communication.publisher import Publisher as NIOPublisher
from nio.modules.communication.publisher import PublisherError
from nio.properties import StringProperty


@discoverable
class Publisher(Block):

    """ A block for publishing to a NIO communication channel.

    Functions regardless of communication module implementation.

    Properties:
        topic (str): Defines topic to use to publish signals.

    """
    topic = StringProperty(title='Topic')

    def __init__(self):
        super().__init__()
        self._publisher = None

    def configure(self, context):
        super().configure(context)
        self._publisher = NIOPublisher(self.topic())
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
        try:
            self._publisher.send(signals)
        except PublisherError:
            self.logger.exception("Error publishing signals")
