"""GUI elements for displaying images.

Classes
-------

**ViewWidget** - Widget providing an interactive viewport.
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel, QScrollArea

import numpy


class ViewWidget(QScrollArea):
    """Widget providing an interactive viewport."""

    def __init__(self, app):
        QScrollArea.__init__(self)
        self.app = app

        self.image = QLabel()
        self.image.setScaledContents(True)
        self.image.setMouseTracking(True)
        self.image.mouseMoveEvent = self.mouseMoveEvent_over_image
        self.image.mousePressEvent = self.mousePressEvent_over_image
        self.image.mouseReleaseEvent = self.mouseReleaseEvent_over_image

        self.zoom_factor = 1
        """The current zoom factor of the image."""

        self.mouse_action = 0
        """The current action on mouse move.
        Can be *ROI*, *WINDOW* or *PAN*."""

        self.last_position = None
        """The last position, from which mouse events were processed."""

        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setWidget(self.image)

        # Hide scrollbars
        self.horizontalScrollBar().setStyleSheet("QScrollBar { height: 0 }")
        self.verticalScrollBar().setStyleSheet("QScrollBar { width: 0 }")

    def set(self, pixmap):
        """Display the image in *pixmap*."""
        self.image.setPixmap(pixmap)

    def zoom(self, factor, relative=True):
        """Set the zoom level for the displayed image.

        By default, the new zoom factor will be relative to the current
        zoom factor. If *relative* is set to False, *factor* will be used as
        the new zoom factor."""

        if self.app.dataset is None \
                or (relative and (0.1 >= self.zoom_factor * factor >= 100)):
            return

        self.zoom_factor = self.zoom_factor * factor if relative else factor
        self.image.resize(self.zoom_factor * self.image.pixmap().size())

        v_scroll = int(factor * self.verticalScrollBar().value() +
                       ((factor-1) * self.verticalScrollBar().pageStep()/2))
        self.verticalScrollBar().setValue(v_scroll)

        h_scroll = int(factor * self.horizontalScrollBar().value() +
                       ((factor-1) * self.horizontalScrollBar().pageStep()/2))
        self.horizontalScrollBar().setValue(h_scroll)

    def zoom_fit(self):
        """Zoom the displayed image to fit the available viewport."""

        image = self.image.pixmap().size()
        viewport = self.size()

        if image.height() == 0 or image.width() == 0:
            return

        v_zoom = viewport.height() / image.height()
        h_zoom = viewport.width() / image.width()
        self.zoom(min(v_zoom, h_zoom)*0.99, False)

    def mousePressEvent(self, event):  # pylint: disable=C0103
        """Handle pan and window functionality on mouse button down."""

        if event.buttons() == Qt.LeftButton \
                and event.modifiers() == Qt.NoModifier:
            self.mouse_action = "PAN"

        elif event.buttons() == Qt.MiddleButton:
            self.mouse_action = "WINDOW"

        self.last_position = event.screenPos()

    def mouseReleaseEvent(self, event):  # pylint: disable=C0103,W0613
        """Handle RoI functionality on mouse button up."""

        if self.mouse_action == "ROI":
            self.app.recalculate()

        self.last_position = None
        self.mouse_action = 0

    def mouseMoveEvent(self, event):  # pylint: disable=C0103
        """Handle pan, window and RoI functionality on mouse move."""

        self.app.window.show_status("")

        if self.mouse_action == "PAN":
            vertical = self.verticalScrollBar().value() \
                + self.last_position.y() - event.screenPos().y()
            horizontal = self.horizontalScrollBar().value() \
                + self.last_position.x() - event.screenPos().x()

            self.verticalScrollBar().setValue(vertical)
            self.horizontalScrollBar().setValue(horizontal)
            self.last_position = event.screenPos()

        elif self.mouse_action == "WINDOW":
            move = self.last_position.x() - event.screenPos().x()
            scale = self.last_position.y() - event.screenPos().y()
            self.last_position = event.screenPos()
            self.app.display.adjust_window(move, scale)
            self.app.refresh()

        elif self.mouse_action == "ROI":
            x_pos = event.pos().x() if event.pos().x() <= self.image.width() \
                else self.image.width()
            y_pos = event.pos().y() if event.pos().y() <= self.image.height() \
                else self.image.height()
            if self.app.tool is not None:
                self.app.tool.end_roi(int(x_pos / self.zoom_factor),
                                      int(y_pos / self.zoom_factor))
            self.app.refresh()

    def mousePressEvent_over_image(self, event):  # pylint: disable=C0103
        """Handle RoI functionality on mouse button down over the image.
        Hands off contorl to *mousePressEvent* when appropriate."""
        if event.buttons() == Qt.LeftButton \
                and event.modifiers() == Qt.ControlModifier:
            self.mouse_action = "ROI"
            self.last_position = event.pos()

            if self.app.tool is not None:
                x_pos = event.pos().x()
                y_pos = event.pos().y()
                self.app.tool.start_roi(int(x_pos / self.zoom_factor),
                                        int(y_pos / self.zoom_factor))

        else:
            self.mousePressEvent(event)

    def mouseMoveEvent_over_image(self, event):  # pylint: disable=C0103
        """Handle value display functionality on mouse move over the image.
        Call *mouseMoveEvent* for pan, window and RoI functionality."""

        self.mouseMoveEvent(event)

        x_coord = int((self.horizontalScrollBar().value()
                       + event.pos().x()) // self.zoom_factor)
        y_coord = int((self.verticalScrollBar().value()
                       + event.pos().y()) // self.zoom_factor)
        slice_ = self.app.dataset.get_pixeldata(self.app.slice)
        shape = slice_.shape
        if(x_coord < shape[0] and y_coord < shape[1]):
            value = slice_[x_coord, y_coord]
            self.app.window.show_status("{} x {}  -  {:.4g}"
                                        .format(x_coord, y_coord, value))

    def mouseReleaseEvent_over_image(self, event):  # pylint: disable=C0103
        """Call *mouseReleaseEvent* on mouse button up for RoI
        functionality."""

        self.mouseReleaseEvent(event)

    def wheelEvent(self, event):  # pylint: disable=C0103
        """Handle scroll wheel events in the viewport.
        Scroll - Change current slice up or down.
        Alt+Scroll - Change current scan up or down.
        Strg+Scroll - Zoom the current image in or out."""

        if event.modifiers() == Qt.NoModifier:
            slice_ = int(numpy.sign(event.delta()))
            self.app.select_slice(slice_, True)

        elif event.modifiers() == Qt.ControlModifier:
            self.zoom(0.8 if event.delta() < 0 else 1.25)

        elif event.modifiers() == Qt.AltModifier:
            scan = int(numpy.sign(event.delta()))
            self.app.select_scan(scan, True)
