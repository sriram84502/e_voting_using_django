from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib import messages

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "id":"aadhar",
        "type":"text",
        "name":"aadhar",
        "placeholder":"Aadhar Number"
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        "id":"phone",
        "name":"phone",
        "type":"text",
        "placeholder":"Phone number"
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        "id":"name",
        "name":"name",
        "type":"text",
        "placeholder":"Enter your name"
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        "id":"pass",
        "type":"password",
        "placeholder":"Enter password"

    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "id":"pass1",
        "type":"password",
        "placeholder":"Confirm Password"
    }))
    district = forms.CharField(widget=forms.TextInput(attrs={
        "type":"text",
        "name":"district",
        "placeholder":"Enter Your district "
    }),label="")
    mandal = forms.CharField(widget=forms.TextInput(attrs={
        "id":"inputDistrict",
        "name":"mandal",
        "type":"text",
        "placeholder":"Enter Your mandal"
    }))
    class Meta:
        model = CustomUser
        fields = ['name','phone','is_phone_verified','username','district','mandal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

    def clean_password(self):
        password= self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError("Your password should be at least 8 Characters")

        return password
        
        