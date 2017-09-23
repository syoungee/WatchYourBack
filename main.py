import sys

import win32con
import win32gui
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5 import uic, QtCore


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('mainwindow.ui', self)

        self.btnRefresh.clicked.connect(self.btnRefresh_onClick)
        self.btnRefresh_onClick(False)
        self.btnHide.clicked.connect(self.btnHide_onClick)
        self.btnShow.clicked.connect(self.btnShow_onClick)
        self.btnExit.clicked.connect(self.btnExit_onClick)

    def btnRefresh_onClick(self, v):
        self.listWindow.clear()

        def callback(hWnd, lParam):
            if win32gui.IsWindowVisible(hWnd):
                title = win32gui.GetWindowText(hWnd)

                if title:
                    print(hex(hWnd), title)
                    item = QListWidgetItem(title)
                    item.setData(QtCore.Qt.UserRole, hWnd)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.listWindow.addItem(item)

        win32gui.EnumWindows(callback, None)

    def btnHide_onClick(self, v):
        for i in range(self.listWindow.count()):
            item = self.listWindow.item(i)

            if item.checkState() == QtCore.Qt.Checked:
                hWnd = item.data(QtCore.Qt.UserRole)
                win32gui.ShowWindow(hWnd, win32con.SW_HIDE)

    def btnShow_onClick(self, v):
        for i in range(self.listWindow.count()):
            item = self.listWindow.item(i)

            if item.checkState() == QtCore.Qt.Checked:
                hWnd = item.data(QtCore.Qt.UserRole)
                win32gui.ShowWindow(hWnd, win32con.SW_SHOW)


    def btnExit_onClick(self, v):
       sys.exit()


app = QApplication(sys.argv)
window = MyWindow()
window.show()

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
