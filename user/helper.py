
from random import randint
from urllib import response

from . import models
import datetime
import time
import pytz


import requests 

def send_otp(mobile, otp):
    mobile = [mobile, ]
    token = "aXw9ZVWoxzv9wIanoN95x-SwibOTrmtLALSlcbA_9jc="
    pid = "u0l8sbffrm"
    fnum = "+985000125475"
    p1 = "code" 
    v1 = otp
    response = requests.get(f"http://ippanel.com:8080/?apikey={token}&pid={pid}&fnum={fnum}&tnum={mobile[0]}&p1={p1}&v1={v1}")

    print('OTP: ', otp)
    print(response)
 





def get_random_otp():
    return  randint(1000, 9999)


def check_otp_expiration(mobile):
    try:
        user = models.MyUser.objects.get(mobile=mobile)
        T =  pytz.timezone('Asia/Tehran')
        now = datetime.datetime.now(T)
        otp_time = user.otp_create_time
        diff_time = now - otp_time
        print('OTP TIME: ', diff_time)

        if diff_time.seconds > 120:
            return False
        return True

    except models.MyUser.DoesNotExist:
        return False

