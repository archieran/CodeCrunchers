from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import Http404
from django.conf import settings
from django.urls import reverse
from .models import Topic, Problem, ConsoleLanguage, Submission, TestCaseResult, Contest, ContestParticipant
from hackerrank.HackerRankAPI import HackerRankAPI
from django.utils import timezone
from .models import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Aggregate, Sum
import json
from django.http import JsonResponse, HttpResponseRedirect

# Begin Coding from here
@login_required
def evaluationhome(request):
    topics = Topic.objects.all()
    context = {
        'topics': topics,
        'active_tab': 'problems'
    }
    return render(request, 'evaluation/topics.html', context)

@login_required
def topic_problems(request, topic_var):
    try:
        probs = Problem.objects.select_related().filter(topic_id=topic_var)
        context = {
            'problems': probs,
            'active_tab': 'problems',
            'topic':Topic.objects.get(id=topic_var).topic_name,
        }
    except:
        raise Http404
    return render(request, 'evaluation/problems.html', context)

@login_required
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

@login_required
def contest_home(request):
    contests = Contest.objects.filter(is_active=True)
    context = {
        'active_tab': 'prac_home',
        'contests': contests
    }
    return render(request, 'evaluation/contest_home.html', context)
@login_required
def contest_details(request, contest_id):
    problems = Problem.objects.all().filter(contest__id = contest_id)
    contest = Contest.objects.filter(id = contest_id)[0]
    print contest
    context = {
        'contest_name':contest,
        'problems': problems,
        'contest_id' : contest_id,
        'active_tab':'prac_home'
    }
    return render(request, 'evaluation/contest_details.html', context)
@login_required
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
    print "Msg: " + str(msg)
    print "Error: "+ str(error)
    print result.output
    try:
        for res in result.output:
            data["id"] = i
            data["input"] = inputsequences[i].strip()
            data["expectedoutput"] = outputsequences[i].strip()
            data["actualoutput"] = res.strip()
            if error[i]:
                data["actualoutput"] = error[i]
            data["status"] = data["actualoutput"] == data["expectedoutput"]
            i=i+1
            output.append(data)
            data = dict()
    except:
        return HttpResponse(msg)
    js = json.dumps(output)
    print js
    print prob_id
    print lang
    print source_code
    
    return HttpResponse(js, content_type='application/json')
@login_required
def run_submission(request):

    # Variable Declarations
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
    i = 0
    actualoutputs = list()
    data = dict()
    output = list()
    total_time = 0.0
    total_memory = 0.0
    achieved_score = 0
    max_score = 0
    contest_question = False
    contest_score = 0
    

    if request.POST['contest_id']:
        contest_id = int(request.POST['contest_id'])
        contest = Contest.objects.filter(id = contest_id)[0]
        print "Contest ID: %d" % contest_id
        contest_question = True

    # Total Marks Calculations
    for case in cases_list:
        inputsequences.append(str(case.input_sequence).replace('\r', ''))
        case_marks.append(int(case.score))
        outputsequences.append(str(case.output_sequence.replace('\r', '')))
    result = compiler.run(
         {
            'source': source_code,
            'lang': lang,
            'testcases': inputsequences,
         }
    )
    msg = result.message
    error = result.error
    try:
        # Memory and Time Calculations
        for time_taken in result.time:
            total_time = total_time + time_taken
        sub.total_execution_time = total_time
        for memory_consumed in result.memory:
            total_memory  = total_memory + memory_consumed
        sub.total_memory_used = total_memory

        # Storing ouput of testcases in data
    
        for res in result.output:
            tcresult = TestCaseResult()
            data["id"] = i
            data["input"] = inputsequences[i].strip()
            data["expectedoutput"] = outputsequences[i].strip()
            data["actualoutput"] = res.strip()
            data["status"] = data["actualoutput"] == data["expectedoutput"]
            data["memory"] = result.memory[i]
            data["time"] = result.time[i]
            max_score = max_score + case_marks[i]
            sub.achieved_score = 0
            sub.save()
            tcresult.submission = sub
            if data["status"]:
                tcresult.status = "P"
            else:
                tcresult.status = "F"
            tcresult.time_submitted = timezone.now()
            tcresult.test_case = cases[i]
            print tcresult
            tcresult.save()
            if data["status"]:
                achieved_score = achieved_score + case_marks[i]
            i=i+1

            output.append(data)
            data = dict()

        # Calculating Reward Points
        max_reward_points = Problem.objects.values('reward_points').filter(id=prob_id)[0]['reward_points']
        scaled_marks = (achieved_score * max_reward_points )/max_score
        sub.achieved_score = int(scaled_marks)

        # Printing Stored and Calculated Variables
        print "Achieved Score: %d" % achieved_score
        print "Max Reward %d" % max_reward_points
        print "Max Score   : %f" % max_score
        print "Scaled Score: %f" % scaled_marks

        current_xp = user.profile.experience_points
        print "Current XP : %d" % current_xp
        previous_max_score = Submission.objects.filter(sub_made_by = user, prob = sub.prob).aggregate(Max('achieved_score')).values()[0]
        print "Previous Score: %d" % previous_max_score
        

        # Logic for XP Calculation
        if previous_max_score < scaled_marks:
            sub.sub_made_by.profile.experience_points = (current_xp - previous_max_score) + scaled_marks
            print "New XP : %d" % sub.sub_made_by.profile.experience_points
            sub.sub_made_by.profile.save()

        # Saving Contest
        if contest_question:
            #contest_participant = ContestParticipant.objects.filter(contest__id = contest_id, user = user)[0]
            contest_participant, created = ContestParticipant.objects.get_or_create(contest = contest, user = user)
            print contest_participant.user
            if created:
                contest_participant.achieved_score = 0
                
            #previous_contest_score = ContestParticipant.objects.filter(user = user, contest = contest_id).aggregate(Max('achieved_score')).values()[0]
            prev_sub_score = Submission.objects.filter(sub_made_by = user, contest = contest, prob = sub.prob).aggregate(Max('achieved_score')).values()[0]
            if prev_sub_score:
                if prev_sub_score < max_reward_points:
                    contest_participant.achieved_score = contest_participant.achieved_score - prev_sub_score + scaled_marks
            else:
                contest_participant.achieved_score = contest_participant.achieved_score + scaled_marks
            print "Prev contest sub : " + str(prev_sub_score)
            print "Current Contest : %d" % contest_participant.achieved_score
            
            sub.contest = contest
            contest_participant.save()
            
            # Do Not Erase or make any changes
            # print "Previous Contest: %d" % previous_contest_score
            # total_contest_score = Problem.objects.filter(contest = contest).aggregate(Sum('reward_points')).values()[0]
            # print "Total Contest Score : %d" % total_contest_score
            # if (contest_participant.achieved_score + scaled_marks) <= total_contest_score:
                # contest_participant.achieved_score = contest_participant.achieved_score + scaled_marks
                # print "New Contest Marks: %d" % contest_participant.achieved_score
                # contest_participant.save()

        # Saving Submissions and JSON
        sub.save()
    except TypeError:
        print msg
        return HttpResponse(msg)
    js = json.dumps(output)
    print js
    # print prob_id
    # print lang
    # print source_code

    return HttpResponse(js, content_type='application/json')
@login_required
def redirect_model_solution(request, prob_id):
    print prob_id
    request.session["model_sol_id"] = prob_id
    return HttpResponseRedirect(reverse('cc:console'))

def view_contest_leaderboard(request, con_id):
    print con_id
    submissions = ContestParticipant.objects.filter(contest__id = con_id)
    print submissions
    context = {
        'submissions':submissions,
        'active_tab':'prac_home',
        'contest_name':Contest.objects.get(id = con_id).title
    }

    return render(request, 'evaluation/contest_leaderboard.html', context)