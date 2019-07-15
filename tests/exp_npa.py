import numpy
import imageio

if __name__ == '__main__':
    pic = imageio.imread('npa.jpg')
    grayscale = (pic[:, :, 0]+pic[:, :, 1]+pic[:, :, 2])
    numpy.savetxt("npa.txt", grayscale, fmt='%1.0f')
