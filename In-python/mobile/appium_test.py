
from appium import webdriver
from appium.options.android import UiAutomator2Options


# 配置所需的参数
desired_caps = {
    # 平台名称，这里是 Android
    "platformName": "Android",
    # 安卓系统版本号，可通过模拟器设置查看
    "platformVersion": "15",
    # 设备名称，可以任意填写，但最好与模拟器名称相关
    "deviceName": "Medium Phone API 35",
    # 要测试的应用包名
    "appPackage": "com.android.chrome",
    "appActivity": "com.google.android.apps.chrome.Main",
    # 不重置应用状态，可加快测试速度
    "noReset": True
}

options = UiAutomator2Options().load_capabilities(desired_caps)
# 连接 Appium 服务器，这里默认使用本地的 4723 端口
driver = webdriver.Remote('http://localhost:4723', options=options)

try:
    # 在这里可以添加具体的测试操作，例如查找元素、点击按钮等
    # 示例：等待 5 秒
    import time
    time.sleep(5)

except Exception as e:
    print(f"测试过程中出现错误: {e}")
finally:
    # 测试结束后关闭驱动
    driver.quit()