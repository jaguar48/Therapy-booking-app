

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
from django.forms import fields
from django.forms.models import ModelForm
from .models import profile, book



Bookingchoice =(
    ("Marital/Relationship", "Marital/Relationship"),
    ("Birthday wishes/greetings", "Birthday wishes/greetings"),
    ("Counselling/motivation", "Counselling/motivation"),
    ("Business tips/ideas", "Business tips/ideas"),
    ("Call a friend", "Call a friend"),
    ("Other", "Other"),
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control"
            }
        ))
        
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "fullname",                
                "class": "form-control"
            }
        ))
    phone = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "placeholder" : "phone",                
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','phone','fullname')



class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
class ProfileEditForm(forms.ModelForm):

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "placeholder" : "date of birth",                
                "class": "form-control"
            }
        )), 

    class Meta:
        model = profile
        fields = ('country','date_of_birth','photo')

class BookForm(forms.ModelForm):
   
    # name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Name",                
    #             "class": "form-control"
    #         }
    #     )) 
    # email = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             "placeholder" : "Email",                
    #             "class": "form-control"
    #         }
    #     )) 

    subject = forms.ChoiceField(choices= Bookingchoice,required=False,
        widget=forms.Select(
            attrs={
                "placeholder" : "Subject",                
                "class": "form-control"
            }
        ))
    specify = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "specify",                
                "class": "form-control subject_specify",
                
            }
        ),required = False)
    # message = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             "placeholder" : "Message",                
    #             "class": "form-control"
    #         }
    #     ))
    
    NOW, LATER = 'now', 'later'
    SCHEDULE_CHOICES = (
        (NOW, 'Send immediately'),
        (LATER, 'Send later'),
    )
    schedule = forms.ChoiceField(choices=SCHEDULE_CHOICES, widget=forms.RadioSelect(
            attrs={
                "placeholder" : "schedule call",                 
                "class": "form-control"
            }
        ))
        
        
    send_dt = forms.DateField(label="", required=False)


    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)

        # If 'later' is chosen, mark send_dt as required.
        if data and data.get('schedule', None) == self.LATER:
            self.fields['send_dt'].required = True

    class Meta:
        model = book
        fields = ('name','email', 'subject', 'specify','message','identification','schedule','send_dt')

