from PyQt5 import QtGui, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams
from QSSPCPlotSettingsDialog import QSSPCPlotSettingsDialog
rcParams.update({'figure.autolayout': True})

font = {'family' : 'sans-serif',
        'size'   : 14}

matplotlib.rc('font', **font)

cl = ['#4F81BD', '#C0504D', '#9BBB59','#F79646','#8064A2','#4BACC6','0','0.5']

class QSSPCPlot(QtWidgets.QMainWindow):  
    
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle(self.tr("QSSPC data"))
        self.resize(1020, 752)
        self.setStyleSheet('font-size: 12pt;')        
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
        self.parent = parent
        data = self.parent.data
        self.rows = []
        for i in range(len(self.parent.view.selectedIndexes())):
            self.rows.append(self.parent.view.selectedIndexes()[i].row())
        
        self.x = []
        self.y = []
        self.name = []
        for i in self.rows:
            self.x.append(data[i].loc[:,6].tolist())
            y = data[i].loc[:,4].tolist()
            y = [j * 1000 for j in y] # convert to milliseconds
            self.y.append(y)
            self.name.append(data[i].index.name)

        if not self.parent.plot_settings:
            self.grid_enabled = True
            self.legend_enabled = True
            self.dots_enabled = True
            self.dotsize = 4
            self.lines_enabled = False
            self.linewidth = 2
        else:
            self.grid_enabled = self.parent.plot_settings['grid_enabled']
            self.legend_enabled = self.parent.plot_settings['legend_enabled']
            self.dots_enabled = self.parent.plot_settings['dots_enabled']
            self.dotsize = self.parent.plot_settings['dotsize']
            self.lines_enabled = self.parent.plot_settings['lines_enabled']
            self.linewidth = self.parent.plot_settings['linewidth'] 
        
        self.create_menu()
        self.create_main_frame()          
        self.on_draw()         
        
    def on_draw(self):

        self.axes.clear()
        
        self.axes.grid(self.grid_enabled)

        self.axes.set_ylabel(r'$\mathrm{\mathsf{Lifetime\ [ms]}}$', fontsize=24, weight='black')
        self.axes.set_xlabel(r'$\mathrm{\mathsf{Minority\ carrier\ density\ [cm^{-3}]}}$', fontsize=24, weight='black')

        self.axes.tick_params(pad=8) 

        for i in range(len(self.rows)):
            color = cl[i % len(cl)]
            edge_color = color
    
            if self.dots_enabled and self.lines_enabled:
                style = '-o'
            elif self.dots_enabled:
                style = '.'
            else:
                style = '-'
            
            count = sum(j > 0 for j in self.y[i]) # do not plot dataset with zero or one data points
            if count > 1:
                self.axes.plot(self.x[i],self.y[i],style,c=color,markersize=self.dotsize,markeredgecolor=edge_color,linewidth=self.linewidth,label=self.name[i])

                     
        self.axes.set_xscale('log')
    
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
        settings_dialog = QSSPCPlotSettingsDialog(self)
        settings_dialog.setModal(True)
        settings_dialog.show()         