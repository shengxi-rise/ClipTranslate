import customtkinter as ctk
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import configparser
import os
import keyboard
from ClipTranslateClass import ClipboardTranslator

# 定义数据保存的文件路径
config_file = "resource/config.ini"
# 如果配置文件不存在，则创建一个新的配置文件
if not os.path.exists(config_file):
    config = configparser.ConfigParser()

    # 添加默认的配置内容
    config["UserData"] = {
        "secretid": "",
        "secretkey": "",
        "projectid": "",
        "shortcut": "ctrl+i",
    }

    # 创建并写入配置文件
    with open(config_file, 'w') as file:
        config.write(file)

# 设置主题和颜色
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 创建窗口
app = ctk.CTk()
app.title("ClipTranslate")
app.geometry("400x500")
app.iconbitmap("resource\logo.ico")


# 加载已保存的数据
def load_data():
    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)
        return {
            "secretid": config.get("UserData", "secretid", fallback=""),
            "secretkey": config.get("UserData", "secretkey", fallback=""),
            "projectid": config.get("UserData", "projectid", fallback=""),
            "shortcut": config.get("UserData", "shortcut", fallback="Ctrl+i"),
        }
    return {}


# 保存用户输入的数据
def save_data():
    config = configparser.ConfigParser()
    config["UserData"] = {
        "secretid": secretid.get(),
        "secretkey": secretkey.get(),
        "projectid": projectid.get(),
        "shortcut": shortcut.get()
    }
    with open(config_file, "w") as file:
        config.write(file)


# 切换主题颜色
def toggle_theme():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        ctk.set_appearance_mode("Light")
        # theme_button.configure(text="切换到黑夜模式")
    else:
        ctk.set_appearance_mode("Dark")
        # theme_button.configure(text="切换到白天模式")


# 创建按钮以显示输入结果
def show_inputs():
    save_data()  # 保存用户输入的数据
    value1 = secretid.get()
    value2 = secretkey.get()
    value3 = projectid.get()
    result_label.configure(text=f"SecretId: {value1}\nSecretKey: {value2}\nProjectId: {value3}")


# 创建弹窗
def create_popup(message, duration=2000):
    popup = ctk.CTkToplevel(app)
    popup.geometry("300x100")

    # 设置无边界和透明度
    popup.overrideredirect(True)  # 去除边框和标题栏
    popup.attributes("-alpha", 0.9)  # 设置透明度，0为完全透明，1为不透明
    popup.attributes("-topmost", True)  # 保持窗口在最上层

    label = ctk.CTkLabel(popup, text=message, font=("Arial", 16))
    label.pack(expand=True, pady=10)

    # 自动关闭弹窗
    popup.after(duration, popup.destroy)


# 快捷键检测
def monitor_shortcut():
    shortcut_key = keyboard.read_hotkey(suppress=False)
    # print(shortcut_key)
    shortcut.set(shortcut_key)
    # create_popup(f"快捷键设置为: {shortcut_key}", duration=2000)
    save_data()
    translator.change_hotkey(shortcut_key)
    # return shortcut_key
    # save_data()


# 创建托盘图标
def create_image():
    image = Image.open("resource/ui.png")  # 替换为你的图片路径
    image = image.resize((256, 256), Image.LANCZOS)  # 调整图片大小以适应托盘图标  好像不起作用
    return image


# 恢复窗口
def restore_window(ico):
    # icon.stop()
    app.after(0, app.deiconify)


# 退出
def quit_app(icon):
    icon.stop()
    app.quit()


# 处理最小化事件的函数
def minimize_to_tray():
    if app.state() == 'iconic':
        app.withdraw()  # 隐藏窗口


# 监听窗口状态变化的函数
def check_window_state():
    if app.state() == 'iconic':  # 当窗口最小化时
        minimize_to_tray()
    app.after(100, check_window_state)


# 加载配置文件

user_data = load_data()

translator = ClipboardTranslator(secretid=user_data['secretid'], secretkey=user_data['secretkey'],
                                 projectid=user_data['projectid'],
                                 hotkeys=user_data['shortcut'])


def refresh_class():
    global translator
    translator = ClipboardTranslator(secretid=secretid.get(), secretkey=secretkey.get(),
                                     projectid=projectid.get(),
                                     hotkeys=shortcut.get())
    translator.change_hotkey(shortcut.get())  # 重启这个进程


# 启动后台线程
keyboard_thread = threading.Thread(target=translator.set_hotkey(), daemon=True)
keyboard_thread.start()

# UI整体layout
# SecretId 输入
label1 = ctk.CTkLabel(app, text="SecretId:", font=("华文行楷", 16))
label1.pack(pady=5)
secretid = ctk.CTkEntry(app, placeholder_text="输入SecretId", font=("Verdana", 14))
secretid.pack(pady=5)
secretid.insert(0, user_data["secretid"])

# SecretKey 输入
label2 = ctk.CTkLabel(app, text="SecretKey:", font=("华文行楷", 16))
label2.pack(pady=5)
secretkey = ctk.CTkEntry(app, placeholder_text="输入SecretKey", font=("Helvetica", 14))
secretkey.pack(pady=5)
secretkey.insert(0, user_data["secretkey"])

# ProjectId 输入
label4 = ctk.CTkLabel(app, text="ProjectId:", font=("华文行楷", 16))
label4.pack(pady=5)
projectid = ctk.CTkEntry(app, placeholder_text="输入ProjectId", font=("Helvetica", 14))
projectid.pack(pady=5)
projectid.insert(0, user_data["projectid"])

# 快捷键显示
label3 = ctk.CTkLabel(app, text="当前快捷键:", font=("华文行楷", 16))
label3.pack(pady=5)
shortcut = ctk.StringVar(value=user_data.get("shortcut", "Ctrl+i"))
shortcut_display = ctk.CTkLabel(app, textvariable=shortcut, font=("Arial", 14))
shortcut_display.pack(pady=5)
# 设置快捷键按键
shortcut_button = ctk.CTkButton(app, text="设置快捷键", command=monitor_shortcut, font=("华文行楷", 16))
shortcut_button.pack(pady=10)
# 保存设置按键
button = ctk.CTkButton(app, text="保存设置", command=lambda: (show_inputs(), refresh_class()), font=("华文行楷", 16))
button.pack(pady=10)

# 创建结果显示标签
result_label = ctk.CTkLabel(app, text="", font=("Arial", 14))

result_label.pack(pady=10)

# 创建主题切换按钮
# theme_button = ctk.CTkButton(app, text="切换到白天模式", command=toggle_theme)
# theme_button.pack(pady=20, side=ctk.LEFT, fill=ctk.BOTH, expand=False, padx=5)

# 托盘菜单
menu = (item('显示', restore_window), item('退出', quit_app))
icon = pystray.Icon("test", create_image(), "ClipTranslate", menu)
threading.Thread(target=icon.run, daemon=True).start()

# 启动检查窗口状态的线程
check_window_state()

app.mainloop()
