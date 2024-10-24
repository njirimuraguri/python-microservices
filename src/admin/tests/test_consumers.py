from unittest.mock import patch
from src.admin.app.consumer import process_order


@patch('app.consumers.send_sms')
def test_process_order(mock_send_sms):
    ch = None
    method = type('obj', (object,), {'delivery_tag': 1})
    properties = None
    body = b'{"phone_number": "+254723262333", "item": "Laptop", "amount": 1000}'

    process_order(ch, method, properties, body)

    mock_send_sms.assert_called_once_with("+254723262333", "Hello! Your order for Laptop worth 1000 has been placed successfully.")  # noqa: E501
