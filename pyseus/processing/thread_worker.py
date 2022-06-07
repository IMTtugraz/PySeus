from PySide2.QtCore import QThread, Signal, QObject
import numpy
from pyseus.processing.tv_denoising import TV_Denoise
from pyseus.processing.tgv_denoising import TGV_Denoise
from pyseus.processing.tgv_reconstruction import TGV_Reco
from pyseus.processing.tv_reconstruction import TV_Reco


class Worker(QObject):
    output = Signal(numpy.ndarray)
    
    def __init__(self, tv_class, tv_function, dataset_type, dataset, params, spac, coil_data = None):
        super(Worker, self).__init__()
        self.dataset = dataset
        self.data_processed = None
        self.dataset_type = dataset_type
        self.tv_class = tv_class
        self.tv_function = tv_function
        self.params = params
        self.spac = spac
        self.coil_data = coil_data
        
    
    
    # cannot pass arguments to run, but to the constructor of the class 
    def run(self):
        # denoising
        if isinstance(self.tv_class,TV_Denoise):
            self.data_processed = self.tv_class.tv_denoising_gen(self.tv_function, self.dataset_type, self.dataset, self.params, self.spac)
        elif isinstance(self.tv_class,TGV_Denoise):
            self.data_processed = self.tv_class.tgv2_denoising_gen(self.dataset_type, self.dataset, self.params, self.spac)
        # reconstruction
        elif isinstance(self.tv_class, TV_Reco):
            self.data_processed = self.tv_class.tv_reconstruction_gen(self.tv_function, self.dataset_type,self.dataset, self.coil_data, self.params, self.spac)
        elif isinstance(self.tv_class, TGV_Reco):
            self.data_processed = self.tv_class.tgv2_reconstruction_gen(self.dataset_type,self.dataset, self.coil_data,  self.params, self.spac)
        else:
            raise TypeError("No valid denoising class selected")            
        self.output.emit(self.data_processed)
        

        

