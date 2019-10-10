import h5py
from functools import partial

from PySide2.QtCore import Qt, QMargins
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPen, QBrush, QPainter, QColor
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLayout, \
        QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem


class Histogram(QtCharts.QChartView):
    def __init__(self):
        QtCharts.QChartView.__init__(self)
        #https://doc.qt.io/qt-5/qtcharts-barchart-example.html
        data = [1,2,3,2,3,4,3,2,1,2,3,4,5,4,3,4,5,4,3]
        chart = QtCharts.QChart()
        series = QtCharts.QLineSeries()
        for k, v in enumerate(data):
            series.append(k,v)
        series.setBrush(QBrush("red"))

        chart.addSeries(series)
        
        series.setBrush(QBrush("red"))
        
        chart.setTheme(QtCharts.QChart.ChartThemeDark)
        chart.setBackgroundVisible(False)
        chart.setDropShadowEnabled(False)
        chart.setMargins(QMargins())
        chart.legend().hide()

        self.setChart(chart)
        self.setRenderHint(QPainter.Antialiasing)


class TestWindow(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Test")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(Histogram())


app = QApplication()
win = TestWindow()
res = win.exec()
