from bs4 import BeautifulSoup

def xss(old):
    """
    对提交的内容进行防xss攻击
    :param old:
    :return:
    """
    valid_tag = {
        'p':['class','id'],
        'img':['src'],
        'div':['class']
    }
    soup = BeautifulSoup(old, 'html.parser')

    tags = soup.find_all()
    for tag in tags:
        if tag.name not in valid_tag:
            tag.decompose()
        if tag.attrs:
            for k in list(tag.attrs.keys()):
                if k not in valid_tag[tag.name]:
                    del tag.attrs[k]
    content_str = soup.decode()
    return content_str