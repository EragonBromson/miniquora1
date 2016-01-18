from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import LoginForm
from .models import CustomUser

# Create your views here.

@require_http_methods(['GET','POST'])
def base(request):
    if(request.user.is_authenticated()):
        return redirect('home')
    if request.method == 'GET':
        f=LoginForm()
    else:
        f = LoginForm(request.POST)
        if f.is_valid():
            user = f.get_user();
            auth_login(request, user)
            return redirect('home')
    return render(request,'authentication/login.html',{ 'form' : f })

@require_GET
def logout(request):
    auth_logout(request)
    return redirect('base')

@require_GET
@login_required
def home(request):
    return render(request , 'base/loggedin.html')
