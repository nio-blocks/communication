from nio import Block
from nio import discoverable
from nio.properties import StringProperty
from nio.modules.communication.subscriber import Subscriber as NIOSubscriber


@discoverable
class Subscriber(Block):

    """ A block for subscribing to a NIO communication channel.

    Functions regardless of communication module implementation.

    Properties:
        topic (str): Defines topic to subscribe to in order to receive signals.

    """
    topic = StringProperty(title='Topic')

    def __init__(self):
        super().__init__()
        self._subscriber = None

    def configure(self, context):
        super().configure(context)
        self._subscriber = NIOSubscriber(self.process_signals,
                                         topic=self.topic())

    def start(self):
        """ Start the block by opening the underlying subscriber

        """
        super().start()
        self._subscriber.open()

    def stop(self):
        """ Stop the block by closing the underlying subscriber

        """
        self._subscriber.close()
        super().stop()

    def process_signals(self, signals):
        """ Subscriber block doesn't do any real processing. Just
        passes incoming signals along to any receivers.

        """
        self.notify_signals(signals)
