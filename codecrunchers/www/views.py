from calendar import calendar
from django.db.models.functions import TruncMonth, Extract
from django.shortcuts import HttpResponse, render, redirect, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from graphos.renderers.base import BaseChart
from graphos.renderers.highcharts import BaseHighCharts
from social_django.models import UserSocialAuth
from .models import Profile
from evaluation.models import ContestParticipant
from django.contrib.auth.models import User
from evaluation.models import Submission, ConsoleLanguage, Problem
from graphos.sources.model import ModelDataSource, SimpleDataSource
from graphos.renderers import morris, highcharts
from django.db.models import Max, Aggregate, Sum, Count
from graphos.renderers.gchart import LineChart
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay, ExtractWeekDay
from www.forms import ProfileForm
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

@login_required
def profile(request):
    # Difficulty wise submissions pie chart
    query_set = Submission.objects.select_related().filter(sub_made_by = request.user).values('prob__difficulty').annotate(subcount = Count('prob__difficulty'))
    print query_set
    options = {
        'title':'Difficulty wise submissions',
        'subtitle': "Total submissions: " + str(Submission.objects.filter(sub_made_by = request.user).count()),
    }
    data = list()
    row = list()
    data.append(['Difficulty', 'submissions'])
    for query in query_set:
        row.append(get_difficulty_verbose(query['prob__difficulty']))
        row.append(query['subcount'])
        data.append(row)
        row = list()
    print data
    data_source = SimpleDataSource(data)
    chart = highcharts.ColumnChart(data_source, options=options)
    chart.html_id = "difficultychart"
    # Topic wise submissions pie chart
    query_set = Submission.objects.select_related().filter(sub_made_by = request.user).values('prob__topic__topic_name').annotate(count = Count('prob__topic__topic_name'))
    options = {
        'title':'Topic wise submissions',
        'subtitle': "Total submissions: " + str(Submission.objects.filter(sub_made_by = request.user).count()),
    }
    row = list()
    data = list()
    data.append(['Topic', 'Submissions'])
    for query in query_set:
        row.append(query['prob__topic__topic_name'])
        row.append(query['count'])
        data.append(row)
        row = list()
    data_source = SimpleDataSource(data)
    topic_chart = highcharts.PieChart(data_source, options=options)
    topic_chart.html_id = "otherchart"
    # Other chart
    query_set = Submission.objects.select_related().filter(sub_made_by = request.user).annotate(month = TruncMonth('attempted')).values('month').annotate(submissions = Count('id'))[:12]
    options = {
        'title':'Monthly  submissions',
        'subtitle': "Total submissions: " + str(Submission.objects.filter(sub_made_by = request.user).count()),
    }
    data = list()
    data.append(['Month', 'Submissions'])
    for query in  query_set:
        count  = query['submissions']
        month = str(query['month'].strftime('%B')) + ", " +  str(query['month'].strftime('%Y'))
        row.append(month)
        row.append(count)
        data.append(row)
        row = list()
    print data
    data_source = SimpleDataSource(data)
    monthly_chart = highcharts.LineChart(data_source, options = options)
    monthly_chart.html_id = 'monthlychart'
    subs = Submission.objects.filter(sub_made_by = request.user).order_by('-attempted')[:10]
    context = {
        'topic_chart':topic_chart,
        'monthly_chart':monthly_chart,
        'chart':chart,
        'submissions':subs,
        'active_tab':'profile',
    }
    return render(request, 'www/profile.html',context)
@login_required
def leaderboard(request):
    users = User.objects.all().order_by('-profile__experience_points')
    context = {
        'active_tab':'leaderboard',
        'users':users,
    }
    return render(request, 'www/leaderboard.html',context)
@login_required
def dashboard(request):
    query_set = Submission.objects.all().values('lang').annotate(langcount = Count('lang'))
    print query_set
    #data_source = ModelDataSource(query_set, fields=['user', 'experience_points', 'experience_points'],)
    row = list()
    data = list()
    data.append(['Langages', 'Submisions'])
    for query in query_set:
        languages = ConsoleLanguage.objects.filter(id = query.values()[0])
        for language in languages:
            row.append(language.lang)
        numbers = query.values()[1]
        row.append(numbers)
        data.append(row)
        row = list()
    print data
    #data.append(['c', '5']) not needed for production

    data_matrix =  [
            data
        ]
    data_source = SimpleDataSource(data=data)
    # chart = morris.DonutChart(data_source)
    options = {
        'title':'Language wise submissions',
        'subtitle': "Total submissions: " + str(Submission.objects.count()),

    }
    chart_language = highcharts.PieChart(data_source, options=options)
    chart_language.html_id = "languagesubmissions"
    # Preparing chart for problem difficulty levels
    query_set = Problem.objects.all().values('difficulty').annotate(difficulty_count = Count('difficulty'))
    print query_set
    data = list()
    row = list()
    data.append(['Difficulty', 'Problem Count'])
    for query in query_set:
        row.append(get_difficulty_verbose(query['difficulty']))
        row.append(query['difficulty_count'])
        data.append(row)
        row = list()
    print data
    data_source = SimpleDataSource(data)
    options = {
        'title':'Problem distribution : Difficulty wise',
        'subtitle': "Total Problems: " + str(Problem.objects.count()),

    }
    chart_difficulty = highcharts.ColumnLineChart(data_source, options=options)
    context = {
        'chart_language':chart_language,
        'chart_difficulty':chart_difficulty,
        'active_tab':'dashboard',
    }
    chart_difficulty.html_id = "difficultychart"
    return render(request, 'www/dashboard.html', context)

def get_difficulty_verbose(c):
    if c == 'E':
        return "Easy"
    elif c == "M":
        return "Medium"
    elif c == "H":
        return "Hard"
    else:
        return "Expert"

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        user_profile, created = Profile.objects.get_or_create(user = request.user)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            user_profile.user_avatar = request.FILES.get('user_avatar')
            user_profile.user_type = user_type
            user_profile.user = request.user
            user_profile.save()
            print user_profile
            # user_profile.save()
            return HttpResponseRedirect(reverse('ev:evhome'))
    else:
        form = ProfileForm()
        form.user = request.user
    
    context = {
        'form':form,
    }
    return render(request,'www/create_profile.html',context)