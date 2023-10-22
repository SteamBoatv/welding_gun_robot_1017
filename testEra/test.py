
import socket
from selfTools.littleTools import LittleTools
# 定义全局变量管理模块
import src.global_var as glo
glo._init()

print("_________________")
littletools = LittleTools()
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2. 链接服务器
server_addr = ("192.168.0.1", 5233)
tcp_socket.connect(server_addr)
# 此处会默认发来一个 connect successful
data = tcp_socket.recv(1024)
print("message in main.py: \n" + data.decode("gbk"))
# 设置全局变量
glo.set_value("tcp_socket", tcp_socket)

FANUCtcpPosition = littletools.tcp_send_and_recv("getTcp")
print(FANUCtcpPosition)
print("----------------")
FANUCtcpPosition = littletools.FANUCpositionToPython(FANUCtcpPosition)
print(FANUCtcpPosition)