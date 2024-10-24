from unittest.mock import patch
from src.admin.app.consumer import send_sms


@patch('app.consumers.sms.send')
def test_send_sms(mock_send):
    phone_number = "+254723262333"
    message = "Your order has been placed!"

    # Call the send_sms function
    send_sms(phone_number, message)

    mock_send.assert_called_once_with(message, [phone_number], sender="TC4A")
