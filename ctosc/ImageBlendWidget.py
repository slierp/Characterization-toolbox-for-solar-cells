# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
from PIL import Image
import os, ntpath

class ImageBlendWidget(QtCore.QObject):
    def __init__(self, parent=None):
        super(ImageBlendWidget, self).__init__(parent)
        
        self.parent = parent
        self.view = self.parent.imageblend_view        
        self.model = self.parent.imageblend_model
        self.statusbar = self.parent.statusBar()

        self.prev_dir_path = ""
        self.images = []
        self.blend_image = None
        
    def open_files(self):   

        if self.blend_image:
            msg = self.tr("Please remove existing blend image.")
            QtWidgets.QMessageBox.about(self, self.tr("Warning"), msg)        
            return
        
        fileNames = QtWidgets.QFileDialog.getOpenFileNames(self.parent,self.tr("Load files"), self.prev_dir_path, "PNG Files (*.png)")
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
            self.model.appendRow(item)                        
            
        if non_ascii_warning:
            msg = self.tr("Filenames with non-ASCII characters were found.\n\nThe application currently only supports ASCII filenames.")
            QtWidgets.QMessageBox.about(self, self.tr("Warning"), msg)            
                              
        if len(self.images):
            self.statusbar.showMessage(self.tr("Ready"),3000)
        else:
            self.statusbar.showMessage(self.tr("No files loaded"),3000)

    def save_files(self):
        
        if not self.blend_image:
            self.statusbar.showMessage(self.tr("Please make blended image."),3000)
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
        
        self.statusbar.showMessage(self.tr("Files saved"),3000) 
                   
    def blend_images(self):

        if len(self.images) > 1:
            self.statusbar.showMessage(self.tr("Blending images..."),3000)
        else:
            self.statusbar.showMessage(self.tr("Please load data files"),3000)
            return     

        self.blend_image=Image.open(self.images[0])
        for i in range(1,len(self.images)):
            image = Image.open(self.images[i])
            self.blend_image = Image.blend(self.blend_image, image, 1.0/(i+1))

        # Clearing associated data sets
        self.images = [] 
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Images'])

        # Update list view
        item = QtGui.QStandardItem('Blended image')
        font = item.font()
        item.setFont(font)
        self.model.appendRow(item) 
                
        self.statusbar.showMessage(self.tr("Ready"),3000)
                                    
    def show_image(self):
        
        if not self.blend_image:
            self.statusbar.showMessage(self.tr("Please blend image files"),3000)
            return

        self.blend_image.show()

        self.statusbar.showMessage(self.tr("Ready"),3000)            
        
    def clear_data(self):        
        self.blend_image = None
        self.images = [] 
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Files'])
        self.statusbar.showMessage(self.tr("All data has been cleared"),3000)        