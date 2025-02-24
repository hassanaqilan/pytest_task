from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError

from main import (get_post_by_id, get_post_by_id_with_validation,
                  get_posts_by_user_id)

BASE_URL = 'https://jsonplaceholder.typicode.com'


@pytest.mark.parametrize('id', [1, 2, 3])
def test_get_post_by_id(id):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'user_id': id}
    with patch('main.http_get', return_value=mock_response) as mock_http_get:
        assert get_post_by_id(id)
        mock_http_get.assert_called_once_with(f'{BASE_URL}/posts/{id}')


def test_get_post_by_id_with_validation(mocker):
    # test for success
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'id': 1}
    mocker.patch('main.http_get', return_value=mock_response)
    assert get_post_by_id_with_validation(1) == {'id': 1}

    mocker.patch("main.http_get", side_effect=HTTPError("HTTP Error"))
    assert get_post_by_id_with_validation(1) is None
    with pytest.raises(ValueError, match='post_id must be greater than 0'):
        get_post_by_id_with_validation(-1)


@pytest.mark.parametrize('id', [1, -1, 99])
def test_get_posts_by_user_id(id):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'userId': id, 'id': id}]

    with patch('main.http_get', return_value=mock_response) as mock_http_get:
        assert get_posts_by_user_id(id)
        mock_http_get.assert_called_once_with(f'{BASE_URL}/posts?userId={id}')


def test_assert_error():
    try:
        assert 1 == 5
    except AssertionError as e:
        print(e, type(e))
