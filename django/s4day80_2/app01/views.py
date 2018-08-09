from django.shortcuts import render,HttpResponse
import json

# Create your views here.
def users(request):
    """
    jsonp
    :param request:
    :return:
    """
    v = request.GET.get('funcname')
    print('请求来了')
    user_list = [
        'alex','eric','egon'
    ]
    user_list_str = json.dumps(user_list)
    temp = "%s(%s)" %(v,user_list_str)
    print(temp)
    return HttpResponse(temp)

def new_users(request):
    """

    :param request:
    :return:
    """
    # 简单请求
    # user_list = [
    #     'alex', 'eric', 'egon'
    # ]
    # user_list_str = json.dumps(user_list)
    # obj = HttpResponse(user_list_str)
    # obj['Access-Control-Allow-Origin'] = "*"
    # return obj

    # 复杂请求
    print(request.method)
    if request.method == "OPTIONS":
        obj = HttpResponse()
        obj['Access-Control-Allow-Origin'] = "*"
        obj['Access-Control-Allow-Methods'] = "DELETE"
        return obj
    obj = HttpResponse("ddddddddddddd")
    obj['Access-Control-Allow-Origin'] = "*"
    return obj

