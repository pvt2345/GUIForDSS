import sys
from PyQt5 import QtWidgets
# from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import Qt, QThread
from pathlib import Path
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import pandas as pd
import update_GUI
import numpy as np
import matplotlib.patches as patches
# import GetData
# import pandas as pd
import threading


# from matplotlib.backends.backend_qt5agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

def series_to_polyline(xdata, ydata):
    size = len(xdata)
    polyline = QPolygonF(size)
    pointer = polyline.data()
    dtype, tinfo = np.float, np.finfo  # integers: = np.int, np.iinfo
    pointer.setsize(2 * polyline.size() * tinfo(dtype).dtype.itemsize)
    memory = np.frombuffer(pointer, dtype)
    memory[:(size - 1) * 2 + 1:2] = xdata
    memory[1:(size - 1) * 2 + 2:2] = ydata
    return polyline


class BigData_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(BigData_UI, self).__init__()
        self.setWindowTitle('DSS')
        self.CentralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.CentralWidget)
        self.ncurves = 0
        self.main_UI()

    def main_UI(self):
        self.btn_Update = QtWidgets.QPushButton("Cập nhật dữ liệu")
        self.main_label = QtWidgets.QLabel("Dự đoán giá đóng cửa cho mã chứng khoán MPC: ")
        self.canvas = FigureCanvas(Figure(figsize = (27, 9)))
        self.h_box1 = QtWidgets.QHBoxLayout()
        self.h_box1.addWidget(self.btn_Update)
        self.h_box1.addStretch()

        self.h_box2 = QtWidgets.QHBoxLayout()
        self.h_box2.addStretch()
        self.h_box2.addWidget(self.main_label)
        self.h_box2.addStretch()

        # self.v_box3 = QtWidgets.QVBoxLayout()
        # self.v_box3.addWidget(self.canvas)

        self.main_hbox = QtWidgets.QVBoxLayout()
        self.main_hbox.addLayout(self.h_box1)
        self.main_hbox.addLayout(self.h_box2)
        self.main_hbox.addWidget(self.canvas)

        self.CentralWidget.setLayout(self.main_hbox)

        df =  pd.read_csv("MPC.csv")
        a = df["Close"]

        pred = pd.read_csv("MPC_pred.csv")
        date = range(201, 251)
        b = pred["pred"]


        self.ax = self.canvas.figure.subplots()
        self.ax.plot(a, color = "blue")
        self.ax.plot(date, b, color = "red")
        # self.ax.plot(a, "o")
        self.btn_Update.clicked.connect(self.btn_Update_clicked)

        self.show()

    def btn_Update_clicked(self):
            self.update_window = update_GUI.Update_UI()
            self.update_window.show()
            # Update_UI = update_GUI.Update_UI()
        # TextMining_Window.show()
        # sys.exit(app.exec_())

    # def condition_ComboBox_currentIndexChanged(self):
    #     try:
    #         i = self.condition_ComboBox.currentIndex()
    #         # print(i)
    #         if (i == 0):
    #             id_case = GetData.DetectID_11(self.data)
    #         elif (i == 1):
    #             id_case = GetData.DetectID_12(self.data)
    #         elif (i == 2):
    #             id_case = GetData.DetectID_13(self.data)
    #         elif (i == 3):
    #             id_case = GetData.DetectID_14(self.data)
    #         else:
    #             id_case = GetData.DetectID_2(self.data)
    #         self.TableWidget.setRowCount(len(id_case))
    #         self.TableWidget.setColumnCount(1)
    #         listitem = [QtWidgets.QTableWidgetItem(item) for item in id_case]
    #         for i in range(-1, len(id_case) - 1):
    #             self.TableWidget.setItem(i, 1, listitem[i + 1])
    #     except Exception as e:
    #         print(e)

    # def TableWidget_CellChanged(self):
    #     try:
    #         i = self.condition_ComboBox.currentIndex()
    #         if(i == 0):
    #             id = int(self.TableWidget.currentItem().text())
    #             data,data2_,info = GetData.Detect_DK11(id, self.df)
    #             n = data.shape
    #
    #             try:
    #                 self._static_ax.remove()
    #             finally:
    #                 self._static_ax = self.canvas.figure.subplots()
    #                 self._static_ax.set_color_cycle(['blue','orange','green'])
    #                 self._static_ax.plot(data)
    #                 # self._static_ax.figure.gca().legend(('Tờ khai', 'Kim ngạch', 'Thuế'))
    #                 # self._static_ax.legend(loc='best')
    #                 self._static_ax.legend(['Tờ khai', 'Kim ngạch', 'Thuế'])
    #                 self._static_ax.plot(data,'o')
    #                 for i in range(0, n[0] - 1):
    #                     if ((data2_[i][0] > 0) & (data2_[i][2] < 0)):
    #                         rect = patches.Rectangle((i + 0.5, 0), 1, 1, linewidth=1, edgecolor='r', facecolor='none')
    #                         self._static_ax.add_patch(rect)
    #                 self._static_ax.figure.canvas.draw()
    #                 self.ThongTin_TableWidget.setColumnCount(len(info.keys()))
    #                 self.ThongTin_TableWidget.setRowCount(len(info) + 1)
    #                 item = [QtWidgets.QTableWidgetItem(key) for key in info.columns.values.tolist()]
    #                 for i in range(0, self.ThongTin_TableWidget.columnCount()):
    #                     self.ThongTin_TableWidget.setItem(0, i, item[i])
    #
    #                 item_ = []
    #                 for i in range(len(info)):
    #                     item_.append([])
    #                 for i in range(len(info)):
    #                     item_[i] = info.iloc[i].tolist()
    #                 for i in range(len(info)):
    #                     item_[i] = [str(a) for a in item_[i]]
    #                     for j in range(1, len(item_[i])):
    #                         item_[i][j] = item_[i][j][0:5]
    #
    #                 # print(item_)
    #                 for i in range(len(item_)):
    #                     # for j in range(self.ThongTin_TableWidget.columnCount()):
    #                     for j in range(len(item_[i])):
    #                         self.ThongTin_TableWidget.setItem(i + 1, j, QtWidgets.QTableWidgetItem(item_[i][j]))
    #                 # print(item_)
    #
    #         elif(i == 1):
    #             id = int(self.TableWidget.currentItem().text())
    #             data, data2_, info = GetData.Detect_DK12(id, self.df)
    #             n = data.shape
    #
    #             try:
    #                 self._static_ax.remove()
    #             finally:
    #                 self._static_ax = self.canvas.figure.subplots()
    #                 self._static_ax.set_color_cycle(['blue', 'orange', 'green'])
    #                 self._static_ax.plot(data)
    #                 self._static_ax.plot(data, 'o')
    #                 for i in range(0, n[0] - 1):
    #                     if ((data2_[i][0] > 0) & (data2_[i][2] < 0)):
    #                         rect = patches.Rectangle((i + 0.5, 0), 1, 1, linewidth=1, edgecolor='r', facecolor='none')
    #                         self._static_ax.add_patch(rect)
    #                 self._static_ax.figure.canvas.draw()
    #                 self.ThongTin_TableWidget.setColumnCount(len(info.keys()))
    #                 self.ThongTin_TableWidget.setRowCount(len(info) + 1)
    #                 item = [QtWidgets.QTableWidgetItem(key) for key in info.columns.values.tolist()]
    #                 for i in range(0, self.ThongTin_TableWidget.columnCount()):
    #                     self.ThongTin_TableWidget.setItem(0, i, item[i])
    #
    #                 item_ = []
    #                 for i in range(len(info)):
    #                     item_.append([])
    #                 for i in range(len(info)):
    #                     item_[i] = info.iloc[i].tolist()
    #                 for i in range(len(info)):
    #                     item_[i] = [str(a) for a in item_[i]]
    #                     for j in range(1, len(item_[i])):
    #                         item_[i][j] = item_[i][j][0:5]
    #
    #                 # print(item_)
    #                 for i in range(len(item_)):
    #                     # for j in range(self.ThongTin_TableWidget.columnCount()):
    #                     for j in range(len(item_[i])):
    #                         self.ThongTin_TableWidget.setItem(i + 1, j, QtWidgets.QTableWidgetItem(item_[i][j]))
    #                 # print(item_)
    #
    #         elif(i == 2):
    #             id = int(self.TableWidget.currentItem().text())
    #             data, data2_, info = GetData.Detect_DK13(id, self.df)
    #             n = data.shape
    #
    #             try:
    #                 self._static_ax.remove()
    #             finally:
    #                 self._static_ax = self.canvas.figure.subplots()
    #                 self._static_ax.set_color_cycle(['blue', 'orange', 'green'])
    #                 self._static_ax.plot(data)
    #                 self._static_ax.plot(data, 'o')
    #                 for i in range(0, n[0] - 1):
    #                     if ((data2_[i][0] > 0) & (data2_[i][2] < 0)):
    #                         rect = patches.Rectangle((i + 0.5, 0), 1, 1, linewidth=1, edgecolor='r', facecolor='none')
    #                         self._static_ax.add_patch(rect)
    #                 self._static_ax.figure.canvas.draw()
    #                 self.ThongTin_TableWidget.setColumnCount(len(info.keys()))
    #                 self.ThongTin_TableWidget.setRowCount(len(info) + 1)
    #                 item = [QtWidgets.QTableWidgetItem(key) for key in info.columns.values.tolist()]
    #                 for i in range(0, self.ThongTin_TableWidget.columnCount()):
    #                     self.ThongTin_TableWidget.setItem(0, i, item[i])
    #
    #                 item_ = []
    #                 for i in range(len(info)):
    #                     item_.append([])
    #                 for i in range(len(info)):
    #                     item_[i] = info.iloc[i].tolist()
    #                 for i in range(len(info)):
    #                     item_[i] = [str(a) for a in item_[i]]
    #                     for j in range(1, len(item_[i])):
    #                         item_[i][j] = item_[i][j][0:5]
    #
    #                 # print(item_)
    #                 for i in range(len(item_)):
    #                     # for j in range(self.ThongTin_TableWidget.columnCount()):
    #                     for j in range(len(item_[i])):
    #                         self.ThongTin_TableWidget.setItem(i + 1, j, QtWidgets.QTableWidgetItem(item_[i][j]))
    #                 # print(item_)
    #
    #         elif(i == 3):
    #             id = int(self.TableWidget.currentItem().text())
    #             data, data2_, info = GetData.Detect_DK14(id, self.df)
    #             n = data.shape
    #
    #             try:
    #                 self._static_ax.remove()
    #             finally:
    #                 self._static_ax = self.canvas.figure.subplots()
    #                 self._static_ax.set_color_cycle(['blue', 'orange', 'green'])
    #                 self._static_ax.plot(data)
    #                 self._static_ax.plot(data, 'o')
    #                 for i in range(0, n[0] - 1):
    #                     if ((data2_[i][0] > 0) & (data2_[i][2] < 0)):
    #                         rect = patches.Rectangle((i + 0.5, 0), 1, 1, linewidth=1, edgecolor='r', facecolor='none')
    #                         self._static_ax.add_patch(rect)
    #                 self._static_ax.figure.canvas.draw()
    #                 self.ThongTin_TableWidget.setColumnCount(len(info.keys()))
    #                 self.ThongTin_TableWidget.setRowCount(len(info) + 1)
    #                 item = [QtWidgets.QTableWidgetItem(key) for key in info.columns.values.tolist()]
    #                 for i in range(0, self.ThongTin_TableWidget.columnCount()):
    #                     self.ThongTin_TableWidget.setItem(0, i, item[i])
    #
    #                 item_ = []
    #                 for i in range(len(info)):
    #                     item_.append([])
    #                 for i in range(len(info)):
    #                     item_[i] = info.iloc[i].tolist()
    #                 for i in range(len(info)):
    #                     item_[i] = [str(a) for a in item_[i]]
    #                     for j in range(1, len(item_[i])):
    #                         item_[i][j] = item_[i][j][0:5]
    #
    #                 # print(item_)
    #                 for i in range(len(item_)):
    #                     # for j in range(self.ThongTin_TableWidget.columnCount()):
    #                     for j in range(len(item_[i])):
    #                         self.ThongTin_TableWidget.setItem(i + 1, j, QtWidgets.QTableWidgetItem(item_[i][j]))
    #                 # print(item_)
    #         elif(i == 5):
    #             id = int(self.TableWidget.currentItem().text())
    #             data, data2_, info = GetData.Detect_DK22(id, self.df)
    #             n = data.shape
    #
    #             try:
    #                 self._static_ax.remove()
    #             finally:
    #                 self._static_ax = self.canvas.figure.subplots()
    #                 self._static_ax.set_color_cycle(['blue', 'orange', 'green'])
    #                 self._static_ax.plot(data)
    #                 self._static_ax.plot(data, 'o')
    #                 for i in range(0, n[0] - 1):
    #                     if ((data2_[i][0] > 0) & (data2_[i][2] < 0)):
    #                         rect = patches.Rectangle((i + 0.5, 0), 1, 1, linewidth=1, edgecolor='r', facecolor='none')
    #                         self._static_ax.add_patch(rect)
    #                 self._static_ax.figure.canvas.draw()
    #                 self.ThongTin_TableWidget.setColumnCount(len(info.keys()))
    #                 self.ThongTin_TableWidget.setRowCount(len(info) + 1)
    #                 item = [QtWidgets.QTableWidgetItem(key) for key in info.columns.values.tolist()]
    #                 for i in range(0, self.ThongTin_TableWidget.columnCount()):
    #                     self.ThongTin_TableWidget.setItem(0, i, item[i])
    #
    #                 item_ = []
    #                 for i in range(len(info)):
    #                     item_.append([])
    #                 for i in range(len(info)):
    #                     item_[i] = info.iloc[i].tolist()
    #                 for i in range(len(info)):
    #                     item_[i] = [str(a) for a in item_[i]]
    #                     for j in range(1, len(item_[i])):
    #                         item_[i][j] = item_[i][j][0:5]
    #
    #                 # print(item_)
    #                 for i in range(len(item_)):
    #                     # for j in range(self.ThongTin_TableWidget.columnCount()):
    #                     for j in range(len(item_[i])):
    #                         self.ThongTin_TableWidget.setItem(i + 1, j, QtWidgets.QTableWidgetItem(item_[i][j]))
    #                 # print(item_)
    #
    #
    #
    #     except Exception as e:
    #         print(e)

    # def Load(self, path):
    #     id_case1 = Test(path)
    #     self.TableWidget.setRowCount(len(id_case1))
    #     self.TableWidg    11et.setColumnCount(1)
    #     listitem = [QtWidgets.QTableWidgetItem(item) for item in id_case1]
    #     for i in range(-1, len(id_case1) - 1):
    #         self.TableWidget.setItem(i, 1, listitem[i + 1])


    # def add_data(self, xdata, ydata, color=None):
    #     curve = QLineSeries()
    #     pen = curve.pen()
    #     if color is not None:
    #         pen.setColor(color)
    #     pen.setWidthF(1)
    #     curve.setPen(pen)
    #     curve.setUseOpenGL(True)
    #     curve.append(series_to_polyline(xdata, ydata))
    #     self.Chart.addSeries(curve)
    #     self.Chart.createDefaultAxes()
    #     # self.Chart
    #     self.ncurves += 1

# class MainBackgroundThread(QThread):
#     def __init__(self, path):
#         QThread.__init__(self)
#         self.path = path
#     def run(self):
#         id_case1 = Test(self.path)
#         return id_case1


def main():
    app = QtWidgets.QApplication(sys.argv)
    TextMining_Window = BigData_UI()
    # TextMining_Window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    t = threading.Thread(target=main)
    t.start()
