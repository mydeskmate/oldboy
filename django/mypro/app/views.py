
from django.shortcuts import HttpResponse,render


def login(request):
    return render(request,'login.html')