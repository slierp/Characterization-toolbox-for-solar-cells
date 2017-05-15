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

class RSheetPlot(QtWidgets.QMainWindow):  
    
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle(self.tr("Contour plot"))

        self.resize(1020, 752)
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        self.data = parent.data
        
        self.create_menu(self)
        self.create_main_frame(self)          
        self.on_draw()         
        
    def on_draw(self):
        # Clear previous and re-draw everything
        self.axes.clear()   
        self.axes.grid(self.grid_selection)

        self.axes.set_xlabel(r'$\mathrm{\mathsf{V_{OC}\ [V]}}$', fontsize=24, weight='black')
        self.axes.set_ylabel(r'$\mathrm{\mathsf{I_{SC}\ [A]}}$', fontsize=24, weight='black')
        self.axes.tick_params(pad=8)
        
        for i in self.plot_selection:
            self.axes.scatter(self.ad[i]['Uoc'],self.ad[i]['Isc'],c=cl[i % len(cl)],edgecolors='white',linewidths=0.3,s=self.dotsize_selection,label=self.ad[i].index.name)

        if self.legend_selection:
            self.axes.legend(loc='lower left',scatterpoints=1,markerscale=3,frameon=False)

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