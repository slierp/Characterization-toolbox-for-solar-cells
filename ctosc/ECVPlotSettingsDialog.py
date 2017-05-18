# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

class ECVPlotSettingsDialog(QtWidgets.QDialog):
    
    def __init__(self, parent):
        super(QtWidgets.QDialog, self).__init__(parent)
        
        self.parent = parent       
        
        self.setWindowTitle(self.tr("ECV plot settings"))
        vbox = QtWidgets.QVBoxLayout()

        group_area = QtWidgets.QGroupBox()
        group_area.setFlat(True)
        group_vbox = QtWidgets.QVBoxLayout()

        self.grid_cb = QtWidgets.QCheckBox(self.tr("Grid"))
        self.grid_cb.setChecked(self.parent.grid_enabled)
        group_vbox.addWidget(self.grid_cb)

        self.legend_cb = QtWidgets.QCheckBox(self.tr("Legend"))
        self.legend_cb.setChecked(self.parent.legend_enabled)
        group_vbox.addWidget(self.legend_cb)
        
        self.dots_cb = QtWidgets.QCheckBox(self.tr("Dot markers"))
        self.dots_cb.setChecked(self.parent.dots_enabled)
        group_vbox.addWidget(self.dots_cb)

        self.dots_sb = QtWidgets.QSpinBox()
        self.dots_sb.setAccelerated(True)
        self.dots_sb.setMaximum(99)
        self.dots_sb.setMinimum(0)        
        self.dots_sb.setValue(self.parent.dotsize)        
        hbox = QtWidgets.QHBoxLayout()
        description = QtWidgets.QLabel(self.tr("Dot marker size"))
        hbox.addWidget(self.dots_sb)
        hbox.addWidget(description)
        hbox.addStretch(1)
        group_vbox.addLayout(hbox)

        self.lines_cb = QtWidgets.QCheckBox(self.tr("Lines"))
        self.lines_cb.setChecked(self.parent.lines_enabled)
        group_vbox.addWidget(self.lines_cb)

        self.lines_sb = QtWidgets.QSpinBox()
        self.lines_sb.setAccelerated(True)
        self.lines_sb.setMaximum(99)
        self.lines_sb.setMinimum(0)        
        self.lines_sb.setValue(self.parent.linewidth)        
        hbox = QtWidgets.QHBoxLayout()
        description = QtWidgets.QLabel(self.tr("Linewidth"))
        hbox.addWidget(self.lines_sb)
        hbox.addWidget(description)
        hbox.addStretch(1)
        group_vbox.addLayout(hbox)

        self.ntype_cb = QtWidgets.QCheckBox(self.tr("Show only n-type doping"))
        self.ntype_cb.setChecked(self.parent.show_only_ndoping)
        group_vbox.addWidget(self.ntype_cb)

        self.ptype_cb = QtWidgets.QCheckBox(self.tr("Show only p-type doping"))
        self.ptype_cb.setChecked(self.parent.show_only_pdoping)
        group_vbox.addWidget(self.ptype_cb)

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
        self.parent.grid_enabled = self.grid_cb.isChecked()
        self.parent.legend_enabled = self.legend_cb.isChecked()        
        self.parent.dots_enabled = self.dots_cb.isChecked()
        self.parent.dotsize = self.dots_sb.value()
        self.parent.lines_enabled = self.lines_cb.isChecked()
        self.parent.linewidth = self.lines_sb.value()
        self.parent.show_only_ndoping = self.ntype_cb.isChecked()
        self.parent.show_only_pdoping = self.ptype_cb.isChecked()        

        self.parent.on_draw()
        self.close()