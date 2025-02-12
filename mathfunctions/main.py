from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json, yaml, logging, functools, inspect, os, sys
import mathfunctions
import google.cloud.logging

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

# Set up logging
client = google.cloud.logging.Client()
client.setup_logging(log_level=int(os.environ['PUBLICAPPS_LOGGING_LEVEL']))

# Load config
config_filename = "config/config_{}.yaml".format(os.environ['PUBLICAPPS_ENVIRONMENT'])
with open(config_filename, "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

# Configure the basic logging level per the config
logging.basicConfig(level=int(os.environ['PUBLICAPPS_LOGGING_LEVEL']))
# Ensure logs are written to stdout (Cloud Logging agent captures stdout/stderr)
# logging.basicConfig(
#     level=int(os.environ['PUBLICAPPS_LOGGING_LEVEL']),  # Capture DEBUG and INFO logs
#     format="%(levelname)s: %(message)s",
#     handlers=[
#         logging.FileHandler(config['log_file']),
#         logging.StreamHandler(sys.stdout)  # Ensures logs go to stdout
#     ]
# )

# Decorator to log function calls
def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the CALLER function name
        caller_frame = inspect.currentframe().f_back
        caller_function_name = caller_frame.f_code.co_name
        caller_module_name = inspect.getmodule(caller_frame).__name__
        caller = "{}.{}".format(caller_module_name,caller_function_name)
        # Get the CALLED function name
        module = "{}.{}".format(__name__,func.__name__)
        logging.debug("ENTER: {}. Caller: {}".format(module,caller))
        # Execute the function
        result = func(*args, **kwargs)
        logging.debug("EXIT: {}.".format(func.__name__))
        return result
    return wrapper

@log_function_call
@app.before_request
def before_request():
    # Log Trace
    trace_message = "elo_trace | method:{}; url:{}; endpoint:{}".format(request.method,request.base_url,request.endpoint)
    logging.info(trace_message)

class HelloMathfunctions(Resource):
    @log_function_call
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
        return data, 200
    
    @log_function_call
    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, 201

class ChangeBase(Resource):
    @log_function_call
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
            data['http_status_code'] = 400
            return data, 400
        # Call the appropriate routine
        output = mathfunctions.changeBase(int(n),int(base))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = 400
            return data, 400
        else:
            data['result'] = output['result']
            data['http_status_code'] = 200
            return data, 200

class GetFactors(Resource):
    @log_function_call
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
            data['http_status_code'] = 400
            return data, 400
        # Call the appropriate routine
        output = mathfunctions.getFactors(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = 400
            return data, 400
        else:
            data['result']['factorsCount'] = output['factorsCount']
            data['result']['isPrime'] = output['isPrime']
            data['result']['factors'] = output['factors']
            data['http_status_code'] = 200
            return data, 200

class GetPrimeFactors(Resource):
    @log_function_call
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
            data['http_status_code'] = 400
            return data, 400
        # Call the appropriate routine
        output = mathfunctions.getPrimeFactors(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = 400
            return data, 400
        else:
            data['result']['factorsCount'] = output['factorsCount']
            data['result']['isPrime'] = output['isPrime']
            data['result']['primeFactors'] = output['primeFactors']
            data['http_status_code'] = 200
            return data, 200

class IsPrime(Resource):
    @log_function_call
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
            data['http_status_code'] = 400
            return data, 400
        # Call the appropriate routine
        output = mathfunctions.isPrime(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = 400
            return data, 400
        else:
            data['result'] = output['result']
            data['http_status_code'] = 200
            return data, 200

class IsEven(Resource):
    @log_function_call
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
            data['http_status_code'] = 400
            return data, 400
        # Call the appropriate routine
        output = mathfunctions.isEven(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = 400
            return data, 400
        else:
            data['result'] = output['result']
            data['http_status_code'] = 200
            return data, 200

class IsPositive(Resource):
    @log_function_call
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
            data['http_status_code'] = 400
            return data, 400
        # Call the appropriate routine
        output = mathfunctions.isPositive(int(n))
        # Check for valid output
        if not output['validOutputReturned']:
            data['user_message'] = output['message']
            data['http_status_code'] = 400
            return data, 400
        else:
            data['result'] = output['result']
            data['http_status_code'] = 200
            return data, 200

class IsInteger(Resource):
    @log_function_call
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
        data['http_status_code'] = 200
        return data, 200

api.add_resource(HelloMathfunctions, '/')
api.add_resource(ChangeBase, '/changebase/<n>/<base>')
api.add_resource(GetFactors, '/getfactors/<n>')
api.add_resource(GetPrimeFactors, '/getprimefactors/<n>')
api.add_resource(IsPrime, '/isprime/<n>')
api.add_resource(IsEven, '/iseven/<n>')
api.add_resource(IsPositive, '/ispositive/<n>')
api.add_resource(IsInteger, '/isinteger/<n>')

if __name__ == "__main__":
    logging.info("Starting {} Flask API in {} on Port {}...".format(config['app']['name'],os.environ['PUBLICAPPS_ENVIRONMENT'].upper(),config['app']['port']))
    app.run(debug=config['app']['debug'], host='0.0.0.0',port=config['app']['port'])