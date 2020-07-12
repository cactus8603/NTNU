from flask import Flask
from model import *
from mongo import *
from mongo import engine

# Create a flask app
app = Flask(__name__)
app.url_map.strict_slashes = False

# Regist flask blueprint
app.register_blueprint(auth_api, url_prefix='/auth')
app.register_blueprint(profile_api, url_prefix='/profile')
app.register_blueprint(search_api, url_prefix='/search')

if Number("User No").obj is None:
    engine.Number(name="User No").save(force_insert=True)

if Number("User data version").obj is None:
    engine.Number(name="User data version").save(force_insert=True)

if Number("Packet interval").obj is None:
    engine.Number(name="Packet interval").save(force_insert=True)

if Boolean("Course taking switch").obj is None:
    engine.Boolean(name="Course taking switch").save(force_insert=True)