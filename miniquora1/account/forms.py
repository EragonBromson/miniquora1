from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(widget = forms.PasswordInput())
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username =username,password = password)
            if user is None:
                raise forms.ValidationError('Invalid Username and Password')
            elif not user.is_active:
                raise forms.ValidationError('User is not Active')
        return self.cleaned_data

#is_active tells us that whether the user is Signed Up or not.
# If no ValidationError is raised, the method should return the cleaned (normalized) data as a Python object.
