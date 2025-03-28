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
from datetime import date

import requests

# DEBUG URL 
DEBUG_URL = "http://127.0.0.1:8000/api/scandata"

# For production, use HTTPS:
# EC2_URL = "https://your-domain.com/api/sensor-data/"

# sensor_data_example = {
#     "dropboxid" :"1", 
#     "date": f"{date.today()}", 
#     "imb": "", 
#     "code39": f"{1001}",
#     "streetaddress": "", 
#     "city": "", 
#     "zipcode": "",  
#     "status": "Valid"
# }

def send_data(data : dict) -> bool:
    '''
    Sends JSON data to a predefined API endpoint via HTTP POST request.

    This function attempts to send the provided data to a debug URL endpoint. 
    It handles the request/response cycle and provides feedback about the operation's success.

    Args:
        data (dict): A dictionary containing the data to be sent as JSON in the request body.
                     The dictionary should be JSON-serializable.

    Returns:
        bool: True if the request was successful (HTTP status code 2xx), False otherwise.
              Note: Only indicates successful delivery, not necessarily server-side processing.


    Example:
        >>> result = send_data({'barcode': 'ABC123', 'status': 'processed'})
        Status Code: 200
        Response: {"success": true, "message": "Data received"}
        >>> print(result)
        True
    '''
    try:
        response = requests.post(
            DEBUG_URL,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        # print(f"Status Code: {response.status_code}")
        # print(f"Response: {response.text}")
        # return response.ok
        return response.ok 
    except Exception as e:
        print(f"Error sending data: {e}")
        return False


