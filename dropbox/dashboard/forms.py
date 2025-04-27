from django import forms


class AccountLogin(forms.Form):
    username = forms.CharField(label="username", max_length=30)
    email = forms.CharField(label="Email", max_length=254)
    password = forms.CharField(label="password", max_length=128)

class AccountRegister(forms.Form):
    username = forms.CharField(label="username", max_length=30)
    email = forms.CharField(label="email", max_length=254)
    password = forms.CharField(label="password", max_length=128)
    confirm_password = forms.CharField(label="confirm_password", max_length=128)

class DropboxCreate(forms.Form): 
    dropboxid  = forms.IntegerField()
    location_name  = forms.CharField(max_length=66)
    coordinates = forms.CharField(max_length=66)


