

class Menu(QtWidgets.QWidget, menu.Ui_Form):
    self.setting_path = 'resource/setting.ini'

    # 自定义信号
    show_ballot_box_manage_signal = QtCore.pyqtSignal()
    show_template_manage_signal = QtCore.pyqtSignal()
    show_item_manage_signal = QtCore.pyqtSignal()
    show_parameter_setting_signal = QtCore.pyqtSignal()
    show_manually_review_signal = QtCore.pyqtSignal()
    show_vote_data_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("首页菜单")
        self.setWindowIcon(QtGui.QIcon('printer.png'))

        self.PushButton_ballot_box_manage.clicked.connect(self.ballot_box_manage)
        self.PushButton_template_manage.clicked.connect(self.template_manage)
        self.PushButton_item_manage.clicked.connect(self.item_manage)
        self.PushButton_parameter_setting.clicked.connect(self.parameter_setting)
        self.PushButton_manually_review.clicked.connect(self.manually_review)
        self.PushButton_vote_data.clicked.connect(self.vote_data)
        self.pushButton_return_project.clicked.connect(return_project_manage)

        self.init()

    def init(self):
        config = configparser.ConfigParser()
        file = config.read(self.setting_path)
        config_dict = config.defaults()

        background_path = config_dict["background"]
        self.gridFrame.setStyleSheet("#gridFrame{border-image: url(" + background_path + ");}")

    def ballot_box_manage(self):
        print('进入票箱管理')
        self.show_ballot_box_manage_signal.emit()

    def template_manage(self):
        print('进入模板管理')
        self.show_template_manage_signal.emit()

    def item_manage(self):
        print('进入候选人管理')
        self.show_item_manage_signal.emit()

    def parameter_setting(self):
        print('进入参数设置')
        self.show_parameter_setting_signal.emit()

    def manually_review(self):
        print('进入人工审核')
        self.show_manually_review_signal.emit()

    def vote_data(self):
        print('进入选票数据')
        self.show_vote_data_signal.emit()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())