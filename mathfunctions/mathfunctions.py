import math, logging, yaml, os, functools, inspect, sys
import google.cloud.logging

# Load config
config_filename = "config/config_{}.yaml".format(os.environ['PUBLICAPPS_ENVIRONMENT'])
with open(config_filename, "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

# Set up logging
client = google.cloud.logging.Client()
client.setup_logging()

# Configure the basic logging level per the config
logging.basicConfig(level=int(os.environ['PUBLICAPPS_LOGGING_LEVEL']))
# Ensure logs are written to stdout (Cloud Logging agent captures stdout/stderr)
# logging.basicConfig(
#     level=int(os.environ['PUBLICAPPS_LOGGING_LEVEL']),  # Capture DEBUG and INFO logs
#     format="%(levelname)s: %(message)s",
#     handlers=[
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
def changeBase(n, base):
    # print("Entering getBinary...")
    baseReference = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    response = {
        "result": 0,
        "message": "",
        "validOutputReturned": True
    }

    if not isInteger(n):
        # Invalid Input, Return error message and indicator.
        response = {
            "message": "Invalid input. Input number must be a positive integer.",
            "validOutputReturned": False
            }
    elif not isInteger(base):
        response = {
            "message": "Invalid input. Input base must be a positive integer between 2 and 36.",
            "validOutputReturned": False
            }
    elif base < 2 or base > 36:
        response = {
            "message": "Invalid input. Input base must be a positive integer between 2 and 36.",
            "validOutputReturned": False
            }
    elif n == 0 or n == 1:
        response['result'] = n
    elif not isPositive(n)['result']:
        # Invalid Input, Return error message and indicator.    
            response = {
                "message": "Invalid input. Cannot process a negative number.",
                "validOutputReturned": False
            }
    else:
        answer = ""
        counter = 1
        keepgoing = True
        originalNumber = n

        while (keepgoing):
            index = n % base
            # answer += str(n % base)
            answer += baseReference[index]
            # print("KeepGoing:{}; Counter:{}; N:{}; Answer:{}".format(keepgoing,counter,n,answer))
            n = n//base
            if (n < base):
                keepgoing = False
                answer += str(n)
                # print("KeepGoing:{}; Counter:{}; N:{}; Answer:{}".format(keepgoing,counter,n,answer))
            counter = counter + 1
        
        # Reverse the answer string and store in response dictionary
        # Remove the trailing zero, if any
        if answer[-1] == "0":
            response['result'] = answer[-2::-1]
        else:
            response['result'] = answer[::-1]        
    
    return response

@log_function_call
def isPrime(n):
    # print("Entering isPrime for {}...".format(n))
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Call the factors function to get factors
    factors = getFactors(n)
    # Populate the isPrime Response dictionary using the values returned from getFactors
    response = {
        "result": factors['isPrime'],
        "message": factors['message'],
        "validOutputReturned": factors['validOutputReturned']
        }
    # Update the message with additional information for Composite i.e. non-Prime numbers
    if not factors['isPrime']:
        response['message'] = "Divisible by {}".format(str(factors['factors'][1:-1]))
    
    return response

@log_function_call
def isEven(n):
    # print("Entering isEven...")
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Validate the input argument to be a valid integer
    if isInteger(n):
        if n % 2 == 0:
            # Valid Input, Positive Result.
            response = {
                "result": True,
                "message": "Input is an Even number.",
                "validOutputReturned": True
            }
        else:
            # Valid Input, Negative Result.
            response = {
                "result": False,
                "message": "Input is an Odd number.",
                "validOutputReturned": True
            }
    else:
        # Invalid Input, Default Negative Result and return error message and indicator.
        response = {
                "result": False,
                "message": "Invalid input. Cannot calculate.",
                "validOutputReturned": False
            }
    return response

@log_function_call
def getFactors(n):
    # print("Entering getFactors...")
    factorsSet = set()
    response = {
            "factorsCount": 1,
            "isPrime": False,
            "factors": [],
            "message": "",
            "validOutputReturned": True
    }
    if not isInteger(n):
        # Invalid Input, Return error message and indicator.
        response['message'] = "Invalid input. Input must be a positive integer."
        response['validOutputReturned'] = False
        return response
    
    if n == 0:
        # Invalid Input, Return error message and indicator.
        response['message'] = "Invalid input. Zero has infinite factors. Cannot populate factors list."
        response['validOutputReturned'] = False
        return response

    if not isPositive(n)['result']:
        # Invalid Input, Return error message and indicator.    
        response['message'] = "Invalid input. Cannot process a negative number."
        response['validOutputReturned'] = False
        return response
    
    # All good. Go ahead with processing.
    if n == 1:
        # Special Processing for 1
        factorsSet.add(n)
    else:
        # The number itself is always a factor
        factorsSet.add(n)
        # Input is a Valid and Positive Integer. Go ahead.
        # Special Processing for 1
        keepGoing = True
        # Determine the half mark
        halfMark = n // 2
        # Start processing from the half mark
        currentNumberBeingTested = halfMark
        while(keepGoing):
            # print("Iteration # {}; Processing {}.".format(iteration,currentNumberBeingTested))
            try:
                if n % currentNumberBeingTested == 0:
                    # currentNumberBeingTested is a factor
                    factorsSet.add(currentNumberBeingTested)
                    # Recursive call to get the factors of currentNumberBeingTested
                    factorsSet.update(getFactors(currentNumberBeingTested)['factors'])
                    currentNumberBeingTested -= 1
                    iteration =+ 1
                else:
                    # Decrement halfMark by 1 and come back in the while loop
                    currentNumberBeingTested -= 1
                    # iteration =+ 1
            except ZeroDivisionError:
                keepGoing = False

    # Sort the factors Set in Ascending order, and store in the list in Response. 
    response['factors'] = sorted(factorsSet)
    response['factorsCount'] = len(response['factors'])
    # Determine whether the number is Prime, based on # of factors
    if response['factorsCount'] <= 2:
        response['isPrime'] = True
    else:
        response['isPrime'] = False

    return response

@log_function_call
def isPositive(n):
    # print("Entering isPositive...")
    # Initialize Response Dictionary
    response = {
        "result": False,
        "message": "",
        "validOutputReturned": True
    }
    # Validate the input argument to be a valid integer
    if isInteger(n):
        if n > 0:
            # Valid Input, Positive Result.
            response = {
                "result": True,
                "message": "Input is a Positive number.",
                "validOutputReturned": True
            }
        elif n == 0:
            # Valid Input, Negative Result.
            response = {
                "result": False,
                "message": "Zero is neither positive nor negative.",
                "validOutputReturned": True
            }
        else:
            # Valid Input, Negative Result.
            response = {
                "result": False,
                "message": "Input is a Negative number.",
                "validOutputReturned": True
            }
    else:
        # Invalid Input, Default Negative Result and return error message and indicator.
        response = {
                "result": False,
                "message": "Invalid input. Cannot calculate.",
                "validOutputReturned": False
            }
    return response

# Validate whether the passed string is a valid integer, and return a boolean result
@log_function_call
def isInteger(str_number):
    # print("Entering isInteger...")
    try:
        temp_int_variable = int(str_number)
    except ValueError:
        return False

    return True

@log_function_call
def getPrimeFactors(n):
    # print("Entering getPrimeFactors...")
    # Initialize Response Dictionary
    primeFactors = []
    response = {
        "factorsCount": 1,
        "primeFactors": [],
        "isPrime": False,
        "message": "",
        "validOutputReturned": True
    }
    # Call the factors function to get factors
    factors = getFactors(n)
    

    if not factors['validOutputReturned']:
        # Not a valid response from getFactors
        response = {
            "primeFactors": [],
            "message": factors['message'],
            "validOutputReturned": False
        }
    elif factors['isPrime']:
        # If the number is Prime, then prime factors are same as factors
        response['isPrime'] = factors['isPrime']
        response['primeFactors'] = factors['factors']
        response['factorsCount'] = len(response['primeFactors'])
    else:
        # Prime Factors is a subset(Prime Numbers Only) of Factors
        response['isPrime'] = factors['isPrime']
        response['primeFactors'] = [x for x in factors['factors'] if isPrime(x)['result']]
        response['factorsCount'] = len(response['primeFactors'])

    return response