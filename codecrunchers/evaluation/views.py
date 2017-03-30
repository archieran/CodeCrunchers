from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import Http404
from django.conf import settings
from .models import Topic, Problem, ConsoleLanguage, Submission
from hackerrank.HackerRankAPI import HackerRankAPI
from django.utils import timezone
from .models import TestCase
from django.contrib.auth.models import User
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

def run_submission(request):
    API_KEY = settings.HACKERRANK_API
    source_code = request.POST.get("code")
    compiler = HackerRankAPI(API_KEY)
    lang = request.POST["lang"]
    language = lang
    lang = lang.lower()
    prob_id = request.POST["prob_id"]
    user = request.user
    sub = Submission()
    sub.prob = Problem.objects.filter(id = prob_id)[0]
    sub.attempted = timezone.now()
    sub.submitted_code = source_code
    sub.sub_made_by = user
    sub.lang = ConsoleLanguage.objects.filter(lang = language)[0]
    cases = TestCase.objects.select_related().filter(is_sample=False, problem=prob_id)
    cases_list = list(cases)
    inputsequences = list()
    outputsequences = list()
    case_marks = list()
    for case in cases_list:
        inputsequences.append(str(case.input_sequence).replace('\r', ''))
        case_marks.append(int(case.score))
        outputsequences.append(str(case.output_sequence.replace('\r', '')))
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
    total_time = 0.0
    total_memory = 0.0
    for time_taken in result.time:
        total_time = total_time + time_taken
    sub.total_execution_time = total_time
    for memory_consumed in result.memory:
        total_memory  = total_memory + memory_consumed
    sub.total_memory_used = total_memory
    achieved_score = 0
    max_score = 0
    for res in result.output:
        data["id"] = i
        data["input"] = inputsequences[i].strip()
        data["expectedoutput"] = outputsequences[i].strip()
        data["actualoutput"] = res.strip()
        data["status"] = data["actualoutput"] == data["expectedoutput"]
        max_score = max_score + case_marks[i]
        if data["status"]:
            achieved_score = achieved_score + case_marks[i]
        i=i+1
        output.append(data)
        data = dict()
    print achieved_score
    
    sub.achieved_score = achieved_score
    if achieved_score == max_score:
        # marks = Submission.objects.filter(achieved_score = achieved_score, prob_id = prob_id)
        cur_points = sub.sub_made_by.profile.experience_points
        sub.sub_made_by.profile.experience_points = cur_points + sub.prob.reward_points
        sub.sub_made_by.profile.save()
    sub.save()
    print max_score
    js = json.dumps(output)
    print js
    print prob_id
    print lang
    print source_code
    return HttpResponse(js)