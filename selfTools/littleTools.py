import time

import src.global_var as glo


class LittleTools:
    def __init__(self):
        pass

    # 使用连接好的tcp socket 来发送message，并以返回值的方式接受数据
    def tcp_send_and_recv(self, message):
        tcp_socket = glo.get_value("tcp_socket")
        tcp_socket.send(message.encode("gbk"))
        time.sleep(1)
        data = tcp_socket.recv(1024)
        data = data.decode("gbk")
        return data

    # 将数组格式化为9位数组 长度保持不变
    def formatTo9(self, target):
        formatted_nums = []
        for num in target:
            num = "{:+09.3f}".format(num)
            formatted_nums.append(num)
        return formatted_nums

    # 将两个数组转换为 AtoB的格式
    def formatToAtoB(self, point1, point2):
        L = LittleTools()
        str1 = L.formatTo9(point1)
        str1 = ''.join([str(x) for x in str1])
        str2 = L.formatTo9(point2)
        str2 = ''.join([str(x) for x in str2])
        temp = "CAtB-" + str1 +"X"+ str2
        return str1,str2
    # 把单个字符的数组 转化为 数组
    def convert_to_number_array(self,array):
        result = []
        temp = ''
        for digit in array:
            if digit in ['+', '-']:
                if temp:
                    result.append(float(temp))
                    temp = ''
                temp += digit
            else:
                temp += digit
        result.append(float(temp))
        return result
    # 将发那科发送来的 带N的坐标转换为 数组
    def FANUCpositionToPython(self,data):
        # --------------------------------------------------------------------------------
        n_index = data.find("N")
        if n_index != -1:
            # 如果找到了 "N"，则将其之前的部分提取出来
            # 去掉了之后的 NUT000内容
            data = data[:n_index]
        numbers = data.strip().split()
        # 循环遍历numbers，将其转换成float类型
        for i in range(len(numbers)):
            numbers[i] = float(numbers[i])
        # [1221.748, 441.721, -336.408, 179.138, 40.088, 139.257]
        return numbers