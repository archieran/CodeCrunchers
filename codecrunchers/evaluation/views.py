from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import Http404
# Create your views here.
from .models import Topic, Problem

def evaluationhome(request):
    topics = Topic.objects.all()
    context = {
        'topics':topics,
        'active_tab':'problems'
    }
    return render(request, 'evaluation/topics.html', context)
def topic_problems(request, topic_var):
    
    probs = Problem.objects.select_related().filter(topic_id =  topic_var)
    context = {
        'problems':probs,
        'active_tab':'problems'
    }
    return render(request, 'evaluation/problems.html', context)

def evaluate(request, prob_id):
    challenge = Problem.objects.select_related().filter(id = prob_id)
    if len(challenge) == 0:
        #if received unknown value in url, raise 404
        raise Http404
    context = {
        'challenge':challenge[0],
        'active_tab':'problems'
    }
    print context
    return render(request, 'evaluation/solve.html', context)

def practice_home(request):
    problems = Problem.objects.select_related().filter(is_practice = True)
    print problems
    context = {
        'active_tab':'prac_home',
        'problems':problems
    }
    return render(request, 'evaluation/practice_home.html', context)