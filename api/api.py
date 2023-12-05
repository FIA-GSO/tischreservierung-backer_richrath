import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
from routes.client_api import client_blueprint
from routes.kellner_api import kellner_blueprint

def init_app():
    @app.route('/', methods=['GET'])
    def home():
        return "<h1>Tischreservierung</h1>"



def create_app():
    DATABASE = './freieTische.db'

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message
    app.register_blueprint(client_blueprint, url_prefix='/api/v1/client') # Registriere den Client-Blueprint
    app.register_blueprint(kellner_blueprint, url_prefix='/api/v1/kellner') # Registriere den Kellner-Blueprint
    
    init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()