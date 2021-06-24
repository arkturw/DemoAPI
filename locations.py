from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast


class Locations(Resource):

    def get(self):
        data = pd.read_csv('locations.csv')
        return {'data': data.to_dict()}, 200


    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('locationId', required=True, type=int)
        parser.add_argument('name', required=True)
        parser.add_argument('rating', required=True, type=float)

        args = parser.parse_args()

        data = pd.read_csv('locations.csv')

        print(args['locationId'])
        print(list(data['locationId']))

        if args['locationId'] in list(data['locationId']):
            return {
                'message': f"'{args['locationId']}' already exists."
            }, 409
        else:
            new_data = pd.DataFrame({
                'locationId': [args['locationId']],
                'name': [args['name']],
                'rating': [args['rating']]
            })

            data = data.append(new_data, ignore_index=True)
            data.to_csv('locations.csv', index=False)
            return {'data': data.to_dict()}, 200


    def patch(self):
        parser = reqparse.RequestParser()

        parser.add_argument('locationId', required=True, type=int)
        parser.add_argument('name', store_missing=False)
        parser.add_argument('rating', store_missing=False, type=float)

        args = parser.parse_args()

        data = pd.read_csv('locations.csv')

        if args['locationId'] in list(data['locationId']):
            user_data = data[data['locationId'] == args['locationId']]

            if 'name' in args:
                user_data['name'] = args['name']
            if 'rating' in args:
                user_data['rating'] = args['rating']

            data[data['locationId'] == args['locationId']] = user_data
            data.to_csv('locations.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                'message': f"'{args['locationId']}' does not exist."
            }, 404


    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument('locationId', required=True, type=int)

        args = parser.parse_args()

        data = pd.read_csv('locations.csv')

        if args['locationId'] in list(data['locationId']):
            data = data[data['locationId'] != args['locationId']]
            data.to_csv('locations.csv', index=False)
            return {'data': data.to_dict()}, 200

        else:
            return {
                'message': f"'{args['locationId']}' location does not exist."
            }, 404
