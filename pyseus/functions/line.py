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

        self.window.show()
        return ""


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
