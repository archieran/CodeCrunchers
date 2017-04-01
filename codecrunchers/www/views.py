from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
from .models import Profile
from evaluation.models import ContestParticipant
from django.contrib.auth.models import User
from evaluation.models import Submission, ConsoleLanguage
from graphos.sources.model import ModelDataSource, SimpleDataSource
from graphos.renderers import morris, highcharts
from django.db.models import Max, Aggregate, Sum, Count
from graphos.renderers.gchart import LineChart

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
    submissions = Submission.objects.filter(sub_made_by = request.user)
    print submissions
    context = {
        'active_tab':'profile'
    }
    return render(request, 'www/profile.html',context)

def leaderboard(request):
    users = User.objects.all().order_by('-profile__experience_points')
    context = {
        'active_tab':'leaderboard',
        'users':users,
    }
    return render(request, 'www/leaderboard.html',context)
def dashboard(request):
    query_set = Submission.objects.all().values('lang').annotate(langcount = Count('lang'))
    print query_set
    #data_source = ModelDataSource(query_set, fields=['user', 'experience_points', 'experience_points'],)
    row = list()
    data = list()
    data.append(['Submissions', 'Language'])
    for query in query_set:
        languages = ConsoleLanguage.objects.filter(id = query.values()[0])
        for language in languages:
            row.append(language.lang)
        numbers = query.values()[1]
        row.append(numbers)
        data.append(row)
        row = list()
    print data
    data.append(['c', '5'])

    data_matrix =  [
            data
        ]
    data_source = SimpleDataSource(data=data)
    chart = morris.DonutChart(data_source)
    context = {
        'chart':chart,
        'active_tab':'dashboard',
    }

    return render(request, 'www/dashboard.html', context)
