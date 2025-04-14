from selenium import webdriver
import time
import json
from flask import Flask, request
import csv
from selenium.webdriver.chrome.options import Options
import threading
from flask_cors import CORS
import undetected_chromedriver as uc ##绕过人机验证的

#options = Options()
options = uc.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\59546\AppData\Local\Google\Chrome\User Data") #使用profile，获取已有的登录信息

# 指向你想用的配置文件夹（比如 Default、Profile 1）
options.add_argument("--profile-directory=Default")
# 启动浏览器
driver = uc.Chrome(options=options)

app = Flask(__name__)
# 允许所有源的请求
CORS(app)

@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data or 'address' not in data or 'info' not in data:
        return 'Invalid data', 400

    address = data['address']
    info = data['info']
    csv_file = f'{address}.csv'

    # 检查 CSV 文件是否存在，如果不存在则创建
    try:
        with open(csv_file, 'x', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=info.keys())
            writer.writeheader()
    except FileExistsError:
        pass

    # 将数据写入 CSV 文件
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=info.keys())
        writer.writerow(info)

    return 'Data saved successfully', 200

#js发起请求，让python翻页，并注入js
@app.route('/nextUrl', methods=['POST'])
def nextUrl():
    data = request.get_json()
    if not data:
        return 'Invalid data', 400

    newUrl = data['url']
    driver.get( newUrl)

    js_file_path = './getHouseInfo.js'
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
    driver.execute_script(custom_js)
    return 'Data saved successfully', 200

def run_flask_app():
    app.run(threaded=True)

def main():
    driver.get('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/')
    # driver.get('https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2')
    # driver.get('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/')

    # time.sleep(20)  # 这里给你时间手动登录，或你自动完成登录
    # driver.execute_script("window.open('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/', '_blank');")
    # # driver.execute_script("window.open('https://www.baidu.com', '_blank');")
    #
    # tabs = driver.window_handles
    # driver.switch_to.window(tabs[1])

    # 定义要追加的 JavaScript 文件路径
    js_file_path = './getHouseInfo.js'
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
    driver.execute_script(custom_js)
    print("execute_script")
    # 保持程序运行，避免自动关闭浏览器
    try:
        while True:
            time.sleep(5)
            driver.title  # 触发一次访问，判断浏览器是否还连着
    except Exception as e:
        print(f"[!] 退出")
        driver.quit()

if __name__ == '__main__':
    # 创建一个新线程来运行 Flask 应用
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    print('PyCharm')
    main()
    print('end')
