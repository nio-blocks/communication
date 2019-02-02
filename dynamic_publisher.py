from collections import defaultdict
from datetime import datetime
from threading import Lock
from time import time

from nio import TerminatorBlock, Block
from nio.modules.communication.publisher import Publisher as NioPublisher
from nio.modules.communication.publisher import PublisherError
from nio.modules.scheduler import Job
from nio.properties import StringProperty, TimeDeltaProperty, VersionProperty

from .connectivity import PubSubConnectivity

class DynamicPublisher(PubSubConnectivity, TerminatorBlock):
    version = VersionProperty("0.1.0")
    topic = StringProperty(title="Topic", default="")

    ttl = TimeDeltaProperty(title="Time-to-live",
                            advanced=True,
                            order=0,
                            default=dict(seconds=10))
    interval = TimeDeltaProperty(title="Teardown Interval",
                                 advanced=True,
                                 default=dict(seconds=1),
                                 order=1)
    def __init__(self):
        super().__init__()
        self._cache = dict()
        self._cache_lock = Lock()
        self._job = None

    def start(self):
        self._job = Job(
            self._cleanup,
            self.interval(),
            True,
        )

    def _cleanup(self):
        now = time()
        ttl = self.ttl().total_seconds()

        with self._cache_lock:
            expired_topics = []
            for topic in self._cache.keys():
                _, prev = self._cache[topic]

                if now - prev > ttl:
                    expired_topics.append(topic)

            for topic in expired_topics:
                self.logger.info('removing expired publisher for ' + topic)
                pub, _ = self._cache[topic]
                pub.close()
                del self._cache[topic]


    def process_signals(self, in_signals):
        """ Publish each list of signals """

        groups = defaultdict(list)
        for signal in in_signals:
            try:
                topic = self.topic(signal)
            except:
                self.logger.error('topic expression failed, ignoring signal')
                continue
            groups[topic].append(signal)


        for topic in groups:
            try:
                out_signals = groups[topic]
                self._get_publisher(topic).send(out_signals)
            except PublisherError:  # pragma no cover
                self.logger.exception("Error publishing " + len(out_signals) + " signals to " + topic)

    def _get_publisher(self, topic):
        now = time()

        with self._cache_lock:
            if topic in self._cache:
                publisher, _ = self._cache[topic]
                self._cache[topic] = (publisher, now)
                return publisher

            self.logger.info('creating new publisher for ' + topic)
            publisher = NioPublisher(topic=topic)

            try:
                publisher.open(on_connected=self.conn_on_connected,
                               on_disconnected=self.conn_on_disconnected)
            except TypeError as e:
                self.logger.warning(
                    "Connecting to an outdated communication module")
                # try previous interface
                publisher.open()
                # no need to configure connectivity if not supported
                return

            self.conn_configure(publisher.is_connected)
            self._cache[topic] = (publisher, now)
            return publisher


