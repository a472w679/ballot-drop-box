# Ballot Drop Box Scanner
A system that scans, tracks, and stores information of ballot envelopes that are deposited in ballot drop boxes.  

## Setup 

### Pre Reqs
1) Make sure you have a Raspberry Pi 
- this system was tested on a Raspberry Pi 5 Model B Rev 1.0 

### Project Modules
1) Make a virtual env in the project root directory 
```
python -m venv .venv 
```
- go into .venv/pyenv.cfg  and set allow global packages to true 


2) Activate it 
3) Install the requirements  
```
pip install -r requirements.txt 
```
4) To test and make sure everything is working, Enter the first `dropbox` directory and run `python3 manage.py runserver`
5) copy the localhost url into your browser 

### Scanner Setup 
This enables more secure use of the interface between the scanner and the system 

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
```
# Scanner 1 - Honeywell Granit 1910i
SUBSYSTEM=="usb", ATTR{idVendor}=="0c2e", ATTR{idProduct}=="0aaf", MODE="0666"

# Scanner 2  - Honeywell Granit 1980
SUBSYSTEM=="usb", ATTR{idVendor}=="0c2e", ATTR{idProduct}=="0c61", MODE="0666"
```
For each scanner that exists, add its corresponding correct idVendor and idProduct numbers 
- Correct idVendor and idProduct numbers for scanners can be found using `lsusb -v`
- in this case, our first scanner, the honeywell granit 1910i, has idVendor `0c2e` and idProduct `0aaf`

4) Add a new thread in `./dropbox/scanner/scanning.py` for each new scanner! 

[./dropbox/scanner/scanning.py]
```python
   # In the main function 
    scanner1_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(EnvelopeScan, 0x0c2e, 0x0aaf,)) 
    scanner1_thread.start()

    scanner2_thread = threading.Thread(target=poll_scanner_input_kernel_detached,  daemon=True, args=(EnvelopeScan, 0x0c2e, 0x0c61,)) 
    scanner2_thread.start()

	
    # Join the threads 
    scanner1_thread.join()
    scanner2_thread.join()
```
- this is located near the bottom of the file in the main function 
- the 2nd and third arguments for the thread are the respective idVendor and idProduct numbers 
- yes I know this is convoluted just hang with us!

More information about this can be gathered from https://github.com/vpatron/barcode_scanner_python 

### Startup Script Setup
1) Create a .desktop file `~/.config/autostart/ballot-dropbox-start.desktop` 

```
mkdir ~/.config/autostart
sudo vim ~/.config/autostart/ballot-dropbox-start.desktop
```

2) Enter this content in the file 

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
- NOTE: that the path to the start.py file is dependent on the raspberry pi 

3) Now you can create a symlink to the .desktop file on the Desktop 
```
cd ~/Desktop
ln -s `~/.config/autostart/ballot-dropbox-start.desktop`
```
- When the RPi starts up, the start.py script should run. You can start it again using the icon on the desktop.  

#### How do I just run the system manually? 
1) In one terminal run `python3 manage.py runserver` 
2) In another terminal run `python3 scanner/insert.py`

## FAQ 
### Where is the web app?
`./dropbox/dashboard`

Html stuff is in `./dropbox/dashboard/templates`

### Where is the Database/Schema?
`./dropbox/dashboard/models.py`

### Where is the rasberry pi/barcode scanning code?
`./dropbox/scanner/`


## Libraries Used 
- OpenCV 
- zxingcpp 
- Django 
- https://github.com/vpatron/barcode_scanner_python




