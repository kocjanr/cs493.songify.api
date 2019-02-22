#source env/bin/activate

from flask import Flask, request
from flask_restful import Resource, Api
import boto3
from boto3.dynamodb.conditions import Key, Attr
import requests
from flask_cors import CORS
from var import Vars
import os

app = Flask(__name__)
api = Api(app)
CORS(app)

class API(Resource):
    def get(self):
        if request.method == 'GET':
            id = request.args.get('id')
            return{'this': id}

        return{'hello': 'goodbye'}

class Song(Resource):
    def get(self):
        songTitle = request.args.get('song')

        dynamodb = boto3.resource('dynamodb',aws_access_key_id=os.environ.get('ACCESS_ID'),
        aws_secret_access_key= os.environ.get('ACCESS_KEY'), region_name='us-east-1')
        table = dynamodb.Table('Music')
        response = table.scan(
            FilterExpression= Attr('SongTitle').eq(songTitle)
        )

        item = response['Items']
        if not item:
            return {'song':'Not found'}   

        url = item[0]['S3Link']   
        
        return {'url': url}

class Genres(Resource):
    def get(self):
        if request.method == 'GET':
            dynamodb = boto3.resource('dynamodb',aws_access_key_id=os.environ.get('ACCESS_ID'),
            aws_secret_access_key= os.environ.get('ACCESS_KEY'), region_name='us-east-1')
            table = dynamodb.Table('Music')

            response = table.scan()
            items = response['Items']

            if not items:
                return{'Genres': 'None'}

            genres = []
            for s in items:
                genres.append(s['Genre'])

            output = list(dict.fromkeys(genres))

            return{'Genres': output}

# http://127.0.0.1:8080/songs/for/album?album=Geodesic
class Songs(Resource):
    def get(self):   
        albumName = request.args.get('album')    

        dynamodb = boto3.resource('dynamodb',aws_access_key_id=os.environ.get('ACCESS_ID'),
        aws_secret_access_key= os.environ.get('ACCESS_KEY'), region_name='us-east-1')
        table = dynamodb.Table('Music')

        response = table.scan()
        items = response['Items'] 

        songs = []

        for s in items:
            if s['Album'] == albumName:
                songs.append(s['SongTitle'])

        return{'Songs':songs}

#"/albums/for/artist?artist=dan
# http://127.0.0.1:8080/albums/for/artist?artist=TheSkyCouldFly
class Albums(Resource):
    def get(self):   
        artist = request.args.get('artist')    

        dynamodb = boto3.resource('dynamodb',aws_access_key_id=os.environ.get('ACCESS_ID'),
        aws_secret_access_key= os.environ.get('ACCESS_KEY'), region_name='us-east-1')
        table = dynamodb.Table('Music')

        response = table.scan()
        items = response['Items'] 

        albums = []

        for s in items:
            if s['Artist'] == artist:
                albums.append(s['Album'])


        return{'Albums': albums}

api.add_resource(API, '/')
api.add_resource(Albums, '/albums/for/artist')
api.add_resource(Songs, '/songs/for/album')
api.add_resource(Song, '/song')
api.add_resource(Genres, '/genres')

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST'), port=os.environ.get('PORT'))    
    app.run(debug=True)
