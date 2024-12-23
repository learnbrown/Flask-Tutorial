import os
from flask import Flask

# 应用工厂
def create_app(testconfig=None):
    app = Flask(__name__, instance_relative_config=True) 
    # instance_relative_config=True 告诉应用配置文件是相对于 instance folder 的相对路径。

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if testconfig == None:
        app.config.from_pyfile('config.py', silent=True)
    else :
        app.config.from_mapping(testconfig)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app