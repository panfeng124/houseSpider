import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import platform

# 设置中文显示
import matplotlib
system = platform.system()
if system == 'Darwin':
    print("当前系统是 macOS")
    matplotlib.rcParams['font.sans-serif'] = ['Hiragino Sans GB']  # 使用Hiragino Sans GB
    # matplotlib.rcParams['font.sans-serif'] = ['AppleGothic']   # 或者使用 AppleGothic
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
elif system == 'Windows':
    print("当前系统是 Windows")
    matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 使用Hiragino Sans GB
    # matplotlib.rcParams['font.sans-serif'] = ['AppleGothic']   # 或者使用 AppleGothic
    matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
else:
    print("其他操作系统")

# 读取所有 CSV 文件
import os
import glob




# 定义读取文件夹中的所有csv文件
def load_data_from_folder(folder_path):
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    df_list = []
    for file in all_files:
        df = pd.read_csv(file)

        # 只将非空的 DataFrame 加入列表
        if not df.empty:
            df_list.append(df)
        else:
            print(f"警告: 文件 {file} 是空的，已跳过")

    # 如果 df_list 为空，返回一个空的 DataFrame
    if df_list:
        return pd.concat(df_list, ignore_index=True)
    else:
        print("警告: 没有有效的数据文件，返回空的 DataFrame")
        return pd.DataFrame()  # 返回一个空的 DataFrame


# 加载数据
folder_path = './houseInfo'  # 数据所在文件夹路径
df = load_data_from_folder(folder_path)

# 查看数据结构
print(df.head())

# 数据清洗：剔除非法数据（如交易价格缺失或负值）
df = df[df['交易价格'] > 0]  # 剔除交易价格小于等于0的记录
df = df.dropna(subset=['交易价格', '面积'])  # 剔除交易价格或面积缺失的记录

# 剔除异常交易价格：使用 IQR 方法来识别异常值
Q1 = df['交易价格'].quantile(0.25)
Q3 = df['交易价格'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['交易价格'] >= lower_bound) & (df['交易价格'] <= upper_bound)]

# 计算每平方米价格
df['每平方米价格'] = df['交易价格'] / df['面积']

# 查看数据情况
print(df.head())

# 转换交易时间为日期格式
df['交易时间'] = pd.to_datetime(df['交易时间'], format='%Y.%m.%d')  # 使用点分隔符
# 过滤掉2023年之前的记录
df = df[df['交易时间'] >= pd.to_datetime('2023-01-01')]

# 按楼盘名字绘制每平方米价格趋势
plt.figure(figsize=(12, 6))

# 使用 Seaborn 绘制各个楼盘的每平方米价格趋势
sns.lineplot(data=df, x='交易时间', y='每平方米价格', hue='楼盘名字', marker='o')

# 使用 Seaborn 绘制各个楼盘的每平方米价格趋势（去掉数据点，线条更细）
# sns.lineplot(data=df, x='交易时间', y='每平方米价格', hue='楼盘名字', marker=False)


# 设置图形标题和标签
plt.title('各楼盘每平方米价格趋势', fontsize=16)
plt.xlabel('交易时间', fontsize=12)
plt.ylabel('每平方米价格 (元)', fontsize=12)

# 调整 x 轴标签的显示方式
# 格式化日期显示，避免显示过多的日期标签
# 设置x轴日期格式，间隔显示每月或者每3个月一个标签
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))  # 每个月的1号显示
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 设置显示格式为 年-月
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator())  # 可选：每月显示为次要标记
plt.xticks(rotation=45)  # 旋转x轴标签

# 显示图形
plt.tight_layout()
plt.savefig("result/xxx.png")  # 保存图像为文件
