from distutils.command.config import config
from flask import Flask, request, jsonify
from flask_api import status
import yaml, json, os
from flask_restful import Resource, Api
from numberwiki import get_number_wiki
import requests

print("Entering main.py...")

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

# Load Config
with open("config.yaml", "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

class HelloNumberWiki(Resource):
    def get(self):
        data = {
            'name': "numberwiki",
            'description': "Number Wiki",
            'owner/maintainer': "everythingcloudplatform.com",
            'version': "1.0",
            'endpoint1':'/<n>',
        }
        return data, status.HTTP_200_OK
    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, status.HTTP_201_CREATED

class NumberWiki(Resource):
    def get(self, n):
        # Initialize the response dictionary
        data = {
            'input_number': n,
            'result': {},
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Validate Input | call the isinteger endpoint from mathfunctions API
        url = "{}/{}/{}".format(os.environ['MATHFUNCTIONS_API'],config['mathfunctions']['endpoint_isinteger'],n)
        response = requests.get(url)
        response_content = json.loads(response.content.decode())
        if response.status_code == status.HTTP_200_OK:
            if response_content['result']:
            # Input URL parameter is Integer. Go ahead with fetching number wiki
                number_wiki  = get_number_wiki(n)
                data['result'] = number_wiki
                data['http_status_code'] = response.status_code
                return data, response.status_code
            else:
                data['user_message'] = "URL parameters must be numeric."
                data['http_status_code'] = status.HTTP_400_BAD_REQUEST
                return data, status.HTTP_400_BAD_REQUEST
        else:
            data['user_message'] = "Request failed."
            data['http_status_code'] = response.status_code
            return data, response.status_code

api.add_resource(HelloNumberWiki, '/')
api.add_resource(NumberWiki, '/<n>')

if __name__ == "__main__":
    port = "8081"
    print("Starting Numberwiki Flask API on Port {}...".format(port))
    app.run(debug=True, host='0.0.0.0',port=port)