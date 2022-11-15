from pydantic import BaseSettings
from sanic import Sanic, response
from pathlib import Path
import sys
import pytest
from sanic import Sanic
from tests.settings_test import AppSettings, FirstUser
from src.core.enums import AuthUrls


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
from src.server import create_app

# @pytest.fixture(scope='module')
# def admin() -> Sanic:
#     app = create_app(AppSettings, FirstUser)
#     yield app
#     print('******TEARDOWN******')


@pytest.fixture(scope='module')
def app() -> Sanic:
    app = create_app(AppSettings, FirstUser)
    yield app
    db = BASE_DIR / 'db.sqlite'
    db.unlink()

def test_basic_test_client(app: Sanic):
    request, response = app.test_client.get('/')
    assert response.status == 404

def test_get_login_url(app: Sanic):
    _, response_empty = app.test_client.post(AuthUrls.LOGIN)
    _, response_body = app.test_client.post(
        AuthUrls.LOGIN,
        json = {
            'username': 'TestUser',
            'password': 12345678
        }
    )
    assert response_empty.status == 400
    assert response_body.status == 200


# def test_activathion_link(app: Sanic):
#     _, response = app.test_client.post(AuthUrls.LOGIN)
#     assert response.status == 200

def test_authetication(app: Sanic):
    _, response_empty = app.test_client.post(
        AuthUrls.AUTH,
        json = {'username': FirstUser.username, 'password': FirstUser.password}
    )
    assert response_empty.status == 200
