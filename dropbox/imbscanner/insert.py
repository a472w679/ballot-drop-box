
import os
import sys

import django

if __name__ == '__main__':
    # Add the parent directory of `dropbox` to Python's path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dropbox/
    sys.path.append(base_dir)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dropbox.settings")
    django.setup()


    from envelopeimb.models import imb

    # this commented code inserts debug test data into the database
    # imbdata = imb(dropboxid="1", date='Feb 14', imb="12345678901234567890", code39="012345678",streetaddress='711 W 23rd St', city="Lawrence", zipcode="66046", status="Invalid Entry")
    # imbdata.save()
    # printing out that data 
    # for test in imb.objects.all():
    #     print(test.date, test.streetaddress, test.city, test.zipcode, test.status)
    # imb.objects.all().delete() # clearing the query set 

