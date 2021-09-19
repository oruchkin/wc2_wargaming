from django import forms
from django.forms.widgets import PasswordInput, Textarea
from . models import  User


# https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef
class Registration_Model_Form(forms.ModelForm):    
    password_conf = forms.CharField(max_length=30, label='Password confirmation', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={"class": "form-control"}),                              
        }


class Query_form(forms.Form):
    query_title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Name of query (movie,book, lecture)'}))
    query_text = forms.CharField(max_length=999999, widget=forms.Textarea(attrs={"class": "form-control", "rows": 15, "cols": 20, 'placeholder': 'put your text right here ===>>>'}))
    
    
class Query_txt_form(forms.Form):
    query_title = forms.CharField(max_length=200, label='Title', widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Name of query (movie,book, lecture)'}))
    docfile = forms.FileField(label='File', widget=forms.FileInput(attrs={"class": "form-control"}))
    


