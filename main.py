from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
from users import Users
from locations import Locations

app = Flask(__name__)
api = Api(app)

api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')


if __name__ == '__main__':
    app.run()

