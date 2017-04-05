from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from hackerrank.HackerRankAPI import HackerRankAPI
from django.conf import settings
from .models import ConsoleLanguage, SavedCode
from django.contrib.auth.decorators import login_required
from evaluation.models import Problem
from django.http import HttpResponseForbidden
# Create your views here.

@login_required
def console(request):
    context = {}
    id =  request.session["model_sol_id"]
    display_model = False
    if id:
        code = Problem.objects.filter(id = id)[0].model_solution
        print str(code)
        display_model = True
        context["display_model"] = True
        context["code"] = code

    context["languages"] = ConsoleLanguage.objects.filter(is_active=True)
    context["active_tab"] = 'console'

    return render(request, 'codeconsole/console.html', context)

def runcode(request):
    print "Inside runcode"
    # print request.POST["code"]
    API_KEY = settings.HACKERRANK_API
    source_code = request.POST.get("code")
    compiler = HackerRankAPI(API_KEY)
    lang = request.POST["lang"]
    lang = lang.lower()
    userinp = request.POST.get("userinp")
    userinp = str(userinp)
    print(userinp)
    result = compiler.run({'source': source_code,
                           'lang': lang,
                           'testcases': [userinp]
                           })
    # Make no changes to below code, please !
    print source_code
    msg = result.message
    outputs = result.output
    error = result.error
    data = ""
    if len(msg) > 0:
        data = msg
    if error is not None:
        if error != False:
            # Runtime error
            data = error[0]
    if error is not None and error[0] == False and msg is not None and len(msg) == 0:
        if outputs is not None:
            # Expected output
            data = outputs[0]
    if len(msg) != 0:
        # Compilation error
        data = msg
    # Can make changes from here
    return HttpResponse(data)


def get_ace_name(request):
    lang_query = request.POST["lang"]
    print lang_query
    res = ConsoleLanguage.objects.get(lang=lang_query)
    return HttpResponse(res.ace_file_name)

def update_livecode(request):
    vals = dict(request.POST)
    sc, created = SavedCode.objects.get_or_create(user = request.user)
    sc.code = vals.get("code")[0]
    sc.save()
    return HttpResponse("Last Saved : " + str(timezone.now()).split('.')[0])

def get_live_code(request):
    try:
        sc = SavedCode.objects.get(user = request.user)
        msg = sc.code
    except SavedCode.DoesNotExist:
        msg = "79f1eb5e35810df3389588190f7dd2ae"
    return  HttpResponse(msg)