# app/__init__.py
from flask import Flask
from flask_login import login_manager, LoginManager
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from app.config import Config

db = MongoEngine()
login_manager = LoginManager()
socketio = SocketIO(ping_timeout=600, ping_interval=10)  # Timeout sürelerini artırın



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['MONGODB_SETTINGS'] = {'db': 'SGS'}
    app.secret_key = 'your_secret_key_here'

    db.init_app(app)  # MongoDB bağlantısını başlat

    # LoginManager'ı uygulamaya kaydediyoruz
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    # Flask-SocketIO'yu başlatıyoruz
    socketio.init_app(app)

    from .main_routes import main_bp
    from app.routes.user_routes import user_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')

    return app

# Flask-Login kullanıcı yükleme fonksiyonu
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.objects(id=user_id).first()
