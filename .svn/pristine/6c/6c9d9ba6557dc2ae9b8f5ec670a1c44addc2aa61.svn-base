import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import re
import time


def show_qcode():#打开二维码图片
    pic = mpimg.imread("qcode.jpg")
    plt.imshow(pic)
    plt.axis("off")
    plt.show()


def delete_tag(name):#清除名字中的图标和span标签
    tag = re.findall("(<span.*?</span>)", name)
    for item in tag:
        name = name.replace(item, "")
    return name


def filter_emoji(desstr,restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def get_synckey(sync_list):#
    synckey = ""
    count = 1
    for item in sync_list:
        if count < len(sync_list):
            key = str(item["Key"]) + "_" + str(item["Val"]) + "|"
        else:
            key = str(item["Key"]) + "_" + str(item["Val"])
        count += 1
        synckey += key
    return synckey


def get_ctime():
    return str("%.3f" % time.time()).replace(".", "")


def get_localtime(create_time):
    localtime = time.localtime(create_time)
    return time.strftime("%Y-%m-%d %H:%M:%S", localtime)


def get_Cookie(cookies):
    cookie = ""
    for k,v in cookies.items():
        new = k + "=" + v + ";"
        cookie += new
    return cookie

