# -*-Function: 授权函数，在数据库层面上的操作
# 使用用户本地的数据库

# 注意：MAC地址的验证是有规则的，需要谨慎处理
import datetime
import hashlib
import pymysql
import uuid
import re
import subprocess
from psutil import net_if_addrs

from dateutil.relativedelta import relativedelta      # 引用自包python-dateutil
from math import sqrt

# 数据库连接信息：当前是本人本机数据库的连接信息，需要根据设置进行修改
# 把连接设置写出去，保存成json文件
connection_Config = {
    "host":"localhost",
    "user":"root",
    "password":"root",
    "database":"vote"
}

# 建立数据库表：
"""数据表字段：
# auth_code: 序列号
# MAC_Address: MAC地址
# Status_Perpetual: 是否永久，1为永久0为试用
# Status_OutDate: 是否过期，1为过期0为未过期
# Auth_Month: 授权月份
# Date_Start: 授权起始日期
# Date_Lastuse: 上次使用日期
# Date_End: 授权终止日期
"""
# 接口：创建数据库表
def create_DataTable():
    db = pymysql.connect(**connection_Config)
    cursor = db.cursor()
    DataTable = """
        create table if not exists auth(
            Auth_Code varchar(255) primary key,
            MAC_Address varchar(255),
            Status_Perpetual int not null default 0,
            Status_OutDate int not null default 0,
            Auth_Month int(3),
            Date_Start varchar(255),
            Date_LastUse varchar(255),
            Date_End varchar(255))
    """
    try:
        # 先查，没有再创建数据表
        exist_auth = cursor.execute("SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_NAME ='auth'")
        if not exist_auth:
            cursor.execute(DataTable)
            print("Table Create Success.")
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(e)
        return False

# 接口：获取设备的MAC地址
def get_mac_address():
    # mac=uuid.UUID(int=uuid.getnode()).hex[-12:]
    # return ":".join([mac[e:e+2] for e in range(0,11,2)])

    for k, v in net_if_addrs().items():
        if k[0] == '以':
            for item in v:
                address = item[1]
                if "-" in address and len(address) == 17:
                    # print(address)
                    return address.replace("-", ":").lower()

    return "11:0e:c6:63:a3:cf"

    # import wmi
    # c = wmi.WMI()
    # return c.Win32_BaseBoard()[0].SerialNumber

# 接口：匹配设备的MAC地址
def is_same_mac_addr(auth_code, trail):
    if trail:
        auth_mac = str(auth_code.replace("-", "").split('V')[:-1][0])
    else:
        auth_mac = str(auth_code.replace("-", "").split('L')[:-1][0])
    local_mac = get_mac_address()
    local_mac_md5 = md5_encode(local_mac)[:len(auth_mac)].upper()
    if auth_mac == local_mac_md5:
        return True
    else:
        return False

# 接口：判断序列号是否为永久序列号
def is_permanent_auth(code):
    id_hex = code.replace("-", "").split('L')[-1]
    id = int(id_hex.upper(), 16)
    id_new = int((id - 13) / 17)
    def isPrimes(n):
        if n > 1:
            if n == 2:
                return True
            if n % 2 == 0:
                return False
            for x in range(3, int(sqrt(n) + 1), 2):
                if n % x == 0:
                    return False
            return True
        return False
    return isPrimes(id_new)

# 接口：判断临时序列号是否过期
def is_InDate(code_EndTime):
    """
  :param: code_EndTime: 序列号对应的过期时间
  :return: Boolean值，True为在有效期内，False为已过期
  """
    # 若当前时间的字符串值大于过期时间对应的字符串值，判定为过期
    Time_Now = datetime.datetime.now().strftime("%Y-%m-%d")
    return code_EndTime > Time_Now

# 接口：MD5加密算法, 使用库hashlib
def md5_encode(str):
    hl = hashlib.md5()    # 创建md5对象
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

# 接口：获取非永久序列号的有效使用时长
def get_trail_month(code):
    month_hex = code.replace("-", "").split('V')[-1].split('L')[0]
    month = int(month_hex.upper(), 16)
    month = int((month - 33) / 4)
    return month

# 接口：写入数据库表
def insert_datatable(auth_code):
    """
    :param auth_code: 待写入数据表的序列号
    :return: 数据库写入操作不需要返回值
    """
    db = pymysql.connect(**connection_Config)
    cursor = db.cursor()
    mac_addr = get_mac_address()
    time_start = datetime.datetime.now().strftime("%Y-%m-%d")
    if is_permanent_auth(code=auth_code):
        # print("永久授权码")
        if not is_same_mac_addr(auth_code=auth_code,trail=False):
            # print("MAC地址不一致")
            return False, "MAC地址不一致"
        else:
            Insert = "INSERT INTO auth(Auth_Code,MAC_Address,Status_Perpetual,Date_Start) VALUES (%s,%s,%s,%s)"
            values = (auth_code, mac_addr, 1, time_start)
            cursor.execute(Insert, values)
            db.commit()
            cursor.close()
            db.close()
            return True, "永久序列号，通过授权。"
    else:
        # 临时序列号
        # 获取临时授权码的可使用时长
        if not is_same_mac_addr(auth_code=auth_code,trail=True):
            # print("MAC地址不一致")
            return False, "MAC地址不一致"
        else:
            month = get_trail_month(auth_code)
            time_delay = (datetime.datetime.now() + relativedelta(months=+month)).strftime("%Y-%m-%d")
            Insert = "INSERT INTO auth(Auth_Code,MAC_Address,Auth_Month,Date_Start,Date_LastUse,Date_End) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (auth_code, mac_addr,month,time_start,time_start,time_delay)
            cursor.execute(Insert, values)
            db.commit()
            cursor.close()
            db.close()
            info = "试用期序列号, 有效期:" + str(month) + "个月"
            return True, info

def get_mac():
    """
    Validates a mac address
    """
    command = "ipconfig /all"
    addr = subprocess.getoutput(command)
    addr = addr.split("\n")
    valid = re.compile(r'(?<!-)(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?!-)', re.IGNORECASE)

    for a in addr:
        print(valid.match(a))

    return

# def get_mac_address():
#     # import uuid
#     # mac=uuid.UUID(int=uuid.getnode()).hex[-12:]
#     # return ":".join([mac[e:e+2] for e in range(0,11,2)])
#
#     for k, v in net_if_addrs().items():
#         for item in v:
#             address = item[1]
#             if "-" in address and len(address) == 17:
#                 # print(address)
#                 return address.replace("-",":").lower()

# 验证授权
def Authorize():
    """
    :return: Boolean值，通过核验则为True，反之则为False
    # 当状态为True，错误码都为0
    # 当状态为False，错误码中1代表数据表为空，2代表MAC地址不一致，3代表试用序列号已过期
    """
    db = pymysql.connect(**connection_Config)
    cursor = db.cursor()
    # 检查数据表是否为空
    Exist = cursor.execute("SELECT CASE WHEN Auth_Code IS NULL THEN 0 ELSE 1 END FROM auth")
    if not Exist:
        # 本地授权码数据表为空
        return False, 1
    else:
        # 本地授权码数据表非空
        Perpetual = cursor.execute("SELECT 1 FROM auth WHERE Status_Perpetual=1 LIMIT 1")
        # 数据表中存在永久序列号
        if Perpetual:
            cursor.execute("SELECT Auth_Code FROM auth WHERE Status_Perpetual = 1")
            code_Query = cursor.fetchall()[0][0]
            # 未通过MAC地址验证，返回False，程序无法使用
            if not is_same_mac_addr(auth_code=code_Query,trail=False):
                return False, 2
            # 能通过MAC地址验证，返回True，程序可以使用
            else:
                return True, 0
        # 数据表中存在临时序列号
        # 补充：只可能存在一条临时序列号，不可能存在多条
        else:
            cursor.execute("SELECT Auth_Code,Date_End FROM auth WHERE Status_Perpetual=0 AND Status_OutDate=0 LIMIT 1")
            result = cursor.fetchall()       # 直接得到序列号
            print(result)
            
            # 存在一个未过期的临时序列号
            if len(result) > 0:
                if not is_same_mac_addr(auth_code=result[0][0],trail=True):
                    return False, 2
                else:
                    if is_InDate(code_EndTime=result[0][1]):
                        time_now = datetime.datetime.now().strftime("%Y-%m-%d")
                        cursor.execute("UPDATE auth SET Date_LastUse = {}".format(repr(time_now)))
                        db.commit()
                        cursor.close()
                        db.close()
                        return True, 0
                    else:
                        cursor.execute("UPDATE auth SET Status_OutDate ={}".format(repr(1)))
                        db.commit()
                        cursor.close()
                        db.close()
                        return False, 3
            # 不存在未过期的临时序列号
            else:
                return False, 3

# 接口：重新授权
# 弹出窗口重新进行授权，获取授权码写入，并重新执行授权函数Authorize()
def re_Authorize():
    """
    :return: 重新授权的实现
    """
    # 第1步：一旦触发重新授权这一逻辑，就要清除授权数据表内的所有内容，之前的所有授权码作废
    db = pymysql.connect(**connection_Config)
    cursor = db.cursor()
    cursor.execute("TRUNCATE TABLE auth")
    cursor.close()

    # 第2步：相当于空表情况下调用Authorize()函数，此处分开进行
    # 此处接弹出窗口的程序
    # 重新生成序列号后写入数据库，调用insert_datatable()函数

    return

# import os
# def get_models_list(project_path):
#     """
#     :param project_path: 工程文件夹路径
#     :return list_of_models: 模板列表，如['mode1', 'mode2', 'mode3', 'mode4', 'mode5']
#     """
#     list_of_models = []
#     valid = re.compile(r'^mode[0-9]', re.IGNORECASE)
#     for model in os.listdir(project_path):
#         if valid.match(model):
#             list_of_models.append(model)
#
#     return list_of_models


# if __name__ == "__main__":
    # project_path = r'D:/develop/smart_vote/vote_template/vote_template/project/普通模板'
    # project_path = r'D:\develop\smart_vote\vote_template\vote_template\project\模板测试12345'
    # print(get_models_list(project_path=project_path))

    # print(get_mac_address())
    # create_DataTable()
    # res, info = Authorize()
    # print(res, info)