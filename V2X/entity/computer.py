import time
from algorithm.kalman_filter import Kalman_filter

class Computer:
    def __init__(self, id: str, ip: str, ctrlIp: str, regionid: int):
        """
        初始化计算节点
        :param id: 编号
        :param ip: IP地址
        :param ctrlIp: 控制中心IP
        :param regionid: 簇编号
        """
        self.result = {}
        self.task = []
        self.order = 0
        self.id = id
        self.ip = ip
        self.ctrlIp = ctrlIp
        self.regionId = regionid

    def dealTask(self, task: dict):
        """
        处理任务，通过if识别任务标号字段进行相应处理,结果保存在result类变量中
        :param task:字典格式的任务
        :return: 计算结果
        """

        if task['taskId'] == 't0001':
            distance = task['param']
            return int(distance[0] + distance[1] + distance[2] + distance[3])/2

        if task['taskId'] == 't0003':
            # 计算传输时间
            # transTime = len(str(task)) * task['t0']

            if task['num'] == 5:
                # 计算传输时间
                transTime = len(str(task)) * task['t5g0']
                t1 = time.time()
                kalmanFusion = Kalman_filter(1, 0.1, 1, 25, 35, 10, 100, 100, 100)
                kalmanFusion.OnceFuse(task['y1'], task['y2'], task['y3'])
                # print(task['y3'])
                kalmanTime = time.time() - t1
                t123456 = transTime + task['t12345'] + kalmanTime
                self.task.append({'taskId': task['taskId'], 'num': 6, 't0': task['t0'], 't5g0': task['t5g0'], 'kalmanTime': kalmanTime, 't123456': t123456, 'x': kalmanFusion.xhat[-1]})
                self.task.append({'taskId': task['taskId'], 'num': 7, 't0': task['t0'], 't5g0': task['t5g0'], 'kalmanTime': kalmanTime, 't123456': t123456, 'x': kalmanFusion.xhat[-1]})

