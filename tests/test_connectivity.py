from unittest.mock import Mock, patch

from nio.testing.block_test_case import NIOBlockTestCase

from ..connectivity import PubSubConnectivity


class TestConnectivity(NIOBlockTestCase):

    def get_test_modules(self):
        return super().get_test_modules() | {'communication'}

    def test_connected(self):
        connectivity = PubSubConnectivity()
        # setup mocks
        connectivity.logger = Mock()
        connectivity._connected_event = Mock()
        connectivity._connected_event.wait = Mock(return_value=False)
        connectivity._notify_disconnection = Mock()
        is_connected = Mock(return_value=True)

        with patch(PubSubConnectivity.__module__ + '.Job') as job_patch:
            connectivity.conn_configure(is_connected)
            self.assertTrue(connectivity._connected)
            # no waiting, notification, etc.
            self.assertEqual(connectivity._connected_event.wait.call_count, 0)
            self.assertEqual(connectivity._notify_disconnection.call_count, 0)
            self.assertEqual(job_patch.call_count, 0)

    def test_disconnected_start(self):
        connectivity = PubSubConnectivity()
        # setup mocks
        connectivity.logger = Mock()
        connectivity.status = Mock()
        connectivity._connected_event = Mock()
        connectivity._connected_event.wait = Mock(return_value=False)
        connectivity.notify_management_signal = Mock()
        # not connected during configure
        is_connected = Mock(return_value=False)

        with patch(PubSubConnectivity.__module__ + '.Job') as job_patch:
            job_instance = Mock()
            job_patch.return_value = job_instance
            connectivity.conn_configure(is_connected)
            self.assertFalse(connectivity._connected)
            connectivity._connected_event.wait.assert_called_once()
            connectivity.notify_management_signal.assert_called_once()
            job_patch.assert_called_once()

            # simulate restoring connection
            connectivity.conn_on_connected()
            self.assertTrue(connectivity._connected)
            job_instance.cancel.assert_called_once()
            connectivity._connected_event.set.assert_called_once()
            self.assertEqual(
                connectivity.notify_management_signal.call_count, 2)

            # simulate losing connection
            connectivity.conn_on_disconnected()
            self.assertFalse(connectivity._connected)
            connectivity._connected_event.clear.assert_called_once()
            job_instance.cancel.assert_called_once()
            self.assertEqual(
                connectivity.notify_management_signal.call_count, 3)

            connectivity.conn_stop()
