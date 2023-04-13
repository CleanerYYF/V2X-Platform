from entity.sensor import Sensor
import time

class RSU:

    def __init__(self, id: str, ip: str, regionid: int, ctrlIP: str, mixRegionFlag: int):
        """
        初始化路边单元RSU
        :param id: RSU编号
        :param ip: RSU IP地址
        :param regionid: 簇编号
        :param ctrlIP: 控制节点IP
        """
        self.fuseOrder = 0
        self.task = []
        self.data = {}
        self.id = id
        self.ip = ip
        self.regionIds = [regionid, ]
        self.ctrlIPs = [ctrlIP, ]
        self.changeFlag = ''
        self.car = {}
        # 断网时单独一个小车进行数据融合标志，仅在非无缝切换场景下有断网时延使用
        self.singleCarFlag = 0
        self.mixRegionFlag = mixRegionFlag

    def addCar(self, car):
        self.car[car.id] = car

    def removeCar(self, car):
        self.car.pop(car.id)

    def addToRegion(self, regionid: int, ctrlIP: str) -> None:
        """
        新加入一个簇，修改簇编号和控制中心IP地址
        :param regionid: 簇编号
        :param ctrlIP: 簇IP地址
        """
        self.regionIds.append(regionid)
        self.ctrlIPs.append(ctrlIP)

    def getTask(self, task: dict) -> None:
        """
        获取任务，修改相应的任务类变量
        :param task: 字典格式的任务
        """

    def dealTask(self, task: dict):
        """
        执行数据融合任务
        :return: 字典格式的处理结果
        """
        if task['taskId'] == 't0003':
            if task['num'] == 2 and self.singleCarFlag == 0:
                beginTime = time.time()
                # 计算传输时间
                transTime = len(str(task)) * task['t0']
                # 执行RSU报文测距
                y31 = (beginTime - task['begin']) * 1  # 体现报文测距，结果不参与计算考虑
                y3sensor = Sensor('y3')
                y3 = y3sensor.getDistance(task['order'])
                self.data['y31'] = y31
                yRA = y3 / 2
                self.data['yRA'] = yRA
                self.data['y1'] = task['y1']
                t2 = transTime - beginTime + time.time()
                self.task.append({'taskId': 't0003', 'num': 3, 't0': task['t0'], 't2': t2, 't1': task['t1'], 'order': task['order']})

            if task['num'] == 2 and self.singleCarFlag == 1:
                # 计算传输时间
                transTime = len(str(task)) * task['t0']
                task['taskId'] = 'changeB'
                task['num'] = 'A_Only1'
                self.dealTask(task)

            if task['num'] == 4:
                beginTime = time.time()
                # 计算传输时间
                transTime = len(str(task)) * task['t0']
                # 执行RSU报文测距
                y32 = (beginTime - task['begin']) * 1  # 体现报文测距，结果不参与计算考虑
                y3sensor = Sensor('y3')
                y3 = y3sensor.getDistance(task['order'])
                self.data['y32'] = y32
                yRB = y3 / 2
                self.data['yRB'] = yRB
                self.data['y2'] = task['y2']
                y3 = self.data['yRA'] + self.data['yRB']
                # print(y3)
                t12345 = max(task['t1'] + task['t2'], task['t4'] + transTime) + task['t3']
                # rsu和控制中心与计算中心的传输采用5G协议，重新计算t5g0
                t5g0 = 8/(500 * 1000000)
                self.task.append({'taskId': 't0003', 'num': 5, 't0': task['t0'], 't5g0': t5g0, 't12345': t12345, 'y1': self.data['y1'], 'y3': y3, 'y2': self.data['y2'], 'begin': time.time(), 'order': task['order']})
