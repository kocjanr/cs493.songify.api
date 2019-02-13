#source env/bin/activate

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class API(Resource):
    def get(self):

        bucketName = 'cs493.songify.library'
        songName = '01FindAWayBack.mp3'
        
        #
        # When runnnig this code on my ec2 i was reciving an 500 error
        # when hitting the proper API route. I tried everything on Stack overflow
        # and GitHub issues but that didn't work. I needed to update one single 
        # package. When I update it still a 500 error. Instead to get any points for
        # this assignment I uploaded a mp3 to a public bucket and removed the AWS skd
        # calls to get a pre signed URL. So instead this API route returns a hard coded
        # JSON with Artist, Album and public link to an mp3 
        # 

        # s3 = boto3.client('s3')
        # url = s3.generate_presigned_url(
        #     ClientMethod='get_object',
        #     Params={
        #         'Bucket':bucketName,
        #         'Key': songName
        #     }
        # )

        return {'Artist': 'TheSkyCouldFly','Album': 'Geodesic','Link':' 	https://s3.amazonaws.com/toast-static-website/01+Find+A+Way+Back.mp3'}


api.add_resource(API, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
    app.run(debug=True)
