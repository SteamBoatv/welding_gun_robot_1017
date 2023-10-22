import os
import src.global_var as glo
import re

def load_positions(project_path):
    # 该代码的目的是读取project_path下的position.xml文件
    # 并将其转换为列表返回
    # 该列表的每一个元素都是一个列表，包含了一个位置的所有信息
    # 0:坐标系 1:时间 2:x 3:y 4:z 5:a 6:b 7:c
    """

    :param path dir:
    :return position list:
    """
    xml_dir = os.path.join(project_path, "position.xml")
    if not os.path.exists(xml_dir):
        print('%s文件不存在'%xml_dir)

    from xml.dom.minidom import parse

    # 读取文件
    dom = parse(xml_dir)
    data = dom.documentElement
    positions = data.getElementsByTagName("position")

    positions_list = []
    for position in positions:
        positions_list.append([float(x) for x in position.childNodes[0].nodeValue[1:-1].split(",")])
    temp_position =  glo.get_value("position")
    for i in range(len(positions_list)):
        temp_position[i+1] = positions_list[i]
    glo.set_value("position",temp_position)
    return positions_list

def save_positions(positions):
    # 该代码的目的是将positions列表保存到project_path下的position.xml文件中
    # 目录地址：E:\PycharmFile\welding_gun_robot\project\1
    """
    :param position list:
    :return: None
    """
    project_path = glo.get_value("project_path")
    if not os.path.exists(project_path):
        print("当前工程：", project_path)
        return

    xml_dir = os.path.join(project_path, "position.xml")
    if os.path.exists(xml_dir):
        print('已经存在文件%s' % xml_dir)

    xml_str = "<positions>\n\t\
              "
    for position in positions:
        xml_str += "<position>" + str(position) + "</position>\n\t\t\
        "
    xml_str +="\n</positions>\n"
    with open(xml_dir,'w') as f:
        f.write(xml_str)
        f.close()
    print('end')

if __name__ == '__main__':
    # load_positions(r"D:\develop\python\code\welding_gun_robot\project\1")
    # save_positions()
    temp_list = []
    str = '[1.0, 2.0, 3.0, 4.0, 5.0, 6.0]'
    for x in str[1:-1].split(","):
        temp_list.append(float(x))
    print(temp_list)
    # num = [int(x) for x in num]
    # print(num)