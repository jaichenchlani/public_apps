import yaml, json, os
from requests.models import Response
from flask_api import status
import requests

# Load Config
with open("config.yaml", "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

def get_number_wiki(n):
    # Declare the output dictionary
    number_wiki = {
        "n": n,
        "wiki_list": {}
    }

    # Process request to populate the results dictionary
    process_request(number_wiki)

    return number_wiki

def process_request(number_wiki):
    # Declare the blank wikiList dictionary

    # Check the number for Even/Odd
    get_even_odd(number_wiki)

    # Get Factors
    get_factors(number_wiki)

    # Get Prime Factors
    get_prime_factors(number_wiki)

    # Get other base numbers per the bases defined in config
    get_other_base_numbers(number_wiki)
    
# Call Mathfunctions API endpoint to get Even/Odd
def get_even_odd(number_wiki):
    key = "even_odd"
    url = "{}/{}/{}".format(os.environ['MATHFUNCTIONS_API'],config['mathfunctions']['endpoint_iseven'],number_wiki['n'])
    response = requests.get(url)
    response_content = json.loads(response.content.decode())
    if response.status_code == status.HTTP_200_OK:
        if response_content['result']:
            number_wiki['wiki_list'][key] = "Even"
        else:
            number_wiki['wiki_list'][key] = "Odd"
    else:
        number_wiki['wiki_list'][key] = "Cannot determine. {}".format(response_content['user_message'])

# Call Mathfunctions API endpoint to get factors
def get_factors(number_wiki):
    key = "factors"
    url = "{}/{}/{}".format(os.environ['MATHFUNCTIONS_API'],config['mathfunctions']['endpoint_getfactors'],number_wiki['n'])
    response = requests.get(url)
    response_content = json.loads(response.content.decode())
    if response.status_code == status.HTTP_200_OK:
        number_wiki['wiki_list'][key] = response_content['result']
    else:
        number_wiki['wiki_list'][key] = "Cannot determine. {}".format(response_content['user_message'])

# Call Mathfunctions API endpoint to get prime factors
def get_prime_factors(number_wiki):
    key = "prime_factors"
    url = "{}/{}/{}".format(os.environ['MATHFUNCTIONS_API'],config['mathfunctions']['endpoint_getprimefactors'],number_wiki['n'])
    response = requests.get(url)
    response_content = json.loads(response.content.decode())
    if response.status_code == status.HTTP_200_OK:
        number_wiki['wiki_list'][key] = response_content['result']
    else:
        number_wiki['wiki_list'][key] = "Cannot determine. {}".format(response_content['user_message'])

def get_other_base_numbers(number_wiki):
    # Change Base Processing for bases defined in Config
    for (key,value) in config['change_base_config'].items():
        url = "{}/{}/{}/{}".format(os.environ['MATHFUNCTIONS_API'],config['mathfunctions']['endpoint_changebase'],number_wiki['n'],value)
        response = requests.get(url)
        if response.status_code == status.HTTP_404_NOT_FOUND:
            number_wiki['wiki_list'][key] = "Cannot determine. Check the URL {}.".format(url)
        else:
            response_content = json.loads(response.content.decode())
            if response.status_code == status.HTTP_200_OK:
                number_wiki['wiki_list'][key] = response_content['result']
            else:
                number_wiki['wiki_list'][key] = "Cannot determine. {}".format(response_content['user_message'])