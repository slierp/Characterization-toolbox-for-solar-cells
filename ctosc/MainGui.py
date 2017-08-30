# -*- coding: utf-8 -*-
from HelpDialog import HelpDialog
from PyQt5 import QtGui, QtWidgets
from ImageBlendWidget import ImageBlendWidget
from RsheetWidget import RsheetWidget
from ECVWidget import ECVWidget

class MainGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainGui, self).__init__(parent)
        self.setWindowTitle("CTOSC")
        self.setWindowIcon(QtGui.QIcon(":CTOSC_icon.png"))        

        ### Set initial geometry and center the window on the screen ###
        self.resize(1024, 576)
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft()) 

        ### Set default font size ###
        self.setStyleSheet('font-size: 12pt;')  

        self.rsheet_view = QtWidgets.QTreeView()
        self.rsheet_model = QtGui.QStandardItemModel()
        self.rsheet_widget = RsheetWidget(self)
        self.rsheet_view.doubleClicked.connect(self.rsheet_widget.show)
        
        self.ecv_view = QtWidgets.QTreeView()
        self.ecv_model = QtGui.QStandardItemModel()
        self.ecv_widget = ECVWidget(self)
        self.ecv_view.doubleClicked.connect(self.ecv_widget.show)        

        self.imageblend_view = QtWidgets.QTreeView()
        self.imageblend_model = QtGui.QStandardItemModel()
        self.image_blend_widget = ImageBlendWidget(self)

        self.status_text = QtWidgets.QLabel("")
        
        self.create_menu()
        self.create_main_frame()

    def open_help_dialog(self):
        help_dialog = HelpDialog(self)
        help_dialog.setModal(True)
        help_dialog.show()

    def on_about(self):
        msg = self.tr("CTOSC - Characterization toolbox for solar cells\nAuthor: Ronald Naber\nLicense: Public domain")
        QtWidgets.QMessageBox.about(self, self.tr("About the application"), msg)
    
    def create_main_frame(self):
        self.setWindowTitle(self.tr("CTOSC")) # do this again so that translator can catch it
        self.main_frame = QtWidgets.QWidget()        

        ##### Rsheet #####     
        self.rsheet_view.setModel(self.rsheet_model)
        self.rsheet_model.setHorizontalHeaderLabels([self.tr('Files')])
        self.rsheet_view.setRootIsDecorated(False)
        self.rsheet_view.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.rsheet_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)        

        rsh_open_files_button = QtWidgets.QPushButton()
        rsh_open_files_button.clicked.connect(self.rsheet_widget.open_files) 
        rsh_open_files_button.setIcon(QtGui.QIcon(":open.png"))
        rsh_open_files_button.setToolTip(self.tr("Open files"))
        rsh_open_files_button.setStatusTip(self.tr("Open files"))

        rsh_make_report = QtWidgets.QPushButton()
        rsh_make_report.clicked.connect(self.rsheet_widget.make_report)
        rsh_make_report.setIcon(QtGui.QIcon(":report.png"))
        rsh_make_report.setToolTip(self.tr("Make report"))
        rsh_make_report.setStatusTip(self.tr("Make report"))

        rsh_show_button = QtWidgets.QPushButton()
        rsh_show_button.clicked.connect(self.rsheet_widget.show)
        rsh_show_button.setIcon(QtGui.QIcon(":chart.png"))
        rsh_show_button.setToolTip(self.tr("Show measurement"))
        rsh_show_button.setStatusTip(self.tr("Show measurement"))

        rsh_clear_data_button = QtWidgets.QPushButton()
        rsh_clear_data_button.clicked.connect(self.rsheet_widget.clear_data)
        rsh_clear_data_button.setIcon(QtGui.QIcon(":erase.png"))
        rsh_clear_data_button.setToolTip(self.tr("Remove all"))
        rsh_clear_data_button.setStatusTip(self.tr("Remove all"))

        buttonbox0 = QtWidgets.QDialogButtonBox()
        buttonbox0.addButton(rsh_open_files_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox0.addButton(rsh_make_report, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox0.addButton(rsh_show_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox0.addButton(rsh_clear_data_button, QtWidgets.QDialogButtonBox.ActionRole)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.rsheet_view)
        vbox.addWidget(buttonbox0)

        tab0 = QtWidgets.QWidget()
        tab0_layout = QtWidgets.QVBoxLayout(tab0)
        tab0_layout.addLayout(vbox)

        ##### ECV #####     
        self.ecv_view.setModel(self.ecv_model)
        self.ecv_model.setHorizontalHeaderLabels([self.tr('Files')])
        self.ecv_view.setRootIsDecorated(False)
        self.ecv_view.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.ecv_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.ecv_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)        

        ecv_open_files_button = QtWidgets.QPushButton()
        ecv_open_files_button.clicked.connect(self.ecv_widget.open_files) 
        ecv_open_files_button.setIcon(QtGui.QIcon(":open.png"))
        ecv_open_files_button.setToolTip(self.tr("Open files"))
        ecv_open_files_button.setStatusTip(self.tr("Open files"))

        ecv_show_button = QtWidgets.QPushButton()
        ecv_show_button.clicked.connect(self.ecv_widget.show)
        ecv_show_button.setIcon(QtGui.QIcon(":chart.png"))
        ecv_show_button.setToolTip(self.tr("Show measurement"))
        ecv_show_button.setStatusTip(self.tr("Show measurement"))

        ecv_clear_data_button = QtWidgets.QPushButton()
        ecv_clear_data_button.clicked.connect(self.ecv_widget.clear_data)
        ecv_clear_data_button.setIcon(QtGui.QIcon(":erase.png"))
        ecv_clear_data_button.setToolTip(self.tr("Remove all"))
        ecv_clear_data_button.setStatusTip(self.tr("Remove all"))

        buttonbox1 = QtWidgets.QDialogButtonBox()
        buttonbox1.addButton(ecv_open_files_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox1.addButton(ecv_show_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox1.addButton(ecv_clear_data_button, QtWidgets.QDialogButtonBox.ActionRole)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.ecv_view)
        vbox.addWidget(buttonbox1)

        tab1 = QtWidgets.QWidget()
        tab1_layout = QtWidgets.QVBoxLayout(tab1)
        tab1_layout.addLayout(vbox)

        ##### Average PL/EL #####     
        self.imageblend_view.setModel(self.imageblend_model)
        self.imageblend_model.setHorizontalHeaderLabels([self.tr('Files')])
        self.imageblend_view.setRootIsDecorated(False)
        self.imageblend_view.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.imageblend_view.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.imageblend_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)        

        ib_open_files_button = QtWidgets.QPushButton()
        ib_open_files_button.clicked.connect(self.image_blend_widget.open_files) 
        ib_open_files_button.setIcon(QtGui.QIcon(":open.png"))
        ib_open_files_button.setToolTip(self.tr("Open files"))
        ib_open_files_button.setStatusTip(self.tr("Open files"))

        ib_save_files_button = QtWidgets.QPushButton()
        ib_save_files_button.clicked.connect(self.image_blend_widget.save_files)        
        ib_save_files_button.setIcon(QtGui.QIcon(":save.png"))
        ib_save_files_button.setToolTip(self.tr("Save files"))
        ib_save_files_button.setStatusTip(self.tr("Save files"))

        #ib_report_button = QtWidgets.QPushButton()
        #ib_report_button.clicked.connect(self.image_blend_widget.make_report)
        #ib_report_button.setIcon(QtGui.QIcon(":report.png"))
        #ib_report_button.setToolTip(self.tr("Make report"))
        #ib_report_button.setStatusTip(self.tr("Make report"))
        
        ib_combine_data_button = QtWidgets.QPushButton()
        ib_combine_data_button.clicked.connect(self.image_blend_widget.blend_images)
        ib_combine_data_button.setIcon(QtGui.QIcon(":combine.png"))
        ib_combine_data_button.setToolTip(self.tr("Blend images"))
        ib_combine_data_button.setStatusTip(self.tr("Blend images"))

        ib_show_button = QtWidgets.QPushButton()
        ib_show_button.clicked.connect(self.image_blend_widget.show_image)
        ib_show_button.setIcon(QtGui.QIcon(":eye.png"))
        ib_show_button.setToolTip(self.tr("Show blend image"))
        ib_show_button.setStatusTip(self.tr("Show blend image"))

        ib_clear_data_button = QtWidgets.QPushButton()
        ib_clear_data_button.clicked.connect(self.image_blend_widget.clear_data)
        ib_clear_data_button.setIcon(QtGui.QIcon(":erase.png"))
        ib_clear_data_button.setToolTip(self.tr("Remove all images"))
        ib_clear_data_button.setStatusTip(self.tr("Remove all images"))

        buttonbox2 = QtWidgets.QDialogButtonBox()
        buttonbox2.addButton(ib_open_files_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox2.addButton(ib_save_files_button, QtWidgets.QDialogButtonBox.ActionRole)
        #buttonbox2.addButton(ib_report_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox2.addButton(ib_combine_data_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox2.addButton(ib_show_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox2.addButton(ib_clear_data_button, QtWidgets.QDialogButtonBox.ActionRole)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.imageblend_view)
        vbox.addWidget(buttonbox2)

        tab2 = QtWidgets.QWidget()
        tab2_layout = QtWidgets.QVBoxLayout(tab2)
        tab2_layout.addLayout(vbox)
        
        ##### main layout settings #####
        tabwidget = QtWidgets.QTabWidget()
        tabwidget.addTab(tab0, "Rsheet")
        tabwidget.addTab(tab1, "ECV")
        tabwidget.addTab(tab2, "PL/EL")
  
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(tabwidget)           
                                       
        self.main_frame.setLayout(vbox)

        self.setCentralWidget(self.main_frame)
        
        self.statusBar().addWidget(self.status_text,1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu(self.tr("File"))  

        tip = self.tr("Quit")        
        quit_action = QtWidgets.QAction(self.tr("Quit"), self)
        quit_action.setIcon(QtGui.QIcon(":quit.png"))
        quit_action.triggered.connect(self.close) 
        quit_action.setToolTip(tip)
        quit_action.setStatusTip(tip)
        quit_action.setShortcut('Ctrl+Q')
    
        self.file_menu.addAction(quit_action)

        self.help_menu = self.menuBar().addMenu(self.tr("Help"))

        tip = self.tr("Help information")        
        help_action = QtWidgets.QAction(self.tr("Help..."), self)
        help_action.setIcon(QtGui.QIcon(":help.png"))
        help_action.triggered.connect(self.open_help_dialog)         
        help_action.setToolTip(tip)
        help_action.setStatusTip(tip)
        help_action.setShortcut('H')

        tip = self.tr("About the application")
        about_action = QtWidgets.QAction(self.tr("About..."), self)
        about_action.setIcon(QtGui.QIcon(":info.png"))
        about_action.triggered.connect(self.on_about)
        about_action.setToolTip(tip)
        about_action.setStatusTip(tip)
        about_action.setShortcut('F1')

        self.help_menu.addAction(help_action)
        self.help_menu.addAction(about_action)