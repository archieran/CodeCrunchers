from django.shortcuts import HttpResponse, render
# Create your views here.
def index(request):
    # return  HttpResponse("<h1>YASH<h1>")
    return render(request, 'www/home.html', {})
