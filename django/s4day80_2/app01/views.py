from django.shortcuts import render,HttpResponse
import json

# Create your views here.
def users(request):
    v = request.GET.get('funcname')
    print('请求来了')
    user_list = [
        'alex','eric','egon'
    ]
    user_list_str = json.dumps(user_list)
    temp = "%s(%s)" %(v,user_list_str)
    print(temp)
    return HttpResponse(temp)