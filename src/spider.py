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
initHouseList = [
    "蜀南春郡",
    "凯莱丽景",
    "红树湾",
    "光明城市",
    "鑫苑鑫都汇",
    "戛纳湾金棕榈",
    "远大都市风景",
    "慕和南道",
    "融创南湖逸家",
    "保利创智锦城",
    "川发天府上城",
    "远大中央公园",
    "锦官丽城亲水湾",
    "蜀郡",
    "中德英伦联邦",
    "华润凤凰城", "保利百合花园",
    "阳光华苑",
    "保利叶语",
    "保利心语花园",
    "中海锦江城",
    "中海兰庭",
    "朗基天香",
    "时代晶科名苑",
    "南城都汇汇朗园五期",
#上面是我提供的，
#下面的是AI提供的

    #锦江区
    "伊泰天骄",
    "人居东湖长岛",
    "建发央玺",
    "滨河湾",
    "环球汇天誉",
    "中化润达丰滨江樾城",
    "塔子山壹号",
    "万科城市花园",
    "锦天府",
    "人居锦城峰荟荟澜阁",
    "华都美林湾",
    "锦江国际花园",
    "青羊区",
    "绿地成都新里城",
    "成都花园别墅",
    "金林半岛",
    "金沙鹭岛四期",
    "博瑞都市花园",
    "中大君悦金沙五期",
    "远洋万和公馆",
    "蓝光雍锦园别墅",
    "金沙云庭",
    "华润金悦湾",
    "仁和金沙",
    "凯德风尚",
    "石人小区",
    "优品道曦岸",

    #武侯区
    "鹭岛国际四期",
    "丽景华庭二期",
    "中华名园",
    "置信丽都花园",
    "双楠小区",
    "龙湖金楠天街",
    "保利花园",
    "中粮祥云国际生活区",
    "蓝光雍锦世家",
    "首信汇",
    "红牌楼广场小区",
    "新希望花园",
    "棕北小区",
    "棕南小区",
    "锦官新城",

    #金牛区
    "中大君悦金沙五期",
    "西城首峻",
    "华侨城纯水岸",
    "蓝光花满庭",
    "保利公园里",
    "天回镇银杏园小区",
    "凯德风尚",
    "万科金域西岭",
    "量力健康城",
    "营门口小区",
    "蜀汉路小区",
    "星河路小区",
    "五块石玉局庵东路小区",

    #成华区
    "保利康桥",
    "河畔华苑二期",
    "华润二十四城",
    "蓝光时代",
    "中铁建青秀城",
    "首创天禧",
    "融创玖阙府",
    "万科魅力之城",
    "隆鑫九熙",
    "蓝光东方天地",
    "成华奥园广场",


    #高新区
    "中大文儒德",
    "中海城南一号",
    "复地金融岛",
    "中海九号公馆",
    "誉峰二期",
    "伊泰天骄",
    "中洲锦城湖岸",
    "建发翡翠鹭洲",
    "朗基御今缘",
    "凯德世纪名邸",
    "大源欢乐颂",
    "保利心语花园",
    "华润凤凰城",
    "中海兰庭",
    "南苑小区",

    #天府新区
    "麓湖生态城麒麟荟",
    "麓湖生态城云树",
    "蔚蓝卡地亚",
    "中海右岸",
    "远大中央公园",
    "南湖国际社区",
    "万科翡翠公园",
    "保利天空之城",
    "合能铂悦华庭",
    "红星美凯龙生活广场",
    "海伦春天",
    "雅居乐花园",
    "融创玖棠府",
    "天投北鑫苑",
]
initHouseList = list(set(initHouseList))

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
        # options.add_argument(r'--user-data-dir=/Users/panfeng/Library/Application Support/Google/Chrome')
        options.add_argument(r'--user-data-dir=/Users/panfeng/coder/myProject/houseSpider/chromeInfo')
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
    options.add_argument("--disable-extensions")
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
