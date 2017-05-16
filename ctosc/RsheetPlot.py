import matplotlib #, Tkinter, FileDialog
from PyQt5 import QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams
from PlotSettingsDialog import PlotSettingsDialog
rcParams.update({'figure.autolayout': True})

font = {'family' : 'sans-serif',
        'size'   : 14}

matplotlib.rc('font', **font)

class RsheetPlot(QtWidgets.QMainWindow):  
    
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("Color map"))

        self.resize(1020, 752)
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        data = parent.data
        row = parent.view.selectedIndexes()[0].row()
        self.data_array = data[row] #.ix[:,2]
        array_width = int(len(self.data_array)**0.5)
        self.x = self.data_array.ix[:,0].values.reshape(array_width,array_width)
        self.y = self.data_array.ix[:,1].values.reshape(array_width,array_width)
        self.z = self.data_array.ix[:,2].values.reshape(array_width,array_width)
        self.name = self.data_array.index.name

        self.interpolation_enabled = False
        self.colorbar_enabled = True
        self.title_enabled = True
        self.scale_min = None
        self.scale_max = None
        
        self.create_menu()
        self.create_main_frame()          
        self.on_draw()         
        
    def on_draw(self):
        # Clear previous and re-draw everything
        self.axes.clear()
        self.fig.clear()
        self.axes = self.fig.add_subplot(111, facecolor='White')

        self.axes.set_xlabel(r'$\mathrm{\mathsf{x}}$', fontsize=24, weight='black')
        self.axes.set_ylabel(r'$\mathrm{\mathsf{y}}$', fontsize=24, weight='black')
        
        if not self.interpolation_enabled:
            plot = self.axes.pcolormesh(self.x, self.y, self.z, cmap='Wistia')
        else:
            plot = self.axes.imshow(self.z, interpolation='gaussian', cmap='Wistia')
        
        if self.colorbar_enabled:
            self.fig.colorbar(plot,ax=self.axes)

        if self.title_enabled:
            self.axes.set_title(self.name)

        self.canvas.draw()
    
    def create_main_frame(self,two_axes=False):
        self.main_frame = QtWidgets.QWidget()
        
        # Create the mpl Figure and FigCanvas objects
        self.dpi = 100
        self.fig = Figure((10.0, 10.0), dpi=self.dpi, facecolor='White')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        
        self.axes = self.fig.add_subplot(111, facecolor='White')
 
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls               
        show_button = QtWidgets.QPushButton()
        show_button.clicked.connect(self.plot_settings_view)
        show_button.setIcon(QtGui.QIcon(":gear.png"))
        show_button.setToolTip(self.tr("Plot settings"))
        show_button.setStatusTip(self.tr("Plot settings"))

        buttonbox0 = QtWidgets.QDialogButtonBox()
        buttonbox0.addButton(show_button, QtWidgets.QDialogButtonBox.ActionRole)               

        self.mpl_toolbar.addWidget(show_button) 
                              
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
        
    def plot_settings_view(self):
        settings_dialog = PlotSettingsDialog(self)
        settings_dialog.setModal(True)
        settings_dialog.show()         