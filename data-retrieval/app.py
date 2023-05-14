import os

from flask import Flask, Response, jsonify, make_response, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)

api = Api(app, title="Data Retrieval Service Controller", version="0.0.1")

scrape = api.namespace("data-retrieval")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
