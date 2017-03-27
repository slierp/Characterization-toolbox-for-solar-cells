# -*- coding: utf-8 -*-
import os, ntpath
from HelpDialog import HelpDialog
from PyQt5 import QtGui, QtWidgets
from PIL import Image

class MainGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainGui, self).__init__(parent)
        self.setWindowTitle(self.tr("Image blend"))

        ### Set initial geometry and center the window on the screen ###
        self.resize(1024, 576)
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft()) 

        ### Set default font size ###
        self.setStyleSheet('font-size: 12pt;')  

        self.series_list_model = QtGui.QStandardItemModel()
        
        self.images = []
        self.blend_image = None

        self.status_text = QtWidgets.QLabel("")       
        
        self.prev_dir_path = ""
        self.wid = None
        
        self.create_menu()
        self.create_main_frame()

    def load_file(self, filename=None):   

        if self.blend_image:
            msg = self.tr("Please remove existing blend image.")
            QtWidgets.QMessageBox.about(self, self.tr("Warning"), msg)        
            return
        
        fileNames = QtWidgets.QFileDialog.getOpenFileNames(self,self.tr("Load files"), self.prev_dir_path, "PNG Files (*.png)")
        fileNames = fileNames[0]
        
        if (not fileNames):
            return          
        
        non_ascii_warning = False

        for filename in fileNames:

            # Check for non-ASCII filenames, give warning and skip loading such files
            try:
                filename.encode('ascii')
            except:
                non_ascii_warning = True
                continue
        
            # Set working directory so that user can remain where they are
            self.prev_dir_path = ntpath.dirname(filename)
            
            self.images.append(filename)
            
            ### add list view item ###
            str_a = ntpath.splitext(ntpath.basename(filename))[0]
            str_a = str_a[0:39] # set name limited to 40 characters
            item = QtGui.QStandardItem(str_a)
            font = item.font()
            item.setFont(font)
            self.series_list_model.appendRow(item)                        
            
        if non_ascii_warning:
            msg = self.tr("Filenames with non-ASCII characters were found.\n\nThe application currently only supports ASCII filenames.")
            QtWidgets.QMessageBox.about(self, self.tr("Warning"), msg)            
                              
        if len(self.images):
            self.statusBar().showMessage(self.tr("Ready"))
        else:
            self.statusBar().showMessage(self.tr("Please load image files"))

    def save_files(self):
        
        if not self.blend_image:
            self.statusBar().showMessage(self.tr("Please make blended image."))
            return

        dest_dir = QtWidgets.QFileDialog.getExistingDirectory(None, self.tr('Open directory'), self.prev_dir_path, QtWidgets.QFileDialog.ShowDirsOnly)
        
        if not dest_dir:
            return

        self.prev_dir_path = dest_dir
            
        yes_to_all = False
        
        filename = 'Blended image.png'
        check_overwrite = False
        save_path = ""
        
        # check if file exists and then ask if overwrite is oke
        if os.name == 'nt': # if windows
            save_path = dest_dir + '\\' + filename
            if os.path.isfile(save_path):
                check_overwrite = True
        else: # if not windows
            save_path = dest_dir + '\/' + filename
            if os.path.isfile(save_path):
                check_overwrite = True

        if check_overwrite and not yes_to_all:
            reply = QtWidgets.QMessageBox.question(self, self.tr("Message"), "Overwrite \'" + filename + "\'?", QtWidgets.QMessageBox.YesToAll | QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:                    
                save_path = QtWidgets.QFileDialog.getSaveFileName(self,self.tr("Save file"), dest_dir, "PNG File (*.png)")
                
                if not save_path:
                    return

            if reply == QtWidgets.QMessageBox.YesToAll:
                yes_to_all = True
                
            if reply == QtWidgets.QMessageBox.Cancel:
                return
                       
        self.blend_image.save(save_path)
        
        self.statusBar().showMessage(self.tr("Files saved")) 
                   
    def blend_images(self):

        if len(self.images) > 1:
            self.statusBar().showMessage(self.tr("Blending images..."))
        else:
            self.statusBar().showMessage(self.tr("Please load data files"))
            return     

        self.blend_image=Image.open(self.images[0])
        for i in range(1,len(self.images)):
            image = Image.open(self.images[i])
            self.blend_image = Image.blend(self.blend_image, image, 1.0/(i+1))

        # Clearing associated data sets
        self.images = [] 
        self.series_list_model.clear()
        self.series_list_model.setHorizontalHeaderLabels(['Images'])

        # Update list view
        item = QtGui.QStandardItem('Blended image')
        font = item.font()
        item.setFont(font)
        self.series_list_model.appendRow(item) 
                
        self.statusBar().showMessage(self.tr("Ready"))
                                    
    def show_image(self):
        
        if not self.blend_image:
            self.statusBar().showMessage(self.tr("Please blend image files"))
            return

        self.blend_image.show()

        self.statusBar().showMessage(self.tr("Ready"))            
        
    def clear_data(self):        
        self.blend_image = None
        self.images = [] 
        self.series_list_model.clear()
        self.series_list_model.setHorizontalHeaderLabels(['Images'])
        self.statusBar().showMessage(self.tr("All image data has been cleared"))

    def open_help_dialog(self):
        help_dialog = HelpDialog(self)
        help_dialog.setModal(True)
        help_dialog.show()

    def on_about(self):
        msg = self.tr("Image blend\nAuthor: Ronald Naber\nLicense: Public domain")
        QtWidgets.QMessageBox.about(self, self.tr("About the application"), msg)
    
    def create_main_frame(self):
        self.setWindowTitle(self.tr("Image blend")) # do this again so that translator can catch it
        self.main_frame = QtWidgets.QWidget()        

        ##### left vbox #####     
        self.series_list_view = QtWidgets.QTreeView()
        self.series_list_view.setModel(self.series_list_model)
        self.series_list_model.setHorizontalHeaderLabels([self.tr('Images')])
        self.series_list_view.setRootIsDecorated(False)
        self.series_list_view.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.series_list_view.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.series_list_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)        

        show_button = QtWidgets.QPushButton()
        show_button.clicked.connect(self.show_image)
        show_button.setIcon(QtGui.QIcon(":eye.png"))
        show_button.setToolTip(self.tr("Show blend image"))
        show_button.setStatusTip(self.tr("Show blend image"))

        open_files_button = QtWidgets.QPushButton()
        open_files_button.clicked.connect(self.load_file)
        open_files_button.setIcon(QtGui.QIcon(":open.png"))
        open_files_button.setToolTip(self.tr("Load files"))
        open_files_button.setStatusTip(self.tr("Load files"))

        save_files_button = QtWidgets.QPushButton()
        save_files_button.clicked.connect(self.save_files)        
        save_files_button.setIcon(QtGui.QIcon(":save.png"))
        save_files_button.setToolTip(self.tr("Save files"))
        save_files_button.setStatusTip(self.tr("Save files"))
        
        combine_data_button = QtWidgets.QPushButton()
        combine_data_button.clicked.connect(self.blend_images)
        combine_data_button.setIcon(QtGui.QIcon(":combine.png"))
        combine_data_button.setToolTip(self.tr("Blend images"))
        combine_data_button.setStatusTip(self.tr("Blend images"))

        clear_data_button = QtWidgets.QPushButton()
        clear_data_button.clicked.connect(self.clear_data)
        clear_data_button.setIcon(QtGui.QIcon(":erase.png"))
        clear_data_button.setToolTip(self.tr("Remove all images"))
        clear_data_button.setStatusTip(self.tr("Remove all images"))

        buttonbox0 = QtWidgets.QDialogButtonBox()
        buttonbox0.addButton(show_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox0.addButton(open_files_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox0.addButton(save_files_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox0.addButton(combine_data_button, QtWidgets.QDialogButtonBox.ActionRole)
        buttonbox0.addButton(clear_data_button, QtWidgets.QDialogButtonBox.ActionRole)

        left_vbox = QtWidgets.QVBoxLayout()
        left_vbox.addWidget(self.series_list_view)
        left_vbox.addWidget(buttonbox0)

        ##### main layout settings #####
        top_hbox = QtWidgets.QHBoxLayout()
        top_hbox.addLayout(left_vbox)
  
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(top_hbox)           
                                       
        self.main_frame.setLayout(vbox)

        self.setCentralWidget(self.main_frame)
        
        self.statusBar().addWidget(self.status_text,1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu(self.tr("File"))

        tip = self.tr("Open file")        
        load_action = QtWidgets.QAction(self.tr("Open..."), self)
        load_action.setIcon(QtGui.QIcon(":open.png"))
        load_action.triggered.connect(self.load_file) 
        load_action.setToolTip(tip)
        load_action.setStatusTip(tip)
        load_action.setShortcut('Ctrl+O')    

        tip = self.tr("Quit")        
        quit_action = QtWidgets.QAction(self.tr("Quit"), self)
        quit_action.setIcon(QtGui.QIcon(":quit.png"))
        quit_action.triggered.connect(self.close) 
        quit_action.setToolTip(tip)
        quit_action.setStatusTip(tip)
        quit_action.setShortcut('Ctrl+Q')

        self.file_menu.addAction(load_action)       
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