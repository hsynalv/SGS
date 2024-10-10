# app/__init__.py
from flask import Flask
from flask_socketio import SocketIO

# app/__init__.py dosyasında timeout süresini artırın
socketio = SocketIO(ping_timeout=600, ping_interval=10)  # Timeout sürelerini artırın


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'

    # Flask-SocketIO'yu başlatıyoruz
    socketio.init_app(app)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
