from main import get_post_by_id, get_posts_by_user_id
from main import get_post_by_id_with_validation
from unittest.mock import patch, Mock
import pytest


@pytest.mark.parametrize('id', [1, 2, 3])
def test_get_post_by_id(id):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'user_id': id}

    with patch('main.http_get', return_value=mock_response) as mock_http_get:
        assert get_post_by_id(id)
        mock_http_get.assert_called_once_with(f'https://jsonplaceholder.typicode.com/posts/{id}')


@pytest.mark.parametrize('id', [-1, 5, 99])
def test_get_post_by_id_with_validation(id):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'userId': id, 'id': id}

    with patch('main.http_get', return_value=mock_response) as mock_http_get:
        if id <= 0:
            with pytest.raises(ValueError):
                get_post_by_id_with_validation(id)
            mock_http_get.assert_not_called()
        else:
            get_post_by_id_with_validation(id)
            mock_http_get.assert_called_once_with(f'https://jsonplaceholder.typicode.com/posts/{id}')


@pytest.mark.parametrize('id', [1, -1, 99])
def test_get_posts_by_user_id(id):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'userId': id, 'id': id}, {'userId': id, 'id': id}]

    with patch('main.http_get', return_value=mock_response) as mock_http_get:
        assert get_posts_by_user_id(id)
        mock_http_get.assert_called_once_with(f'https://jsonplaceholder.typicode.com/posts?userId={id}')


def test_assert_error():
    try:
        assert 1 == 5
    except AssertionError as e:
        print(e, type(e))