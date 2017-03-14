from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth

# Create your views here.
def index(request):
    # return  HttpResponse("<h1>YASH<h1>")
    return render(request, 'www/home.html', {})

# Social_Auth Login and Management
@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
    
    return render(request, 'www/settings.html', {
        'github_login': github_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm
    
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please Correct the Error Below.')
    else:
        form = PasswordForm(request.user)
    
    return render(request, 'www/password.html', {form:'form'})

def profile(request):
    return render(request, 'www/profile.html', {})