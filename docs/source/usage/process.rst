Process
=======

The Process menu offers a denoising and a reconstruction option, depending
on the datatype of the loaded data.

Denoising
---------

If the loaded file contains image data denoising can be conducted. In **Data Selection**
the user can choose wether the whole scan or just the current slice should be denoised.
With the **Model Type** option it is possible to choose between different regularizations and 
dataterm types for the assumed inverse problem model. The selection of the model determines which type 
of noise can be removed from the image data. The **Parameters** option holds the value for the regularizations
parameter Lambda, whereby a lower value enforces higher regularization. Furthermore, the amount of 
iterations for the algorithms can be chosen as well as the values for Alpha (only Huber-L2) and
Alpha0 and Alpha1 (both only TGV-L2). The last option is the definition of the **Inverted Spacing**
which defines the inverted spacing for the isotropic x and y dimension between the pixels
as well as inverted spacing between the slices of a dataset in the z dimension. After the button **OK** is pressed,
the calculation of the denoised image starts in a separate thread, so that the user interface does not freeze. Once
the calculation terminates, the denoised dataset is presented in a new window and can be loaded in the main window 
by pressing **OK** in this new window. From there the new dataset can be saved in a new file 
with the **Save dataset** option. 


Reconstruction
--------------

If the loaded file contains kspace data reconstruction can be conducted. In **Data Selection**
the user can choose wether the the current slice, the whole dataset applying 2D-FFT or the whole
dataset applying 3D-FFT should be reconstructed. With the **Model Type** option it is possible 
to choose between TV and TGV reconstruction, alway with a L2 dataterm. TV favors piecewise linear solutions
whereas TGV favors piecewise continous solutions.
The **Parameters** option holds the value for the regularizations
parameter Lambda, whereby a lower value enforces higher regularization. Furthermore, the amount of 
iterations for the algorithms can be chosen as well as the values Alpha0 and Alpha1 (both only TGV-L2). 
The last option is the definition of the **Inverted Spacing**
which defines the inverted spacing for the isotropic x and y dimension between the pixels
as well as inverted spacing between the slices of a dataset in the z dimension which is important for the gradient
calculation. After the button **OK** is pressed,
the calculation of the reconstructed image starts in a separate thread, so that the user interface does not freeze. Once
the calculation terminates, the reconstructed dataset is presented in a new window and can be loaded in the main window 
by pressing **OK** in this new window. From there the new dataset can be saved in a new file 
with the **Save dataset** option. 
