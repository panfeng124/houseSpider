from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from flask import Flask, request
import csv

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()

app = Flask(__name__)


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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def main():
    print(f'Hi')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.baidu.com')
    # driver.get('https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2')
    # driver.get('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/')

    time.sleep(120)  # 这里给你时间手动登录，或你自动完成登录
    driver.execute_script("window.open('https://cd.lianjia.com/chengjiao/rs%E5%87%AF%E8%8E%B1%E4%B8%BD%E6%99%AF/', '_blank');")
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    # 定义要植入的 JavaScript 代码
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
    # time.sleep(5)
    # driver.quit()


if __name__ == '__main__':
    # app.run(debug=True)
    print_hi('PyCharm')
    main()
    print_hi('end')
