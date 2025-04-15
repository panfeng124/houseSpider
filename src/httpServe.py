import json
from flask import Flask, request
import csv
import threading
from flask_cors import CORS
from .spider import goToLianJiaPage

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


# js发起请求，让python翻页，并注入js
@app.route('/nextUrl', methods=['POST'])
def nextUrl():
    data = request.get_json()
    if not data:
        return 'Invalid data', 400
    newUrl = data['url']
    goToLianJiaPage(newUrl)


def run_flask_app():
    app.run(threaded=True)
