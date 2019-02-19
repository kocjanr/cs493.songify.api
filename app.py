#source env/bin/activate

from flask import Flask, request
from flask_restful import Resource, Api
import boto3
from boto3.dynamodb.conditions import Key, Attr
import requests
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)


class API(Resource):
    def get(self):
        if request.method == 'GET':
            id = request.args.get('id')
            return{'this': id}

        return{'this': 'that'}


class Artists(Resource):
    def get(self):
        if request.method == 'GET':
            id = request.args.get('id')
            return{'artists': id}


class Song(Resource):
    def get(self):
        if request.method == 'GET':
            songTitle = request.args.get('song')

            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Music')
            response = table.scan(
                FilterExpression= Attr('SongTitle').eq(songTitle)
            )

            item = response['Items']
            if not item:
                return {'song':'Not found'}           
            
            return item


class Genres(Resource):
    def get(self):
        if request.method == 'GET':
            dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
            table = dynamodb.Table('Music')

            response = table.scan()
            items = response['Items']

            if not items:
                return{'Generes': 'None'}

            genres = []
            for s in items:
                genres.append(s['Genre'])

            return{'Genres': genres}


class Albums(Resource):
    def get(self):
        if request.method == 'GET':
            songTitle = request.args.get('song')
            return{'Song Title': songTitle}


class Songs(Resource):
    def get(self):
        if request.method == 'GET':
            id = request.args.get('id')
            return{'artists': id}


api.add_resource(API, '/')
api.add_resource(Artists, '/artists/by/genre')
api.add_resource(Albums, '/albums/for/artist')
api.add_resource(Songs, '/songs/for/album')
api.add_resource(Song, '/song')
api.add_resource(Genres, '/genres')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
    app.run(debug=False)
