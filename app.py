import dash
import flask

external_stylesheets = ["assets/1bootstrap.css", "assets/2style.css"]

flask_server = flask.Flask(__name__)

app = dash.Dash(__name__, server=flask_server, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions = True,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

server = app.server