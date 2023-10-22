import socket
import json
import zlib
import time
import threading
import select
import traceback

class my_bot:
    '''连接、控制纳博特控制器'''
    def __init__(self,ip,port=6000):
        '''
        简单的构造函数
        :param ip: 控制器ip
        :param port: 控制器端口，默认6000
        '''
        # 机器人各项参数，如上电状态等。字典形式。-1为默认，根据控制器返回更改
        '''speed：速度  
           servo_deadman：伺服上下电状态。0：下电，1：上电
           servo_status：伺服工作状态。0：停止，1：就绪，2：错误，3：运行
           operation_mode：控制器操作模式。0：示教，1：远程，2：运行
           bot_xyz_point：直角坐标系下的坐标。后三位为弧度。第一位为时间戳
           bot_joy_point：关节坐标系下的坐标。第一位为时间戳
           bot_programrun_status：机器人程序执行状态。0：停止，1：暂停，2：运行
        '''
        self.bot_state={"speed":-1,"servo_deadman":-1,"servo_status":-1,"operation_mode":-1,
                        "bot_xyz_point":[0,0,0,0,0,0,0],"bot_joy_point":[0,0,0,0,0,0,0],
                        "bot_programrun_status":-1}

        self.is_moving_jog = [0, 0, 0, 0, 0, 0]#记录正在点动的点，用于连续点动
        self.bot_point=[0,0,0,0,0,0,0,0]# 第0为为坐标模式0：关节  1：直角  2：工具  3：用户  -1：控制器当前坐标。
                                        # 第1位为当前坐标获取时对应时间戳 2-7位对应六个轴的坐标。


        self.__ip=ip
        self.__port=port
        self.__is_conncet=False
        self.bot_sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_lock=threading.RLock()
        self.send_lock=threading.RLock()
        self.clear_lock=threading.Lock()
        self.__msg_recv_class=msg_recv_thread(self)
        self.__msg_recv_class.start()
        self.__tech_keepmoving_class=tech_keep_moving_point(self)
        self.__send_refreshdata_msg_class=send_refreshdata_msg(self)
        self.__send_refreshdata_msg_class.start()

    def __get_buffer(self,command,data):
        '''
        根据命令和数据获取待发送的数据
        :param command: 命令代码，如0x2101为设置操作模式
        :param data:命令数据，json格式，如{"mode": 0}
        :return:返回待发送的数据二进制，可直接使用socket发送。若出错则返回-1
        '''
        try:
            _preSend = bytearray()
            # get byte of data
            databyte = json.dumps(data).encode()
            # Length
            dataLength = databyte.__len__()
            dataLengthBytes = dataLength.to_bytes(
                length=2, byteorder="big", signed=False)
            # Command
            commandBytes = command.to_bytes(length=2, byteorder="big", signed=False)
            # _preSend
            _preSend.append(0x4E)
            _preSend.append(0x66)
            _preSend.extend(dataLengthBytes)
            _preSend.extend(commandBytes)
            _preSend.extend(databyte)
            # Crc32
            crc32Num = zlib.crc32(bytes(_preSend[2:]), 0)
            crc32Bytes = crc32Num.to_bytes(length=4, byteorder="big", signed=False)
            _preSend.extend(crc32Bytes)
            return bytes(_preSend)
        except:
            print('__get_buffer except')
            print(traceback.print_exc())
            return -1
    def Send_data(self,command,data):
        '''
        发送二级制数据。外部调用
        :param command:命令
        :param data: 数据
        :return: 1：未连接socket
                 2：合成二进制数出错
                 3：发送二进制出错
                 0：正常发送
        '''
        #应该加锁，目前未加，存在隐患
        self.send_lock.acquire()
        if self.__is_conncet==False:
            self.send_lock.release()
            return 1
        _preSend=self.__get_buffer(command,data)
        if(_preSend==-1):
            self.send_lock.release()
            return 2
        try:
            self.bot_sock.send(_preSend)
            self.send_lock.release()
            return 0
        except:
            self.send_lock.release()
            print('Send_data except')
            print(traceback.print_exc())
            return 3
    def connect_bot(self):
        '''
        连接控制器.由类外部调用
        :return:连接成功返回0，连接失败返回1
        '''
        if self.__is_conncet==False:
            try:
                self.bot_sock.connect((self.__ip,self.__port))
                self.__is_conncet=True
                return 0
            except:
                print('connect_bot except')
                print(traceback.print_exc())
                return 1
        else:
            return 0
    def set_is_connect(self,is_connect):
        '''
        设置是否连接，由外部调用
        :param is_connect: 是否连接
        :return:null
        '''
        self.__is_conncet=is_connect
        try:
            if(self.__is_conncet==False):
                self.bot_sock.close()
        except:
            print('set_is_connect except')
            print(traceback.print_exc())
    def see_is_conect(self):
        '''
        参看是否连接
        :return:0：未连接
                1：连接
        '''
        return self.__is_conncet
    def recv_data(self):
        '''
        使用socket阻塞接收一次数据
        :return: -1：接收错误
                re：接受到的数据
        '''
        self.recv_lock.acquire()
        self.bot_sock.setblocking(1)
        #self.clear_lock.acquire()
        try:
            re=self.bot_sock.recv(1024)
            self.recv_lock.release()
            #self.clear_lock.release()
            return re
        except:
            self.recv_lock.release()
            print('recv_data except')
            print(traceback.print_exc())
            #self.clear_lock.release()
            return -1
    def clear_recv_data(self):
        '''清空socket缓存'''
        self.recv_lock.acquire()
        self.bot_sock.setblocking(0)
        i = 0
        while True:
            # time.sleep(0.1)
            # to_client.sendall(b'helloclient')
            ready = select.select([self.bot_sock], [], [], 1)
            if ready[0]:
                m=self.bot_sock.recv(1024)
                print(m)
                i = 1
            else:
                print('cache empty_wwx:' + str(i))
                break
        self.bot_sock.setblocking(1)
        self.recv_lock.release()

    #机器人控制功能具体函数——ctrl_fun
    def set_operate_mode(self,mode):
        '''
        设置机器人操作模式
        :param mode: 0：示教模式
                     1：远程模式
                     2：运行模式
        :return:0：设置正常
                1：mode错误数据异常
                2：发送异常
        '''
        if((mode!=0)&(mode!=1)&(mode!=2)):
            return 1
        re=self.Send_data(0x2101, {"mode": mode})
        if re==0:
            return 0
        return 2
    def set_servo_status(self,status,robot=1):
        '''
        设置机器人伺服状态
        :param robot: 机器人id，从1开始。无联机时目前只允许为1
        :param status: 0：停止
                       1：就绪
                       2：错误
                       3：运行
        :return:0：设置正常
                1：rabot或status错误数据异常
                2：发送异常
        '''
        if((robot!=1)|((status!=0)&(status!=1)&(status!=2)&(status!=3))):
            return 1
        re=self.Send_data(0x2001, {"robot": robot, "status": status})
        if re==0:
            return 0
        return 2
    def set_deadman_status(self,deadman):
        '''
        设置伺服上电下电状态
        :param deadman:0：下电
                       1：上电
        :return:0：设置正常
                1：deadman错误数据异常
                2：发送异常
        '''
        if ((deadman != 0) & (deadman != 1) ):
            return 1
        re = self.Send_data(0x2301, {"deadman": deadman})
        if re == 0:
            return 0
        return 2
    def set_coord_mode(self,coord,robot=1):
        '''
        设置坐标系模式
        :param coord:0：关节坐标
                     1：直角坐标
                     2：工具坐标
                     3：用户坐标
        :param robot: 机器人id，从1开始。无联机时目前只允许为1
        :return:0：设置正常
                1：rabot或coord错误数据异常
                2：发送异常
        '''
        if ((robot != 1) |( (coord != 0) & (coord != 1) & (coord != 2) & (coord != 3))):
            return 1
        re = self.Send_data(0x2201, {"robot": robot, "coord": coord})
        if re == 0:
            return 0
        return 2
    def set_speed(self,speed,robot=1):
        '''
        设置机器人运行速度
        :param speed: 0-100，一般认为5一档，101代表0.1°微动挡，102代表0.01°微动挡
        :param robot:机器人id，从1开始。无联机时目前只允许为1
        :return:0：设置正常
                1：rabot或speed错误数据异常
                2：发送异常
        '''
        if ((robot != 1) | (not(isinstance(speed,int))|(not((speed>=0)&(speed<=102))))):
            return 1
        re = self.Send_data(0x2601, {"robot": robot, "speed": speed})
        if re == 0:
            return 0
        return 2
    def move_jog(self,axis,direction):
        '''
        示教器执行点动操作时
        :param axis:一般1-6.存在外部轴时从8开始。目前仅可1-6的int
        :param derection:1：正向
                         -1：反向
        :return:0：设置正常
                1：axis或direction错误数据异常
                2：发送异常
        '''
        if (((direction != 1)&(direction!=-1)) | (not(isinstance(axis,int))|(not((axis>=1)&(axis<=6))))):
            return 1
        re = self.Send_data(0x2901, {"axis": axis, "direction": direction})
        if re == 0:
            return 0
        return 2
    def stop_jog(self,axis):
        '''
        示教器停止点动
        :param axis:一般1-6.存在外部轴时从8开始。目前仅可1-6的int
        :return:0：设置正常
                1：axis错误数据异常
                2：发送异常
        '''
        if (not(isinstance(axis,int))|(not((axis>=1)&(axis<=6)))):
            return 1
        re = self.Send_data(0x2902, {"axis": axis})
        if re == 0:
            return 0
        return 2
    def change_bot_speed(self,type):
        '''
        以5为单位增减速度
        :param type: 1：速度+5
                     -1：速度-5
        :return: speed更改后速度
                 -1 ：type错误
        '''
        if((type!=1)&(type!=-1)):
            return -1
        if((type==1)&(self.__bot_speed<=95)):
            self.__bot_speed +=5
            return self.__bot_speed
        elif((type==-1)&self.__bot_speed>=5):
            self.__bot_speed -=5
            return self.__bot_speed
        else:
            return self.__bot_speed
    def set_socket_ctrl(self,cmd):
        '''
        设置开或关socket直接控制运动模式
        :param cmd:0：关闭  1：开启
        :return:0：设置正常
                1：cmd异常
                2：发送异常
        '''
        if((cmd!=0)&(cmd!=1)):
            return 1
        re = self.Send_data(0x50B1, {"robot": 1, "open": cmd})
        if re == 0:
            return 0
        return 2
    def send_socket_cmd(self,cmd):
        '''
        生成并发送socket控制需要的指令
        :param cmd:暂时只用movl。后续增加。暂时只传入点位
        :return:
        '''
        data={"robot":1,
	        "data":
	        [
		        { "RobotPos":{
                "ctype":80,
                "data":[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "key":5242881
                            },
                "acc":10,
                "dec":10,
                "pl":0,
                "positionId":5242881,
                "velocity": 10.0,
                "type":2 }

	        ]
            }
        data["data"][0]["RobotPos"]["data"][7:13]=cmd
        self.Send_data(0x50B4,data)
    #ctrl_fun end

    #较为完善的对外提供接口
    def ctrl_tech_keepmoving_class(self,cmd):
        '''
        开始、结束线程
        :param cmd: 1：开启
                    0：停止
        :return: 0：正常
                 1：cmd错误
                 2：开启线程错误
        '''
        if((cmd!=0)&(cmd!=1)):
            return 1
        if(cmd==0):
            self.__tech_keepmoving_class.stop_t()
            return 0
        else:
            if(self.__tech_keepmoving_class.is_run()):
                return 0
            try:
                self.__tech_keepmoving_class.start()
            except:
                try:
                    self.__tech_keepmoving_class=tech_keep_moving_point(self)
                    self.__tech_keepmoving_class.start()
                    return 0
                except:
                    print('tech_keepmoving_class start faild')
                    print(traceback.print_exc())
                    return 2
    def start_moving_jog(self,axis,direction,cmd):
        '''
        非阻塞函数，调用一次后，开始移动或停止.调用前请确定以开启示教点动控制线程
        :param axis:一般1-6.存在外部轴时从8开始。目前仅可1-6的int
        :param direction:1：正向
                         -1：反向
        :param cmd:1：开始
                   0：停止。cmd=0时direction可随意
        :return: 0：正常
                 1：axis或dirction或cmd异常
                 2：发送异常
                 3：示教点动线程未启动
        '''
        if (((direction != 1)&(direction!=-1)) | (not(isinstance(axis,int))|(not((axis>=1)&(axis<=6))))|((cmd != 0)&(cmd!=1))):
            return 1
        if(self.__tech_keepmoving_class.is_run()==False):
            return 3
        if(cmd==0):
            re=self.stop_jog(axis)
            self.is_moving_jog[axis-1]=0
            return re
        else:
            self.is_moving_jog[axis-1]=direction
            return
    def set_refresh(self,Num,cmd):
        '''
        设置开始、结束刷新某一个参数
        :param Num:0：获取关节坐标系下位置点
                   1：获取直角坐标系下位置点
                   2：获取程序运行状态
        :param cmd:0：结束
                   1：开始
        :return:0：正常
                1：异常
        '''
        return self.__send_refreshdata_msg_class.set_refresh(Num,cmd)
    def set_tool(self,toolnum,robot=1):
        '''
        设置机器人工具手
        :param toolnum:要选择的工具手编号.0表示无工具手
        :param robot:机器人编号。目前只允许1
        :return:0：正常
                1：toolnum或robot异常
                2：发送异常
        '''
        if ((robot != 1) | (not(isinstance(toolnum,int))|(not((toolnum>=0)&(toolnum<=10))))):
            return 1
        re = self.Send_data(0x380A, {"robot": robot, "curToolNum": toolnum})
        if re == 0:
            return 0
        return 2
    def movl(self,vel,coord,pos):
        '''
        机器人直线移动，从当前点移动到pos
        :param vel: 速度，单位mm/s，1以上整数
        :param coord:坐标系  0关节，1直角
        :param pos:长度为6点位坐标
        :return:0：正常
                1：vel、coord、pos等错误
                2：发送异常
        '''
        if((not(isinstance(vel,int))|(not((vel>=1)&(vel<=100))))|((coord!=0)&(coord!=1))|(not(isinstance(pos,list)))):
            return 1
        else:
            if(pos.__len__()!=6):
                return 1
            else:
                for i in range(6):
                    if(not(isinstance(pos[i],float))):
                        return 1
        re = self.Send_data(0x4502, {"robot": 1, "vel":vel,"coord":coord,"pos":pos})
        if re == 0:
            return 0
        return 2
    def get_bot_xyz_point(self):
        '''
        获取机器人的xyz坐标
        :return: 长度为7的list，第0为为时间戳，1-3为xyz坐标单位mm，4-6为旋转，单位弧度
        '''
        return self.bot_state['bot_xyz_point']
    def socket_movl(self,pos,acc=10,dec=10,pl=0,vel=10):
        '''
        当socket直接控制打开时，可调用直线移动
        :param pos: 长度为6list，点位坐标，要求直角坐标
        :param acc: 加速度，1-100
        :param dec:减速度，1-100
        :param pl:平滑，0-5
        :param vel:速度，2-1000，mm/s
        :return:0：正常
                1：参数错误
                2：发送错误
        '''
        if((not(isinstance(vel,int))|(not((vel>=2)&(vel<=1000))))|
                (not(isinstance(pl,int))|(not((pl>=0)&(pl<=5))))|
                (not (isinstance(dec, int)) | (not ((dec >= 1) & (dec <= 100))))|
                (not (isinstance(acc, int)) | (not ((acc >= 1) & (acc <= 100))))|(not(isinstance(pos,list)))):
            return 1
        else:
            if (pos.__len__() != 6):
                return 1
            else:
                for i in range(6):
                    if (not (isinstance(pos[i], float))):
                        return 1
        data = {"robot": 1,
                "data":
                    [
                        {"RobotPos": {
                            "ctype": 80,
                            "data": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            "key": 5242881
                        },
                            "acc": 10,
                            "dec": 10,
                            "pl": 0,
                            "positionId": 5242881,
                            "velocity": 10.0,
                            "type": 2}

                    ]
                }
        data["data"][0]["RobotPos"]["data"][7:13] = pos
        data["data"][0]["acc"]=acc
        data["data"][0]["dec"] = dec
        data["data"][0]["pl"] = pl
        data["data"][0]["velocity"] = vel
        re=self.Send_data(0x50B4, data)
        if re == 0:
            return 0
        return 2
    def socket_movj(self, pos, acc=10, dec=10, pl=0, vel=10):
        '''
        当socket直接控制打开时，可调用点到点移动
        :param pos: 长度为6list，点位坐标，要求直角坐标
        :param acc: 加速度，1-100
        :param dec:减速度，1-100
        :param pl:平滑，0-5
        :param vel:速度，2-1000，mm/s
        :return:0：正常
                1：参数错误
                2：发送错误
        '''
        if ((not (isinstance(vel, int)) | (not ((vel >= 1) & (vel <= 100)))) |
                (not (isinstance(pl, int)) | (not ((pl >= 0) & (pl <= 5)))) |
                (not (isinstance(dec, int)) | (not ((dec >= 1) & (dec <= 100)))) |
                (not (isinstance(acc, int)) | (not ((acc >= 1) & (acc <= 100)))) | (not (isinstance(pos, list)))):
            return 1
        else:
            if (pos.__len__() != 6):
                return 1
            else:
                for i in range(6):
                    if (not (isinstance(pos[i], float))):
                        return 1
        data = {"robot": 1,
                "data":
                    [
                        {"RobotPos": {
                            "ctype": 80,
                            "data": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            "key": 5242881
                        },
                            "acc": 10,
                            "dec": 10,
                            "pl": 0,
                            "positionId": 5242881,
                            "velocity": 10.0,
                            "type": 1}

                    ]
                }
        data["data"][0]["RobotPos"]["data"][7:13] = pos
        data["data"][0]["acc"] = acc
        data["data"][0]["dec"] = dec
        data["data"][0]["pl"] = pl
        data["data"][0]["velocity"] = vel
        re = self.Send_data(0x50B4, data)
        if re == 0:
            return 0
        return 2
    def get_bot_state(self,par:str):
        '''
        获取机器人的一些状态
        :param par: str类型：具体功能如下
                   speed：速度
                   servo_deadman：伺服上下电状态。0：下电，1：上电
                   servo_status：伺服工作状态。0：停止，1：就绪，2：错误，3：运行
                   operation_mode：控制器操作模式。0：示教，1：远程，2：运行
                   bot_xyz_point：直角坐标系下的坐标。后三位为弧度。第一位为时间戳
                   bot_joy_point：关节坐标系下的坐标。第一位为时间戳
                   bot_programrun_status：机器人程序执行状态。0：停止，1：暂停，2：运行
        :return: 状态值：正常   -2：par错误
        '''
        if(not(isinstance(par,str))):
            return -2
        if(par in self.bot_state.keys()):
            return self.bot_state[par]
        else:
            return -2

class heart_beat_thread(threading.Thread):
    '''心跳检测控制线程'''
    def __init__(self,bot_class:my_bot):
        super(heart_beat_thread,self).__init__()
        self.__is_run=False
        self.__real_is_run = False
        self.__bot_class=bot_class
        self.daemon = True
    def run(self):
        self.__is_run=True
        self.__real_is_run=True
        while(self.__is_run):
            try:
                self.__bot_class.send_lock.acquire()
                self.__bot_class.recv_lock.acquire()
                if(self.__bot_class.see_is_conect()==False):
                    self.__bot_class.connect_bot()
                    print('当前连接状态：'+str(self.__bot_class.see_is_conect()))
                else:
                    now=time.time()
                    re=self.__bot_class.Send_data(0x7266,{"time":now})
                    if(re!=0):
                        self.__bot_class.set_is_connect(False)
                        print('连接中断')
                    else:
                        re=self.__bot_class.recv_data()
                        if(re==-1):
                            print('接收回应出错，连接中断')
                            self.__bot_class.set_is_connect(False)
                        else:
                            #command = re[4:6].decode()
                            data=re[6:-4].decode()
                            #print(command)
                            #debug
                            print(data)
                self.__bot_class.send_lock.release()
                self.__bot_class.recv_lock.release()
                time.sleep(3)
            except:
                # self.__is_run=False
                # self.__real_is_run=False
                self.__bot_class.send_lock.release()
                self.__bot_class.recv_lock.release()
                print('hear_beat_thread_except')
                print(traceback.print_exc())
        self.__real_is_run=False

    def stop_t(self):
        '''
        结束线程
        :return:NULL
        '''
        self.__is_run=False
    def is_run(self):
        '''
        返回线程是存在
        :return: true为正常运行，flase为非正常运行
        '''
        return self.__real_is_run

class msg_recv_thread(threading.Thread):
    '''
    开启时，用于持续接收socket消息并处理.该类置于my_bot类内部
    '''
    def __init__(self,bot_class:my_bot):
        super(msg_recv_thread,self).__init__()
        self.__bot_class=bot_class
        self.__is_run = False
        self.__real_is_run = False
        self.daemon = True
        self.submsg_dir={0x2A03:self.submsg_set_bot_point,0x2603:self.submsg_set_bot_speed,
                         0x3D03:self.submsg_set_bot_programrun_status,0x2303:self.submsg_set_servo_deadman,
                         0x2003:self.submsg_set_servo_status,0x2103:self.submsg_set_operation_mode,
                         0x2B03:self.submsg_error_code,0x2B04:self.submsg_warning_code,
                         0x2B01:self.submsg_info}
    def run(self):
        self.__is_run=True
        self.__real_is_run=True
        self.__have_recv=False
        while(self.__is_run):
            try:
                self.__bot_class.recv_lock.acquire()
                self.__bot_class.bot_sock.setblocking(0)
                ready = select.select([self.__bot_class.bot_sock], [], [], 1)
                if ready[0]:
                    m = self.__bot_class.bot_sock.recv(1024)
                    self.__have_recv=True
                self.__bot_class.bot_sock.setblocking(1)
                self.__bot_class.recv_lock.release()
            except:
                self.__is_run=False
                self.__real_is_run=False
                self.__bot_class.recv_lock.release()
                print('msg_recv_thread_break')
                print(traceback.print_exc())
            if(self.__have_recv):
                self.process_msg(m)
                self.__have_recv=False
            time.sleep(0.1)
        self.__real_is_run=False

    def stop_t(self):
        '''
        结束线程
        :return:NULL
        '''
        self.__is_run=False
    def is_run(self):
        '''
        返回线程是存在
        :return: true为正常运行，flase为非正常运行
        '''
        return self.__real_is_run
    def process_msg(self,msg:bytearray):
        self.__have_recv=False
        #debug
        #print(msg)
        msg_len=msg.__len__()
        cont=0
        if(msg_len<10):
            print('recv_wrong_msg')
        while(cont+1<msg_len):
            try:
                if ((msg[cont] == 0x4E) & (msg[cont + 1] == 0x66)):
                    msg = msg[cont:]
                    msg_len=msg_len-cont
                    len = int(msg[2:4].hex(), 16)
                    cmd=int(msg[4:6].hex(), 16)
                    if(len!=0):
                        data = json.loads(msg[6:6 + len].decode())
                    else:
                        data={}
                    #debug
                    #print(data)
                    cont = 6 + len + 4
                    if cmd in self.submsg_dir.keys():
                        re=self.submsg_dir[cmd](data)
                    else:
                        print('no cmd function:',cmd)
                else:
                    cont += 1
            except:
                print('process_msg except')
                print(traceback.print_exc())
                break
    def submsg_set_bot_point(self,data):
        '''
        消息检测到控制器发送坐标点消息时调用此函数，更新机器人当前点位信息
        :param data: json数据
        :return: 0：正常
                 1：错误
        '''
        #debug
        #print('in submsg_set_bot_point,msg=',data)
        try:
            now=int(time.time())
            self.__bot_class.bot_point[0]=data['coord']
            self.__bot_class.bot_point[1]=now
            self.__bot_class.bot_point[2:]=data['pos'][:-1]
            if(self.__bot_class.bot_point[0]==1):
                tmp=[0,0,0,0,0,0,0]
                tmp[0]=now
                tmp[1:]=self.__bot_class.bot_point[2:]
                self.__bot_class.bot_state['bot_xyz_point']=tmp
            if(self.__bot_class.bot_point[0]==0):
                tmp = [0, 0, 0, 0, 0, 0, 0]
                tmp[0] = now
                tmp[1:] = self.__bot_class.bot_point[2:]
                self.__bot_class.bot_state['bot_joy_point']=tmp
            return 0
        except:
            print('submsg_set_bot_point except')
            print(traceback.print_exc())
            return 1
    def submsg_set_bot_speed(self,data):
        '''
        消息检测到控制器发送速度消息时调用此函数，更新机器人当前速度信息
        :param data: json数据
        :return: 0：正常  1：错误
        '''
        #debug
        print('in submsg_set_bot_speed,msg=',data)
        try:
            self.__bot_class.bot_state['speed']=data['speed']
            return 0
        except:
            print('submsg_set_bot_speed except')
            print(traceback.print_exc())
            return 1
    def submsg_set_bot_programrun_status(self,data):
        '''
        消息检测到控制器返回程序执行状态时调用此函数，更新机器人执行程序状态
        :return: 0：正常  1：错误
        '''
        #debug
        print('in submsg_set_bot_programrun_status,msg=', data)
        try:
            self.__bot_class.bot_state['bot_programrun_status']=data['status']
            return 0
        except:
            print('submsg_set_bot_programrun_status except')
            print(traceback.print_exc())
            return 1
    def submsg_set_servo_deadman(self,data):
        '''
        消息检测到伺服上电状态消息时调用，更新机器人伺服上电状态
        :param data:json
        :return:0：正常  1：错误
        '''
        # debug
        print('in submsg_set_servo_deadman,msg=', data)
        try:
            self.__bot_class.bot_state['servo_deadman'] = data['deadman']
            return 0
        except:
            print('submsg_set_servo_deadman except')
            print(traceback.print_exc())
            return 1
    def submsg_set_servo_status(self,data):
        '''
        检测到机器人伺服状态发生变化消息时调用，更新机器人伺服状态
        :param data: json
        :return: 0：正常  1：错误
        '''
        # debug
        print('in submsg_set_servo_status,msg=', data)
        try:
            self.__bot_class.bot_state['servo_status'] = data['status']
            return 0
        except:
            print('submsg_set_servo_status except')
            print(traceback.print_exc())
            return 1
    def submsg_set_operation_mode(self,data):
        '''
        检测到机器人操作模式变化时调用，更新机器人操作模式
        :param data:json
        :return:0：正常  1：错误
        '''
        # debug
        print('in submsg_set_operation_mode,msg=', data)
        try:
            self.__bot_class.bot_state['operation_mode'] = data['mode']
            return 0
        except:
            print('submsg_set_operation_mode except')
            print(traceback.print_exc())
            return 1
    def submsg_error_code(self,data):
        '''
        收到控制器传送错误代码时调用
        :param data: json
        :return: 0：正常  1：错误
        '''
        # debug
        print('in submsg_error_code,msg=', data)
        try:
            pass
            return 0
        except:
            print('submsg_error_code except')
            print(traceback.print_exc())
            return 1
    def submsg_warning_code(self,data):
        '''
        收到控制器传送警告代码时调用
        :param data: json
        :return: 0：正常  1：错误
        '''
        # debug
        print('in submsg_warning_code,msg=', data)
        try:
            pass
            return 0
        except:
            print('submsg_warning_code except')
            print(traceback.print_exc())
            return 1
    def submsg_info(self,data):
        '''
        收到控制器传送信息提示时调用
        :param data: json
        :return: 0：正常  1：错误
        '''
        # debug
        print('in submsg_info,msg=', data)
        try:
            pass
            return 0
        except:
            print('submsg_info except')
            print(traceback.print_exc())
            return 1

class tech_keep_moving_point(threading.Thread):
    '''
    示教模式下用于连续发移动指令保持移动.该类置于my_bot类内部
    '''
    def __init__(self,bot_class:my_bot):
        super(tech_keep_moving_point,self).__init__()
        self.__bot_class=bot_class
        self.__is_run = False
        self.__real_is_run = False
        self.daemon = True
    def run(self):
        self.__is_run = True
        self.__real_is_run = True
        while (self.__is_run):
            try:
                for i in range(6):
                    if(self.__bot_class.is_moving_jog[i]!=0):
                        self.__bot_class.move_jog(i+1,self.__bot_class.is_moving_jog[i])
            except:
                print('tech_keep_moving_thread_break')
                print(traceback.print_exc())
            time.sleep(0.05)
        self.__real_is_run = False
    def stop_t(self):
        '''
        结束线程
        :return:NULL
        '''
        self.__is_run=False
    def is_run(self):
        '''
        返回线程是存在
        :return: true为正常运行，flase为非正常运行
        '''
        return self.__real_is_run

class send_refreshdata_msg(threading.Thread):
    def __init__(self,bot_class:my_bot):
        super(send_refreshdata_msg,self).__init__()
        self.__bot_class=bot_class
        self.__is_run = False
        self.__real_is_run = False
        self.daemon = True
        #下面两个对应，__ctrl第几位为1则发送哪一位的刷新信息
        #
        '''0:获取关节坐标系下位置点  1:获取直角坐标系下位置点  2:获取程序运行状态
        '''
        self.__data_dir={0:(0x2A02,{"robot":1,"coord":0}),1:(0x2A02,{"robot":1,"coord":1}),
                         2:(0x3D02,{"robot":1})}
        self.__ctrl=[]#在记录的命令会被刷新
        self.__once_cmd=[]#在其中的命令，只刷新一次
        #end
    def run(self):
        self.__is_run = True
        self.__real_is_run = True
        while (self.__is_run):
            len=self.__ctrl.__len__()
            count=0
            try:
                while(count<len):
                    try:
                        cmd=self.__data_dir[self.__ctrl[count]][0]
                        data=self.__data_dir[self.__ctrl[count]][1]
                    except:
                        print('dir error,ctrl num not exit,ctrl num=',self.__ctrl[count])
                        print(traceback.print_exc())
                        self.__ctrl.pop(count)
                        len = self.__ctrl.__len__()
                        continue
                    re=self.__bot_class.Send_data(cmd,data)
                    if(re!=0):
                        print('refresh send wrong,num=',count,'re=',re)
                    if(self.__ctrl[count] in self.__once_cmd):
                        self.__ctrl.pop(count)
                        len = self.__ctrl.__len__()
                    else:
                        count +=1
            except:
                print('send_refreshdata_msg_thread_erro')
                print(traceback.print_exc())
            time.sleep(0.5)
        self.__real_is_run = False
    def stop_t(self):
        '''
        结束线程
        :return:NULL
        '''
        self.__is_run=False
    def is_run(self):
        '''
        返回线程是存在
        :return: true为正常运行，flase为非正常运行
        '''
        return self.__real_is_run
    def set_refresh(self,Num,cmd):
        '''
        设置开始、结束刷新某一个参数
        :param Num:0：获取关节坐标系下位置点
                   1：获取直角坐标系下位置点
                   2：获取程序运行状态
        :param cmd:0：结束
                   1：开始
        :return:0：正常
                1：异常
        '''
        if((cmd !=0)&(cmd !=1)):
            return 1
        if(cmd==1):
            if(Num in self.__ctrl):
                return 0
            else:
                self.__ctrl.append(Num)
                return 0
        else:
            if(Num in self.__ctrl):
                self.__ctrl.remove(Num)
                return 0
            else:
                return 0

class control_thread_class(threading.Thread):
    '''试用版控制类'''
    def __init__(self,ip='192.168.1.13'):
        super(control_thread_class,self).__init__()
        self.__bot_class=my_bot(ip,6000)
        self.__heart_class=heart_beat_thread(self.__bot_class)
        self.daemon=True


    #对外接口。暂定将所有接口集中到该类
    def conncet(self):
        '''连接控制器'''
        if(self.__heart_class.is_run()==False):
            try:
                self.__heart_class.start()
            except:
                self.__heart_class=heart_beat_thread(self.__bot_class)
                self.__heart_class.start()
    def user_see_is_conncet(self):
        '''
        参看是否连接
        :return:0：未连接
                1：连接
        '''
        return self.__bot_class.see_is_conect()
    def user_set_coord_mode(self,coord):
        '''
        设置坐标系模式
        :param coord:0：关节坐标
                     1：直角坐标
                     2：工具坐标
                     3：用户坐标
        :param robot: 机器人id，从1开始。无联机时目前只允许为1
        :return:0：设置正常
                1：rabot或coord错误数据异常
                2：发送异常
        '''
        return self.__bot_class.set_coord_mode(coord)
    def user_set_operate_mode(self,mode):
        '''
        设置机器人操作模式
        :param mode: 0：示教模式
                     1：远程模式
                     2：运行模式
        :return:0：设置正常
                1：mode错误数据异常
                2：发送异常
        '''
        return self.__bot_class.set_operate_mode(mode)
    def user_set_servo_status(self,status):
        '''
        设置机器人伺服状态
        :param robot: 机器人id，从1开始。无联机时目前只允许为1
        :param status: 0：停止
                       1：就绪
                       2：错误
                       3：运行
        :return:0：设置正常
                1：rabot或status错误数据异常
                2：发送异常
        '''
        return self.__bot_class.set_servo_status(status)
    def user_set_deadman_status(self,deadman):
        '''
        设置伺服上电下电状态
        :param deadman:0：下电
                       1：上电
        :return:0：设置正常
                1：deadman错误数据异常
                2：发送异常
        '''
        return self.__bot_class.set_deadman_status(deadman)
    def user_set_speed(self,speed):
        '''
        设置机器人运行速度
        :param speed: 0-100，一般认为5一档，101代表0.1°微动挡，102代表0.01°微动挡
        :param robot:机器人id，从1开始。无联机时目前只允许为1
        :return:0：设置正常
                1：rabot或speed错误数据异常
                2：发送异常
        '''
        return self.__bot_class.set_speed(speed)
    def user_ctrl_tech_keepmoving_class(self,cmd):
        '''
        开始、结束线程
        :param cmd: 1：开启
                    0：停止
        :return: 0：正常
                 1：cmd错误
                 2：开启线程错误
        '''
        return self.__bot_class.ctrl_tech_keepmoving_class(cmd)
    def user_start_moving_jog(self,axis,direction,cmd):
        '''
        非阻塞函数，调用一次后，开始移动或停止.调用前请确定以开启示教点动控制线程
        :param axis:一般1-6.存在外部轴时从8开始。目前仅可1-6的int
        :param direction:1：正向
                         -1：反向
        :param cmd:1：开始
                   0：停止。cmd=0时direction可随意
        :return: 0：正常
                 1：axis或dirction或cmd异常
                 2：发送异常
                 3：示教点动线程未启动
        '''
        return self.__bot_class.start_moving_jog(axis,direction,cmd)
    def user_set_refresh(self,Num,cmd):
        '''
        设置开始、结束刷新某一个参数
        :param Num:0：获取关节坐标系下位置点
                   1：获取直角坐标系下位置点
                   2：获取程序运行状态
        :param cmd:0：结束
                   1：开始
        :return:0：正常
                1：异常
        '''
        return self.__bot_class.set_refresh(Num,cmd)
    def user_get_bot_point(self):
        '''
        返回坐标点位
        :return: 返回长度为8的数组
        第1位：坐标系
        第2位：获取此坐标时事件
        第3-8位：六个坐标
        '''
        return self.__bot_class.bot_point
    def user_set_tool(self,toolnum,robot=1):
        '''
        设置机器人工具手
        :param toolnum:要选择的工具手编号.0表示无工具手
        :param robot:机器人编号。目前只允许1
        :return:0：正常
                1：toolnum或robot异常
                2：发送异常
        '''
        return self.__bot_class.set_tool(toolnum)
    def user_movl(self,vel,coord,pos):
        '''
        机器人直线移动，从当前点移动到pos。建议在示教模式下使用
        :param vel: 速度，单位mm/s，1以上整数
        :param coord:坐标系  0关节，1直角
        :param pos:长度为6点位坐标,list,每个元素都为float
        :return:0：正常
                1：vel、coord、pos等错误
                2：发送异常
        '''
        return self.__bot_class.movl(vel,coord,pos)
    def user_get_bot_xyz_point(self):
        '''
        获取机器人的xyz坐标
        :return: 长度为7的list，第0为为时间戳，1-3为xyz坐标单位mm，4-6为旋转，单位弧度
        '''
        return self.__bot_class.get_bot_xyz_point()
    def user_set_socket_ctrl(self,cmd):
        '''
        设置开或关socket直接控制运动模式。建议在运行拍照时使用此模式
        :param cmd: 0：关闭  1：开启
        :return:0：设置正常
                1：cmd异常
                2：发送异常
        '''
        return self.__bot_class.set_socket_ctrl(cmd)
    def user_socket_movl(self,pos,acc=10,dec=10,pl=0,vel=10):
        '''
        当socket直接控制打开时，可调用移动直线。（使用前请调用user_set_socket_ctrl开启控制）
        调用成功一次后机器人程序运行状态bot_programrun_status变为2，指令执行结束后变为0
        :param pos: 长度为6list，点位坐标，要求直角坐标
        :param acc: 加速度，1-100
        :param dec:减速度，1-100
        :param pl:平滑，0-5
        :param vel:速度，2-1000，mm/s
        :return:0：正常
               1：参数错误
               2：发送错误
        '''
        return self.__bot_class.socket_movl(pos,acc,dec,pl,vel)
    def user_socket_movj(self,pos,acc=10,dec=10,pl=0,vel=10):
        '''
        当socket直接控制打开时，可调用点到点移动。（使用前请调用user_set_socket_ctrl开启控制）
        调用成功一次后机器人程序运行状态bot_programrun_status变为2，指令执行结束后变为0
        :param pos: 长度为6list，点位坐标，要求直角坐标
        :param acc: 加速度，1-100
        :param dec:减速度，1-100
        :param pl:平滑，0-5
        :param vel:速度，1-100
        :return:0：正常
               1：参数错误
               2：发送错误
        '''
        return self.__bot_class.socket_movj(pos,acc,dec,pl,vel)
    def user_get_bot_state(self,par:str):
        '''
        获取机器人的一些状态
        :param par: str类型：具体功能如下
                   speed：速度
                   servo_deadman：伺服上下电状态。0：下电，1：上电
                   servo_status：伺服工作状态。0：停止，1：就绪，2：错误，3：运行
                   operation_mode：控制器操作模式。0：示教，1：远程，2：运行
                   bot_xyz_point：直角坐标系下的坐标。后三位为弧度。第一位为时间戳
                   bot_joy_point：关节坐标系下的坐标。第一位为时间戳
                   bot_programrun_status：机器人程序执行状态。0：停止，1：暂停，2：运行
        :return: 状态值：正常   -2：par错误（包括不是str，或不存在于dir）
        '''
        return self.__bot_class.get_bot_state(par)

    #测试用接口。通常请勿调用
    def test_get_bot_status_dir(self):
        return self.__bot_class.bot_state
    def test_set_socket_ctrl(self,cmd):
        return self.__bot_class.set_socket_ctrl(cmd)
    def test_send_scokect_ctrl(self,cmd):
        return self.__bot_class.send_socket_cmd(cmd)