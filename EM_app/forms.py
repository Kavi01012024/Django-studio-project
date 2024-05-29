from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User



class CreateUserForms(UserCreationForm):

    class Meta:

        model = User
        fields = ["username","email","password1","password2"]



    def clean_email(self):

        mail = self.cleaned_data.get("email")

        existing_user = User.objects.filter(email=mail).exists()

        if existing_user:
            raise forms.ValidationError("Email already exists")
        return mail
        

    def clean(self):

        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")



        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return self.cleaned_data
    


class Email_verification_form(forms.Form):
    e_input = forms.IntegerField()

class Addresses_form(forms.Form):
    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs = {'placeholder':'Name'}),label='Name')
    phone = forms.IntegerField(widget=forms.TextInput(attrs = {'placeholder':'Mobile no'}),label='Phone')
    addr1 = forms.CharField(max_length=100,widget=forms.TextInput(attrs = {'placeholder':'House no/build no/street'}),label='line 1')
    addr2 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={ 'placeholder':'street/city/state'}),label='line 2')
    pincode = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Pincode'}))

    def clean_pincode(self):
        super().clean()
        pincode = self.cleaned_data['pincode']
        if len(str(pincode)) == 6:
            return pincode
        raise forms.ValidationError('Enter Valid pincode')
    
    


