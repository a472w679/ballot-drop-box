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

import threading
import os
import select
import sys
from datetime import date
import time
import django
from barcode_usb_scanner import hid2ascii

import usb.core
import usb.util

def insert_code39_data(barcode, model): 
    barcode_res = if_is_valid_code39(barcode) 
    if barcode_res:
        if not len(model.objects.all().filter(code39=f"{barcode_res}")):  # check for duplicates 
            data_to_insert = model(dropboxid="1", date=f"{date.today()}", imb="", code39=f"{barcode_res}",streetaddress="", city="", zipcode="", status="Valid")
            data_to_insert.save() 


def get_input(): 
    try: 
        while True: 
            scanned_data = sys.stdin.readline().strip()
            return scanned_data
    except KeyboardInterrupt: 
        print("Exiting...")

def if_is_valid_code39(barcode : str) -> bool: 
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


def poll_scanner_input(model): 
    # granit 1980i scanner settings (I should already have this as default though)
    # 1) turn on code 39 use
    # 2) enable start and end characters 
    # 3) Set usb keyboard pc 
    # 4) Enable presentation mode 
    while True: 
        barcode = get_input() 
            
        barcode_res = if_is_valid_code39(barcode) 
        if barcode_res:
            if not len(model.objects.all().filter(code39=f"{barcode_res}")):  # check for duplicates 
                data_to_insert = model(dropboxid="1", date=f"{date.today()}", imb="", code39=f"{barcode_res}",streetaddress="", city="", zipcode="", status="Valid")
                data_to_insert.save() 



def poll_scanner_input_kernel_detached(model, id_vendor_val : int, id_product_val : int): 
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
                insert_code39_data(data, model)
                line = ''

def main(): 
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dropbox/
    sys.path.append(base_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dropbox.settings")
    django.setup()

    from dashboard.models import EnvelopeScan

    scanner1_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(EnvelopeScan, 0x0c2e, 0x0aaf,)) 
    scanner1_thread.start()

    scanner2_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(EnvelopeScan, 0x0c2e, 0x0c61,)) 
    scanner2_thread.start()

    # Join the threads 
    scanner1_thread.join()
    scanner2_thread.join()

    # poll_scanner_input_kernel_detached(EnvelopeScan, 0x0c2e, 0x0aaf)

    # poll_scanner_input(EnvelopeScan) 
    # print(len(EnvelopeScan.objects.all().filter(code39="test"))) 
    # EnvelopeScan.objects.all().delete() # clearing the query set 



if __name__ == '__main__':
    main()
    # Add the parent directory of `dropbox` to Python's path

    # this commented code inserts debug test data into the database
    # imbdata = imb(dropboxid="1", date='Feb 14', imb="12345678901234567890", code39="012345678",streetaddress='711 W 23rd St', city="Lawrence", zipcode="66046", status="Invalid Entry")
    # imbdata.save()
    # printing out that data 
    # for test in imb.objects.all():
    #     print(test.date, test.streetaddress, test.city, test.zipcode, test.status)
    # imb.objects.all().delete() # clearing the query set 

