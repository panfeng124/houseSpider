# from selenium import webdriver
import time
import json
import platform
import undetected_chromedriver as uc  # 绕过人机验证的
import os
from urllib.parse import quote

global_driver = None
current_dir = os.path.dirname(os.path.abspath(__file__))
print(os.path.join(current_dir, '..', 'jsScript', 'lianJiaHouseInfo.js'))

# houseArray = {
#     "蜀南春郡": "https://cd.lianjia.com/chengjiao/rs%E8%9C%80%E5%8D%97%E6%98%A5%E9%83%A1/",
#     "凯莱丽景": "https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/",
# }
initHouseList = ["蜀南春郡", "凯莱丽景", "红树湾", "光明城市","鑫苑鑫都汇","戛纳湾金棕榈","远大都市风景","慕和南道","融创南湖逸家","保利创智锦城"]
addHouseList = ["蜀南春郡", "凯莱丽景", "红树湾", "光明城市"]
runType = "init"  # add | init
houseList = []
if runType == "add":
    houseList = addHouseList
else:
    houseList = initHouseList

currentIndex = 0
haveDone = False

js_file_path = os.path.join(current_dir, '..', 'jsScript', 'lianJiaHouseInfo.js')
# 读取 JavaScript 文件内容
with open(js_file_path, 'r', encoding='utf-8') as file:
    js_content = file.read()


def goToLianJiaPage(houseName, pageNum=1, isInit=False):
    global global_driver
    injected_js = f'let houseName = "{houseName}";\n let pageNum = {pageNum};\n'

    if isInit:
        injected_js += f'let isInit = true;\n'
    print(injected_js)

    injected_js += js_content

    if pageNum <= 1:
        url = "https://cd.lianjia.com/chengjiao/rs" + quote(houseName) + "/"
    else:
        url = "https://cd.lianjia.com/chengjiao/pg" + str(pageNum) + "rs" + quote(houseName) + "/"

    global_driver.get(url)

    # 使用 JSON 编码确保内容被正确转义
    escaped_js_content = json.dumps(injected_js)  # 输出带双引号的合法 JS 字符串
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


def initSpider():
    print("main:")
    # options = Options()
    options = uc.ChromeOptions()

    system = platform.system()

    # 使用profile，获取已有的登录信息
    if system == 'Darwin':
        print("当前系统是 macOS")
        options.add_argument(r'--user-data-dir=/Users/panfeng/Library/Application Support/Google/Chrome')
    elif system == 'Windows':
        print("当前系统是 Windows")
        # options.add_argument(r"--user-data-dir=C:\Users\59546\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r"--user-data-dir=E:\code\houseSpider\chromeInfo")
    else:
        print("其他操作系统")

    # 指向你想用的配置文件夹（比如 Default、Profile 1）
    options.add_argument("--profile-directory=spiderProfile")
    # options.add_argument("--profile-directory=Default")
    options.headless = False
    # options.headless = True
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

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
    nextRun()
    global haveDone
    try:
        while not haveDone:
            time.sleep(5)
            global_driver.title  # 触发一次访问，判断浏览器是否还连着
    except Exception as e:
        print(f"[!] 退出")
        global_driver.quit()


def nextRun():
    global haveDone
    global currentIndex
    # goToLianJiaPage("蜀南春郡", "https://cd.lianjia.com/chengjiao/rs%E8%9C%80%E5%8D%97%E6%98%A5%E9%83%A1/")

    if currentIndex < len(houseList):
        aName = houseList[currentIndex]
        print(aName)
        goToLianJiaPage(aName, 1, runType == "init")
        currentIndex += 1
    else:
        currentIndex = 0
        haveDone = True
