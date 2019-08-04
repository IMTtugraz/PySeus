import sys
import webbrowser

from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QAction, \
    QLabel, QScrollArea, QFileDialog


class ViewWidget(QScrollArea):
    """The widget providing an iamge viewport."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app

        self.view = QLabel()
        self.view.setScaledContents(True)
        self.zoom_factor = 1
        self.mouse_action = 0

        self.setWidget(self.view)
        # Reset Scroll event Handler
        # self.wheelEvent = lambda e: False

    def zoom(self, factor, relative=True):
        if relative and not (0.1 <= self.zoom_factor * factor <= 10):
            return

        self.zoom_factor = self.zoom_factor * factor if relative else factor
        self.view.resize(self.zoom_factor * self.view.pixmap().size())

        # @TODO Refactor into View Widgete (!!!)
        v_scroll = int(factor * self.verticalScrollBar().value() +
            ((factor - 1) * self.verticalScrollBar().pageStep()/2))
        self.verticalScrollBar().setValue(v_scroll)
        
        # @TODO Refactor into View Widgete (!!!)
        h_scroll = int(factor * self.horizontalScrollBar().value() +
            ((factor - 1) * self.horizontalScrollBar().pageStep()/2))
        self.horizontalScrollBar().setValue(h_scroll)

    def mousePressEvent(self, event):
        """Handle pan, window and RoI functionality on mouse button down."""
        self.last_position = event.pos()
        if(event.buttons() == QtCore.Qt.RightButton):
            self.mouse_action = "PAN"
        elif(event.buttons() == QtCore.Qt.MiddleButton):
            self.mouse_action = "WINDOW"
        elif(event.buttons() == QtCore.Qt.LeftButton):
            self.mouse_action = "ROI"
            scroll_x = int(self.horizontalScrollBar().value()
                           / self.zoom_factor)
            scroll_y = int(self.verticalScrollBar().value()
                           / self.zoom_factor)
            self.app.roi[0] = int((event.pos().x()) / self.zoom_factor) \
                + scroll_x
            self.app.roi[1] = int((event.pos().y() - 26) / self.zoom_factor) \
                + scroll_y
        else:
            self.mouse_action = ""  # nothing

    def mouseReleaseEvent(self, event):
        """Handle pan, window and RoI functionality on mouse button up."""
        if(self.mouse_action == "ROI"):
            scroll_x = int(self.horizontalScrollBar().value()
                           / self.zoom_factor)
            scroll_y = int(self.verticalScrollBar().value()
                           / self.zoom_factor)
            roi_end_x = int((event.pos().x()) / self.zoom_factor) + scroll_x
            roi_end_y = int((event.pos().y() - 26) / self.zoom_factor) \
                + scroll_y
            if(self.app.roi[0] == roi_end_x and self.app.roi[1] == roi_end_y):
                self.app.roi = [0, 0, 0, 0]
                self.app.refresh()
            self.app.recalculate()

        self.last_position = None
        self.mouse_action = 0

    def mouseMoveEvent(self, event):
        """Handle pan, window and RoI functionality on mouse move."""
        if(self.mouse_action == "PAN"):
            vertical = self.verticalScrollBar().value() \
                + self.last_position.y() - event.pos().y()
            horizontal = self.horizontalScrollBar().value() \
                + self.last_position.x() - event.pos().x()

            self.verticalScrollBar().setValue(vertical)
            self.horizontalScrollBar().setValue(horizontal)
            self.last_position = event.pos()

        elif(self.mouse_action == "WINDOW"):
            move = self.last_position.x() - event.pos().x()
            scale = self.last_position.y() - event.pos().y()
            self.last_position = event.pos()
            self.app.mode.adjust(move, scale)
            self.app.refresh()
        elif(self.mouse_action == "ROI"):
            scroll_x = int(self.horizontalScrollBar().value()
                           / self.zoom_factor)
            scroll_y = int(self.verticalScrollBar().value()
                           / self.zoom_factor)
            self.app.roi[2] = int((event.pos().x()) / self.zoom_factor) \
                + scroll_x
            self.app.roi[3] = int((event.pos().y() - 26) / self.zoom_factor) \
                + scroll_y
            self.app.refresh()

    def wheelEvent(self, event):
        self.zoom(0.8 if event.delta() < 0 else 1.25)
