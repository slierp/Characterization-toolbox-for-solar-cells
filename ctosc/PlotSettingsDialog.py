# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class PlotSettingsDialog(QtWidgets.QDialog):
    
    def __init__(self, parent):
        super(QtWidgets.QDialog, self).__init__(parent)
        
        self.parent = parent       
        
        self.setWindowTitle(self.tr("Color map settings"))
        vbox = QtWidgets.QVBoxLayout()

        self.title_cb = QtWidgets.QCheckBox(self.tr("Title"))
        self.title_cb.setChecked(self.parent.title_enabled)
        vbox.addWidget(self.title_cb)

        self.colorbar_cb = QtWidgets.QCheckBox(self.tr("Color bar"))
        self.colorbar_cb.setChecked(self.parent.colorbar_enabled)
        vbox.addWidget(self.colorbar_cb)
        
        self.interpolation_cb = QtWidgets.QCheckBox(self.tr("Interpolation"))
        self.interpolation_cb.setChecked(self.parent.interpolation_enabled)
        vbox.addWidget(self.interpolation_cb)
                    
        #self.scatter_sb = QtWidgets.QDoubleSpinBox()
        #self.scatter_sb.setAccelerated(True)
        #self.scatter_sb.setMaximum(0.5)
        #self.scatter_sb.setMinimum(0)
        #self.scatter_sb.setSingleStep(0.01)
        #self.scatter_sb.setDecimals(2)            
        #self.scatter_sb.setValue(self.parent.scatter_selection)
        
        #hbox = QtWidgets.QHBoxLayout()
        #description = QtWidgets.QLabel(self.tr("Scatter amount"))
        #hbox.addWidget(self.scatter_sb)
        #hbox.addWidget(description)
        #hbox.addStretch(1)
        #group_vbox.addLayout(hbox)

        ### Buttonbox for ok ###
        hbox = QtWidgets.QHBoxLayout()
        buttonbox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.read)
        buttonbox.rejected.connect(self.reject)
        hbox.addStretch(1) 
        hbox.addWidget(buttonbox)
        hbox.addStretch(1)
        hbox.setContentsMargins(0,0,0,4)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setMinimumWidth(800)        
        
    def read(self):
        self.parent.title_enabled = self.title_cb.isChecked()
        self.parent.colorbar_enabled = self.colorbar_cb.isChecked()        
        self.parent.interpolation_enabled = self.interpolation_cb.isChecked()

        self.parent.on_draw()
        self.close()