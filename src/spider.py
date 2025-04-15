# from selenium import webdriver
import time
import json
import platform
import undetected_chromedriver as uc  # 绕过人机验证的

global_driver = None


def goToLianJiaPage(url):
    global global_driver
    global_driver.get(url)
    js_file_path = './getLianJiaHouseInfo.js'
    # 读取 JavaScript 文件内容
    with open(js_file_path, 'r', encoding='utf-8') as file:
        js_content = file.read()

    # 使用 JSON 编码确保内容被正确转义
    escaped_js_content = json.dumps(js_content)  # 输出带双引号的合法 JS 字符串

    # 植入的 JS 代码
    custom_js = f"""
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.textContent = {escaped_js_content};
    document.head.appendChild(script);
    """
    # 执行 JavaScript 代码
    global_driver.execute_script(custom_js)
    print("execute_script")


global_driver = None


def initSpider():
    print("main:")
    # options = Options()
    options = uc.ChromeOptions()

    system = platform.system()

    # 使用profile，获取已有的登录信息
    if system == 'Darwin':
        print("当前系统是 macOS")
        options.add_argument( r'--user-data-dir="/Users/panfeng/Library/Application Support/Google/Chrome"')
    elif system == 'Windows':
        print("当前系统是 Windows")
        options.add_argument( r'--user-data-dir="C:\Users\59546\AppData\Local\Google\Chrome\User Data"')
    else:
        print("其他操作系统")
    # 指向你想用的配置文件夹（比如 Default、Profile 1）
    options.add_argument("--profile-directory=Default")
    # options.headless = False
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-blink-features=AutomationControlled")

    # 启动浏览器
    global global_driver
    global_driver = uc.Chrome(options=options)
    global_driver.get('https://www.baidu.com')
    # driver.get('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/')
    # driver.get('https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2')
    # driver.get('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/')

    # time.sleep(20)  # 这里给你时间手动登录，或你自动完成登录
    # driver.execute_script("window.open('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/', '_blank');")
    # driver.execute_script("window.open('https://www.baidu.com', '_blank');")
    #
    # tabs = driver.window_handles
    # driver.switch_to.window(tabs[1])
    print('initSpider ok')
    try:
        while True:
            time.sleep(5)
            global_driver.title  # 触发一次访问，判断浏览器是否还连着
    except Exception as e:
        print(f"[!] 退出")
        global_driver.quit()
