from django.shortcuts import render

# Create your views here.
def jsonp(request):
    return render(request,'jsonp.html')


def cors(request):
    return render(request,'cors.html')