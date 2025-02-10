# Douglas County Ballot Drop Box Scanner
A system that scans and tracks envelopes deposited in ballot drop boxes using an IMb scanner and Raspberry Pi.  

## Setup 

1) Make a virtual env in the project root directory 
```
python3 -m venv .venv 
```
2) Activate it 
3) Install Django 
```
pip install django 
```

4) Go to the first `dropbox` directory 
5) run `python3 manage.py runserver`
6) copy the localhost url into your browser 

## Dev Notes 
### Where the actual web app is 
`./dropbox/envelopeimb`

html stuff is in `./dropbox/envelopeimb/templates`

### Where the Schema is 
`./dropbox/envelopeimb/models.py`

### Where Rasberry Pi related code goes 
`./dropbox/imbscanner/`
