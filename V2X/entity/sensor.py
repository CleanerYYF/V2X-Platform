import numpy

class Sensor:
    result = ''
    data = []

    def __init__(self, result: str):
        """
        初始化数据采集节点
        :param result: 需要采集的数据
        """
        self.result = result
        self.data = (numpy.load('../data/'+result+'.npy')).tolist()

    def getTask(self, task: dict) -> None:
        """
        获取数据采集任务，结果保存在task类变量中
        :param task: 数据采集任务
        """
        self.task.append(task)

    def getDistance(self, orderNum: int):
        """
        执行数据采集任务，返回结果
        """
        # return self.data[orderNum*5 : (orderNum+1)*5]
        return self.data[orderNum]


    def sendData(self) -> None:
        """
        将结果返回给请求数据获取的节点，涉及网络通信和安全问题
        """
