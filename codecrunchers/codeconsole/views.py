from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from hackerrank.HackerRankAPI import HackerRankAPI
from django.conf import settings
# Create your views here.

def console(request):
	return render(request, 'codeconsole/console.html', {})

def runcode(request):
	print request.POST["code"]
	API_KEY = settings.HACKERRANK_API
	source_code = request.POST["code"]
	compiler = HackerRankAPI(API_KEY)
	result = compiler.run({'source': source_code,
                       'lang':'python',
					   'testcases':[""]
                       })
	data = result.output
	data[0].strip()
	return HttpResponse(data)