import matplotlib #, Tkinter, FileDialog
from PyQt5 import QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

font = {'family' : 'sans-serif',
        'size'   : 14}

matplotlib.rc('font', **font)

cl = ['#4F81BD', '#C0504D', '#9BBB59','#F79646','#8064A2','#4BACC6','0','0.5'] # colour
axis_label = r'$\mathrm{\mathsf{I_{REV}\ [A]}}$'

########## Main class - only for inheriting ##########

class RsheetPlot(QtWidgets.QMainWindow):  
    
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("Contour plot"))

        self.resize(1020, 752)
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        data = parent.data
        row = parent.view.selectedIndexes()[0].row()
        self.data_array = data[row].ix[:,2]
        array_width = int(len(self.data_array)**0.5)
        self.data_array = self.data_array.values.reshape(array_width,array_width)
        
        self.create_menu()
        self.create_main_frame()          
        self.on_draw()         
        
    def on_draw(self):
        # Clear previous and re-draw everything
        self.axes.clear()

        self.axes.set_xlabel(r'$\mathrm{\mathsf{x}}$', fontsize=24, weight='black')
        self.axes.set_ylabel(r'$\mathrm{\mathsf{y}}$', fontsize=24, weight='black')
        
        self.axes.imshow(self.data_array, cmap='Wistia')
        #self.axes.imshow(self.data_array, interpolation='gaussian', cmap='Wistia')

        self.canvas.draw()
    
    def create_main_frame(self,two_axes=False):
        self.main_frame = QtWidgets.QWidget()
        
        # Create the mpl Figure and FigCanvas objects
        self.dpi = 100
        self.fig = Figure((10.0, 10.0), dpi=self.dpi, facecolor='White')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        self.axes = self.fig.add_subplot(111, facecolor='White')
        
        if two_axes:
            self.axes2 = self.axes.twinx()        
 
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
                                
        vbox = QtWidgets.QVBoxLayout()        
        vbox.addWidget(self.mpl_toolbar)
        vbox.addWidget(self.canvas)
        
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
        
        self.status_text = QtWidgets.QLabel("")        
        self.statusBar().addWidget(self.status_text,1)       
        
    def create_menu(self):

        self.file_menu = self.menuBar().addMenu(self.tr("File"))
        tip = self.tr("Quit")
        quit_action = QtWidgets.QAction(tip, self)
        quit_action.setIcon(QtGui.QIcon(":quit.png"))
        quit_action.triggered.connect(self.close) 
        quit_action.setToolTip(tip)
        quit_action.setStatusTip(tip)
        quit_action.setShortcut('Ctrl+Q')
       
        self.file_menu.addAction(quit_action)