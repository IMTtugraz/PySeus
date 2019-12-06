from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QScrollArea

import numpy


class ViewWidget(QScrollArea):
    """The widget providing an image viewport."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app

        self.view = QLabel()
        self.view.setScaledContents(True)
        self.view.setMouseTracking(True)
        self.view.mouseMoveEvent = self._view_mouseMoveEvent
        self.view.mousePressEvent = self._view_mousePressEvent
        self.view.mouseReleaseEvent = self._view_mouseReleaseEvent

        self.zoom_factor = 1
        self.mouse_action = 0

        self.setMouseTracking(True)
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setWidget(self.view)

        # Hide scrollbars
        self.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0 }")
        self.verticalScrollBar().setStyleSheet("QScrollBar { width: 0 }")

    def set(self, pixmap):
        # if pixmap is None:
        #     self.view.clear()
        # else:
        self.view.setPixmap(pixmap)

    def zoom(self, factor, relative=True):
        """Zoom"""
        if self.app.dataset is None \
                or (relative and (0.1 >= self.zoom_factor * factor >= 100)):
            return

        self.zoom_factor = self.zoom_factor * factor if relative else factor
        self.view.resize(self.zoom_factor * self.view.pixmap().size())

        v_scroll = int(factor * self.verticalScrollBar().value() +
                       ((factor-1) * self.verticalScrollBar().pageStep()/2))
        self.verticalScrollBar().setValue(v_scroll)

        h_scroll = int(factor * self.horizontalScrollBar().value() +
                       ((factor-1) * self.horizontalScrollBar().pageStep()/2))
        self.horizontalScrollBar().setValue(h_scroll)

    def zoom_fit(self):
        """Zoom Fit"""
        image = self.view.pixmap().size()
        viewport = self.size()

        if image.height() == 0 or image.width() == 0:
            return

        v_zoom = viewport.height() / image.height()
        h_zoom = viewport.width() / image.width()
        self.zoom(min(v_zoom, h_zoom)*0.99, False)

    def mousePressEvent(self, event):
        """Handle pan, window and RoI functionality on mouse button down."""

        if(event.buttons() == QtCore.Qt.LeftButton
                and event.modifiers() == Qt.NoModifier):
            self.mouse_action = "PAN"

        elif(event.buttons() == QtCore.Qt.MiddleButton):
            self.mouse_action = "WINDOW"

        self.last_position = event.screenPos()

    def mouseReleaseEvent(self, event):
        """Handle pan, window and RoI functionality on mouse button up."""

        if(self.mouse_action == "ROI"):
            self.app.recalculate()

        self.last_position = None
        self.mouse_action = 0

    def mouseMoveEvent(self, event):
        """Handle pan, window and RoI functionality on mouse move."""

        self.app.window.show_status("")

        if(self.mouse_action == "PAN"):
            vertical = self.verticalScrollBar().value() \
                + self.last_position.y() - event.screenPos().y()
            horizontal = self.horizontalScrollBar().value() \
                + self.last_position.x() - event.screenPos().x()

            self.verticalScrollBar().setValue(vertical)
            self.horizontalScrollBar().setValue(horizontal)
            self.last_position = event.screenPos()

        elif(self.mouse_action == "WINDOW"):
            move = self.last_position.x() - event.screenPos().x()
            scale = self.last_position.y() - event.screenPos().y()
            self.last_position = event.screenPos()
            self.app.display.adjust_window(move, scale)
            self.app.refresh()

        elif(self.mouse_action == "ROI"):
            x_pos = event.pos().x() if event.pos().x() <= self.view.width() \
                else self.view.width()
            y_pos = event.pos().y() if event.pos().y() <= self.view.height() \
                else self.view.height()
            if self.app.tool is not None:
                self.app.tool.end_roi(int(x_pos / self.zoom_factor),
                                      int(y_pos / self.zoom_factor))
            self.app.refresh()

    def _view_mousePressEvent(self, event):
        if(event.buttons() == QtCore.Qt.LeftButton
                and event.modifiers() == Qt.ControlModifier):
            self.mouse_action = "ROI"
            self.last_position = event.pos()

            if self.app.tool is not None:
                x_pos = event.pos().x()
                y_pos = event.pos().y()
                self.app.tool.start_roi(int(x_pos / self.zoom_factor),
                                        int(y_pos / self.zoom_factor))

        else:
            self.mousePressEvent(event)

    def _view_mouseMoveEvent(self, event):
        self.mouseMoveEvent(event)

        x = int((self.horizontalScrollBar().value()
                 + event.pos().x()) // self.zoom_factor)
        y = int((self.verticalScrollBar().value()
                 + event.pos().y()) // self.zoom_factor)
        shape = self.app.dataset.pixeldata[self.app.slice].shape
        if(x < shape[0] and y < shape[1]):
            val = self.app.dataset.pixeldata[self.app.slice][x, y]
            self.app.window.show_status("{} x {}  -  {:.4g}".format(x, y, val))

    def _view_mouseReleaseEvent(self, event):
        self.mouseReleaseEvent(event)

    def wheelEvent(self, event):
        """Wheel Event Handler."""
        if event.modifiers() == Qt.NoModifier:
            slice = int(numpy.sign(event.delta()))
            self.app.select_slice(slice, True)

        elif event.modifiers() == Qt.ControlModifier:
            self.zoom(0.8 if event.delta() < 0 else 1.25)

        elif event.modifiers() == Qt.AltModifier:
            scan = int(numpy.sign(event.delta()))
            self.app.select_scan(scan, True)
