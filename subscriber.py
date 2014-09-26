from nio.common.versioning.dependency import DependsOn
from nio.common.discovery import Discoverable, DiscoverableType
from nio.modules.communication.subscriber import Subscriber as NIOSubscriber
from .topics import TopicsBlock


@DependsOn("nio.modules.communication")
@Discoverable(DiscoverableType.block)
class Subscriber(TopicsBlock):

    """ A block for subscribing to a NIO communication channel.

    Functions regardless of communication module implementation.

    Properties:
        signal_type (str): The block will subscribe to channels
            with a matching type.

    """

    def __init__(self):
        super().__init__()
        self._subscriber = None

    def configure(self, context):
        super().configure(context)
        self._subscriber = NIOSubscriber(self.process_signals,
                                         **self._flatten_topics())

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
