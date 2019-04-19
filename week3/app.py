#!/usr/bin/env python
# app.py - a minimal flask api using flask_restful
from flask import Flask
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        SERVICE_NAMESPACE=os.environ.get("SERVICE_NAMESPACE")
        return {'hello': 'world', 'namespace':SERVICE_NAMESPACE}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
