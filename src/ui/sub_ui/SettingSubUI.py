import configparser
import os

from PyQt5 import QtWidgets, QtGui

from UI.sub_UI import Setting
import pyqtgraph.opengl as gl
import numpy as np
import open3d as o3d
import src.global_var as glo
from pyqtgraph.opengl import GLViewWidget

class SettingSubUI(QtWidgets.QMainWindow, Setting.Ui_MainWindow):
    def __init__(self, parent=None):
        super(SettingSubUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("设置界面")

        self.pushButton.clicked.connect(self.acition)

    def init(self):
        self.load_para()
        self.pushButton.setText("修改")
        self.groupBox_2.setDisabled(True)
        pass

    def acition(self):
        if  self.pushButton.text() == "修改":
            self.change()
        elif self.pushButton.text() == "保存":
            self.save()

    def save(self):
        self.save_para()

        self.pushButton.setText("修改")
        self.groupBox_2.setDisabled(True)

    def change(self):
        self.pushButton.setText("保存")
        self.groupBox_2.setDisabled(False)

    def load_para(self):
        project_path = glo.get_value("project_path")
        # 在当前文件路径下查找.ini文件
        configPath = os.path.join(project_path, "weld_config.ini")
        if not os.path.exists(configPath):
            raise Exception("ini dose not exist")

        conf = configparser.ConfigParser()
        # 读取.ini文件
        conf.read(configPath)
        # get()函数读取section里的参数值
        arcon_v = conf.get("1", "arcon_v")
        arcon_a = conf.get("1", "arcon_a")
        arcon_time = conf.get("1", "arcon_time")
        arcoff_v = conf.get("1", "arcoff_v")
        arcoff_a = conf.get("1", "arcoff_a")
        arcoff_time = conf.get("1", "arcoff_time")
        welding_v = conf.get("1", "welding_v")
        welding_a = conf.get("1", "welding_a")
        is_flight_arc = conf.get("1", "is_flight_arc")
        anti_stick_v = conf.get("1", "anti_stick_v")
        anti_stick_a = conf.get("1", "anti_stick_a")
        anti_stick_time = conf.get("1", "anti_stick_time")

        arcon_check_time = conf.get("Welding_equipment_setting", "arcon_check_time")
        arcon_check_confirm_time = conf.get("Welding_equipment_setting", "arcon_check_confirm_time")
        arcoff_check_time = conf.get("Welding_equipment_setting", "arcoff_check_time")
        air_on_time = conf.get("Welding_equipment_setting", "air_on_time")
        air_off_time = conf.get("Welding_equipment_setting", "air_off_time")
        pumpback_time = conf.get("Welding_equipment_setting", "pumpback_time")
        arcoff_pumpback_time = conf.get("Welding_equipment_setting", "arcoff_pumpback_time")
        is_pumpback = conf.get("Welding_equipment_setting", "is_pumpback")
        is_arcoff_pumpback = conf.get("Welding_equipment_setting", "is_arcoff_pumpback")
        is_weldingoff_check = conf.get("Welding_equipment_setting", "is_weldingoff_check")
        is_zero_setting = conf.get("Welding_equipment_setting", "is_zero_setting")
        reboot_d = conf.get("Welding_equipment_setting", "reboot_d")
        reboot_speed = conf.get("Welding_equipment_setting", "reboot_speed")
        is_anti_impact = conf.get("Welding_equipment_setting", "is_anti_impact")
        anti_impact_io = conf.get("Welding_equipment_setting", "anti_impact_io")
        anti_impact_level = conf.get("Welding_equipment_setting", "anti_impact_level")
        anti_impact_output = conf.get("Welding_equipment_setting", "anti_impact_output")
        anti_impact_output_level = conf.get("Welding_equipment_setting", "anti_impact_output_level")
        anti_impact_stop_time = conf.get("Welding_equipment_setting", "anti_impact_stop_time")
        stop_anti_impact_time = conf.get("Welding_equipment_setting", "stop_anti_impact_time")
        stop_anti_impact = conf.get("Welding_equipment_setting", "stop_anti_impact")

        self.lineEdit_arcon_v.setText(arcon_v)
        self.lineEdit_arcon_a.setText(arcon_a)
        self.lineEdit_arcon_time.setText(arcon_time)
        self.lineEdit_arcoff_v.setText(arcoff_v)
        self.lineEdit_arcoff_a.setText(arcoff_a)
        self.lineEdit_arcoff_time.setText(arcoff_time)
        self.lineEdit_welding_v.setText(welding_v)
        self.lineEdit_welding_a.setText(welding_a)
        self.checkBox_is_flight_arc.setChecked(True) if is_flight_arc else self.checkBox_is_flight_arc.setChecked(False)
        self.lineEdit_anti_stick_a.setText(anti_stick_a)
        self.lineEdit_anti_stick_v.setText(anti_stick_v)
        self.lineEdit_anti_stick_time.setText(anti_stick_time)

        self.lineEdit_arcon_check_time.setText(arcon_check_time)
        self.lineEdit_arcon_check_confirm_time.setText(arcon_check_confirm_time)
        self.lineEdit_arcoff_check_time.setText(arcoff_check_time)
        self.lineEdit_air_off_time.setText(air_off_time)
        self.lineEdit_air_on_time.setText(air_on_time)
        self.lineEdit_pumpback_time.setText(pumpback_time)
        self.lineEdit_arcoff_pumpback_time.setText(arcoff_pumpback_time)
        self.checkBox_is_pumpback.setChecked(True) if is_pumpback else self.checkBox_is_pumpback.setChecked(False)
        self.checkBox_is_arcoff_pumpback.setChecked(True) if is_arcoff_pumpback else self.checkBox_is_arcoff_pumpback.setChecked(False)
        self.checkBox_is_weldingoff_check.setChecked(True) if is_weldingoff_check else self.checkBox_is_weldingoff_check.setChecked(False)
        self.checkBox_is_zero_setting.setChecked(True) if is_zero_setting else self.checkBox_is_zero_setting.setChecked(False)
        self.lineEdit_reboot_d.setText(reboot_d)
        self.lineEdit_reboot_speed.setText(reboot_speed)
        self.checkBox_is_anti_impact.setChecked(True) if is_anti_impact else self.checkBox_is_anti_impact.setChecked(False)
        self.comboBox_anti_impact_io.setCurrentText(anti_impact_io)
        self.comboBox_anti_impact_level.setCurrentText(anti_impact_level)
        self.comboBox_anti_impact_output.setCurrentText(anti_impact_output)
        self.comboBox_anti_impact_output_level.setCurrentText(anti_impact_output_level)
        self.lineEdit_anti_impact_stop_time.setText(anti_impact_stop_time)
        self.lineEdit_stop_anti_impact_time.setText(stop_anti_impact_time)
        self.checkBox_stop_anti_impact.setChecked(True) if stop_anti_impact else self.checkBox_stop_anti_impact.setChecked(False)

    def save_para(self):
        # 当前文件路径
        project_path = glo.get_value("project_path")
        # 在当前文件路径下查找.ini文件
        configPath = os.path.join(project_path, "weld_config.ini")
        print(configPath)
        conf = configparser.ConfigParser()
        num = self.comboBox_symbol_num.currentText()
        conf.add_section(num)
        conf.set(num, "arcon_v", self.lineEdit_arcon_v.text())
        conf.set(num, "arcon_a", self.lineEdit_arcon_a.text())
        conf.set(num, "arcon_time", self.lineEdit_arcon_time.text())
        conf.set(num, "arcoff_v", self.lineEdit_arcoff_v.text())
        conf.set(num, "arcoff_a", self.lineEdit_arcoff_a.text())
        conf.set(num, "arcoff_time", self.lineEdit_arcoff_time.text())

        conf.set(num, "welding_v", self.lineEdit_welding_v.text())
        conf.set(num, "welding_a", self.lineEdit_welding_a.text())
        if self.checkBox_is_flight_arc.checkState():
            conf.set(num, "is_flight_arc", "True")
        else:
            conf.set(num, "is_flight_arc", "False")
        conf.set(num, "anti_stick_v", self.lineEdit_anti_stick_v.text())
        conf.set(num, "anti_stick_a", self.lineEdit_anti_stick_a.text())
        conf.set(num, "anti_stick_time", self.lineEdit_anti_stick_time.text())

        conf.add_section("Welding_equipment_setting")
        conf.set("Welding_equipment_setting", "arcon_check_time", self.lineEdit_arcon_check_time.text())
        conf.set("Welding_equipment_setting", "arcon_check_confirm_time", self.lineEdit_arcon_check_confirm_time.text())
        conf.set("Welding_equipment_setting", "arcoff_check_time", self.lineEdit_arcoff_check_time.text())
        conf.set("Welding_equipment_setting", "air_on_time", self.lineEdit_air_on_time.text())
        conf.set("Welding_equipment_setting", "air_off_time", self.lineEdit_air_off_time.text())
        conf.set("Welding_equipment_setting", "pumpback_time", self.lineEdit_pumpback_time.text())
        conf.set("Welding_equipment_setting", "arcoff_pumpback_time", self.lineEdit_arcoff_pumpback_time.text())
        if self.checkBox_is_pumpback.checkState():
            conf.set("Welding_equipment_setting", "is_pumpback", "True")
        else:
            conf.set("Welding_equipment_setting", "is_pumpback", "False")
        if self.checkBox_is_arcoff_pumpback.checkState():
            conf.set("Welding_equipment_setting", "is_arcoff_pumpback", "True")
        else:
            conf.set("Welding_equipment_setting", "is_arcoff_pumpback", "False")
        if self.checkBox_is_weldingoff_check.checkState():
            conf.set("Welding_equipment_setting", "is_weldingoff_check", "True")
        else:
            conf.set("Welding_equipment_setting", "is_weldingoff_check", "False")
        if self.checkBox_is_zero_setting.checkState():
            conf.set("Welding_equipment_setting", "is_zero_setting", "True")
        else:
            conf.set("Welding_equipment_setting", "is_zero_setting", "False")

        conf.set("Welding_equipment_setting", "reboot_d", self.lineEdit_reboot_d.text())
        conf.set("Welding_equipment_setting", "reboot_speed", self.lineEdit_reboot_speed.text())
        if self.checkBox_is_anti_impact.checkState():
            conf.set("Welding_equipment_setting", "is_anti_impact", "True")
        else:
            conf.set("Welding_equipment_setting", "is_anti_impact", "False")
        conf.set("Welding_equipment_setting", "anti_impact_io", self.comboBox_anti_impact_io.currentText())
        conf.set("Welding_equipment_setting", "anti_impact_level", self.comboBox_anti_impact_level.currentText())
        conf.set("Welding_equipment_setting", "anti_impact_output", self.comboBox_anti_impact_output.currentText())
        conf.set("Welding_equipment_setting", "anti_impact_output_level", self.comboBox_anti_impact_output_level.currentText())
        conf.set("Welding_equipment_setting", "anti_impact_stop_time", self.lineEdit_anti_impact_stop_time.text())
        conf.set("Welding_equipment_setting", "stop_anti_impact_time", self.lineEdit_stop_anti_impact_time.text())

        if self.checkBox_stop_anti_impact.checkState():
            conf.set("Welding_equipment_setting", "stop_anti_impact", "True")
        else:
            conf.set("Welding_equipment_setting", "stop_anti_impact", "False")

        conf.write(open(configPath, 'w+'))