from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from .forms import LoginForm

# Create your views here.

@require_GET
def base(request):
    if(request.user.is_authenticated()):
        return HttpResponse('User is authenticated')
    f=LoginForm(initial = { 'username' : 'admin' })
    #THIS IS AN UNBOUNDED FORM WHICH WILL BE RENDERED ON BASE
    context = { 'form' : f }
    return render(request,'base/base.html')

#@require_POST
def login(request):
    return HttpResponse('LoginForm to be displayed.')

#@login_required
def secret(request):
    return HttpResponse('User logged in')
