from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.template import loader
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from .forms import LoginForm, SignUpForm, ForgotPasswordForm, resetPasswordForm
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

@require_http_methods(['GET','POST'])
def signup(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'GET':
        f = SignUpForm()
    else:
        f = SignUpForm(request.POST)
        if f.is_valid():
            user = f.save();
            email_body_context = {
                    'username' : user.username,
                    'domain' : get_current_site(request).domain,
                    'uid' : user.id,
                    'token' : urlsafe_base64_encode(force_bytes(user.username)),
                    'protocol' : 'http',
                }
#body context of verification mail sent to the mail id of the user
            body = loader.render_to_string('authentication/signup_email_body_text.html',email_body_context)
            email_message = EmailMultiAlternatives('Welcome to MiniQuora1', body, settings.DEFAULT_FROM_EMAIL , [user.email])
            email_message.send()
#EmailMultiAlternatives(subject, text_content, from_email, [to])
            return render(request, 'authentication/signup_email_sent.html', {'email': user.email})
    return  render(request, 'authentication/signup.html', { 'form' : f })

@require_GET
@login_required
def home(request):
    return render(request , 'base/logged.html')

@require_GET
def activate(request , uid = None,  token = None):
    if request.user.is_authenticated():
        return redirect('home')
    user = get_object_or_404(CustomUser, id=uid)
    username_from_token = force_text(urlsafe_base64_decode(token))
    if user.is_active:
        return redirect('base')

    if user.username == username_from_token : 
        user.is_active = True
        user.save()
        return render(request,'authentication/activation_successful.html')
    else:
        return render('authentication/activation_failure.html')

@require_http_methods(['GET','POST'])
def forgot_password(request):
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'GET':
        f = ForgotPasswordForm()
    if request.method == 'POST':
        f = ForgotPasswordForm(request.POST)
        if f.is_valid():
            user = CustomUser.objects.get(email = f.cleaned_data['email'])
            email_body_context = {
                    'username' : user.username,
                    'token' : default_token_generator.make_token(user),
                    'uid' : user.id,
                    'domain' : get_current_site(request).domain,
                    'protocol' : 'http',
                    }
            body = loader.render_to_string('authentication/forgot_password_email_body_text.html',email_body_context)
            email_message = EmailMultiAlternatives('Reset your password', body, settings.DEFAULT_FROM_EMAIL, [user.email])
            email_message.send()
            return render(request,'authentication/forgot_password_email_sent.html',{'email' : user.email})
    return render(request,'authentication/forgot_password.html', {'form' : f})

@require_http_methods(['GET', 'POST'])
def reset_password(request, uid = None, token=None):
    if request.user.is_authenticated():
        return redirect('home')
    try:
        user = CustomUser.objects.get(id = uid)
    except (CustomUser.DoesNotExist):
        user = None
    if not user or not default_token_generator.check_token(user, token):
        context = { 'validlink' : False}
        return render(request, 'authentication/set_password.html', context)
    if request.method == 'GET':
        f = resetPasswordForm()
    else:
        f = resetPasswordForm(request.POST)
        if f.is_valid():
            user.set_password(f.cleaned_data['password1'])
            user.save()
            return redirect('base')
    context = { 'validlink' : True, 'form' : f}
    return render(request, 'authentication/set_password.html', context)
