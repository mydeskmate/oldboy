from django.shortcuts import render,HttpResponse
from app01 import models

# Create your views here.
def index(request,*args,**kwargs):

    # if type_id:
    #     article_list = models.Article.objects.filter(article_type_id=type_id)
    # else:
    #     article_list = models.Article.objects.all()

    #分类查找文章表
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    condition = {}
    if type_id:
        condition['article_type_id'] = type_id

    article_list = models.Article.objects.filter(**condition)
    article_type_choices = models.Article.type_choices

    return render(
        request,
        'index.html',
        {
            'article_type_choices':article_type_choices,
            'type_id': type_id,
            'article_list':article_list
        },
    )

def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        input_code = request.POST.get('code')
        session_code = request.session.get('code')
        if input_code == session_code:
            pass
        else:
            pass


def check_code(request):
    from io import BytesIO
    from utils.random_check_code import rd_check_code

    img, code = rd_check_code()
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())


    # from PIL import Image,ImageDraw,ImageFont
    # from io import BytesIO
    # import random

    # f = BytesIO()
    # img = Image.new(mode='RGB',size=(120,30),color=(255,255,255))
    # draw = ImageDraw.Draw(img,mode='RGB')
    # draw.point([10,10],fill='red')
    # draw.point([20,10],fill='red')
    # draw.point([30,10],fill='red')
    # draw.point([40,10],fill='red')
    #
    # draw.line((15, 10, 50, 50), fill='red')
    # draw.line((45, 20, 100, 100), fill=(0, 255, 0))
    #
    # font = ImageFont.truetype('kumo.ttf',28)
    # draw.text([0,0],'python',(0,255,0),font=font)

    # f = BytesIO()
    # img = Image.new(mode='RGB',size=(120,30),color=(255,255,255))
    # draw = ImageDraw.Draw(img,mode='RGB')
    # char_list = []
    # for i in range(5):
    #     char = chr(random.randint(65,90))
    #     char_list.append(char)
    #     font = ImageFont.truetype("kumo.ttf",28)
    #     draw.text([i*24,0],char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
    #
    # img.save(f,'png')
    # data = f.getvalue()
    # #保存到session,用来验证
    # code = ''.join(char_list)
    # request.session['code'] = code
    # return HttpResponse(data)



