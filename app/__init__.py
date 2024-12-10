from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuraciones (puedes agregar más adelante)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Registrar rutas
    from .routes import main
    app.register_blueprint(main)

    return app

