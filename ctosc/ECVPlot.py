from PyQt5 import QtGui, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams
from ECVPlotSettingsDialog import ECVPlotSettingsDialog
rcParams.update({'figure.autolayout': True})

font = {'family' : 'sans-serif',
        'size'   : 14}

matplotlib.rc('font', **font)

cl = ['#4F81BD', '#C0504D', '#9BBB59','#F79646','#8064A2','#4BACC6','0','0.5']

class ECVPlot(QtWidgets.QMainWindow):  
    
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("Color map"))
        self.resize(1020, 752)
        self.setStyleSheet('font-size: 12pt;')        
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        data = parent.data
        self.rows = []
        for i in range(len(parent.view.selectedIndexes())):
            self.rows.append(parent.view.selectedIndexes()[i].row())
        
        self.x = []
        self.y0 = []
        self.y1 = []
        self.name = []
        for i in self.rows:
            self.x.append(data[i].ix[:,0].tolist())
            self.y0.append(data[i].ix[:,5].tolist())
            self.y1.append(data[i].ix[:,7].tolist())
            self.name.append(data[i].index.name)

        self.grid_enabled = True
        self.legend_enabled = True
        self.dots_enabled = True
        self.dotsize = 4
        self.lines_enabled = True
        self.linewidth = 2
        self.show_only_ndoping = False
        self.show_only_pdoping = False
        
        self.create_menu()
        self.create_main_frame()          
        self.on_draw()         
        
    def on_draw(self):

        self.axes.clear()
        
        self.axes.grid(self.grid_enabled)

        self.axes.set_xlabel(r'$\mathrm{\mathsf{Depth\ [\mu m]}}$', fontsize=24, weight='black')
        self.axes.set_ylabel(r'$\mathrm{\mathsf{N\ [cm^{-3}]}}$', fontsize=24, weight='black')

        self.axes.tick_params(pad=8) 

        for i in range(len(self.rows)):
            color0 = cl[i % len(cl)]
            edge_color0 = color0
            color1 = cl[i+2 % len(cl)]
            edge_color1 = color1
    
            if self.dots_enabled and self.lines_enabled:
                style = '-o'
            elif self.dots_enabled:
                style = '.'
            else:
                style = '-'
            
            if not self.show_only_pdoping:
                count = sum(j > 0 for j in self.y0[i]) # do not plot dataset with zero or one data points
                if count > 1:
                    self.axes.plot(self.x[i],self.y0[i],style,c=color0,markersize=self.dotsize,markeredgecolor=edge_color0,linewidth=self.linewidth,label=self.name[i])
            
            if not self.show_only_ndoping:
                count = sum(j > 0 for j in self.y1[i])
                if count > 1:
                    self.axes.plot(self.x[i],self.y1[i],style,c=color1,markersize=self.dotsize,markeredgecolor=edge_color1,linewidth=self.linewidth,label=self.name[i])
            
        self.axes.set_yscale('log')
    
        if self.legend_enabled:
            self.axes.legend(loc='lower left',scatterpoints=1,markerscale=3,frameon=True)
            
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
        settings_dialog = ECVPlotSettingsDialog(self)
        settings_dialog.setModal(True)
        settings_dialog.show()         