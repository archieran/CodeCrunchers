from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hackerrank.HackerRankAPI import HackerRankAPI
from django.conf import settings
from .models import ConsoleLanguage
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
# Create your views here.

def console(request):
    context = {}
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
