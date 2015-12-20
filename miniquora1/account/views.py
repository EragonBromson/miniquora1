from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators.http import require_http_methods, require_GET, require_POST

# Create your views here.

@require_GET
def base(request):
    return render(request,'base/base.html')

@require_POST
def login(request):
    return HttpResponse('LoginForm to be displayed.')

@login_required
def secret(request):
    return HttpResponse('User logged in')
