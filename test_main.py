from main import get_post_by_id, get_posts_by_user_id
from main import get_post_by_id_with_validation
import pytest
from unittest.mock import patch
from unittest import mock

@pytest.mark.parametrize("id", [
    (1),
    (2),
    (3)
])
def test_get_post_by_id(id):

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"user_id": id}

    with patch("main.http_get", return_value=mock_response):
        assert get_post_by_id(id) == {"user_id": id}

@pytest.mark.parametrize("id", [
    (-1),
    (5),
    (99)
])
def test_get_post_by_id_with_validation(id):

    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'userId': id, 'id': id}

    with patch("main.http_get", return_value=mock_response):
        if id <= 0:
            with pytest.raises(ValueError):
                get_post_by_id_with_validation(id)
        else:
            assert get_post_by_id_with_validation(id) == {'userId': id, 'id': id}


@pytest.mark.parametrize("id", [
    (1),
    (-1),
    (99)
])
def test_get_posts_by_user_id(id):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{'userId': id, 'id': id}, {'userId': id, 'id': id}]
    with patch("main.http_get", return_value=mock_response):
        assert get_posts_by_user_id(id) == [{'userId': id, 'id': id}, {'userId': id, 'id': id}]
