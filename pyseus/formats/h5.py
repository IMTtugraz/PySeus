"""Support for DICOM files.

Classes
-------

**H5** - Class modeling HDF5 datasets.
**H5Explorer** - Dialog for selecting a dataset in an H5 file.
"""

import os
import numpy
from ..settings import DataType
from enum import IntEnum

import h5py

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QLabel, QLayout, QVBoxLayout, \
    QDialogButtonBox, QMessageBox, \
    QListWidget, QListWidgetItem

from .base import BaseFormat, LoadError


class H5(BaseFormat):
    """Class modeling DICOM datasets.

    Supports *.h5*-files in HDF5 format.
    Supports metadata, pixelspacing, scale, units and orientation
    using attributes with DICOM or NIfTI standard keywords."""

    EXTENSIONS = (".h5", ".hdf5")

    @classmethod
    def can_handle(cls, path):
        _, ext = os.path.splitext(path)
        return ext.lower() in H5.EXTENSIONS

    def __init__(self):
        BaseFormat.__init__(self)

        self.meta_keymap = {
            "pys:patient": ["PatientName"],
            "pys:series": ["SeriesDescription"],
            "pys:sequence": ["SequenceName"],
            "pys:matrix": ["AcquisitionMatrix"],
            "pys:tr": ["RepetitionTime"],
            "pys:te": ["EchoTime"],
            "pys:alpha": ["FlipAngle"]
        }

        self.subpath = ""
        """Internal path to the current image dataset in the H5 file."""

        self.subpath_real = ""
        """Internal path to the current real part of k-space of the dataset in the H5 file."""

        self.subpath_imag = ""
        """Internal path to the current imaginary part of k-space of the dataset in the H5 file."""

        self.subpath_coil = ""
        """Internal path to the coil sensitivity map for the corresponding current dataset in the H5 file."""

        self.dims = 0
        """Number of dimensions of the current dataset in the H5 file."""

    def load(self, path, data_type):
        if not os.path.isfile(path):
            raise LoadError("File not found.")

        self.data_type = data_type

        with h5py.File(path, "r") as file_:

            nodes = []

            def _walk(name, item):
                if isinstance(item, h5py.Dataset):
                    nodes.append(name)

            file_.visititems(_walk)

            def _openH5Explorer(title):
                dialog = H5Explorer(nodes, title)
                choice = dialog.exec()
                if choice == QDialog.Accepted:
                    subpath = dialog.result()
                    return subpath
                else:
                    return False

            if len(nodes) == 1 and (self.data_type ==
                                    DataType.IMAGE or self.data_type == DataType.KSPACE):
                self.subpath = nodes[0]

            elif self.data_type == DataType.KSPACE:
                self.subpath_real = _openH5Explorer("Select Real Dataset")
                self.subpath_imag = _openH5Explorer("Select Imag Dataset")
                self.subpath_coil = _openH5Explorer("Select Coil Dataset")
                len_re = len(file_[self.subpath_real].dims)
                len_im = len(file_[self.subpath_imag].dims)

                if len_re == len_im:
                    # to be consistent with dimension check of the
                    # scans below subpath variable of image data is used
                    self.subpath = self.subpath_real
                else:
                    raise TypeError("Real and imag part of k-space data \
                                    do not agree in dimensions")

            elif self.data_type == DataType.IMAGE:
                self.subpath = _openH5Explorer("Select Dataset")

            else:
                raise TypeError("Unknown chosen datatype")

            self.path = path
            self.dims = len(file_[self.subpath].dims)

            if 2 <= self.dims <= 3:  # single or multiple slices
                self.scans = [0]

            elif self.dims == 4:  # multiple scans
                self.scans = list(range(0, len(file_[self.subpath])))

            elif self.dims == 5:
                message = ("The selected dataset is 5-dimensional."
                           "The first two dimensions will be concatenated.")
                QMessageBox.warning(None, "Pyseus", message)
                scan_count = (file_[self.subpath].shape[0]
                              * file_[self.subpath].shape[1])
                self.scans = list(range(0, scan_count))

            else:
                message = "Invalid dataset '{}' in '{}': Wrong dimensions." \
                          .format(self.subpath, path)
                raise LoadError(message)

            self.scan = 0
            return True

    def get_scan_pixeldata(self, scan):
        with h5py.File(self.path, "r") as file_:

            if self.data_type == DataType.IMAGE:

                if self.dims == 2:  # single slice
                    return numpy.asarray([file_[self.subpath]])

                if self.dims == 3:  # multiple slices
                    return numpy.asarray(file_[self.subpath])

                if self.dims == 4:  # multiple scans
                    return numpy.asarray(file_[self.subpath][scan])

                if self.dims == 5:
                    dim_4, dim_5 = divmod(scan, file_[self.subpath].shape[1])
                    return numpy.asarray(file_[self.subpath][dim_4][dim_5])

            elif self.data_type == DataType.KSPACE:
                if self.dims == 2:  # single slice
                    return (numpy.asarray(
                        [file_[self.subpath_real]]) + 1j * numpy.asarray([file_[self.subpath_imag]]))

                if self.dims == 3:  # multiple slices
                    return (
                        numpy.asarray(
                            file_[
                                self.subpath_real]) +
                        1j *
                        numpy.asarray(
                            file_[
                                self.subpath_imag]))

                if self.dims == 4:  # multiple scans
                    return (
                        numpy.asarray(
                            file_[
                                self.subpath_real][scan]) +
                        1j *
                        numpy.asarray(
                            file_[
                                self.subpath_imag][scan]))

                if self.dims == 5:
                    dim_4, dim_5 = divmod(
                        scan, file_[self.subpath_real].shape[1])
                    return (
                        numpy.asarray(
                            file_[
                                self.subpath_real][dim_4][dim_5]) +
                        1j *
                        numpy.asarray(
                            file_[
                                self.subpath_imag][dim_4][dim_5]))

            return []  # can´t interpret data with dimensions <= 1 or > 5

    # just with 4 dims or more, Coils are needed and assumption that there is
    # just  3D sample (no 2D only)
    def get_reco_pixeldata(self, scan, slice_):
        with h5py.File(self.path, "r") as file_:

            if self.data_type == DataType.KSPACE:

                if self.dims == 4:  # multiple scans
                    if slice_ == -1:
                        return (
                            numpy.asarray(
                                file_[
                                    self.subpath_real]) +
                            1j *
                            numpy.asarray(
                                file_[
                                    self.subpath_imag]))[
                            :,
                            :,
                            :,
                            :]
                    else:
                        return (
                            numpy.asarray(
                                file_[
                                    self.subpath_real]) +
                            1j *
                            numpy.asarray(
                                file_[
                                    self.subpath_imag]))[
                            :,
                            slice_:slice_ +
                            1,
                            :,
                            :]

                # dim 5 is arbitrary parameter, dim 4 is the coil dimension and
                # is always completely loaded therefore no indexing of dim 4
                if self.dims == 5:
                    dim_5, dim_coil = divmod(
                        scan, file_[self.subpath_real].shape[1])
                    if slice_ == -1:
                        return (
                            numpy.asarray(
                                file_[
                                    self.subpath_real][dim_5]) +
                            1j *
                            numpy.asarray(
                                file_[
                                    self.subpath_imag][dim_5]))[
                            :,
                            :,
                            :,
                            :]
                    else:
                        return (
                            numpy.asarray(
                                file_[
                                    self.subpath_real][dim_5]) +
                            1j *
                            numpy.asarray(
                                file_[
                                    self.subpath_imag][dim_5]))[
                            :,
                            slice_:slice_ +
                            1,
                            :,
                            :]

        return []

    def get_coil_data(self, slice_):
        # Asumption that coil data is 4D always.
        # Return is also always 4D, even if less dim are needed, other dims are
        # len=1
        with h5py.File(self.path, "r") as file_:

            if slice_ == -1:
                return numpy.asarray(file_[self.subpath_coil])

            return numpy.asarray(file_[self.subpath_coil])[
                :, slice_:slice_ + 1, :, :]

    def get_scan_metadata(self, scan):
        metadata = {}

        with h5py.File(self.path, "r") as file_:
            for attribute in file_[self.subpath].attrs:
                metadata[attribute[0]] = attribute[1]

        return metadata

    def get_spacing(self, reset=False):
        if not self.pixel_spacing or reset:
            if "PixelSpacing" in self.metadata.keys():
                self.pixel_spacing = list(self.metadata["PixelSpacing"])
            elif "pixdim" in self.metadata.keys():
                self.pixel_spacing = list(self.metadata["pixdim"])
            else:
                self.pixel_spacing = [1, 1, 1]

        return self.pixel_spacing

    def get_scale(self):
        # DICOM implementation
        if "PixelSpacing" in self.metadata.keys():
            pixel_spacing = list(self.metadata["PixelSpacing"])
            return float(min(pixel_spacing))

        # NIfTI implementation
        if "xyzt_units" in self.metadata.keys():
            pixdim = min(self.get_spacing())  # units per pixel
            if self.metadata["xyzt_units"] & 1:
                return 1000.0 * pixdim
            if self.metadata["xyzt_units"] & 2:
                return 1.0 * pixdim
            if self.metadata["xyzt_units"] & 3:
                return 0.001 * pixdim

        return 0.0

    def get_units(self):
        if "Units" in self.metadata.keys():
            return "{}".format(self.metadata["Units"])
            # not accounting for Rescale Intercept, Rescale Slope

        return "1"

    def get_orientation(self):
        return []


class H5Explorer(QDialog):  # pylint: disable=R0903
    """Dialog for selecting a dataset in an H5 file."""

    def __init__(self, items, title):
        QDialog.__init__(self)
        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.label = QLabel("Choose the dataset to load:")
        self.label.setStyleSheet("color: #000")
        self.view = QListWidget()

        for i in items:
            self.view.addItem(QListWidgetItem(i))

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok
                                        | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self._button_ok)
        self.buttons.rejected.connect(self._button_cancel)

        layout = QVBoxLayout()
        layout.setSizeConstraint(QLayout.SetFixedSize)
        layout.addWidget(self.label)
        layout.addWidget(self.view)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def _button_ok(self):
        self.accept()

    def _button_cancel(self):
        self.reject()

    def result(self):
        """Returns the selected element."""
        return self.view.currentItem().text()
