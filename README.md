# 车联网边缘计算任务处理模拟平台

### 系统组件：

1. car：联网车辆
2. rsu：路边基站
3. controller：边缘控制节点
4. computer：边缘服务器
5. sensor：传感器

1~4均具有计算、存储和网络处理资源，通过dealTask函数处理任务

5内部逻辑为文件读取，通过读取文件读取操作模拟数据采集，数据需根据模拟场景预先生成

### 交互方式

传输的消息为json格式，即键值对，如下

```json
{
    "taskId " : 模拟任务编号（必须）;
    "num"：模拟任务中子任务编号（必须）；
    具体服务数据等其他内容
}
```

交互过程中的消息传输时延，通过网络传输速率和消息数据量大小计算而来

### 过程模拟步骤

1. 确定需要模拟的场景、对执行服务的算法进行实现，确定taskId
2. 确定传输流程以及每个过程中的消息，确定各个过程中的num和消息结构
3. 在simulate中实现场景，获取数据，模拟流程

### PS

- 现有代码中对基于卡尔曼滤波的数据融合任务进行了模拟，可结合内容理解

- 本项目对于数据丢包率等指标未进行模拟，可fork完善工程
- 在python中的time.time()时间戳函数精度较低，现发现不适宜本项目中的低时延时间统计，可以使用datetime模块统计时间戳进而统计时延（https://www.zkxjob.com/49954）