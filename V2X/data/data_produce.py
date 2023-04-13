# 数据生成器
import numpy as np
import time

v1 = 25
v2 = 35

# 生成模拟噪声数据
y1 = np.random.normal(0, 10, 500)
y2 = np.random.normal(0, 10, 500)
y3 = np.random.normal(0, 10, 500)
y4 = np.random.normal(0, 20, 500)
y5 = np.random.normal(0, 10, 500)

# 生成模拟数据
for i in range(0, 100):
    y1[i] = y1[i] + (v2-v1)*i*0.1 + 50
    y2[i] = y2[i] + 50 + (v2-v1)*i*0.1
    y3[i] = y3[i] + 50 + (v2-v1)*i*0.1
for i in range(100, 150):
    y1[i] = y1[i] + (v2 - v1) * i * 0.1 + 50
    y2[i] = y2[i] + 50 + (v2 - v1) * i * 0.1
    y3[i] = y3[i] + 50 + (v2-v1)*i*0.1

for i in range(150, 500):
    y1[i] = y1[i] + (v2 - v1) * i * 0.1 + 50
    y2[i] = y2[i] + 50 + (v2 - v1) * i * 0.1
    y3[i] = y3[i] + 50 + (v2 - v1) * i * 0.1

np.save('y1.npy', y1)
np.save('y2.npy', y2)
np.save('y3.npy', y3)
