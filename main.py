from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def main():
    # driver = webdriver.Edge(ChromeDriverManager().install())
    driver = webdriver.Chrome()
    # driver.get('https://www.baidu.com')
    driver.get('https://www.cdzjryb.com/SCXX/Default.aspx?action=ucEveryday2')
    # 定义要植入的 JavaScript 代码
    # 定义要追加的 JavaScript 文件路径
    js_file_path = './test.js'
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
    print_hi('PyCharm')
    main()
    print_hi('end')
