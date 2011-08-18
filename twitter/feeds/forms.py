from django import forms
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=75)
    password = forms.CharField(max_length=30,min_length=6,widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30,min_length=6,widget=forms.PasswordInput)
    
    def clean(self):
        clean = self.cleaned_data
        pass1 = clean.get('password')
        pass2 = clean.get('password_confirm')
        
        if pass1 != pass2:
            raise forms.ValidationError("Passwords do not match.")
        
        try:
            User.objects.get(email=clean.get('email'))
            raise forms.ValidationError('Email is already registered. Please login.')
        except ObjectDoesNotExist:
            pass
        
        return clean
    
    def save(self):
        user = User.objects.create_user('', self.cleaned_data['email'], 
                                        self.cleaned_data['password'])
        user.username = str(user.id)
        user.save()
        user.groups.add(Group.objects.get(name='Free'))
        
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=75)
    password = forms.CharField(max_length=30, min_length=6, widget=forms.PasswordInput)
    
    def clean(self):
        if not self._errors:
            user = authenticate(email=self.cleaned_data.get('email'),
                                password=self.cleaned_data.get('password'))
            
            if user is None:
                raise forms.ValidationError('Email and password combination does not match')
        
        return self.cleaned_data