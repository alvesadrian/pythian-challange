from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import xmltodict
import requests
#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder


app = Flask(__name__)
api = Api(app)
class CatAPI(Resource):
    def get(self):
        response = requests.get('http://thecatapi.com/api/images/get?api_key=[YOUR-API-KEY]&format=xml&results_per_page=1')
        return xmltodict.parse(response.content)['response']['data']['images']


class HistoryAPI(Resource):
    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient

api.add_resource(CatAPI, '/cat')
api.add_resource(HistoryAPI, '/history')

if __name__ == '__main__':
     app.run()
