from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
from .models import Topic, Problem

def evaluationhome(request):
    topics = Topic.objects.all()
    context = {
        'topics':topics
    }

    return render(request, 'evaluation/topics.html', context)
def topic_problems(request, topic_var):
    
    probs = Problem.objects.select_related().filter(topic_id =  topic_var)
    context = {
        'problems':probs
    }
    return render(request, 'evaluation/problems.html', context)

def evaluate(request, prob_id):
    challenge = Problem.objects.select_related().filter(id = prob_id)
    context = {
        'challenge':challenge[0]
    }
    print context
    return render(request, 'evaluation/solve.html', context)