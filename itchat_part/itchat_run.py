import time
from wxpy import *
import os
import requests
import random
from apscheduler.schedulers.background import BackgroundScheduler
os.environ['DJANGO_SETTINGS_MODULE'] = 'wechat.settings'
import django
django.setup()
from wechat_app.models import *
from wechat.settings import TULIN_KEY_LIST, TULIN_API
from wechat.settings import STATICFILES_DIRS, BASE_DIR
import configparser


def login_action():
    os.remove(os.path.join(STATICFILES_DIRS[0], "QR.png"))
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, "itchat_part", "wechat.cfg"), encoding='utf-8')
    config.set("status", "login", "True")
    config.write(open(os.path.join(BASE_DIR, "itchat_part", "wechat.cfg"), "w"))


def logout_action():
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, "itchat_part", "wechat.cfg"), encoding='utf-8')
    config.set("status", "login", "False")
    config.write(open(os.path.join(BASE_DIR, "itchat_part", "wechat.cfg"), "w"))

#
#



def run():
    sched = BackgroundScheduler()
    bot = Bot(cache_path=True)
    @bot.register(Friend)
    def friend_reply(msg):
        data = {
            'key': random.choice(TULIN_KEY_LIST),  # Tuling Key
            'info': msg.text,  # 这是我们发出去的消息
            'userid': 'wechat-robot',  # 这里你想改什么都可以
        }
        # 我们通过如下命令发送一个post请求
        r = requests.post(TULIN_API, data=data).json()
        msg.reply_msg(r.get("text"))

    @bot.register(Group)
    def group_reply(msg):
        chatroom_nickname = msg.sender.name  # 群名
        keyword = msg.text  # 关键词
        chatroom = Chatroom.objects.get(nickname=chatroom_nickname)
        if chatroom:
            current_time = int(time.time())
            if current_time in range(chatroom.start_time, chatroom.end_time):
                reply = ReplyToChatroom.objects.filter(chatroom__nickname=chatroom_nickname,
                                                       reply__keyword__contains=keyword).values("msg", "filepath",
                                                                                                "reply__type").first()
                if reply:
                    reply_nickname = "@" + msg.member.name
                    if reply["reply__type"] == 1:  # 文字信息
                        msg.reply_msg(msg=reply_nickname + reply["msg"])
                    elif reply["reply__type"] == 2:  # 图片
                        msg.reply_msg(msg=reply_nickname)
                        msg.reply_image(path=reply["filepath"])
                    elif reply["reply__type"] == 3:  # 文件
                        msg.reply_msg(msg=reply_nickname + " 发送文件中，请稍等。")
                        msg.reply_file(path=reply["filepath"])
            else:
                print("not in time")

    sched.start()
    embed()


if __name__ == '__main__':
    pass
