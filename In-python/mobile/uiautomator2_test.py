import time
import uiautomator2 as u2

d = u2.connect('emulator-5554')

app_package = "com.android.chrome"
app_activity = "com.google.android.apps.chrome.Main"
d.app_start(app_package, app_activity)

url_bar = d(resourceId="com.android.chrome:id/url_bar")
time.sleep(3)
if url_bar.exists:
    url_bar.clear_text()
    url_bar.set_text("https://www.baidu.com")
    print("成功输入内容到 URL 栏")
else:
    print("未找到 URL 栏元素")

d.press(187)


width, height = d.window_size()

start_x = int(width * 0.1)  # 起始点 x 坐标，这里取屏幕宽度的 10% 位置
start_y = int(height * 0.5)  # 起始点 y 坐标，这里取屏幕高度的 50% 位置
end_x = int(width * 0.9)  # 结束点 x 坐标，这里取屏幕宽度的 90% 位置
end_y = int(height * 0.5)  # 结束点 y 坐标，这里取屏幕高度的 50% 位置

d.swipe(start_x, start_y, end_x, end_y, duration=0.5)

clear_all_button = d(resourceId="com.google.android.apps.nexuslauncher:id/clear_all")

if clear_all_button.exists:
    clear_all_button.click()
    print("成功点击元素")
else:
    print("未找到指定元素")
while True:
    time.sleep(1)