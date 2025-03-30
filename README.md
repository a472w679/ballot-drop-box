# Ballot Drop Box Scanner
A system that scans, tracks, and stores information of ballot envelopes that are deposited in ballot drop boxes.  

## Setup 

### Pre Reqs
1) Make sure you have a Raspberry Pi and an AWS EC2 Instance 
- this system was tested on a Raspberry Pi 5 Model B Rev 1.0 
- hosting was tested on a AWS EC2 Debian instance 

### Project Modules
1) Make a virtual env in the project root directory 
```
python -m venv .venv 
```
2) Activate it 
3) Install the requirements  

```
pip install -r requirements.txt 
```

4) Make migrations 
```
python3 dropbox/manage.py makemigrations 
python3 dropbox/manage.py migrate  
```
5) To test and make sure everything is working,  `python3 dropbox/manage.py runserver 0.0.0.0:8000`
6) copy the host url into your browser 

### Scanner Setup (Raspberry Pi)
This enables more secure use of the interface between the scanner and the raspberry pi 

1) Install pyusb  and libusb 
```
sudo apt install libusb-1.0-0-dev
```
- NOTE: pyusb was already installed using requirements.txt in the previous section 

2) Make sure the member is a member of plugdev so that you can use USB devices
```
sudo addgroup <myuser> plugdev
```

3) Navigate to `/etc/udev/rules.d` and create a file that ends with .rules
[test.rules]
```
# Scanner 1 - Honeywell Granit 1910i ex 
SUBSYSTEM=="usb", ATTR{idVendor}=="0c2e", ATTR{idProduct}=="0aaf", MODE="0666"

# Scanner 2  - Honeywell Granit 1980 ex
SUBSYSTEM=="usb", ATTR{idVendor}=="0c2e", ATTR{idProduct}=="0c61", MODE="0666"
```
For each scanner that exists, add its corresponding correct idVendor and idProduct numbers 
- Correct idVendor and idProduct numbers for scanners can be found using `lsusb -v`
- in this case, our first scanner, the honeywell granit 1910i, has idVendor `0c2e` and idProduct `0aaf`

More information: https://github.com/vpatron/barcode_scanner_python 

### Scanner Config
[`scanner/config.yaml`]

#### prod
```yaml
prod: false 
```
- set prod to false if testing locally, true if not 
- this is a work in progress 

#### server
```yaml
server: 
  host: "127.0.0.1"    # ip the django server is hosted on 
  port: 8000           # port the django server is on 
  live_feed_port: 5005 # what port the live feed is connected to
```
- the host can be replaced with the ec2 instance ip if not testing locally 

#### dropbox 
Enter correct dropbox id
```yaml
dropbox: 
  id: 1 
  address: ""
```
- scan data will go to corresponding dropbox id tab on the server (subject to change)
- address optional 

#### scanners
```
lsusb -v
```
- find the vendor id and product id for each scanner as before 
- enter them into `scanner/config.yaml` 

Example: 
```yaml
scanners:  
  scanner1: 
    vendor_id: 0x0c2e
    product_id: 0x0aaf
  scanner2: 
    vendor_id: 0x0c2e
    product_id: 0x0aaf

  # ...
  # add more scanners as needed
```

### Startup Script Setup (Raspberry Pi)
1) Create a .desktop file `~/.config/autostart/ballot-dropbox-start.desktop` 

```
mkdir ~/.config/autostart
sudo vim ~/.config/autostart/ballot-dropbox-start.desktop
```

2) Enter this content in the file where Exec runs the absolute path to start.py 

[ballot-dropbox-start.desktop]
```ini
[Desktop Entry]
Name=Ballot Drop Box Start
Comment=Start the ballot drop box system
Terminal=true
Type=Application
Categories=Utility;Application;
Exec=lxterminal -e "python3 /home/xruyle/dev/ballot-drop-box/dropbox/start.py"
```

3) Now you can create a symlink to the .desktop file on the Desktop 
```
cd ~/Desktop
ln -s `~/.config/autostart/ballot-dropbox-start.desktop`
```
- When the RPi starts up, the start.py script should run. You can start it again using the icon on the desktop.  


### How do I run it manually? 
```
python3 dropbox/manage.py runserver 0.0.0.0:8000
```

### AWS Setup 
- Install necessary tools like git
- Clone this repository 

-Make sure redis is running 
```
redis-cli ping 
> PONG 
```
- install and enable using systemctl if it isn't 

#### Add Security Groups 
Django server 
- CUSTOM TCP port range 8000

Redis Server 
- CUSTOM TCP port range 6379

Incoming Live Feed
- CUSTOM TCP port range 5005 

## FAQ 
### Where is the web app?
`./dropbox/dashboard`

Html stuff is in `./dropbox/dashboard/templates`

### Where is the Database/Schema?
`./dropbox/dashboard/models.py`

### Where is the rasberry pi/barcode scanning code?
`./dropbox/scanner/`

## Credits  
https://github.com/vpatron/barcode_scanner_python
- for some of the pyusb related code 

