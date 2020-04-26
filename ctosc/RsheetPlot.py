from PyQt5 import QtGui, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams
from RshPlotSettingsDialog import RshPlotSettingsDialog
from math import ceil, floor
import numpy as np
rcParams.update({'figure.autolayout': True})

font = {'family' : 'sans-serif',
        'size'   : 14}

matplotlib.rc('font', **font)

class RsheetPlot(QtWidgets.QMainWindow):  
    
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("Color map"))
        self.resize(1020, 752)
        self.setStyleSheet('font-size: 12pt;')        
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        self.parent = parent
        data = self.parent.data
        row = self.parent.view.selectedIndexes()[0].row()
        self.data_array = data[row]
        self.x = self.data_array.ix[:,0].tolist()     
        self.y = self.data_array.ix[:,1].tolist()       
        self.z  = self.data_array.ix[:,2].tolist()                        
        
        self.x_points = len(set(self.x)) # no of unique points
        self.y_points = len(set(self.y))
        self.x_ticks = sorted(set(self.x))
        self.y_ticks = sorted(set(self.y))

        for i in range(len(self.x)): # replace x_values for x-point number
            self.x[i] = self.x_ticks.index(self.x[i])

        for i in range(len(self.y)): # replace y_values for y-point number
            self.y[i] = self.y_ticks.index(self.y[i])

        self.matrix = np.zeros([self.x_points,self.y_points])
        self.matrix[:] = np.NaN
        self.matrix[self.x,self.y] = self.z # make image matrix

        self.name = self.data_array.index.name
        self.cmap_options = ['nipy_spectral','Wistia','jet','rainbow','seismic','gray','magma','Reds','Greens','Blues']
        self.interpolation_options = ['none','hanning','bilinear','bicubic','gaussian']

        if not self.parent.plot_settings:
            self.interpolation = 0
            self.colorbar_enabled = True
            self.title_enabled = True
            self.scale_min = floor(min(self.z))
            self.scale_max = ceil(max(self.z))
            self.cmap = 0
        else:
            self.interpolation = self.parent.plot_settings['interpolation']
            self.colorbar_enabled = self.parent.plot_settings['colorbar_enabled']
            self.title_enabled = self.parent.plot_settings['title_enabled']
            self.scale_min = self.parent.plot_settings['scale_min']
            self.scale_max = self.parent.plot_settings['scale_max']
            self.cmap = self.parent.plot_settings['cmap']          
        
        self.create_menu()
        self.create_main_frame()          
        self.on_draw()         
        
    def on_draw(self):

        self.axes.clear()
        self.fig.clear()
        self.axes = self.fig.add_subplot(111, facecolor='White')

        self.axes.set_xticklabels([0]+self.x_ticks) # zero added because mpl seems to ignore first value
        self.axes.set_yticklabels([0]+self.y_ticks)

        self.axes.set_xlabel(r'$\mathrm{\mathsf{x}}$', fontsize=24, weight='black')
        self.axes.set_ylabel(r'$\mathrm{\mathsf{y}}$', fontsize=24, weight='black')

        custom_cmap = matplotlib.cm.get_cmap(self.cmap_options[self.cmap])
        custom_cmap.set_bad('k',1.0)
        plot = self.axes.imshow(self.matrix, origin='lower', interpolation=self.interpolation_options[self.interpolation], cmap=custom_cmap, clim=(self.scale_min, self.scale_max))           

        if self.colorbar_enabled:
            colorbar = self.fig.colorbar(plot,ax=self.axes)
            colorbar.set_clim(self.scale_min, self.scale_max)

        if self.title_enabled:
            self.axes.set_title(self.name)
            
        self.canvas.draw() # perform the second and final draw
        
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
        settings_dialog = RshPlotSettingsDialog(self)
        settings_dialog.setModal(True)
        settings_dialog.show()         