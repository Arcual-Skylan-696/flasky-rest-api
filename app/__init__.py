from flask import Flask
# from flask_bootstrap import Bootstrap  <-- 🔹 BINAGO: Nilagyan ng # sa unahan
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_mysqldb import MySQL  # 🔹 1. Added MySQL Import
from config import config

# bootstrap = Bootstrap()  <-- 🔹 BINAGO: Nilagyan ng # sa unahan
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
mysql = MySQL()  # 🔹 2. Initialize the Global MySQL Object

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # bootstrap.init_app(app)  <-- 🔹 BINAGO: Nilagyan ng # sa unahan
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    mysql.init_app(app)  # 🔹 3. Bind MySQL to the App Factory

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app