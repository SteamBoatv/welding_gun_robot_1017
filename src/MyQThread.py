import sys
import threading
import time
import traceback

from PyQt5.QtCore import QThread, pyqtSignal


class MyQThread(QThread):
    """
    change sleep_time and thread_name then start
    """
    # 通过类成员对象定义信号
    update_data = pyqtSignal(str)
    flag = 1
    sleep_time = 1
    thread_name = "thread_name"

    # 处理业务逻辑
    def run(self):
        self.flag = 1
        while self.flag == 1:
            self.update_data.emit("1")
            time.sleep(self.sleep_time)

    def stop(self):
        self.flag = 0
        self.wait()
        print(self.thread_name + "停止刷新线程")

# class runScriptThread(threading.Thread):  # The timer class is derived from the class threading.Thread
#     def __init__(self, funcName, *args):
#         threading.Thread.__init__(self)
#         self.args = args
#         self.funcName = funcName
#         self.exitcode = 0
#         self.exception = None
#         self.exc_traceback = ''
#
#     def run(self):  # Overwrite run() method, put what you want the thread do here
#         try:
#             self._run()
#         except Exception as e:
#             self.exitcode = 1  # 如果线程异常退出，将该标志位设置为1，正常退出为0
#             self.exception = e
#             self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))  # 在改成员变量中记录异常信息
#
#     def _run(self):
#         try:
#             self.funcName()
#         except Exception as e:
#             raise e
