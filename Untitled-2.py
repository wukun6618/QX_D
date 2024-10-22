import pandas as pd
import matplotlib.pyplot as plt
import time

# 初始化数据
data = {
    "time": [],
    "principal": [],
    "profit": [],
    "rate_of_return": []
}

# 创建空DataFrame
df = pd.DataFrame(data)

# 定义更新数据的函数
def update_data(df):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    principal = 1000  # 这里可以替换为实际的本金
    profit = (len(df) + 1) * 50  # 示例收益，逐步增加
    rate_of_return = profit / principal  # 示例收益率

    # 添加新数据到DataFrame
    new_data = pd.DataFrame({
        "time": [current_time],
        "principal": [principal],
        "profit": [profit],
        "rate_of_return": [rate_of_return]
    })

    df = pd.concat([df, new_data], ignore_index=True)
    return df

# 每15分钟更新一次数据并保存到CSV文件
for _ in range(10):  # 示例运行10次，即150分钟
    df = update_data(df)
    df.to_csv('financial_data.csv', index=False)
    time.sleep(900)  # 等待15分钟

# 从CSV文件读取数据并绘制折线图
df = pd.read_csv('financial_data.csv')

plt.figure(figsize=(10, 6))

# 绘制本金曲线
plt.plot(df['time'], df['principal'], label='本金', marker='o')

# 绘制收益曲线
plt.plot(df['time'], df['profit'], label='收益', marker='o')

# 绘制收益率曲线
plt.plot(df['time'], df['rate_of_return'], label='收益率', marker='o')

plt.title('收益，本金和收益率折线图')
plt.xlabel('时间')
plt.ylabel('金额 / 收益率')
plt.xticks(rotation=45)  # 旋转x轴标签以便阅读
plt.legend()
plt.tight_layout()
plt.show()
