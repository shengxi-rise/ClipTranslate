import json
import pyperclip
import keyboard
import time
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from pynput.keyboard import Controller, Key

### TODO: 后续把报错信息全都显示到弹窗上

class ClipboardTranslator:
    def __init__(self, secretid, secretkey, projectid, hotkeys, lang):
        self.secretid = secretid
        self.secretkey = secretkey
        self.keyctrl = Controller()
        self.projectid = str(projectid)
        self.hotkeys = hotkeys
        self.lang = lang
        self.running = True  # 可用于控制线程

    def translate(self, text):
        try:
            cred = credential.Credential(self.secretid, self.secretkey)

            httpProfile = HttpProfile()
            httpProfile.endpoint = "tmt.tencentcloudapi.com"
            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile

            params = "{\"SourceText\":\"" + text + "\",\"Source\":\"auto\",\"Target\":\"" + self.lang + "\",\"ProjectId\":" + self.projectid + "}"
            common_client = CommonClient("tmt", "2018-03-21", cred, "ap-guangzhou", profile=clientProfile)
            try:
                content = common_client.call_json("TextTranslate", json.loads(params))
                return content['Response']['TargetText']
            except  json.decoder.JSONDecodeError as e:
                print(e)
                return "快捷键不可用"

        except TencentCloudSDKException as err:
            return "请检查配置信息"

    def get_clipboard(self):
        return pyperclip.paste()

    def copy(self):
        self.keyctrl.press(Key.ctrl)
        self.keyctrl.press('c')
        self.keyctrl.release('c')
        self.keyctrl.release(Key.ctrl)

    def paste(self):
        self.keyctrl.press(Key.ctrl)
        self.keyctrl.press('v')
        self.keyctrl.release('v')
        self.keyctrl.release(Key.ctrl)

    def execute(self):
        self.copy()
        time.sleep(1)  # 确保复制完成
        result = self.translate(self.get_clipboard())
        if result:
            print(result)
            pyperclip.copy(result)
            self.paste()

    def set_hotkey(self):
        keyboard.add_hotkey(self.hotkeys, self.execute)
        # keyboard.wait()   单独开了一个进程，不需要再wait了

    def change_hotkey(self, hotkeys):
        self.hotkeys = hotkeys
        keyboard.remove_all_hotkeys()  # 清空绑定的hotkey
        keyboard.add_hotkey(self.hotkeys, self.execute)  # 重新添加
