# ./app/init.py
from flask import Flask, jsonify


def create_app(test_config=None):

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://usr:pwd@pgsql:5432/medical"

    return app
