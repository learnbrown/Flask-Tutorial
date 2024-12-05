import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING':True,
        'DATABASE':db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

        yield app

        os.close(db_fd)
        os.unlink(db_fd)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# 对于大多数视图，用户需要登录。在测试中最方便的方法是使用客户端制作一个 POST 请求发送给 login 视图。
# 与其每次都写一遍，不如写一个类，用 类的方法来做这件事，并使用一个固件把它传递给每个测试的客户端。

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
            'auth/login',
            data={'username':username, 'password':password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')
    
@pytest.fixture
def auth(client):
    return AuthActions(client)