from django import forms
from .models import *



class LoginForm(forms.Form):
    userid = forms.CharField(label='學號', max_length=9)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput())

class teachlog(forms.Form):
    psw = forms.CharField(label='密碼', widget=forms.PasswordInput())

class new_week(forms.Form):
    name=forms.CharField(label='名稱', max_length=20 )


class changepsw(forms.Form):
    opsw = forms.CharField(label='舊密碼', widget=forms.PasswordInput())
    npsw = forms.CharField(label='新密碼', widget=forms.PasswordInput())
    npsw2 = forms.CharField(label='再次輸入新密碼', widget=forms.PasswordInput())





