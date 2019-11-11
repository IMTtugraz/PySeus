from functools import partial

from PySide2.QtCore import Qt, QMargins
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QFont, QImage, QPixmap, QPainter, QColor, QPen
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLayout, \
        QVBoxLayout, QDialogButtonBox, QTreeWidget, QTreeWidgetItem

from .base import BaseTool


class LineTool(BaseTool):
    """Evaluates data along a line."""

    def __init__(self, app):
        BaseTool.__init__(self)
        self.app = app
        self.roi = [0,0,0,0]
        self.window = LineEvalWindow()
    
    @classmethod
    def setup_menu(cls, app, menu, ami):
        ami(menu, "&Line Eval", partial(cls.start, app))

    def start_roi(self, x, y):
        self.roi[0] = x
        self.roi[1] = y
    
    def end_roi(self, x, y):
        self.roi[2] = x
        self.roi[3] = y

    def draw_overlay(self, pixmap):
        if self.roi == [0,0,0,0]: return pixmap

        painter = QPainter(pixmap)

        pen = QPen(QColor("green"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLine(self.roi[0], self.roi[1], self.roi[2], 
                         self.roi[3])

        painter.end()
        return pixmap

    def clear(self):
        self.roi = None

    def recalculate(self, data):
        result = []
        for i in range(0, 100):
            x = round(self.roi[0] + (self.roi[2]-self.roi[0])*i/100)
            y = round(self.roi[1] + (self.roi[3]-self.roi[1])*i/100)
            result.append(data[y][x])

        self.window.load_data(result)

        self.window.show()


class LineEvalWindow(QDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Line Eval")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setLayout(QVBoxLayout())

        # Startup window size
        self.resize(320, 320)

    def load_data(self, data):
        if hasattr(self, "view"): self.view.deleteLater()

        series = QtCharts.QLineSeries()
        for k, v in enumerate(data):
            series.append(k,v)

        self.view = QtCharts.QChartView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.chart().addSeries(series)
        self.view.chart().createDefaultAxes()
        self.view.chart().setTheme(QtCharts.QChart.ChartThemeDark)
        self.view.chart().setBackgroundVisible(False)
        self.view.chart().setDropShadowEnabled(False)
        self.view.chart().setMargins(QMargins())
        self.view.chart().legend().hide()

        self.layout().addWidget(self.view)
        series.setColor(QColor("white"))
