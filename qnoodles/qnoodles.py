#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
    A graphical user interface (PySide) on top of the FireWorks workflow engine.

    @author: Johan Hidding
    @organisation: Netherlands eScience Center (NLeSC)
    @contact: j.hidding@esciencecenter.nl
"""

import sys, os
from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from .nodebox import NodeBox
#from .sourceview import SourceView
        
class NodeView(QtGui.QGraphicsView):
    def __init__(self, scene):
        super(NodeView, self).__init__(scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.show()

class NodeScene(QtGui.QGraphicsScene):
    def __init__(self, data_model):
        super(NodeScene, self).__init__()            
        self.nodes = [NodeBox(n, self) for i, n in data_model.all_nodes()]
                
    def noodletPressed(self, i, s):
        pass
        #print("{0}-{1} pressed".format(i, s))
        
    def noodletReleased(self, i, s):
        pass
        #print("{0}-{1} released".format(i, s))

class NoodlesWindow(QtGui.QMainWindow):    
    def __init__(self, data_model):
        super(NoodlesWindow, self).__init__()
        
        self.data_model = data_model
        self.initUI()
        
    def initUI(self):
        style = str(open("static/qt-style.css", "r").read())
        self.nodeScene = NodeScene(self.data_model)
        self.nodeView = NodeView(self.nodeScene)

        self.nodeView.setStyleSheet(style)
        
        #self.sourceView = SourceView()
        
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(self.nodeView, "Graph view")
        #self.tabWidget.addTab(self.sourceView, "Source view")
        self.setCentralWidget(self.tabWidget)
        
        self.setGeometry(300, 300, 1024, 600)
        self.setWindowTitle('Noodles')    
        self.setWindowIcon(QtGui.QIcon('static/noodles-icon.png'))
        
        self.statusBar().showMessage('Ready')

        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme('application-exit'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.nodeRepository = QtGui.QToolBox()
        self.flowNodeList = QtGui.QListWidget()
        self.compositeNodeList = QtGui.QListWidget()
        self.libraryNodeList = QtGui.QListWidget()
        self.nodeRepository.addItem(self.flowNodeList, "flow control")
        self.nodeRepository.addItem(self.libraryNodeList, "library nodes")
        self.nodeRepository.addItem(self.compositeNodeList, "composite nodes")
        dockWidget = QtGui.QDockWidget("Noodles node repository")
        dockWidget.setWidget(self.nodeRepository)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

        self.show()

    def closeEvent(self, event):
#        reply = QtGui.QMessageBox.question(self, 'Message',
#            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
#            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

#        if reply == QtGui.QMessageBox.Yes:
#            event.accept()
#        else:
#            event.ignore()

        #self.sourceView.backend.stop()
                

def main(model):
    app = QtGui.QApplication(sys.argv)
    
#    Qode.backend.CodeCompletionWorker.providers.append(
#        backend.DocumentWordsProvider())
#    Qode.backend.serve_forever()
    
    win = NoodlesWindow(model)
    sys.exit(app.exec_())



