from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class TweetForms(forms.ModelForm):
    class Meta:
        model = Tweet # model define krna compulsory hai 
        fields = ['text','photo'] # model ki field Add kr rhe hai Array me  ye Arr me es liye hai kyu ki ese hmne bnaya hai nhi to inbuilt ke liye tupple lete hai 
        
        
class UserRegistrationForm(UserCreationForm):
   email=forms.EmailField()
   
   class Meta:
       model = User
       fields =('username','email','password1','password2') # esme tuple ka use ke rhe hai kyu ki inbuilt feature ka use kr hai
        