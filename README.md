# Ballot Drop Box Scanner
A system that scans, tracks, and stores information of ballot envelopes that are deposited in ballot drop boxes.  

## Setup 
1) Make a virtual env in the project root directory 
```
python -m venv .venv 
```
2) Activate it 
3) Install the requirements  
```
pip install -r requirements.txt 
```
4) Enter the first `dropbox` directory and run `python3 manage.py runserver`
5) copy the localhost url into your browser 

## FAQ 
### Where is the web app?
`./dropbox/envelopeimb`

Html stuff is in `./dropbox/envelopeimb/templates`

### Where is the Database/Schema?
`./dropbox/envelopeimb/models.py`

### Where is the rasberry pi/barcode scanning code?
`./dropbox/imbscanner/`
