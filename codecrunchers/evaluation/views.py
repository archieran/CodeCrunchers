from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import Http404
from django.conf import settings
from .models import Topic, Problem, ConsoleLanguage
from hackerrank.HackerRankAPI import HackerRankAPI
from .models import TestCase
import json


def evaluationhome(request):
    topics = Topic.objects.all()
    context = {
        'topics': topics,
        'active_tab': 'problems'
    }
    return render(request, 'evaluation/topics.html', context)


def topic_problems(request, topic_var):
    probs = Problem.objects.select_related().filter(topic_id=topic_var)
    context = {
        'problems': probs,
        'active_tab': 'problems'
    }
    return render(request, 'evaluation/problems.html', context)


def evaluate(request, prob_id):
    languages = ConsoleLanguage.objects.filter(is_active=True)
    challenge = Problem.objects.select_related().filter(id=prob_id)
    if len(challenge) == 0:
        # if received unknown value in url, raise 404
        raise Http404
    context = {
        'challenge': challenge[0],
        'active_tab': 'problems',
        'languages': languages,
    }
    print context
    return render(request, 'evaluation/solve.html', context)


def practice_home(request):
    problems = Problem.objects.select_related().filter(is_practice=True)
    print problems
    context = {
        'active_tab': 'prac_home',
        'problems': problems
    }
    return render(request, 'evaluation/practice_home.html', context)


def run_testcases(request):
    #code runs just fine, make sure that there is atleast one sample test cases to not let this view blow up
    API_KEY = settings.HACKERRANK_API
    source_code = request.POST.get("code")
    compiler = HackerRankAPI(API_KEY)
    lang = request.POST["lang"]
    lang = lang.lower()
    prob_id = request.POST["prob_id"]
    cases = TestCase.objects.select_related().filter(is_sample=True, problem=prob_id)
    cases_list = list(cases)
    inputsequences = list()
    outputsequences = list()
    for case in cases_list:
        inputsequences.append(str(case.input_sequence).replace('\r', ''))
        outputsequences.append(str(case.output_sequence.replace('\r', '')))
    print inputsequences
    print outputsequences
    result = compiler.run(
        {'source': source_code,
         'lang': lang,
          'testcases': inputsequences,
         }
    )
    i = 0
    actualoutputs = list()
    data = dict()
    output = list()
    msg = result.message
    error = result.error
    print msg
    print error
    print result.output
    for res in result.output:
        data["id"] = i
        data["input"] = inputsequences[i].strip()
        data["expectedoutput"] = outputsequences[i].strip()
        data["actualoutput"] = res.strip()
        data["status"] = data["actualoutput"] == data["expectedoutput"]
        i=i+1
        output.append(data)
        data = dict()
    js = json.dumps(output)
    print js
    print prob_id
    print lang
    print source_code
    return HttpResponse(js)