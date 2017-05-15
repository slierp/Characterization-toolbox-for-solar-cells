# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
import os, ntpath
import pandas as pd

class RsheetWidget(QtCore.QObject):
    def __init__(self, parent=None):
        super(RsheetWidget, self).__init__(parent)
        
        self.parent = parent
        self.view = self.parent.rsheet_view        
        self.model = self.parent.rsheet_model
        self.statusbar = self.parent.statusBar()
        self.data = []

        self.prev_dir_path = ""
        
    def open_files(self):
        
        fileNames = QtWidgets.QFileDialog.getOpenFileNames(self.parent,self.tr("Load files"), self.prev_dir_path, "TXT Files (*.txt)")
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
            
            self.data.append(pd.read_csv(filename, skiprows=18, sep="\t", header=None, error_bad_lines=False))
            self.data[-1].columns = ["x", "y", "pos", "neg"]
            
            ### add list view item ###
            str_a = ntpath.splitext(ntpath.basename(filename))[0]
            str_a = str_a[0:100] # set name limited to 99 characters
            self.data[-1].index.name = str_a
            item = QtGui.QStandardItem(str_a)
            self.model.appendRow(item)
            
        if non_ascii_warning:
            msg = self.tr("Filenames with non-ASCII characters were found.\n\nThe application currently only supports ASCII filenames.")
            QtWidgets.QMessageBox.about(self, self.tr("Warning"), msg)            
                              
        if len(self.data):
            self.statusbar.showMessage(self.tr("Ready"),3000)
        else:
            self.statusbar.showMessage(self.tr("No files loaded"),3000)

    def make_report(self):
        
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