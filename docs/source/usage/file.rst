File
====

PySeus can load image or kspace data. Furthermore denoised or reconstructed datasets 
can be saved in a separate file.

Load image
----------

Assumes that the loaded file contains only one real-valued image dataset 
representing the amplitude of the image data. If this selection is chosen, the representation of the loaded data switches
automatically to **IMAGE**.

Load k-space
------------

Assumes that the loaded file contains at least three datasets, storing
the real-valued and the imaginary-valued kspace data in two datasets as well as the coil sensitivities 
in a third dataset. If this selection is chosen, the representation of the loaded data switches
automatically to **KSPACE**.


Save dataset
------------

After the denoising or reconstruction of a selected dataset, the new dataset can be saved
in a separate NumPy file.

Reload
------

Reload the current file and show it in standard representation.