# Name of code artifact: views.py 
# Brief description of what the code does: Sends a post request to django web server 
# Programmer’s name: Xavier Ruyle 
# Date the code was created: 3/28/25 
# Preconditions: Django Web server running  
# Postconditions: N/A 
# Return values or types, and their meanings: N/A 
# Error and exception condition values or types that can occur, and their meanings: N/A 
# Side effects: N/A 
# Invariants: N/A 
import os
from datetime import date

import requests
import yaml

with open(os.path.join(os.path.dirname(__file__), "config.yaml"), 'r') as file:
    config = yaml.safe_load(file)

def send_data(data : dict) -> bool:
    '''
    Sends JSON data to a predefined API endpoint via HTTP POST request.

    Args:
        data (dict): A dictionary containing the data to be sent as JSON in the request body.

    Returns:
        bool: True if the request was successful (HTTP status code 2xx), False otherwise.
    '''

    server_config = config['server']
    if not config["prod"]: 
        API_ENDPOINT = f"http://{server_config['host']}:{server_config['port']}/api/scandata"
    else: 
        API_ENDPOINT = f"https://{server_config['host']}/api/scandata"

    try:
        response = requests.post(
            API_ENDPOINT,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        return response.ok 
    except Exception as e:
        print(f"Error sending data: {e}")
        return False

# debug 
# from datetime import datetime, timedelta
# delta = timedelta(days=1)
# for i in range(7): 
#     date = datetime(2025, 3, 31) + i * delta
#     send_data(
#             {
#                 "dropboxid" : 1, 
#                 "date": f"{date.strftime('%Y-%m-%d')}", 
#                 "imb": "", 
#                 "code39": f"ABB-12{i}1",
#                 "streetaddress": "", 
#                 "city": "", 
#                 "zipcode": "",  
#                 "status": "Valid"
#             }
#     )
#
