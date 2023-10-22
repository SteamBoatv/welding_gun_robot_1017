import configparser
import os

class InitResource:
    def __init__(self):
        self.initPath("project/")
        self.initPath("resource/")
        self.initUserIni("resource/")
        self.initSysSetting("resource/")

    def initPath(self, dir):
        # 初始化相关路径
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(dir + '文件夹创建成功')

    def initUserIni(self, dir):
        # 初始化user.ini
        # 写入用户配置文件
        path = dir + "user.ini"
        if not os.path.exists(path):
            config = configparser.ConfigParser()
            config["DEFAULT"] = {
                "user_name": "admin",
                "password": "123",
                "remember": "True"
            }
            with open(path, 'w')as configfile:
                config.write(configfile)

    def initSysSetting(self, dir):
        # 初始化存储设置信息的配置文件
        #写入公司配置文件
        path = dir + "setting.ini"
        if not os.path.exists(path):
            config = configparser.ConfigParser()
            config["DEFAULT"] = {
                "company": "天海科技有限公司",
                "symbol": "/pic_rc/icon.jpg",
                "background": "/pic_rc/背景2.jpg"
            }
            with open(path, 'w')as configfile:
                config.write(configfile)
