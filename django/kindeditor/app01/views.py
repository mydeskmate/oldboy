from django.shortcuts import render,HttpResponse
from django.forms import Form
from django.forms import fields
from django.forms import widgets
# Create your views here.

class ArticleForm(Form):
    title = fields.CharField(max_length=32)
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'i1'})
    )

    def clean_content(self):
        """
        对提交的内容进行xss防护
        :return:
        """
        old = self.cleaned_data['content']
        from utils.xss import xss
        return xss(old)







## kindeditor使用
CONTENT = ""
def kindeditor(request):
    if request.method == "GET":
        obj = ArticleForm()
        return render(request,'kindeditor.html',{'obj':obj})
    else:
        obj = ArticleForm(request.POST)
        if obj.is_valid():
            content = obj.cleaned_data['content']
            global CONTENT
            CONTENT = content
            return HttpResponse('...')
        else:
            return HttpResponse(',,,,,,,')


def see(request):
    """
    模拟查看上面提交的数据
    :param request:
    :return:
    """
    print(CONTENT)
    return render(request,'see.html',{'con':CONTENT})

def upload_img(request):
    """
    在kindeditor中上传图片
    :param request:
    :return:
    """
    import os
    import json
    upload_type = request.GET.get('dir')   #获取上传文件的文件类型，以便分类存放， 此处未试用
    file_obj = request.FILES.get('imgFile')  #imgFile是默认name
    file_path = os.path.join('static/temps',file_obj.name)
    with open(file_path,'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

    # 返回文件路径等数据到前端
    dic = {
        'error':0,
        'url':'/'+file_path,
        'message':'错误了'
    }
    return HttpResponse(json.dumps(dic))