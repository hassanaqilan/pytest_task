import pytest
from main import fetch_data
from unittest.mock import patch, Mock


@pytest.fixture
def mock_request():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'name': 'Hassan'}
    
    with patch('main.http_get', return_value=mock_response) as mock_get:
        yield mock_get 
    
    print('\nTeardown: Mock completed')


def test_fetch_data(mock_request):
    url = 'test'
    result = fetch_data(url)
    
    assert result == {'name': 'Hassan'}
    mock_request.assert_called_once_with(url)