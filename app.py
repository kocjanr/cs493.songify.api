#source env/bin/activate

from flask import Flask
from flask_restful import Resource, Api
import boto3
import requests
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class API(Resource):
    def get(self):

        bucketName = 'cs493.songify.library'
        songName = '01FindAWayBack.mp3'
        #Expires
        s3 = boto3.client('s3')
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket':bucketName,
                'Key': songName
            }
        )
        response = requests.get(url)

        print(response)
        

        return {'Artist': 'TheSkyCouldFly','Album': 'Geodesic','Link':url}


api.add_resource(API, '/')

if __name__ == '__main__':
    app.run(debug=True)
