import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os
from glob import glob

# 配置matplotlib使用macOS上的中文字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Hiragino Sans GB']  # 使用Hiragino Sans GB
# matplotlib.rcParams['font.sans-serif'] = ['AppleGothic']   # 或者使用 AppleGothic
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# Step 1: 读取多个CSV文件并合并
folder_path = './houseInfo'
csv_files = glob(os.path.join(folder_path, '*.csv'))

# 读取并合并所有CSV文件
data = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# 查看数据概况
print("数据预览:")
print(data.head())

# Step 2: 数据预处理
# 处理交易时间列
data['交易时间'] = pd.to_datetime(data['交易时间'], format='%Y.%m.%d')

# 填补挂牌价为空的数据，可以选择用均值或中位数填充，或删除这些行
data['挂牌价'].fillna(data['挂牌价'].median(), inplace=True)

# 转换‘是否精装’列为布尔值
data['是否精装'] = data['是否精装'].astype(bool)

# Step 3: 可视化分析

# 1. 交易价格的时间趋势
data['year_month'] = data['交易时间'].dt.to_period('M')
monthly_avg_price = data.groupby('year_month')['交易价格'].mean()

plt.figure(figsize=(10, 6))
monthly_avg_price.plot()
plt.title('成都二手房每月平均交易价格趋势')
plt.xlabel('日期')
plt.ylabel('平均价格 (万元)')
plt.grid(True)
plt.savefig("result/monthly_avg_price.png")  # 保存图像为文件


# 2. 交易价格与面积的关系
plt.figure(figsize=(8, 6))
sns.scatterplot(data=data, x='面积', y='交易价格', hue='是否精装', palette='coolwarm', alpha=0.7)
plt.title('交易价格与面积的关系')
plt.xlabel('面积 (平方米)')
plt.ylabel('交易价格 (万元)')
plt.savefig("result/price_vs_area.png")  # 保存图像为文件


# 3. 精装与非精装房的价格差异
plt.figure(figsize=(8, 6))
sns.boxplot(data=data, x='是否精装', y='交易价格')
plt.title('精装与非精装房的价格差异')
plt.xlabel('是否精装')
plt.ylabel('交易价格 (万元)')
plt.savefig("result/price_vs_decor.png")  # 保存图像为文件


# 4. 楼盘的价格分布
plt.figure(figsize=(10, 6))
sns.boxplot(data=data, x='楼盘名字', y='交易价格')
plt.title('各楼盘交易价格分布')
plt.xlabel('楼盘名字')
plt.ylabel('交易价格 (万元)')
plt.xticks(rotation=90)
plt.savefig("result/loupan_price_distribution.png")  # 保存图像为文件


# Step 4: 统计和总结
# 你可以在这里进一步处理数据，生成统计报告或执行回归预测等
print("\n数据描述:")
print(data.describe())

# 例如：查看每个楼盘的平均交易价格
average_prices_by_loupan = data.groupby('楼盘名字')['交易价格'].mean().sort_values(ascending=False)
print("\n各楼盘的平均交易价格:")
print(average_prices_by_loupan)
