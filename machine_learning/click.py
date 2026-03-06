# 升级pip3 pip3 install --upgrade pip
# 先安装 pip3 install numpy
import numpy as np
# 先安装 pip3 install matplotlib
import matplotlib.pyplot as plt

# 读入训练数据
train = np.loadtxt('data/click.csv',delimiter=',',skiprows=1)
train_x = train[:,0]
train_y = train[:,1]

# 绘图
plt.plot(train_x, train_y,'o')

# 随便给参与定义值之后画直线用于演示误差
theta_0 = 1
theta_1 = 2
y = theta_0 + theta_1 * train_x
plt.plot(train_x, y, label='f(x) = 1 + 2x')
plt.show()
