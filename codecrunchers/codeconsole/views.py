from django.shortcuts import render, HttpResponse

# Create your views here.

def console(request):
	return render(request, 'codeconsole/console.html', {})