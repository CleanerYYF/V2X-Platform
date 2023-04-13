from entity.sensor import Sensor
from entity.rsu import RSU
import time
import math


class Car:
    def __init__(self, id: str, ip: str, regionid: int, ctrlIP: str):
        """
        初始化路边单元RSU
        :param id: RSU编号
        :param ip: RSU IP地址
        :param regionid: 簇编号
        :param ctrlIP: 控制节点IP
        """
        self.task = []
        self.data = {}
        self.nowRsuId = ''
        self.rsu = {}
        self.newRsu = object
        self.result = {}
        self.fuseOrder = 0
        self.id = id
        self.ip = ip
        self.regionIds = [regionid, ]
        self.ctrlIPs = [ctrlIP, ]

    def addToRegion(self, regionid: int, ctrlIP: str, rsu: RSU) -> None:
        """
        新加入一个簇，修改簇编号和控制中心IP地址
        :param regionid: 簇编号
        :param ctrlIP: 簇IP地址
        :param rsu: 所在簇的rsu
        """
        self.regionIds.append(regionid)
        self.ctrlIPs.append(ctrlIP)
        self.rsu[rsu.id] = rsu
        self.nowRsuId = rsu.id

    def bornTask(self, rawTask: dict) -> None:
        """
        按照任务编号生成任务
        :param rawTask: 初始任务
        :return: 无返回值，任务存到类变量中
        """
        if rawTask['taskId'] == 't0003':
            t0 = 4 / (27 * 1000000)  # 在802.11g定义的54Mbps的WiFi中单个字符传输时间，用于传输时间定义
            if rawTask['period'] == 1:
                # 定义第一阶段A两次测距任务
                # carA红外测距
                self.task.append(
                    {'taskId': 't0003', 'num': 1, 'dealer': self, 'distance': (self, rawTask['end']), 't0': t0})
                # carA报文测距
                self.task.append(
                    {'taskId': 't0003', 'num': 2, 'dealer': self, 'distance': (self, rawTask['end']), 't0': t0})
            if rawTask['period'] == 2:
                # 定义第二阶段RSU测距任务
                y1data = [self.result['y1result']['distance'], self.result['y1result']['dealTime']]
                y2data = [self.result['y2result']['distance'], self.result['y2result']['dealTime']]
                self.task.append({'taskId': 't0003', 'num': 3, 'dealer': self.rsu[0], 'distance': (self, rawTask['end']), 'y1data': y1data, 'y2data': y2data, 't0': t0})

        if rawTask['taskId'] == 'local001':
            t0 = 4 / (27 * 1000000)  # 在802.11g定义的54Mbps的WiFi中单个字符传输时间，用于传输时间定义
            # 定义红外测距任务
            self.task.append(
                {'taskId': 'local001', 'num': 1, 'dealer': self, 'distance': (self, rawTask['end']), 't0': t0})
            # carA报文测距
            self.task.append(
                {'taskId': 'local001', 'num': 2, 'dealer': self, 'distance': (self, rawTask['end']), 't0': t0})
            # RSU报文测距
            self.task.append(
                {'taskId': 'local001', 'num': 3, 'dealer': self.rsu, 'distance': (self, rawTask['end']), 't0': t0})
            # carA执行数据融合与最终的时间计算任务由RSU生成

    def dealTask(self, task: dict):
        """
        执行数据融合任务
        :return: 字典格式的处理结果
        """
        if task['taskId'] == 't0003':
            if task['num'] == 1:
                beginTime = time.time()
                # 执行红外测距
                y1sensor = Sensor('y1')
                y1 = y1sensor.getDistance(task['order'])
                t1 = time.time() - beginTime
                self.task.append({'taskId': task['taskId'], 'num': 2, 't0': task['t0'], 'y1': y1, 't1': t1, 'begin': time.time(), 'order': task['order']})

            if task['num'] == 3:
                beginTime = time.time()
                # 计算传输时间
                transTime = len(str(task)) * task['t0']
                # 执行红外测距
                y2sensor = Sensor('y2')
                y2 = y2sensor.getDistance(task['order'])
                t3 = transTime
                t4 = time.time() - beginTime
                # 检查信号值
                changeFlag = 0
                if task['signalRsu2'] >= 0:
                    changeFlag = 1
                self.task.append({'taskId': task['taskId'], 'num': 4, 't0': task['t0'], 'y2': y2, 't3': t3, 't4': t4, 't1': task['t1'], 't2': task['t2'], 'begin': time.time(), 'order': task['order'], 'aChangeFlag': changeFlag})

            if task['num'] == 6:
                beginTime = time.time()
                # 计算传输时间
                transTime = len(str(task)) * task['t5g0']
                # print(transTime)
                t1234567 = task['t123456'] + transTime - beginTime + time.time()
                self.data = {'taskId': task['taskId'], 'totalTime': t1234567, 'x': task['x'], 'kalmanTime': task['kalmanTime']}
