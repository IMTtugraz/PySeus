from functools import partial
from math import sqrt

from PySide2.QtCore import Qt, QMargins
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtWidgets import QDialog, QVBoxLayout

from .base import BaseTool


class LineTool(BaseTool):
    """Evaluates data along a line."""

    def __init__(self, app):
        BaseTool.__init__(self, app)

        self.line = [0, 0, 0, 0]
        """Start and end coordinates of the current line."""

        self.window = LineToolWindow()

    @classmethod
    def setup_menu(cls, app, menu, ami):
        ami(menu, "&Line Eval", partial(cls.start, app))

    def start_roi(self, x, y):
        self.line[0] = x
        self.line[1] = y

    def end_roi(self, x, y):
        self.line[2] = x
        self.line[3] = y

    def draw_overlay(self, pixmap):
        if self.line == [0, 0, 0, 0]:
            return pixmap

        painter = QPainter(pixmap)

        pen = QPen(QColor("green"))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawLine(self.line[0], self.line[1], self.line[2],
                         self.line[3])

        painter.end()
        return pixmap

    def clear(self):
        self.line = [0, 0, 0, 0]

    def recalculate(self, data):
        result = []
        width = self.line[2]-self.line[0]
        height = self.line[3]-self.line[1]
        distance = sqrt(width**2 + height**2)
        for i in range(0, int(distance*10)):
            x = round(self.line[0] + (width)*i / int(distance*10))
            y = round(self.line[1] + (height)*i / int(distance*10))
            result.append(data[y][x])

        axes = [self.app.dataset.get_scale(), 
                self.app.dataset.get_units()]

        self.window.load_data(result, axes)

        self.window.show()


class LineToolWindow(QDialog):
    """Dispalys LineTool results in a chart window."""

    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Line Eval")
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)

        self.setLayout(QVBoxLayout())

        # Startup window size
        self.resize(480, 320)

    def load_data(self, data, axes):
        """Display a list of values in the chart."""

        if hasattr(self, "view"):
            self.view.deleteLater()

        series = QtCharts.QLineSeries()
        for k, v in enumerate(data):
            series.append(k, v)

        self.view = QtCharts.QChartView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.chart().addSeries(series)
        self.view.chart().createDefaultAxes()

        x_axis = self.view.chart().axes(Qt.Horizontal, series)
        x_axis[0].hide()
        real_x = QtCharts.QValueAxis()
        real_x.setTitleText("[x] = {} mm".format(axes[0]))
        real_x.setRange(x_axis[0].min(), int(x_axis[0].max()/10))
        self.view.chart().addAxis(real_x, Qt.AlignBottom)

        y_axis = self.view.chart().axes(Qt.Vertical, series)
        y_axis[0].setTitleText("[y] = {}".format(axes[1]))

        self.view.chart().setTheme(QtCharts.QChart.ChartThemeDark)
        self.view.chart().setBackgroundVisible(False)
        self.view.chart().setDropShadowEnabled(False)
        self.view.chart().setMargins(QMargins())
        self.view.chart().legend().hide()

        self.layout().addWidget(self.view)
        series.setColor(QColor("white"))
