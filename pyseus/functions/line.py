from PySide2.QtCore import Qt, QMargins
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPen, QBrush, QPainter, QColor
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLayout, \
        QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem

from .base import BaseFct


class LineEval(BaseFct):
    """Displays the coordinates of the current RoI."""

    MENU_NAME = ""

    def __init__(self):
        BaseFct.__init__(self)
        self.window = None

    def recalculate(self, data, roi):
        if self.window == None:
            self.window = LineEvalWindow()

        result = []
        for i in range(0, 100):
            x = round(roi[0] + (roi[2]-roi[0])*i/100)
            y = round(roi[1] + (roi[3]-roi[1])*i/100)
            result.append(data[y][x])

        self.window.load_data(result)

        self.window.exec()
        return ""


class LineEvalChart(QtCharts.QChartView):
    def __init__(self):
        QtCharts.QChartView.__init__(self)
        self.setRenderHint(QPainter.Antialiasing)
    
    def load_data(self, data):
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


class LineEvalWindow(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Line Eval")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.chart = LineEvalChart()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.chart)

    def load_data(self, data):
        self.chart.load_data(data)
