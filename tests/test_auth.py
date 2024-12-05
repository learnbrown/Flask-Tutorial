import pytest
from flask import g, session
from flaskr.db import get_db


# client.get() 制作一个 GET 请求并 由 Flask 返回 Response 对象。
# 类似的 client.post() 制作一个 POST 请求， 转换 data 字典为表单数据。

# 为了测试页面是否渲染成功，制作一个简单的请求，并检查是否返回 一个 200 OK status_code 。
# 如果渲染失败， Flask 会返回一个 500 Internal Server Error 代码。

# 当注册视图重定向到登录视图时， headers 会有一个包含登 录 URL 的 Location 头部。

# data 以字节方式包含响应的身体。如果想要检测渲染页面中 的某个值，请在 data 中检测。
# 字节值只能与字节值作比较，如果想比较文 本，请使用 get_data(as_text=True) 。
def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username':'a', 'password':'a'}
    )
    assert response.header["Location"] == '/auth/login'

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

# pytest.mark.parametrize 告诉 Pytest 以不同的参数运行同一个测试。
# 这里用于测试不同的非法输入和出错信息，避免重复写三次相同的代码。
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username':username, 'password':password}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == '/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'), 
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

