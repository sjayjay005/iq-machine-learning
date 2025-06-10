"""
Unit tests for the API connection module.
"""
import unittest
from unittest.mock import patch, MagicMock

from iqoption_startup.api.connection import connect_to_iqoption

class TestApiConnection(unittest.TestCase):
    """Test cases for the API connection module."""

    @patch('iqoption_startup.api.connection.IQ_Option')
    def test_connect_success(self, mock_iq_option):
        """Test successful connection to IQ Option API."""
        # Setup mock
        mock_api = MagicMock()
        mock_api.connect.return_value = (True, "")
        mock_api.check_connect.return_value = True
        mock_api.get_profile_ansyc.return_value = {"name": "Test User"}
        mock_api.get_balances.return_value = [{"amount": 1000}]
        mock_iq_option.return_value = mock_api

        # Call the function
        result = connect_to_iqoption("test@example.com", "password")

        # Assertions
        self.assertIsNotNone(result)
        mock_iq_option.assert_called_once_with("test@example.com", "password")
        mock_api.connect.assert_called_once()
        mock_api.check_connect.assert_called_once()
        mock_api.get_profile_ansyc.assert_called_once()
        mock_api.get_balances.assert_called_once()

    @patch('iqoption_startup.api.connection.IQ_Option')
    def test_connect_failure(self, mock_iq_option):
        """Test failed connection to IQ Option API."""
        # Setup mock
        mock_api = MagicMock()
        mock_api.connect.return_value = (False, "Invalid credentials")
        mock_iq_option.return_value = mock_api

        # Call the function
        result = connect_to_iqoption("test@example.com", "wrong_password")

        # Assertions
        self.assertIsNone(result)
        mock_iq_option.assert_called_once_with("test@example.com", "wrong_password")
        mock_api.connect.assert_called_once()

    @patch('iqoption_startup.api.connection.IQ_Option')
    def test_connect_check_failure(self, mock_iq_option):
        """Test connection check failure."""
        # Setup mock
        mock_api = MagicMock()
        mock_api.connect.return_value = (True, "")
        mock_api.check_connect.return_value = False
        mock_iq_option.return_value = mock_api

        # Call the function
        result = connect_to_iqoption("test@example.com", "password")

        # Assertions
        self.assertIsNone(result)
        mock_iq_option.assert_called_once_with("test@example.com", "password")
        mock_api.connect.assert_called_once()
        mock_api.check_connect.assert_called_once()

    @patch('iqoption_startup.api.connection.IQ_Option')
    @patch('iqoption_startup.api.connection.time.sleep')
    def test_connect_retry(self, mock_sleep, mock_iq_option):
        """Test connection retry mechanism."""
        # Setup mock
        mock_api = MagicMock()
        # First attempt fails, second succeeds
        mock_api.connect.side_effect = [
            (False, "Network error"),
            (True, "")
        ]
        mock_api.check_connect.return_value = True
        mock_api.get_profile_ansyc.return_value = {"name": "Test User"}
        mock_api.get_balances.return_value = [{"amount": 1000}]
        mock_iq_option.return_value = mock_api

        # Call the function with max_retries=2 to allow for retry
        result = connect_to_iqoption("test@example.com", "password", max_retries=2)

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(mock_iq_option.call_count, 1)
        self.assertEqual(mock_api.connect.call_count, 2)
        mock_sleep.assert_called_once()

if __name__ == '__main__':
    unittest.main()
