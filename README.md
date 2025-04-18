# Ballot Drop Box Scanner
A system that scans, tracks, and stores information of ballot envelopes that are deposited in ballot drop boxes.  

## Documentation Outline 

[Basic Initial Setup](#setup) 
- [Setup](#setup)
- [Installation](#installation)
- [Installing Dependencies](#installing-dependencies)
- [Email Service](#email-service)
- [Testing](#testing)

[Raspberry Pi Setup](#raspberry-pi)
- [USB Scanners](#industrial-usb-scanner-setup)
- [Config File](#config)
  - [Server and Token Authorization](#server-and-token-authorization)
- [Startup Script](#startup-script)

[EC2 Instance](#aws-ec2-setup)
- [Security Groups](#security-groups)
- [Deploying the Django App](#ec2-instance-configuration-for-deploying-django)
  - [Nginx](#nginx)
  - [systemd](#systemd)

This system was tested on a Raspberry Pi 5 Model B Rev 1.0 

Hosting was tested on a AWS EC2 Debian instance 
## Setup  
Use this section either for the AWS EC2 instance or testing on your local host. 

### Installation
```
git clone https://github.com/a472w679/ballot-drop-box

cp scanner/config.yaml.secret scanner/config.yaml
cp dropbox/.env.secret dropbox/.env 
```

### Installing Dependencies
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
python dropbox/manage.py makemigrations 
python dropbox/manage.py migrate  
python dropbox/manage.py collectstatic  
```

```
python dropbox/manage.py createsuperuser  
```
- the superuser will be the credentials you use to sign in as admin on the website

### Email Service 
in `./dropbox/.env` set up an email service for email sending using the example given in `.env.secret` 

### Testing
To test and make sure everything is working,  `python dropbox/manage.py runserver 0.0.0.0:8000`

copy the host url into your browser 

## Raspberry Pi 
### Industrial USB Scanner Setup 
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
```
For each scanner that exists, add its corresponding correct idVendor and idProduct numbers 
- Correct idVendor and idProduct numbers for scanners can be found using `lsusb -v`
- in this case, our first scanner, the honeywell granit 1910i, has idVendor `0c2e` and idProduct `0aaf`

More information: https://github.com/vpatron/barcode_scanner_python 

### Config 
```
cp scanning/config.yaml.secret scanning/config.yaml 
```
- config.yaml.secret is an example 

#### server and token authorization
```yaml
server: 
  host: "127.0.0.1"    # ip the django server is hosted on 
  port: 8000           # port the django server is on 
  live_feed_port: 5005 # what port the live feed is connected to
  authentication: "your-auth-token-here" 
```
- the host can be replaced with the ec2 instance ip if not testing locally 

You can obtain an `auth-token` by logging into an account on the site and accessing `accounts/`
- click on one of the accounts' API Key button to get an auth token 

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
  # add more scanners if needed
```

### Startup Script 
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
Exec=lxterminal -e "python3 /home/xruyle/dev/ballot-drop-box/scanner/start.py"
```

3) Now you can create a symlink to the .desktop file on the Desktop 
```
cd ~/Desktop
ln -s `~/.config/autostart/ballot-dropbox-start.desktop`
```
- When the RPi starts up, the start.py script should run. You can start it again using the icon on the desktop.  

## AWS EC2 Setup 

This was tested on a debian EC2  instance 
### Security Groups 
Django server 
- CUSTOM TCP port range 8000

Redis Server 
- CUSTOM TCP port range 6379

Incoming Live Feed
- CUSTOM TCP port range 5005 

CIDR: 0.0.0.0/0

### EC2 Instance Configuration for Deploying Django
SSH into the instance using security.pem
- `ssh -i "security.pem" admin@ec2-domain`

1) Install necessary tools like git
2) Clone this repository 
3) Install and enable redis
```
sudo systemctl enable redis # starts at boot 
sudo systemctl start redis    
sudo systemctl restart redis  
```

Make sure redis is running 
```
redis-cli ping 
> PONG 
```

4) [Install dependencies](#installing-dependencies) and make migrations  
```
python3 dropbox/manage.py makemigrations 
python3 dropbox/manage.py migrate  
```

Configure `.dropbox/dropbox/settings.py`
```python
DEBUG = False  # set debug to false 
ALLOWED_HOSTS = ["ec2-server-ip"]
```

#### nginx  
```
sudo apt install nginx
sudo systemctl stop nginx
sudo rm /etc/nginx/sites-enabled/default

```

`sudo nano /etc/nginx/sites-available/django.conf`
```
server {
	   listen 80;
	       server_name ec2-server-ip;  
		   location / {
               proxy_pass http://127.0.0.1:8000;
               proxy_http_version 1.1;
               proxy_set_header Upgrade $http_upgrade;
               proxy_set_header Connection "upgrade";
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			}
		}
```

```
sudo ln -s /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/
sudo nginx -t  # Test config
sudo systemctl start nginx
```

#### Systemd
Make systemd services in `/etc/systemd/system`

[django.service]
```
[Unit]
Description=Django RunServer
After=network.target

[Service]
User=admin
Group=www-data
WorkingDirectory=/home/admin/dev/ballot-drop-box/dropbox
ExecStart=daphne -b 0.0.0.0 -p 8000 dropbox.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

[udp_receiver.service]
```
[Unit]
Description=Django Start UDP Receiver
After=network.target

[Service]
User=admin
Group=www-data
WorkingDirectory=/home/admin/dev/ballot-drop-box
ExecStart=/home/admin/dev/ballot-drop-box/.venv/bin/python3 dropbox/manage.py start_udp_receiver
Restart=always

[Install]
WantedBy=multi-user.target
```
7) Run the systemd services 
```
systemctl daemon-reload
systemctl start django.service
systemctl start udp_receiver.service
```


## FAQ 
### Your documentation is confusing 
Sorry, there are a lot of moving parts 

### Where is the web app?
`./dropbox/dashboard`

Html stuff is in `./dropbox/dashboard/templates`

### Where is the Database/Schema?
`./dropbox/dashboard/models.py`

### Where is the rasberry pi/barcode scanning code?
`./scanner/`

## Credits  
https://github.com/vpatron/barcode_scanner_python
- for some of the pyusb related code 

