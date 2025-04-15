import threading
from src.httpServe import run_flask_app
from src.spider import initSpider


if __name__ == '__main__':
    # 创建一个新线程来运行 Flask 应用
    # flask_thread = threading.Thread(target=run_flask_app)
    # flask_thread.start()
    initSpider()
