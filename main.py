import threading
from src.httpServe import run_flask_app
from src.spider import initSpider, global_driver

if __name__ == '__main__':
    try:
        # 创建一个新线程来运行 Flask 应用
        flask_thread = threading.Thread(target=run_flask_app)
        flask_thread.start()
        initSpider()
    except Exception as e:
        print("exit")
        global_driver.quit()
        print("quit ok")
