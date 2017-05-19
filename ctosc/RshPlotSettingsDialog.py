# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class RshPlotSettingsDialog(QtWidgets.QDialog):
    
    def __init__(self, parent):
        super(QtWidgets.QDialog, self).__init__(parent)
        
        self.parent = parent       
        
        self.setWindowTitle(self.tr("Color map settings"))
        vbox = QtWidgets.QVBoxLayout()

        group_area = QtWidgets.QGroupBox()
        group_area.setFlat(True)
        group_vbox = QtWidgets.QVBoxLayout()

        self.title_cb = QtWidgets.QCheckBox(self.tr("Title"))
        self.title_cb.setChecked(self.parent.title_enabled)
        group_vbox.addWidget(self.title_cb)

        self.colorbar_cb = QtWidgets.QCheckBox(self.tr("Color bar"))
        self.colorbar_cb.setChecked(self.parent.colorbar_enabled)
        group_vbox.addWidget(self.colorbar_cb)
        
        self.interpolation_cb = QtWidgets.QCheckBox(self.tr("Gaussian interpolation"))
        self.interpolation_cb.setChecked(self.parent.interpolation_enabled)
        group_vbox.addWidget(self.interpolation_cb)
                    
        self.min_sb = QtWidgets.QDoubleSpinBox()
        self.min_sb.setAccelerated(True)
        self.min_sb.setMaximum(9999)
        self.min_sb.setMinimum(0)
        self.min_sb.setDecimals(1)            
        self.min_sb.setValue(self.parent.scale_min)        
        hbox = QtWidgets.QHBoxLayout()
        description = QtWidgets.QLabel(self.tr("Scale minimum"))
        hbox.addWidget(self.min_sb)
        hbox.addWidget(description)
        hbox.addStretch(1)
        group_vbox.addLayout(hbox)

        self.max_sb = QtWidgets.QDoubleSpinBox()
        self.max_sb.setAccelerated(True)
        self.max_sb.setMaximum(9999)
        self.max_sb.setMinimum(0)
        self.max_sb.setDecimals(1)            
        self.max_sb.setValue(self.parent.scale_max)        
        hbox = QtWidgets.QHBoxLayout()
        description = QtWidgets.QLabel(self.tr("Scale maximum"))
        hbox.addWidget(self.max_sb)
        hbox.addWidget(description)
        hbox.addStretch(1)
        group_vbox.addLayout(hbox)

        self.cmap_combobox = QtWidgets.QComboBox(self)
        for i in self.parent.cmap_options:
            self.cmap_combobox.addItem(i)               
        self.cmap_combobox.setCurrentIndex(self.parent.cmap)
        hbox = QtWidgets.QHBoxLayout()
        description = QtWidgets.QLabel(self.tr("Color map"))
        hbox.addWidget(self.cmap_combobox)
        hbox.addWidget(description)
        hbox.addStretch(1)
        group_vbox.addLayout(hbox)
        
        self.default_cb = QtWidgets.QCheckBox(self.tr("Keep settings for other data sets"))
        self.default_cb.setChecked(True if self.parent.parent.plot_settings else False)
        group_vbox.addWidget(self.default_cb)        

        group_area.setLayout(group_vbox)
        vbox.addWidget(group_area)

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
        self.parent.scale_min = self.min_sb.value()
        self.parent.scale_max = self.max_sb.value()
        self.parent.cmap = self.cmap_combobox.currentIndex()
        
        if self.default_cb.isChecked():
            self.parent.parent.plot_settings = {}
            self.parent.parent.plot_settings['interpolation_enabled'] = self.interpolation_cb.isChecked()
            self.parent.parent.plot_settings['colorbar_enabled'] = self.colorbar_cb.isChecked()
            self.parent.parent.plot_settings['title_enabled'] = self.title_cb.isChecked()
            self.parent.parent.plot_settings['scale_min'] = self.min_sb.value()
            self.parent.parent.plot_settings['scale_max'] = self.max_sb.value()
            self.parent.parent.plot_settings['cmap'] = self.cmap_combobox.currentIndex()
        else:
            self.parent.parent.plot_settings = None

        self.parent.on_draw()
        self.close()