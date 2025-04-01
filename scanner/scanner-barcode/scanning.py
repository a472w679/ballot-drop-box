# Name of code artifact: scanning.py 
# Brief description of what the code does: Scans barcodes using industrial scanner. Contains modified code from the vpatron/barcode_scanner_python repo which defends against the case where a would be attacker can't just enter things in 
# Programmer’s name: Xavier Ruyle   
# Date the code was created: 2/20/25
# Preconditions: Industrial scanner hooked up to device 
# Postconditions: barcode scanned and printed to screen 
# Return values or types, and their meanings: N/A
# Error and exception condition values or types that can occur, and their meanings: N/A
# Side effects: 
# Invariants: N/A
import os.path
import sys
import threading
from datetime import date

import usb.core
import usb.util
import yaml
from barcode_usb_scanner import hid2ascii

# importing post_request from above 
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)
from post_request import config, send_data


def send_code39_to_server(barcode : str) -> bool: 
    '''
    Sends post request to django server api endpoing containing code39 barcode

    Args: 
        barcode (str): the code39 string

    Returns: 
        bool: true if post request  
    '''

    res = is_valid_code39(barcode) 
    if res: 
        data = {
            "dropboxid" : config["dropbox"]["id"], 
            "date": f"{date.today()}", 
            "imb": "", 
            "code39": f"{res}",
            "streetaddress": "", 
            "city": "", 
            "zipcode": "",  
            "status": "Valid"
        }

        return send_data(data)
    else: 
        return False 



def is_valid_code39(barcode : str) -> bool | str: 
    '''
    Checks if barcode str is valid code 39

    Args: 
        barcode (str): the code39 string

    Returns: 
        bool: false if code 39 was not valid  
        str:  code39 string without start and end * characters if barcode was valid 

    Example: 
        *ABC-123* 
        >>> ABC-123
    '''

    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-. $/+%*")

    # Check if the barcode starts and ends with '*'
    if not (barcode[0] == '*' and barcode[-1] == '*'):
        return False

    # Remove the start and stop characters for validation
    barcode_content = barcode[1:-1]

    # Check if all characters are valid
    for char in barcode_content:
        if char not in valid_chars:
            return False

    # Check if the barcode has at least one character
    if len(barcode_content) == 0:
        return False

    return barcode_content


def poll_scanner_input_kernel_detached(id_vendor_val : int, id_product_val : int): 
    '''
    Detaches scanner from kernel and reads directly from USB endpoint 

    Args: 
        id_vendor_val (int): the id vendor of the scanner 
        id_product_val (int): the id product of the scanner 

    Returns: 
        None 
    '''

    # Find our device using the VID (Vendor ID) and PID (Product ID)
    # use lsusb -v to find this 
    dev = usb.core.find(idVendor=id_vendor_val, idProduct=id_product_val)
    if dev is None:
        raise ValueError('USB device not found')

    # Disconnect it from kernel
    needs_reattach = False
    if dev.is_kernel_driver_active(0):
        try: 
            needs_reattach = True
            dev.detach_kernel_driver(0)
            print("Detached USB device from kernel driver")
        except usb.core.USBError as e: 
            sys.exit("Could not detatch kernel driver from interface({0}): {1}".format(i, str(e)))


    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    # dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()
    intf = cfg[(0,0)]

    ep = usb.util.find_descriptor(
        intf,
        # match the first IN endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)

    assert ep is not None, "Endpoint for USB device not found. Something is wrong."

    # Loop through a series of 8-byte transactions and convert each to an
    # ASCII character. Print output after 0.5 seconds of no data.
    line = ''
    while True:
        try:
            # Wait up to 0.5 seconds for data. 500 = 0.5 second timeout.
            data = ep.read(1000, 500)  
            ch = hid2ascii(data)
            line += ch
        except KeyboardInterrupt:
            print("Stopping program, attempting to reattach usb device to kernel driver, please be patient...")
            dev.reset()
            dev.attach_kernel_driver(0)
            break
        except usb.core.USBError:
            # Timed out. End of the data stream. Print the scan line.
            if len(line) > 0:
                data = line.strip()
                print("Scanner: ", data)
                send_code39_to_server(data) 
                line = ''

def main(): 
    with open(os.path.join(parent_dir, "config.yaml"), 'r') as file:
        config = yaml.safe_load(file)

    threads = []

    try:
        for scanner, idvals in config["scanners"].items(): 
            vendor_id = idvals["vendor_id"]
            product_id = idvals["product_id"]

            scanner_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(vendor_id, product_id,)) 
            threads.append(scanner_thread)
    except KeyError: 
        raise Exception("Invalid scanner configuration")

    for thread in threads: 
        thread.start()

    for thread in threads: 
        thread.join()





        # scanner1_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(0x0c2e, 0x0aaf,)) 
        # scanner1_thread.start()

        # scanner2_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(0x0c2e, 0x0c61,)) 
        # scanner2_thread.start()

        # Join the threads 
        # scanner1_thread.join()
        # scanner2_thread.join()



if __name__ == '__main__':
    main()
