from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.http import require_GET, require_POST
from .forms import LoginForm

# Create your views here.

@require_GET
def base(request):
    if(request.user.is_authenticated()):
        return redirect('secret')
    f=LoginForm(initial = { 'username' : 'admin' })
    #THIS IS AN UNBOUNDED FORM WHICH WILL BE RENDERED ON BASE
    context = { 'form' : f }
    return render(request,'base/base.html',context)

@require_POST
def login(request):
    if(request.user.is_authenticated()):
        return redirect('secret')
    f = LoginForm(request.POST)
    if f.is_valid():
        return redirect('secret')
    else:
        return render(request,'base/base.html',{ 'form' : f })

@require_GET
@login_required
def secret(request):
    return HttpResponse('User logged in')
