from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
import sys
import sample
import ctrl_inexbot
import threading
import time
# class moving(threading.Thread):
#     def __init__(self,a):
#         super(moving,self).__init__()
#         self.myclass:Main_window=a
#         self.pre=False
#     def run(self):
#         while True:
#             #print(self.myclass.keep9)
#             #print(self.myclass.keep15)
#             if(self.myclass.keep9):
#                 self.pre=True
#                 self.myclass.control_class.bot_class.move_jog(6, -1)
#             else:
#                 if self.pre==True:
#                     self.pre=False
#                     self.myclass.control_class.bot_class.stop_jog(6)
#             if(self.myclass.keep15):
#                 self.pre=True
#                 self.myclass.control_class.bot_class.move_jog(6,1)
#             else:
#                 if self.pre==True:
#                     self.pre=False
#                     self.myclass.control_class.bot_class.stop_jog(6)
#             time.sleep(0.05)




class Main_window(QtWidgets.QWidget,sample.Ui_Form):
    def __init__(self):
        super(Main_window,self).__init__()
        self.bot_point=[0,0,0,0,0,0,0,0]
        self.now_point=[0,0,0,0,0,0]
        self.setupUi(self)
        self.control_class=ctrl_inexbot.control_thread_class()
        self.is_connect=self.control_class.user_see_is_conncet()
        self.pushButton.clicked.connect(self.conncet_bot)
        self.pushButton_3.clicked.connect(self.deadman_on_button)
        self.pushButton_4.clicked.connect(self.deamman_down_button)

        self.pushButton_16.clicked.connect(self.start_get_point)
        self.pushButton_17.clicked.connect(self.stop_get_point)
        self.pushButton_18.clicked.connect(self.refresh_point)
        self.pushButton_19.clicked.connect(self.use_tool)
        self.pushButton_20.clicked.connect(self.enduse_tool)
        self.pushButton_23.clicked.connect(self.use_coord_1)
        self.pushButton_24.clicked.connect(self.use_coord_0)
        self.pushButton_21.clicked.connect(self.rem_nowpoint)
        self.pushButton_22.clicked.connect(self.mov_to_nowpoint)

        self.pushButton_2.pressed.connect(self.start_mov_jog1)
        self.pushButton_2.clicked.connect(self.stop_mov_jog1)
        self.pushButton_10.pressed.connect(self.start_mov_jog1)
        self.pushButton_10.clicked.connect(self.stop_mov_jog1)
        self.pushButton_5.pressed.connect(self.start_mov_jog2)
        self.pushButton_5.clicked.connect(self.stop_mov_jog2)
        self.pushButton_11.pressed.connect(self.start_mov_jog2)
        self.pushButton_11.clicked.connect(self.stop_mov_jog2)
        self.pushButton_6.pressed.connect(self.start_mov_jog3)
        self.pushButton_6.clicked.connect(self.stop_mov_jog3)
        self.pushButton_12.pressed.connect(self.start_mov_jog3)
        self.pushButton_12.clicked.connect(self.stop_mov_jog3)
        self.pushButton_7.pressed.connect(self.start_mov_jog4)
        self.pushButton_7.clicked.connect(self.stop_mov_jog4)
        self.pushButton_13.pressed.connect(self.start_mov_jog4)
        self.pushButton_13.clicked.connect(self.stop_mov_jog4)
        self.pushButton_8.pressed.connect(self.start_mov_jog5)
        self.pushButton_8.clicked.connect(self.stop_mov_jog5)
        self.pushButton_14.pressed.connect(self.start_mov_jog5)
        self.pushButton_14.clicked.connect(self.stop_mov_jog5)
        self.pushButton_9.pressed.connect(self.start_mov_jog6)
        self.pushButton_9.clicked.connect(self.stop_mov_jog6)
        self.pushButton_15.pressed.connect(self.start_mov_jog6)
        self.pushButton_15.clicked.connect(self.stop_mov_jog6)

        #self.pushButton.pressed.connect(self.conncet_bot)
    def conncet_bot(self):
        self.control_class.conncet()
    def deadman_on_button(self):
        self.control_class.user_set_coord_mode(0)
        time.sleep(0.2)
        self.control_class.user_set_operate_mode(0)
        time.sleep(0.2)
        self.control_class.user_set_servo_status(1)
        time.sleep(0.2)
        self.control_class.user_set_deadman_status(1)
        time.sleep(0.2)
        self.control_class.user_set_speed(100)
        time.sleep(0.2)
        self.control_class.user_ctrl_tech_keepmoving_class(1)
    def deamman_down_button(self):
        self.control_class.user_set_deadman_status(0)
        self.control_class.user_ctrl_tech_keepmoving_class(0)

    def start_get_point(self):
        self.control_class.user_set_refresh(1,1)
    def stop_get_point(self):
        self.control_class.user_set_refresh(1,0)
    def refresh_point(self):
        self.bot_point=self.control_class.user_get_bot_point()
        self.lineEdit.setText(str(int(self.bot_point[2])))
        self.lineEdit_2.setText(str(int(self.bot_point[3])))
        self.lineEdit_3.setText(str(int(self.bot_point[4])))
        self.lineEdit_4.setText(str(int(self.bot_point[5])))
        self.lineEdit_5.setText(str(int(self.bot_point[6])))
        self.lineEdit_6.setText(str(int(self.bot_point[7])))
        self.lineEdit_8.setText(str(self.bot_point[0]))
        self.lineEdit_7.setText(str(self.bot_point[1]))
    def use_tool(self):
        self.control_class.user_set_tool(1)
    def enduse_tool(self):
        self.control_class.user_set_tool(0)
    def use_coord_0(self):
        self.control_class.user_set_coord_mode(0)
    def use_coord_1(self):
        self.control_class.user_set_coord_mode(1)
    def rem_nowpoint(self):
        self.now_point=self.bot_point[2:]
    def mov_to_nowpoint(self):
        self.control_class.user_movl(10,1,self.now_point)

    def start_mov_jog1(self):
        send=self.sender().text()
        print(send)
        if(send=='-'):
            print('start axis 1,dir=-1')
            self.control_class.user_start_moving_jog(1,-1,1)
        else:
            print('start axis 1,dir=1')
            self.control_class.user_start_moving_jog(1,1,1)
    def stop_mov_jog1(self):
        send=self.sender().text()
        print(send)
        self.control_class.user_start_moving_jog(1, -1, 0)
        print('stop axis 1')
    def start_mov_jog2(self):
        send=self.sender().text()
        print(send)
        if(send=='-'):
            print('start axis 2,dir=-1')
            self.control_class.user_start_moving_jog(2,-1,1)
        else:
            print('start axis 2,dir=1')
            self.control_class.user_start_moving_jog(2,1,1)
    def stop_mov_jog2(self):
        send=self.sender().text()
        print(send)
        self.control_class.user_start_moving_jog(2, -1, 0)
        print('stop axis 2')
    def start_mov_jog3(self):
        send=self.sender().text()
        print(send)
        if(send=='-'):
            print('start axis 3,dir=-1')
            self.control_class.user_start_moving_jog(3,-1,1)
        else:
            print('start axis 3,dir=1')
            self.control_class.user_start_moving_jog(3,1,1)
    def stop_mov_jog3(self):
        send=self.sender().text()
        print(send)
        self.control_class.user_start_moving_jog(3, -1, 0)
        print('stop axis 3')
    def start_mov_jog4(self):
        send=self.sender().text()
        print(send)
        if(send=='-'):
            print('start axis 4,dir=-1')
            self.control_class.user_start_moving_jog(4,-1,1)
        else:
            print('start axis 4,dir=1')
            self.control_class.user_start_moving_jog(4,1,1)
    def stop_mov_jog4(self):
        send=self.sender().text()
        print(send)
        self.control_class.user_start_moving_jog(4, -1, 0)
        print('stop axis 4')
    def start_mov_jog5(self):
        send=self.sender().text()
        print(send)
        if(send=='-'):
            print('start axis 5,dir=-1')
            self.control_class.user_start_moving_jog(5,-1,1)
        else:
            print('start axis 5,dir=1')
            self.control_class.user_start_moving_jog(5,1,1)
    def stop_mov_jog5(self):
        send=self.sender().text()
        print(send)
        self.control_class.user_start_moving_jog(5, -1, 0)
        print('stop axis 5')
    def start_mov_jog6(self):
        send=self.sender().text()
        print(send)
        if(send=='-'):
            print('start axis 6,dir=-1')
            self.control_class.user_start_moving_jog(6,-1,1)
        else:
            print('start axis 6,dir=1')
            self.control_class.user_start_moving_jog(6,1,1)
    def stop_mov_jog6(self):
        send=self.sender().text()
        print(send)
        self.control_class.user_start_moving_jog(6, -1, 0)
        print('stop axis 6')
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    q = Main_window()
    q.show()
    # a=moving(q)
    # a.start()
    sys.exit(app.exec_())
