import json
from flask import Flask, request
import csv
import threading
from flask_cors import CORS
from .spider import goToLianJiaPage, nextRun
import os
import pandas as pd

app = Flask(__name__)
# 允许所有源的请求
CORS(app)


@app.route('/add_data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data or 'address' not in data or 'info' not in data:
        return 'Invalid data', 400

    address = data['address']
    csv_file = f'houseInfo/{address}.csv'
    info_list = data['info']
    new_df = pd.DataFrame(info_list)

    # print(data)

    required_keys = ["面积", "交易时间", "交易价格"]

    # 如果文件不存在，直接写入所有数据
    if not os.path.exists(csv_file):
        new_df.to_csv(csv_file, mode='w', index=False, header=True, encoding='utf-8')
    else:
        try:
            existing_df = pd.read_csv(csv_file)
        except Exception as e:
            existing_df = pd.DataFrame(columns=new_df.columns)

        # 计算实际存在的去重字段（可能部分字段缺失）
        actual_keys = [col for col in required_keys if col in new_df.columns and col in existing_df.columns]

        if not actual_keys:
            # 无可用于去重的字段，直接插入所有
            new_only_df = new_df
        else:
            # 确保字段类型一致（转换为字符串）
            for col in actual_keys:
                new_df[col] = new_df[col].astype(str)
                existing_df[col] = existing_df[col].astype(str)

            try:
                merged_df = pd.merge(new_df, existing_df, on=actual_keys, how="left", indicator=True)
                new_only_df = merged_df[merged_df["_merge"] == "left_only"]
                new_only_df = new_only_df[new_df.columns]
            except Exception as e:
                new_only_df = new_df  # merge失败也别中断，直接全部插入

        if not new_only_df.empty:
            new_only_df.to_csv(csv_file, mode='a', index=False, header=False, encoding='utf-8')

    if "nextPage" in data:
        goToLianJiaPage(address, data['nextPage'], True)
    else:
        nextRun()
    return '', 200


def run_flask_app():
    app.run(threaded=True)
