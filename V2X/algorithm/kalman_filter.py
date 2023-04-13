import numpy as np

# 三维卡尔曼滤波算法

class Kalman_filter:
    xhat = [10, ]  # 距离后验估计值
    p = [4, ]

    def __init__(self, f: int, b: float, h: int, v1: float, v2: float, q: float,
                 r1: float, r2: float, r3: float):
        """
        初始化数据融合环境
        :param f: 状态转移矩阵
        :param b: 控制矩阵
        :param h: 测量系统参数
        :param x0: 两车初始距离
        :param v1: A车初始速度
        :param v2: B车初始速度
        :param p: 初始设置的后验估计方差
        :param q: 外部扰动得到的速度方差
        :param r1: 车载红外传感器的测量方差
        :param r2: 车载报文测距传感器的测量方差
        :param r3: RSU中报文测距传感器的测量方差
        """

        self.h = np.full([3, 1], h)
        self.f = f
        self.b = b
        self.u = v2-v1
        self.q = q
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r = np.diag([r1, r2, r3])  # 测量误差协方差矩阵

    def OnceFuse(self, y1: float, y2: float, y3: float):
        """
        执行一次数据融合
        :param y1: 传感器1得到的测量结果，即红外测得的距离
        :param y2: 传感器2得到的测量结果，即车间通信报文得到的距离
        :param y3: 传感器3得到的测量结果，即RSU通信报文得到的距离
        :param order: 数据融合的次序号
        :return: 结果保存在self.xhat中
        """

        # 观测数据转换为观测矩阵
        # print(y3)
        # self.y3.append(y3)
        # self.y1.append(y1)
        z = np.array([y1, y2, y3]).reshape(3, 1)

        # 先验估计
        x_hat_minus = self.f * self.xhat[-1] + self.b*self.u
        p_minus = self.p[-1]+self.q

        # 更新
        k = np.dot(np.dot(p_minus, self.h.T), np.linalg.inv(np.dot(np.dot(self.h, p_minus), self.h.T)+self.r))

        self.xhat.append((x_hat_minus+np.dot(k, (z-np.dot(self.h, x_hat_minus))))[0][0])
        self.p.append((1-np.dot(k, self.h))*p_minus)