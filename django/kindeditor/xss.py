content = """
<p id="i1" a="123" b="999">
    <script>alert(123)</script>
</p>
<p id="i2">
    <img src="/static/temps/6.jpg" />
</>
"""


from bs4  import BeautifulSoup
# soup = BeautifulSoup(content,'html.parser')

# 查找标签
# tag = soup.find(name='img')
# print(tag)


# 查找子标签
# tag = soup.find(name='p')
# sc = tag.find('script')
# print(sc)

#根据id查找
# v = soup.find(attrs={'id':'i2'})
# print(v)

#根据name查找 只找到第一个
# v = soup.find(name='p')
# print(v)

#查找所有的标签
# tags = soup.find_all(name="p")
# for tag in tags:
    # print(tag)
    # print(tag.name)

# 删除不合法标签
# soup = BeautifulSoup(content,'html.parser')
# valid_tag = ['p','img','div']
# tags = soup.find_all()
# for tag in tags:
#     if tag.name not in valid_tag:
#         tag.decompose()
# print(soup)
# # 获取标签的字符串形式
# print(soup.decode())
#

# 指定标签的属性
valid_tag = {
    'p':['class','id'],
    'img':['src'],
    'div':['class']
}
soup = BeautifulSoup(content,'html.parser')
tags = soup.find_all()
for tag in tags:
    if tag.name not in valid_tag:
        tag.decompose()
    if tag.attrs:
        for k in list(tag.attrs.keys()):
            if k not in valid_tag[tag.name]:
                del tag.attrs[k]
content_str = soup.decode()
print(content_str)


