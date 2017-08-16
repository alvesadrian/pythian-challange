import flask
import flask_restful
import json
import redis
import requests
import xmltodict


app = flask.Flask(__name__)
app.debug = True
api = flask_restful.Api(app)

redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)


class CatsAPI(flask_restful.Resource):

    def get(self):
        response = requests.get('http://thecatapi.com/api/images/get?format=xml&results_per_page=1')
        data = xmltodict.parse(response.content)['response']['data']['images']
        redis_db.rpush('cat', json.dumps(data['image']))
        return data


class HistoryAPI(flask_restful.Resource):

    def get(self):
        history = redis_db.lrange('cat', 0, -1)
        return {'images': [json.loads(item.decode('utf8')) for item in history]}


api.add_resource(CatsAPI, '/cat')
api.add_resource(HistoryAPI, '/history')


if __name__ == '__main__':
    app.run()
