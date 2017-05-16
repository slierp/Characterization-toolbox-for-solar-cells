# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
import ntpath

class ECVWidget(QtCore.QObject):
    def __init__(self, parent=None):
        super(ECVWidget, self).__init__(parent)
        
        self.parent = parent
        self.view = self.parent.ecv_view        
        self.model = self.parent.ecv_model
        self.statusbar = self.parent.statusBar()

        self.prev_dir_path = ""
        
    def open_files(self):   

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
            self.statusbar.showMessage(self.tr("Please load image files"),3000)
                                    
    def show(self):
        
        return
        
        if not self.blend_image:
            self.statusbar.showMessage(self.tr("Please blend image files"),3000)
            return

        self.blend_image.show()

        self.statusbar.showMessage(self.tr("Ready"),3000)            
        
    def clear_data(self):         
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Files'])
        self.statusbar.showMessage(self.tr("All data has been cleared"),3000)        