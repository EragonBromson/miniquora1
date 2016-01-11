from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(widget = forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        self.user_cache = None;
        super(LoginForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username =username,password = password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid Username and Password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('User is not Active')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

#is_active tells us that whether the user is Signed Up or not.
# If no ValidationError is raised, the method should return the cleaned (normalized) data as a Python object.
#__init__ is the initialiser
