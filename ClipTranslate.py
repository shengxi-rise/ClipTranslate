# -*- coding: utf-8 -*-
import json

import pyperclip
import keyboard
import threading
import time

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from pynput.keyboard import Controller, Key

keyctrl = Controller()

secretid = ''
secretkey = ''

def translate(text):
    try:
        cred = credential.Credential(secretid, secretkey)

        httpProfile = HttpProfile()
        httpProfile.endpoint = "tmt.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        params = "{\"SourceText\":\"" + text + "\",\"Source\":\"auto\",\"Target\":\"en\",\"ProjectId\":1300003896}";
        common_client = CommonClient("tmt", "2018-03-21", cred, "ap-guangzhou", profile=clientProfile)
        content = common_client.call_json("TextTranslate", json.loads(params))
        return content['Response']['TargetText']

    except TencentCloudSDKException as err:
        print(err)


def getclipboard():
    clipboard_content = pyperclip.paste()
    return clipboard_content


def excute():
    copy()  # Replication sometimes fails
    print("copy end")
    time.sleep(1)  # Pause to make sure the copy is complete
    result = translate(getclipboard())
    #  Empty the shear board
    # pyperclip.copy('')
    if result != None:
        print(result)
        pyperclip.copy(result)
        paste()


# def other_task():
#     while True: Hello
#         print("Other task is keyctrl...")
#         time.sleep(1)  # Simulate time-consuming operations


def paste():
    keyctrl.press(Key.ctrl)
    keyctrl.press('v')
    keyctrl.release('v')
    keyctrl.release(Key.ctrl)


def copy():
    keyctrl.press(Key.ctrl)
    keyctrl.press('c')
    keyctrl.release('c')
    keyctrl.release(Key.ctrl)


keyboard.add_hotkey('ctrl+i', excute)

# Run other tasks in new threads
# Multithreading is not needed for the time being
# threading.Thread(target=other_task).start()

keyboard.wait()
