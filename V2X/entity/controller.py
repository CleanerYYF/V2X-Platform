import time

from entity.rsu import RSU
from entity.computer import Computer
from entity.car import Car


class Controller:
    def __init__(self, id: str, regionid: int, ip: str):
        """
        控制节点初始化
        :param id: 控制节点编号
        :param regionid: 控制节点所属簇编号
        :param ip: 控制节点IP地址
        """
        self.id = id
        self.regionId = regionid
        self.ip = ip
        self.computer = {}
        self.task = []
        self.rsus = {}
        self.carsInfo = {}
        self.proportion = []
        self.schedule = []
        self.dataPool = {}

    def addCar(self, car: Car, rsu: RSU) -> None:
        """
        在簇中对应RSU下新增一辆车
        :param car: 车辆信息
        :param rsu: 车辆所属的RSU
        """
        self.carsInfo[rsu.id][car.id] = car

    def removeCar(self, car: Car, rsu: RSU) -> None:
        """
        在簇中对应RSU下删除一辆车
        :param car: 车辆信息
        :param rsu: 车辆所属的RSU
        :return: 无
        """
        self.carsInfo[rsu.id].pop(car.id)

    def addRSU(self, rsu: RSU) -> None:
        """
        簇中加入RSU
        :param rsu: dict格式的RSU信息
        """
        self.rsus[rsu.id] = rsu
        self.carsInfo[rsu.id] = rsu.car

    def addComputer(self, computer: Computer) -> None:
        """
        簇中加入Computer
        :param computer: dict格式的Computer信息
        """

    def dealTask(self, task: dict):
        """
        将数据融合任务根据taskTd字段查找拟定的划分规则进行划分，结果保存在类变量中
        :param task:字典格式源任务
        """


