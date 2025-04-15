import json
from flask import Flask, request
import csv
import threading
from flask_cors import CORS
from .spider import goToLianJiaPage
import os
app = Flask(__name__)
# 允许所有源的请求
CORS(app)


@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data or 'address' not in data or 'info' not in data:
        return 'Invalid data', 400

    address = data['address']
    info_list = data['info']  # 假设是一个字典数组
    if not isinstance(info_list, list) or not all(isinstance(item, dict) for item in info_list):
        return 'Invalid info format', 400

    csv_file = f'{address}.csv'

    # 如果文件不存在，创建并写入表头
    file_exists = os.path.exists(csv_file)
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        # 用第一个字典的 key 作为表头
        fieldnames = info_list[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for info in info_list:
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
