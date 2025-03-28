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
import sys
import threading
from datetime import date

import django
import usb.core
import usb.util
from barcode_usb_scanner import hid2ascii
from post_request import send_data


def send_code39_to_server(barcode : str) -> bool: 
    data = {
        "dropboxid" :"1", 
        "date": f"{date.today()}", 
        "imb": "", 
        "code39": f"{barcode}",
        "streetaddress": "", 
        "city": "", 
        "zipcode": "",  
        "status": "Valid"
    }

    return send_data(data)


def get_input(): 
    try: 
        while True: 
            scanned_data = sys.stdin.readline().strip()
            return scanned_data
    except KeyboardInterrupt: 
        print("Exiting...")

def if_is_valid_code39(barcode : str) -> bool | str: 
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
    Contains modified code from the vpatron/barcode_scanner_python repo which defends against the case where a would be attacker can't just enter things in
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
    scanner1_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(0x0c2e, 0x0aaf,)) 
    scanner1_thread.start()

    scanner2_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(0x0c2e, 0x0c61,)) 
    scanner2_thread.start()

    # Join the threads 
    scanner1_thread.join()
    scanner2_thread.join()




if __name__ == '__main__':
    main()
