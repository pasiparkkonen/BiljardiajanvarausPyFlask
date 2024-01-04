# Initializing flask application
import flask

app = flask.Flask(__name__, static_url_path='/applicationfiles/static')

from applicationfiles import views