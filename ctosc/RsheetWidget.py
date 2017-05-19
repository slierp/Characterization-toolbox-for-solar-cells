# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, QtGui
import ntpath
import pandas as pd
from RsheetPlot import RsheetPlot

class RsheetWidget(QtCore.QObject):
    def __init__(self, parent=None):
        super(RsheetWidget, self).__init__(parent)
        
        self.parent = parent
        self.view = self.parent.rsheet_view        
        self.model = self.parent.rsheet_model
        self.statusbar = self.parent.statusBar()
        self.data = []
        self.wid = None
        self.prev_dir_path = ""
        
    def open_files(self):
        
        fileNames = QtWidgets.QFileDialog.getOpenFileNames(self.parent,self.tr("Load files"), self.prev_dir_path, "TXT Files (*.txt)")
        fileNames = fileNames[0]
        
        if (not fileNames):
            return          
        
        non_ascii_warning = False
        read_warning = False

        for filename in fileNames:

            # Check for non-ASCII filenames, give warning and skip loading such files
            try:
                filename.encode('ascii')
            except:
                non_ascii_warning = True
                continue
        
            # Set working directory so that user can remain where they are
            self.prev_dir_path = ntpath.dirname(filename)
            
            try:
                self.data.append(pd.read_csv(filename, skiprows=18, sep="\t", header=None, error_bad_lines=False))
            except:
                read_warning = True
                continue
                
            self.data[-1].columns = ["x", "y", "Rsh","Rsh_tmp"]
            self.data[-1][self.data[-1] < 0] = None # set negative values to NaN
            self.data[-1]['Rsh'] = self.data[-1][['Rsh','Rsh_tmp']].mean(axis=1) # average positive and negative measurement
            del self.data[-1]['Rsh_tmp']
            self.data[-1] = self.data[-1].dropna()
            
            ### add list view item ###
            str_a = ntpath.splitext(ntpath.basename(filename))[0]
            str_a = str_a[0:100] # set name limited to 99 characters
            self.data[-1].index.name = str_a
            item = QtGui.QStandardItem(str_a)
            self.model.appendRow(item)

        warning_string = ""

        if read_warning:
            warning_string += self.tr("[Error] Some files could not be read properly. ") 
            
        if non_ascii_warning:
            warning_string += self.tr("[Error] Filenames with non-ASCII characters were found. The application currently only supports ASCII filenames.")
        
        if read_warning or non_ascii_warning:
            QtWidgets.QMessageBox.about(self.parent, self.tr("Warning"), warning_string)            
                              
        if len(self.data):
            self.statusbar.showMessage(self.tr("Ready"),3000)
        else:
            self.statusbar.showMessage(self.tr("No files loaded"),3000)

    def make_report(self):
        
        if len(self.data):
            self.reportname = QtWidgets.QFileDialog.getSaveFileName(self.parent,self.tr("Save file"), self.prev_dir_path, "Excel Files (*.xlsx)")
            self.reportname = self.reportname[0]
            
            if not self.reportname:
                return

            if self.reportname:
                self.statusbar.showMessage(self.tr("Making an Excel report..."),3000)
            else:
                return
        else:
            self.statusbar.showMessage(self.tr("Please load data files"),3000)
            return

        try:
            self.reportname.encode('ascii')
        except:
            msg = self.tr("Filenames with non-ASCII characters were found.\n\nThe application currently only supports ASCII filenames.")
            QtWidgets.QMessageBox.about(self, self.tr("Warning"), msg) 
            self.reportname = None
            return

        rp_summ = pd.DataFrame(columns=['Name','Average','Std.dev.','Min','Max'])                                       
                                                   
        for i in range(len(self.data)):
            tmp_list = []
            tmp_list.append(self.data[i].index.name)
            tmp_list.append(self.data[i].ix[:,2].mean())
            tmp_list.append(self.data[i].ix[:,2].std())
            tmp_list.append(self.data[i].ix[:,2].min())
            tmp_list.append(self.data[i].ix[:,2].max())
            rp_summ.loc[i] = tmp_list
        
        rp_summ = rp_summ.round(3)
        writer = pd.ExcelWriter(self.reportname, engine='xlsxwriter')
        rp_summ.to_excel(writer,self.tr('Summary'))                
        writer.save()                 
        
        self.statusbar.showMessage(self.tr("File saved"),3000)
                                    
    def show(self):
        
        if (not len(self.view.selectedIndexes())):
            # if nothing selected
            self.statusbar.showMessage(self.tr("Please select position"),3000)
            return
        
        if (not len(self.data)):
            self.statusbar.showMessage(self.tr("Please load data files"),3000)
            return      

        self.statusbar.showMessage(self.tr("Creating plot window..."),3000)

        if (self.wid):
            if (self.wid.isWindow()):
                # close previous instances of child windows to save system memory                
                self.wid.close()                

        self.wid = RsheetPlot(self)

        self.wid.show()

        self.statusbar.showMessage(self.tr("Ready"),3000)            
        
    def clear_data(self):
        self.data = []        
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Files'])
        self.statusbar.showMessage(self.tr("All data has been cleared"),3000)        