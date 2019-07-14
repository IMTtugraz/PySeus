from sys import stdin, argv

from .core import PySeus
from .ui import MainWindow

def load(data = None):
    app = PySeus()
    app.window = MainWindow(app)
    app.window.show()
    
    if(data != None):
        # check for data format
        print("data")
    
    elif( len(argv) > 1 ):
        # Check arguments
        print("arguments")
    
    elif(not stdin.isatty()):
        # Check stdin
        print("stdin")

    return app.exec_()
