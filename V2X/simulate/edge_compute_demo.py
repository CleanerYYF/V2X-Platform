from entity.controller import Controller
from entity.rsu import RSU
from entity.computer import Computer
from entity.car import Car
from algorithm.kalman_filter import Kalman_filter
from matplotlib import pyplot as plt
import numpy as np

# *********融合测距应用场景初始化*********
# 初始化控制节点
controller = Controller('ctrl1001', 1234, '127.0.0.1')
# 初始化计算节点
computer = Computer('cpt1001', '127.0.0.1', '127.0.0.1', 1234)
# 初始化RSU
rsu = RSU('rsu1001', '127.0.0.1', 1234, '127.0.0.1', 0)
# 初始化carA
carA = Car('carA', '127.0.0.1', 1234, '127.0.0.1')
# 初始化carB
carB = Car('carB', '127.0.0.1', 1234, '127.0.0.1')
# 将Computer加入1234簇中
controller.addComputer(computer)
# 将RSU加入1234号簇中
controller.addRSU(rsu)
# 将车辆AB加入1234号簇中
controller.addCar(carA, rsu)
controller.addCar(carB, rsu)
carA.addToRegion(1234, '127.0.0.1', rsu)
carB.addToRegion(1234, '127.0.0.1', rsu)


# 在802.11b定义的11Mbps的WiFi中单个字符传输时间，用于传输时间定义
t0 = 8 / (20 * 1000000)
# 记录总时延
totalTime = 0
# 记录卡尔曼滤波时延
kalmanTime = 0
# 融合得到的距离序列
x = []
for i in range(0, 500):
    # A车生成第一阶段任务
    task1 = {'taskId': 't0003', 'num': 1, 't0': t0, 'end': carB, 'order': i}
    carA.dealTask(task1)
    # A 向RSU请求的任务
    task2 = carA.task[-1]
    # print(task2['y1'])
    # RSU处理任务2
    rsu.dealTask(task2)

    # RSU发给B的任务
    task3 = rsu.task[-1]
    task3['signalRsu2'] = -1

    # B处理任务，并检测是否有满足信号强度的新信号
    carB.dealTask(task3)

    # B发给RSU的结果任务
    task4 = carB.task[-1]

    # RSU处理任务4
    rsu.dealTask(task4)

    # RSU发给controller和computer处理的任务
    task5 = rsu.task[-1]

    # computer处理任务
    computer.dealTask(task5)

    # 发给A的返回结果的任务
    task6 = computer.task[-2]

    # 发给B的返回结果的任务
    task7 = computer.task[-1]

    # A处理任务
    carA.dealTask(task6)

    totalTime = totalTime + carA.data['totalTime']
    kalmanTime = kalmanTime + carA.data['kalmanTime']
    x.append(carA.data['x'])

print('总时延：'+str(totalTime)+'秒')
print('kalman滤波时延:'+str(kalmanTime)+'秒')
print('最小通信时延:'+str(totalTime - kalmanTime)+'秒')
# print('最终融合得到的距离序列' + str(x) + ' (单位：米)')
# print('方差P'+str(KalmanFilter_3d.KalmanFusion3d.p))

y1 = np.load('../data/y1.npy')
y2 = np.load('../data/y2.npy')
y3 = np.load('../data/y3.npy')
x_ = range(1, 201)
plt.figure(1)
plt.plot(x_, y1[:200], color='green', label = 'Car A Result', linewidth=1)
plt.plot(x_, y2[:200], color='orange', label= 'Car B Result', linewidth=1)
plt.plot(x_, y3[:200], color='#409ed7', label = 'RSU Result', linewidth=1)
plt.plot(x_, x[:200], color='red', label = 'Data Merge Result', linewidth=1)
plt.xlabel('Data Acquisition Sequence')
plt.ylabel('Distance AB/m')
plt.legend()
plt.figure(2)
plt.plot(x_,Kalman_filter.p[:200], label = 'P', color='#ffc700', linewidth=1)
plt.xlabel('Data Acquisition Sequence')
plt.ylabel('Estimated variance')
plt.legend()

plt.show()

