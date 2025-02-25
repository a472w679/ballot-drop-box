import os
import select
import sys
from datetime import date

import django


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
    if not (barcode.startswith('*') and barcode.endswith('*')):
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
        barcode = input("Waiting for scanner:\n> ")
        
        # TODO implement 
        barcode_res = if_is_valid_code39(barcode) 
        if barcode_res:
            if not len(model.objects.all().filter(code39=f"{barcode_res}")):  # check for duplicates 
                data_to_insert = model(dropboxid="1", date=f"{date.today()}", imb="", code39=f"{barcode_res}",streetaddress="", city="", zipcode="", status="Valid")
                data_to_insert.save() 
        # else if IsValidIMb(): 




def main(): 
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dropbox/
    sys.path.append(base_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dropbox.settings")
    django.setup()

    from envelopeimb.models import imb

    poll_scanner_input(imb) 
    # print(len(imb.objects.all().filter(code39="test"))) 

    # imb.objects.all().delete() # clearing the query set 



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

