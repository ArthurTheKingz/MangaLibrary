from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_uploads import UploadSet, IMAGES, configure_uploads
from config import config, Config
from flask_limiter import Limiter
from .celery import make_celery
from celery import Celery

db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Пожалуйста, войдите на сайт, чтобы получить доступ к этой странице."
login_manager.login_message_category = 'info'
mail = Mail()
limiter = Limiter()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

users_upload = UploadSet('users', IMAGES)
manga_upload = UploadSet('manga', IMAGES)
news_upload = UploadSet('news', IMAGES)

def create_app(config_name, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    limiter.init_app(app)
    configure_uploads(app, (users_upload, manga_upload, news_upload))


    from .auth import auth
    from .comment import comment
    from .errors import errors
    from .main import main
    from .manga import manga
    from .news import news
    from .user import user

    for blueprint in [auth, comment, errors, main, manga, news, user]:
        app.register_blueprint(blueprint)

    if kwargs.get('celery'):
        make_celery(kwargs.get('celery'), app)

    return app
