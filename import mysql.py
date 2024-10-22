import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import time

# 连接到 MySQL 数据库
conn = mysql.connector.connect(
    host='localhost',
    user='yourusername',
    password='yourpassword',
    database='financial_data_db'
)
cursor = conn.cursor()

# 检查表是否存在，如果不存在则创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS financial_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    principal FLOAT NOT NULL,
    profit FLOAT NOT NULL,
    rate_of_return FLOAT NOT NULL
)
''')

# 插入数据的函数
def insert_data():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    principal = 1000  # 替换为实际的本金
    cursor.execute("SELECT COUNT(*) FROM financial_data")
    count = cursor.fetchone()[0]
    profit = (count + 1) * 50  # 示例收益
    rate_of_return = profit / principal

    sql = "INSERT INTO financial_data (timestamp, principal, profit, rate_of_return) VALUES (%s, %s, %s, %s)"
    val = (current_time, principal, profit, rate_of_return)
    cursor.execute(sql, val)
    conn.commit()

# 每 15 分钟插入一次数据
for _ in range(10):  # 示例运行10次，即150分钟
    insert_data()
    time.sleep(900)  # 等待15分钟

# 从数据库读取数据并绘制折线图
df = pd.read_sql('SELECT * FROM financial_data', conn)

plt.figure(figsize=(10, 6))

# 绘制本金曲线
plt.plot(df['timestamp'], df['principal'], label='本金', marker='o')

# 绘制收益曲线
plt.plot(df['timestamp'], df['profit'], label='收益', marker='o')

# 绘制收益率曲线
plt.plot(df['timestamp'], df['rate_of_return'], label='收益率', marker='o')

plt.title('收益，本金和收益率折线图')
plt.xlabel('时间')
plt.ylabel('金额 / 收益率')
plt.xticks(rotation=45)  # 旋转x轴标签以便阅读
plt.legend()
plt.tight_layout()
plt.show()

# 关闭数据库连接
conn.close()
