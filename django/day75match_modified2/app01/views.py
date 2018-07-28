from django.shortcuts import render,HttpResponse
from app01 import models
# Create your views here.
# def test(request):
#     # models.U2U.objects.create(b_id=1,g_id=1)
#     # models.U2U.objects.create(b_id=1,g_id=2)
#
#     # han = models.UserInfo.objects.filter(id=1).first()
#     # result = han.girls.all()
#     # for u in result:
#     #     print(u.g.nickname)
#
#     return HttpResponse('....')


def test(request):
    # han = models.UserInfo.objects.filter(id=1).first()
    # u = han.m.all()
    # for row in u:
    #     print(row.nickname)

    hua = models.UserInfo.objects.filter(id=4).first()
    v = hua.userinfo_set.all()
    for row in v:
        print(row.nickname)
    return HttpResponse('....')