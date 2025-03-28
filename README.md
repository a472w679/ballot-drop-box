# Ballot Drop Box Scanner
A system that scans, tracks, and stores information of ballot envelopes that are deposited in ballot drop boxes.  

## Setup 
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







