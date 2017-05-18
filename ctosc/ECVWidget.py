# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
import ntpath
import pandas as pd
from ECVPlot import ECVPlot

class ECVWidget(QtCore.QObject):
    def __init__(self, parent=None):
        super(ECVWidget, self).__init__(parent)
        
        self.parent = parent
        self.view = self.parent.ecv_view        
        self.model = self.parent.ecv_model
        self.statusbar = self.parent.statusBar()
        self.data = []
        self.wid = None

        self.prev_dir_path = ""
        
    def open_files(self):   

        fileNames = QtWidgets.QFileDialog.getOpenFileNames(self.parent,self.tr("Load files"), self.prev_dir_path, "CSV Files (*.csv)")
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
            
            self.data.append(pd.read_csv(filename, skiprows=29, header=None, error_bad_lines=False, encoding='utf-8',usecols=[0,5,7]))

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
                                    
    def show(self):
        
        if (not len(self.data)):
            self.statusbar.showMessage(self.tr("Please load data files"),3000)
            return      

        self.statusbar.showMessage(self.tr("Creating plot window..."),3000)

        if (self.wid):
            if (self.wid.isWindow()):
                # close previous instances of child windows to save system memory                
                self.wid.close()                

        self.wid = ECVPlot(self)

        self.wid.show()

        self.statusbar.showMessage(self.tr("Ready"),3000)           
        
    def clear_data(self):
        self.data = []         
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Files'])
        self.statusbar.showMessage(self.tr("All data has been cleared"),3000)        