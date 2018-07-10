from django.shortcuts import render,HttpResponse,render

# Create your views here.
def index(request):
    user_list = [
        1,2,3
    ]
    return render(request,'index.html',{'user_list':user_list})

def edit(request,a1):
    print(a1)
    return HttpResponse('....')



# def edit(request,*args,**kwargs):
#     print(args,**kwargs)
#     return HttpResponse('...')