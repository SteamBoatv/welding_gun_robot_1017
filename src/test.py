import configparser
import os

import numpy as np
from PyQt5 import QtWidgets

import src.untitled

class MyWindow(QtWidgets.QMainWindow, src.untitled.Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    def hello(self):
        self.textEdit.setText("hello world")


# if __name__ == "__main__":
import jieba.posseg as pseg


def isname(single_word_string):
    pair_word_list = pseg.lcut(single_word_string)
    for eve_word, cixing in pair_word_list:
        if cixing == "nr":
            return True
    return False


single_word_string = "另选他人"
print(isname(single_word_string))

    # 当前文件路径
    # proDir = os.path.split(os.path.realpath(__file__))[0]
    # # 在当前文件路径下查找.ini文件
    # configPath = os.path.join(proDir, "config.ini")
    # print(configPath)
    # conf = configparser.ConfigParser()
    # # 读取.ini文件
    # conf.read(configPath)
    # # get()函数读取section里的参数值
    # name = conf.get("section1", "name")
    # print(name)
    # print(conf.sections())
    # print(conf.options('section1'))
    # print(conf.items('section1'))

    # 写入配置文件 set()
    # 修改指定的section的参数值
    # conf.set("section1", 'name', '3号')
    # # 增加指定section的option
    # conf.set("section1", "option_plus", "value")
    # name = conf.get("section1", "name")
    # print(name)
    # conf.write(open(configPath, 'w+'))
    # 增加section
    # conf.add_section("section_test_1")
    # conf.set("section_test_1", "name", "test_1")
    # conf.write(open(configPath, 'w+'))

    # import sys
    #
    # app = QtWidgets.QApplication(sys.argv)
    # myshow = MyWindow()
    # myshow.show()
    # sys.exit(app.exec_())
# 1.
    # import open3d as o3d
    #
    # pcd = o3d.io.read_point_cloud("../Car_body.ply")
    #
    # o3d.visualization.draw_geometries([pcd])
# 2.
#     import open3d as o3d
#
#     pcd = o3d.io.read_point_cloud(r"C:\Users\87058\Documents\pointcloud.ply")
#     vis = o3d.visualization.Visualizer()
#     vis.create_window()
#
#     # # 将点云添加至visualizer
#     vis.add_geometry(pcd)
#
#     # points = np.random.rand(10000, 3)
#     # point_cloud = o3d.geometry.PointCloud()
#     # point_cloud.points = o3d.utility.Vector3dVector(points)
#     # vis.visualization.draw_geometries([point_cloud])
#
#     # 让visualizer渲染点云
#     vis.poll_events()
#     vis.update_renderer()
#     vis.run()

    # import open3d as o3d
    # import numpy as np
    #
    # vis = o3d.visualization.Visualizer()
    # vis.create_window()
    #
    # points = []
    # colors = []
    # for i in range(5000):
    #     # 获取数据至 x,y,z r,g,b ,其中rgb范围为0-1.0
    #     x = ...
    #     y = ...
    #     z = ...
    #     r = ...
    #     g = ...
    #     b = ...
    #     points.append([x, y, z])
    #     colors.append([r, g, b])
    #
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(points)
    # pcd.colors = o3d.utility.Vector3dVector(colors)
    #
    # vis.add_geometry(pcd)
    # vis.poll_events()
    # vis.update_renderer()
    # vis.run()
