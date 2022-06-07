from PySide2.QtWidgets import QBoxLayout, QButtonGroup, QCheckBox, QDesktopWidget, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLayout, QLineEdit, QMainWindow, QAction, QLabel, QFileDialog, \
    QFrame, QPushButton, QRadioButton, QScrollArea, QSizePolicy, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout

from pyseus.processing.tv_reconstruction import TV_Reco


from ..settings import ProcessType, ProcessSelDataType, ProcessRegType, DataType

from pyseus.processing.thread_worker import Worker
from pyseus.processing.tv_denoising import TV_Denoise
from pyseus.processing.tgv_denoising import TGV_Denoise
from pyseus.processing.tgv_reconstruction import TGV_Reco
from pyseus.modes.grayscale import Grayscale
from PySide2.QtCore import Qt, QThread
import numpy


class ProcessDialog(QDialog):
    """ Dialog for Image Processing with input parameters "denoising" or "reconstruction" as processing type"""

    def __init__(self, app, proc_type):
        super().__init__()

        self.app = app
        self.proc_type = proc_type
        self.window_processed = ProcessedWindow(app, self.proc_type)

        vlayout_sel = QVBoxLayout()
        vlayout_type = QVBoxLayout()
        grp_box_sel = QGroupBox("Data Selection")
        grp_box_type = QGroupBox("Model Type")

        # Take "Denoising" or "Reconstruction" as title straight from the ENUM
        self.setWindowTitle(str.capitalize(self.proc_type.name))

        # subgroup of radio buttons for data selection
        self.grp_data_sel = QButtonGroup()
        self.btn_curr_slice = QRadioButton("Current Slice")
        self.btn_curr_slice.setChecked(True)
        if self.proc_type == ProcessType.DENOISING:
            self.btn_all_slices_2D = QRadioButton("Whole Scan")
        else:
            self.btn_all_slices_2D = QRadioButton("2D - Whole Scan")
        self.btn_all_slices_3D = QRadioButton("3D - Whole Scan")
        self.grp_data_sel.addButton(
            self.btn_curr_slice,
            ProcessSelDataType.SLICE_2D)
        self.grp_data_sel.addButton(
            self.btn_all_slices_2D,
            ProcessSelDataType.WHOLE_SCAN_2D)
        self.grp_data_sel.addButton(
            self.btn_all_slices_3D,
            ProcessSelDataType.WHOLE_SCAN_3D)

        # subgroup of radio buttons to dataset selection
        self.grp_tv_type = QButtonGroup()
        self.btn_tv_L1 = QRadioButton("TV-L1")
        self.btn_hub_L2 = QRadioButton("Huber-L2")
        self.btn_tv_L2 = QRadioButton("TV-L2")
        self.btn_tv_L2.setChecked(True)
        self.btn_tgv2_L2 = QRadioButton("TGV2-L2")
        self.grp_tv_type.addButton(self.btn_tv_L1, int(ProcessRegType.TV_L1))
        self.grp_tv_type.addButton(self.btn_hub_L2, int(ProcessRegType.HUB_L2))
        self.grp_tv_type.addButton(self.btn_tv_L2, int(ProcessRegType.TV_L2))
        self.grp_tv_type.addButton(
            self.btn_tgv2_L2, int(
                ProcessRegType.TGV2_L2))

        vlayout_sel.addWidget(self.btn_curr_slice)
        vlayout_sel.addWidget(self.btn_all_slices_2D)
        if self.proc_type == ProcessType.RECONSTRUCTION:
            vlayout_sel.addWidget(self.btn_all_slices_3D)
        grp_box_sel.setLayout(vlayout_sel)

        if self.proc_type == ProcessType.DENOISING:
            vlayout_type.addWidget(self.btn_tv_L1)
            vlayout_type.addWidget(self.btn_hub_L2)
        vlayout_type.addWidget(self.btn_tv_L2)
        vlayout_type.addWidget(self.btn_tgv2_L2)
        grp_box_type.setLayout(vlayout_type)

        # form layout for parameter input for processing algorithm
        vlayout_par = QVBoxLayout()
        vlayout_spac = QVBoxLayout()
        grp_box_par = QGroupBox("Parameters")
        grp_box_spac = QGroupBox("Inverted Spacing")

        v_form_par = QFormLayout()
        self.qline_lambd = QLineEdit()
        self.qline_lambd.setText("30")
        v_form_par.addRow("Lambda", self.qline_lambd)

        self.qline_iter = QLineEdit()
        self.qline_iter.setText("100")
        v_form_par.addRow("Iterations", self.qline_iter)

        v_form_par.addRow(" ", None)
        self.qline_alpha = QLineEdit()
        self.qline_alpha.setText("0.03")
        size_pol = self.qline_alpha.sizePolicy()
        size_pol.setRetainSizeWhenHidden(True)
        self.qline_alpha.setSizePolicy(size_pol)
        self.qline_alpha.hide()
        v_form_par.addRow("Alpha", self.qline_alpha)

        self.qline_alpha0 = QLineEdit()
        self.qline_alpha0.setText("2")
        size_pol0 = self.qline_alpha0.sizePolicy()
        size_pol0.setRetainSizeWhenHidden(True)
        self.qline_alpha0.setSizePolicy(size_pol0)
        self.qline_alpha0.hide()
        v_form_par.addRow("Alpha0", self.qline_alpha0)

        self.qline_alpha1 = QLineEdit()
        self.qline_alpha1.setText("1")
        size_pol1 = self.qline_alpha1.sizePolicy()
        size_pol1.setRetainSizeWhenHidden(True)
        self.qline_alpha1.setSizePolicy(size_pol1)
        self.qline_alpha1.hide()
        v_form_par.addRow("Alpha1", self.qline_alpha1)

        self.btn_tv_L1.clicked.connect(lambda: self.qline_alpha.hide())
        self.btn_hub_L2.clicked.connect(lambda: self.qline_alpha.show())
        self.btn_tv_L2.clicked.connect(lambda: self.qline_alpha.hide())
        self.btn_tgv2_L2.clicked.connect(lambda: self.qline_alpha.hide())

        self.btn_tv_L1.clicked.connect(lambda: self.qline_alpha0.hide())
        self.btn_hub_L2.clicked.connect(lambda: self.qline_alpha0.hide())
        self.btn_tv_L2.clicked.connect(lambda: self.qline_alpha0.hide())
        self.btn_tgv2_L2.clicked.connect(lambda: self.qline_alpha0.show())

        self.btn_tv_L1.clicked.connect(lambda: self.qline_alpha1.hide())
        self.btn_hub_L2.clicked.connect(lambda: self.qline_alpha1.hide())
        self.btn_tv_L2.clicked.connect(lambda: self.qline_alpha1.hide())
        self.btn_tgv2_L2.clicked.connect(lambda: self.qline_alpha1.show())

        v_form_spac = QFormLayout()
        self.qline_hiso_inv = QLineEdit()
        self.qline_hiso_inv.setText("1.0")
        v_form_spac.addRow("h_iso inverted", self.qline_hiso_inv)

        self.qline_hz_inv = QLineEdit()
        self.qline_hz_inv.setText("1.0")
        v_form_spac.addRow("h_z inverted", self.qline_hz_inv)

        self.box_btns = QDialogButtonBox()
        self.box_btns.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.box_btns.accepted.connect(self.signal_ok)
        self.box_btns.rejected.connect(lambda: self.close())

        # organize items on GUI

        vlayout_par.addLayout(v_form_par)
        grp_box_par.setLayout(vlayout_par)

        vlayout_spac.addLayout(v_form_spac)
        grp_box_spac.setLayout(vlayout_spac)

        gridlayout = QGridLayout()
        gridlayout.addWidget(grp_box_sel, 0, 0)
        gridlayout.addWidget(grp_box_type, 1, 0)
        gridlayout.addWidget(grp_box_par, 0, 1)
        gridlayout.addWidget(grp_box_spac, 1, 1)

        vlayout_all = QVBoxLayout()
        vlayout_all.addLayout(gridlayout)
        vlayout_all.addWidget(self.box_btns)

        self.setLayout(vlayout_all)
        self.setStyleSheet("QLineEdit"
                           "{"
                           "color: white; background : darkgray;"
                           "}"
                           "QLabel"
                           "{"
                           "color: white;"
                           "}"
                           "QRadioButton"
                           "{"
                           "color: white;"
                           "}"
                           "QGroupBox"
                           "{"
                           "color: white"
                           "}"
                           "QCheckBox"
                           "{"
                           "color: white"
                           "}"
                           )

    def signal_ok(self):

        alpha = float(self.qline_alpha.text())
        alpha0 = float(self.qline_alpha0.text())
        alpha1 = float(self.qline_alpha1.text())
        lambd = float(self.qline_lambd.text())
        iterations = int(self.qline_iter.text())

        h_iso_inv = float(self.qline_hiso_inv.text())
        h_z_inv = float(self.qline_hz_inv.text())

        dataset_type = ProcessSelDataType(self.grp_data_sel.checkedId())
        tv_type = ProcessRegType(self.grp_tv_type.checkedId())

        self.window_processed.start_calculation(
            alpha,
            alpha0,
            alpha1,
            lambd,
            iterations,
            h_iso_inv,
            h_z_inv,
            dataset_type,
            tv_type)


class ProcessedWindow(QDialog):

    def __init__(self, app, proc_type):
        super().__init__()

        self.app = app
        self.processed = None
        self.array_shape = None
        self.slice_id_selected = None
        self.dataset_type = None
        self.proc_type = proc_type

        self.setWindowTitle("Processed Data")

        self.view = ProcessedViewWidget(self.app, self)
        self.box_btns_ok = QDialogButtonBox()
        self.box_btns_ok.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.box_btns_ok.accepted.connect(self.signal_ok)
        self.box_btns_ok.rejected.connect(lambda: self.close())

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.view)
        self.layout().addWidget(self.box_btns_ok)

        self.thread = None
        self.worker = None

        self.mode = Grayscale()

    def calculation_callback(self, data_obj):

        self.thread.requestInterruption()
        self.thread.quit()
        self.thread.wait()

        del self.thread
        del self.worker
        self.thread = None

        self.processed = data_obj

        if self.dataset_type == ProcessSelDataType.WHOLE_SCAN_2D or self.dataset_type == ProcessSelDataType.WHOLE_SCAN_3D:
            self.slice_id_selected = (self.app.dataset.slice_count() // 2)
            processed_displayed = self.processed[self.slice_id_selected, :, :]
        elif self.dataset_type == ProcessSelDataType.SLICE_2D:
            processed_displayed = self.processed

        self.display_image(processed_displayed)

    def start_calculation(
            self,
            alpha,
            alpha0,
            alpha1,
            lambd,
            iterations,
            hiso_inv,
            hz_inv,
            dataset_type,
            tv_type):

        self.dataset_type = dataset_type

        if self.proc_type == ProcessType.DENOISING:

            if self.dataset_type == ProcessSelDataType.WHOLE_SCAN_2D or self.dataset_type == ProcessSelDataType.WHOLE_SCAN_3D:
                dataset_noisy = self.app.dataset.get_pixeldata(-1)
            elif self.dataset_type == ProcessSelDataType.SLICE_2D:
                dataset_noisy = self.app.dataset.get_pixeldata(
                    self.app.get_slice_id())

            if tv_type == ProcessRegType.TV_L1:
                tv_class = TV_Denoise()
                tv_type_func = tv_class.tv_denoising_L1
                params = (lambd, iterations)
            if tv_type == ProcessRegType.HUB_L2:
                tv_class = TV_Denoise()
                tv_type_func = tv_class.tv_denoising_huberROF
                params = (lambd, iterations, alpha)
            if tv_type == ProcessRegType.TV_L2:
                tv_class = TV_Denoise()
                tv_type_func = tv_class.tv_denoising_L2
                params = (lambd, iterations)
            if tv_type == ProcessRegType.TGV2_L2:
                # tv_type_func not needed, just one possible case for tgv
                tv_class = TGV_Denoise()
                tv_type_func = None
                params = (lambd, alpha0, alpha1, iterations)

            spac = (hiso_inv, hz_inv)

            if self.thread is None:
                self.thread = QThread()
                self.worker = Worker(
                    tv_class,
                    tv_type_func,
                    dataset_type,
                    dataset_noisy,
                    params,
                    spac)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run)
                self.worker.output.connect(self.calculation_callback)
                self.thread.start()

        elif self.proc_type == ProcessType.RECONSTRUCTION:

            if self.app.dataset.get_data_type() != DataType.KSPACE:
                raise TypeError("Loaded dataset must be kspace data")

            scan_id = self.app.dataset.scan
            slice_id = self.app.get_slice_id()
            if self.dataset_type == ProcessSelDataType.WHOLE_SCAN_2D or self.dataset_type == ProcessSelDataType.WHOLE_SCAN_3D:
                dataset_kspace = self.app.dataset.get_reco_pixeldata(
                    scan_id, -1)  # dataset_noisy = self.app.dataset.get_pixeldata(-1)
                data_coils = self.app.dataset.get_coil_data(-1)
            elif self.dataset_type == ProcessSelDataType.SLICE_2D:
                # dataset_noisy = self.app.dataset.get_pixeldata(self.app.get_slice_id())
                dataset_kspace = self.app.dataset.get_reco_pixeldata(
                    scan_id, slice_id)
                data_coils = self.app.dataset.get_coil_data(slice_id)

            if tv_type == ProcessRegType.TV_L2:
                tv_class = TV_Reco()
                tv_type_func = tv_class.tv_l2_reconstruction
                params = (lambd, iterations)
            if tv_type == ProcessRegType.TGV2_L2:
                # tv_type_func not needed, just one possible case for tgv
                tv_class = TGV_Reco()
                tv_type_func = None
                params = (lambd, alpha0, alpha1, iterations)

            spac = (hiso_inv, hz_inv)

            if self.thread is None:
                self.thread = QThread()
                self.worker = Worker(
                    tv_class,
                    tv_type_func,
                    dataset_type,
                    dataset_kspace,
                    params,
                    spac,
                    data_coils)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run)
                self.worker.output.connect(self.calculation_callback)
                self.thread.start()

    def display_image(self, image):

        self.mode.temporary_window(image)
        pixmap = self.mode.get_pixmap(image)
        self.view.set(pixmap)
        self.show()
        screen_size = QDesktopWidget().screenGeometry()
        self.resize(screen_size.width() * 0.3, screen_size.height() * 0.3)
        self.view.zoom_fit()

    def refresh_slice(self, slice_inc):

        if self.dataset_type == ProcessSelDataType.WHOLE_SCAN_2D or self.dataset_type == ProcessSelDataType.WHOLE_SCAN_3D:
            new_slice = self.slice_id_selected + slice_inc
            if 0 <= new_slice < self.app.dataset.slice_count():
                self.display_image(self.processed[new_slice])
                self.slice_id_selected = new_slice
            elif new_slice < 0:
                self.slice_id_selected = 0
            else:
                self.slice_id_selected = self.app.dataset.slice_count()

    def signal_ok(self):

        self.app.set_processed_dataset(self.processed)

    def resizeEvent(self, event):  # pylint: disable=C0103
        """Keep the viewport centered and adjust zoom on window resize."""
        x_factor = event.size().width() / event.oldSize().width()
        # y_factor = event.size().height() / event.oldSize().height()
        # @TODO x_factor if xf < yf or xf * width * zoom_factor < viewport_x
        self.view.zoom(x_factor, True)


class ProcessedViewWidget(QScrollArea):
    """Widget providing an interactive viewport."""

    def __init__(self, app, dialog):
        QScrollArea.__init__(self)
        self.app = app
        self.dialog = dialog

        self.image = QLabel()
        self.image.setScaledContents(True)
        self.image.setMouseTracking(True)

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

        if self.image is None \
                or (relative and (0.1 >= self.zoom_factor * factor >= 100)):
            return

        self.zoom_factor = self.zoom_factor * factor if relative else factor
        self.image.resize(self.zoom_factor * self.image.pixmap().size())

        v_scroll = int(factor * self.verticalScrollBar().value() +
                       ((factor - 1) * self.verticalScrollBar().pageStep() / 2))
        self.verticalScrollBar().setValue(v_scroll)

        h_scroll = int(factor * self.horizontalScrollBar().value() +
                       ((factor - 1) * self.horizontalScrollBar().pageStep() / 2))
        self.horizontalScrollBar().setValue(h_scroll)

    def zoom_fit(self):
        """Zoom the displayed image to fit the available viewport."""

        image = self.image.pixmap().size()
        viewport = self.size()

        if image.height() == 0 or image.width() == 0:
            return

        v_zoom = viewport.height() / image.height()
        h_zoom = viewport.width() / image.width()
        self.zoom(min(v_zoom, h_zoom) * 0.99, False)

    def wheelEvent(self, event):  # pylint: disable=C0103
        """Handle scroll wheel events in the viewport.
        Scroll - Change current slice up or down."""

        slice_ = int(numpy.sign(event.delta()))
        self.dialog.refresh_slice(slice_)
