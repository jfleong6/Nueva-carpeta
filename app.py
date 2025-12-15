from flask import Flask, jsonify, render_template
from flask_cors import CORS
from routes.hotel import *  # Asegúrate de que esté importando bien

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita CORS si usas frontend separado

    # Configuración general
    app.config['JSON_AS_ASCII'] = False
    app.config['JSON_SORT_KEYS'] = False

    # Registrar Blueprints
    app.register_blueprint(hotel_bp)

    @app.route('/')
    def home():
        return render_template("home.html")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

