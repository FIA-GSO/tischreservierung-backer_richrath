import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
from api.routes.client_api import client_blueprint
from api.routes.kellner_api import kellner_blueprint

DATABASE = 'C:\Users\fclen\Documents\Berufsschule\FU1\tischreservierung-backer_richrath\api\schema.sql'

app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

@app.route('/', methods=['GET'])
def home():
    return "<h1>Tischreservierung</h1>"

app.register_blueprint(client_blueprint, url_prefix='/client')
app.register_blueprint(kellner_blueprint, url_prefix='/kellner')

app.run()