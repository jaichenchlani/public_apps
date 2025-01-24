from urllib import response
from flask import Flask, request, jsonify
from flask_api import status
import json
from flask_restful import Resource, Api
import mathfunctions

print("Entering main.py...")

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

class HelloMathfunctions(Resource):
    def get(self):
        data = {
            'name': "mathfunctions",
            'description': "Math Functions",
            'owner/maintainer': "everythingcloudplatform.com",
            'version': "1.0",
            'endpoint1':'/changebase/<n>/<base>',
            'endpoint2':'/getfactors/<n>',
            'endpoint3':'/getprimefactors/<n>',
            'endpoint4':'/isprime/<n>',
            'endpoint5':'/iseven/<n>',
            'endpoint6':'/ispositive/<n>',
            'endpoint7':'/isinteger/<n>'
        }
        return data, status.HTTP_200_OK
    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, status.HTTP_201_CREATED

class ChangeBase(Resource):
    def get(self, n, base):
        # Initialize the response dictionary
        data = {
            'input_number': n,
            'Base': base,
            'result': 0,
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Validate Input
        if not mathfunctions.isInteger(n) or not mathfunctions.isInteger(base):
            data['user_message'] = "Both the URL parameters must be numeric."
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        # Call the appropriate routine
        output = mathfunctions.changeBase(int(n),int(base))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        else:
            data['result'] = output['result']
            data['http_status_code'] = status.HTTP_200_OK
            return data, status.HTTP_200_OK

class GetFactors(Resource):
    def get(self, n):
        data = {
            'input_number': n,
            'result': {
                "factorsCount": 1,
                "isPrime": False,
                "factors": []
            },
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Validate Input
        if not mathfunctions.isInteger(n):
            data['user_message'] = "URL parameters must be numeric."
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        # Call the appropriate routine
        output = mathfunctions.getFactors(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        else:
            data['result']['factorsCount'] = output['factorsCount']
            data['result']['isPrime'] = output['isPrime']
            data['result']['factors'] = output['factors']
            data['http_status_code'] = status.HTTP_200_OK
            return data, status.HTTP_200_OK

class GetPrimeFactors(Resource):
    def get(self, n):
        data = {
            'input_number': n,
            'result': {
                "factorsCount": 1,
                "isPrime": False,
                "primeFactors": []
            },
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Validate Input
        if not mathfunctions.isInteger(n):
            data['user_message'] = "URL parameters must be numeric."
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        # Call the appropriate routine
        output = mathfunctions.getPrimeFactors(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        else:
            data['result']['factorsCount'] = output['factorsCount']
            data['result']['isPrime'] = output['isPrime']
            data['result']['primeFactors'] = output['primeFactors']
            data['http_status_code'] = status.HTTP_200_OK
            return data, status.HTTP_200_OK

class IsPrime(Resource):
    def get(self, n):
        data = {
            'input_number': n,
            'result': None,
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Validate Input
        if not mathfunctions.isInteger(n):
            data['user_message'] = "URL parameters must be numeric."
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        # Call the appropriate routine
        output = mathfunctions.isPrime(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        else:
            data['result'] = output['result']
            data['http_status_code'] = status.HTTP_200_OK
            return data, status.HTTP_200_OK

class IsEven(Resource):
    def get(self, n):
        data = {
            'input_number': n,
            'result': None,
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Validate Input
        if not mathfunctions.isInteger(n):
            data['user_message'] = "URL parameters must be numeric."
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        # Call the appropriate routine
        output = mathfunctions.isEven(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        else:
            data['result'] = output['result']
            data['http_status_code'] = status.HTTP_200_OK
            return data, status.HTTP_200_OK

class IsPositive(Resource):
    def get(self, n):
        data = {
            'input_number': n,
            'result': None,
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Validate Input
        if not mathfunctions.isInteger(n):
            data['user_message'] = "URL parameters must be numeric."
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        # Call the appropriate routine
        output = mathfunctions.isPositive(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = status.HTTP_400_BAD_REQUEST
            return data, status.HTTP_400_BAD_REQUEST
        else:
            data['result'] = output['result']
            data['http_status_code'] = status.HTTP_200_OK
            return data, status.HTTP_200_OK

class IsInteger(Resource):
    def get(self, n):
        data = {
            'input_number': n,
            'result': None,
            'user_message': "Request completed successfully.",
            'base_url': request.base_url,
            'endpoint': request.endpoint,
            'host_url': request.host_url,
            'http_status_code': None
        }
        # Call the appropriate routine
        data['result'] = mathfunctions.isInteger(n)
        data['http_status_code'] = status.HTTP_200_OK
        return data, status.HTTP_200_OK

api.add_resource(HelloMathfunctions, '/')
api.add_resource(ChangeBase, '/changebase/<n>/<base>')
api.add_resource(GetFactors, '/getfactors/<n>')
api.add_resource(GetPrimeFactors, '/getprimefactors/<n>')
api.add_resource(IsPrime, '/isprime/<n>')
api.add_resource(IsEven, '/iseven/<n>')
api.add_resource(IsPositive, '/ispositive/<n>')
api.add_resource(IsInteger, '/isinteger/<n>')

if __name__ == "__main__":
    port = "8080"
    print("Starting Mathfunctions Flask API on Port {}...".format(port))
    app.run(debug=True, host='0.0.0.0',port=port)