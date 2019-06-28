# coding=utf-8
import base64
import os
import re
from time import sleep

import requests


def getText(_url):
    _data = None
    for i in range(3):  # Try 3 times,interval 3 seconds
        try:
            r = requests.get(_url,  timeout=(3, 7))
            r.raise_for_status()  # check status:200
            r.encoding = r.apparent_encoding  # Ensure decoding successful

            _data = r.text
        except:
            _data = None
            sleep(3)  # Try 3 times,interval 3 seconds

        if len(_data) > 1:
            break
        else:
            print('Request Fail')
    return _data

def Decode(encodestr):
    missing_padding = 4 - len(encodestr) % 4
    if missing_padding:
        encodestr += '=' * missing_padding
    try:
        base64_decrypt = base64.decodebytes(encodestr.encode('utf-8')).decode('utf-8')
    except:
         print('decode error')
    else:
        return base64_decrypt


def Encode(decodestr):
    base64_encrypt = base64.b64encode(decodestr.encode('utf-8')).decode('utf-8')
    return base64_encrypt


if __name__ == "__main__":

    exeDir = '.\pinginfoview'
    exe = "PingInfoView.exe"

    # 在线解析
    url = 'https://xxxxxxxxxxxxxxxx'
    
    txt = getText(url)

    # # 离线解析
    # with open("ssr.txt", "rb") as f:
    #     txt = f.read().decode()

    # print (txt)
    ssrList = Decode(txt).split('\n')

    savefile = open(exeDir+'\PingInfoView_hosts.txt', 'w')
    for ssr in ssrList:
        if len(ssr) > 5:
            # print(len(ssr),ssr[6:])
            # print(ssr)
            if Decode(ssr[6:]):
                decode_ssr = Decode(ssr[6:]).split('/?')
                if len(decode_ssr) > 1:
                    ssr_info = decode_ssr[0]
                else:
                    ssr_info = decode_ssr
                # print(ssr_info)
                ssr_detial = (re.split(':|&', ssr_info))
                server = ssr_detial[0]
                savefile.write(server+'\n')
    savefile.close()

    runExe = os.system(exeDir+'\\'+exe)
