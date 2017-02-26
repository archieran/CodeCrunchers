from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hackerrank.HackerRankAPI import HackerRankAPI
from django.conf import settings
from .models import ConsoleLanguages
# Create your views here.

def console(request):
	context = {}
	context["languages"] = ConsoleLanguages.objects.all()
	return render(request, 'codeconsole/console.html', context)

def runcode(request):
	#print request.POST["code"]
	API_KEY = settings.HACKERRANK_API
	source_code = request.POST["code"]
	compiler = HackerRankAPI(API_KEY)
	lang = request.POST["lang"]
	lang = lang.lower()
	result = compiler.run({'source': source_code,
                       'lang':lang,
					   # 'testcases':[""]
                       })
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
			#Expected output
			data = outputs[0]
	if len(msg) != 0:
		#Compilation error
		data = msg
	return HttpResponse(data)