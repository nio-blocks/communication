from threading import RLock, Event

from nio.properties import TimeDeltaProperty
from nio.modules.scheduler import Job
from nio.signal.status import BlockStatusSignal
from nio.util.runner import RunnerStatus


class PubSubConnectivity(object):
    """ Adds connectivity awareness to pubsub blocks
    """
    timeout = TimeDeltaProperty(title='Connect Timeout',
                                default={'seconds': 2},
                                advanced=True)

    def __init__(self):
        super().__init__()
        self._connected = None
        self._connected_lock = RLock()
        self._timeout_job = None
        self._status_set = {RunnerStatus.warning: False,
                            RunnerStatus.error: False}
        self._connected_event = Event()

    def conn_configure(self, is_connected):
        """ Sets up instance for connectivity checks

        Args:
            is_connected (callable): function to invoke to establish initial
                connectivity status
        """
        with self._connected_lock:
            self._connected = is_connected()
            self.logger.info("Starting in: '{}' state".format(
                "connected" if self._connected else "disconnected"))

        if not self._connected:
            # per spec, hold the configure method hoping to get connected
            if not self._connected_event.wait(self.timeout().total_seconds()):
                self._notify_disconnection(RunnerStatus.warning)
                # start changed to error status notification countdown
                self._timeout_job = Job(self._notify_disconnection,
                                        self.timeout(), False,
                                        RunnerStatus.error)

    def conn_stop(self):
        # cancel existing timeout job if any
        if self._timeout_job:
            self._timeout_job.cancel()  # pragma no cover

    def conn_on_connected(self):
        # remove any possible wait for on_connected event
        self._connected_event.set()

        with self._connected_lock:
            self._connected = True

        # cancel existing timeout job if any
        if self._timeout_job:
            self._timeout_job.cancel()

        # if there was a warning or error status formerly notified then
        # notify "recovery"
        if self._clear_former_status():
            # notify status change
            signal = BlockStatusSignal(RunnerStatus.started,
                                       message="Block is connected")
            self.notify_management_signal(signal)

    def conn_on_disconnected(self):
        self._connected_event.clear()
        with self._connected_lock:
            self._connected = False
        self._notify_disconnection(RunnerStatus.warning)

    def _notify_disconnection(self, status_to_report):
        self._clear_former_status()

        with self._connected_lock:
            # double check that we are disconnected before notifying
            if not self._connected:
                signal = BlockStatusSignal(status_to_report,
                                           message="Block is not connected")
                self.notify_management_signal(signal)
                # add intended block status
                self.status.add(status_to_report)
                self._status_set[status_to_report] = True

                self._timeout_job = None

    def _clear_former_status(self):
        status_cleared = False
        for status in self._status_set:
            if self._status_set[status]:
                # remove block status previously added
                self.status.remove(status)
                self._status_set[status] = False
                status_cleared = True
                break
        return status_cleared
