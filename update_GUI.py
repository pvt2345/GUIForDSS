from PyQt5 import QtWidgets
import sys

class Update_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(Update_UI, self).__init__()
        self.setWindowTitle('DSS')
        self.CentralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.CentralWidget)
        self.ncurves = 0
        self.main_UI()

    def main_UI(self):
        self.calendar = QtWidgets.QCalendarWidget()
        self.txtBox_price = QtWidgets.QLineEdit()
        self.btn_Update = QtWidgets.QPushButton("Cập nhật")
        self.lbl1 = QtWidgets.QLabel("Chọn ngày: ")
        self.lbl2 = QtWidgets.QLabel("Nhập giá đóng cửa: ")
        self.vbox1 = QtWidgets.QVBoxLayout()
        self.vbox1.addWidget(self.lbl1)
        self.vbox1.addWidget(self.calendar)
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.hbox1.addWidget(self.lbl2)
        self.hbox1.addWidget(self.txtBox_price)
        self.hbox1.addWidget(self.btn_Update)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.vbox1)
        self.vbox.addLayout(self.hbox1)

        self.CentralWidget.setLayout(self.vbox)
        # self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    TextMining_Window = Update_UI()
    # TextMining_Window.show()
    sys.exit(app.exec_())
