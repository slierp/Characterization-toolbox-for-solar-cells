# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets

help_text = """
<html>
<head><head/>
<body>
<h1>CTOSC</h1>

<p>
The image blend functionality is a simple tool for make an average image out of a series of images. 
Such blending is useful for example when comparing large series of photolumiscence measurements on silicon solar cells.
</p>
<p>
The required image format is PNG (Portable Network Graphics). To convert images to the PNG format it is recommended
to use the batch conversion tool in the IrfanView program (on Windows). 
</p>


</body>
</html>
"""

class HelpDialog(QtWidgets.QDialog):
    # Generates help document browser    
    
    def __init__(self, parent):
        super(QtWidgets.QDialog, self).__init__(parent)
        
        self.parent = parent       
        
        self.setWindowTitle(self.tr("Help"))
        vbox = QtWidgets.QVBoxLayout()

        browser = QtWidgets.QTextBrowser()
        browser.insertHtml(help_text)
        browser.moveCursor(QtGui.QTextCursor.Start)

        vbox.addWidget(browser)

        ### Buttonbox for ok ###
        hbox = QtWidgets.QHBoxLayout()
        buttonbox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        buttonbox.accepted.connect(self.close)
        hbox.addStretch(1) 
        hbox.addWidget(buttonbox)
        hbox.addStretch(1)
        hbox.setContentsMargins(0,0,0,4)                
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setMinimumHeight(576)
        self.setMinimumWidth(1024)