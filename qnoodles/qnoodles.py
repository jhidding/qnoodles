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

from .sourceview import SourceView


class MyFrame(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
    def _alt_paintEvent(self, event):
        pt = QtGui.QPainter(self)
        pt.setRenderHints(pt.Antialiasing)
        w, h = self.size().toTuple()
        
        path = QtGui.QPainterPath()
        brush = QtGui.QBrush(Qt.gray)
        pen = QtGui.QPen(QtGui.QBrush(Qt.black), 3)
        path.addRoundedRect(1, 1, w-2, h-2, 16, 16)
        pt.fillPath(path, brush)
        pt.strokePath(path, pen)
        
    def paintEvent(self, event):
        pt = QtGui.QPainter(self)
        pt.setRenderHints(pt.Antialiasing)
        w, h = self.size().toTuple()
        
        path = QtGui.QPainterPath()
        brush = QtGui.QBrush(Qt.gray)
        pen = QtGui.QPen(QtGui.QBrush(Qt.black), 1.0)
        path.addRoundedRect(1, 1, w-2, h-2, 8, 8)
        pt.fillPath(path, brush)
        #pt.strokePath(path, pen)

class Noodlet(QtGui.QGraphicsWidget):
    def __init__(self, x, y):
        super(Noodlet, self).__init__()
        
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        
        self.setPos(x, y)
        self.setScale(0.6)

        self.outer_path = QtGui.QPainterPath()
        self.outer_path.addEllipse(-16, -16, 32, 32)
        self.inner_path = QtGui.QPainterPath()
        self.inner_path.addEllipse(-9, -9, 18, 18)
        
        self.bg_color = QtGui.QColor(60,60,200)
        self.inner_line_color = Qt.white
        self.outer_line_color = Qt.black
        
    def boundingRect(self):
        #return QtCore.QRectF(-16, -16, 16, 16)
        return QtCore.QRectF(-16, -16, 48, 48)
        
    def paint(self, painter, option, widget):
        painter.setRenderHints(painter.Antialiasing)
        painter.fillPath(self.inner_path, QtGui.QBrush(self.bg_color))
        painter.strokePath(self.inner_path, QtGui.QPen(QtGui.QBrush(self.inner_line_color), 1))
        painter.strokePath(self.outer_path, QtGui.QPen(QtGui.QBrush(self.outer_line_color), 1))
        
    def shape(self):
        return self.outer_path

    def mousePressEvent(self, event):
        self.dragging = True
        #self.drag_pos = (event.x(), event.y())
        print("draging... ", end='', flush=True)
        
    def mouseMoveEvent(self, event):
        print(".", end='', flush=True)
#        x = (event.x() - self.drag_pos[0])
#        y = (event.y() - self.drag_pos[1])
        
#        print("({0}, {1}) ".format(x,y), end='', flush=True)
            
    def mouseReleaseEvent(self, event):
        self.dragging = False
        print(" done")
        
    def hoverEnterEvent(self, event):
        self.bg_color = QtGui.QColor(200,60,60)
        self.update()
        #print("h-e ", end='', flush=True)
    
    def hoverLeaveEvent(self, event):
        self.bg_color = QtGui.QColor(60,60,200)
        self.update()
        #print("h-l ", end='', flush=True)

    
class NodeBox(MyFrame):
    def __init__(self, name, scene, x = 0, y = 0):
        super(NodeBox, self).__init__()
        self.scene = scene
        
        style = str(open("static/qt-style.css", "r").read())
        #self.setFrameStyle(self.StyledPanel | self.Plain)
        self.box = QtGui.QVBoxLayout()
        self.setLayout(self.box)
        
        self.title = QtGui.QLabel(name, self)
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.box.addWidget(self.title)
        
        self.items = [QtGui.QPushButton("Blah {0}".format(i), self) for i in range(3)]
        for i in self.items:
            self.box.addWidget(i)

        self.proxy = scene.addWidget(self)
        self.proxy.setZValue(0)
        self.move(x, y)
        
        #self.group = QtGui.QGraphicsItemGroup(self.proxy, scene)
        #self.group.addToGroup(self.proxy)
        
        self.noodlets = [Noodlet(*self.output_item_pos(i)) for i in self.items] \
                      + [Noodlet(*self.input_item_pos(i)) for i in self.items]
                      
        for n in self.noodlets:
            scene.addItem(n)
            n.setZValue(10)
        #    self.group.addToGroup(n)

        #scene.addItem(self.group)
        
        #self.setProperty('frameClass', 'blue')
        self.setStyleSheet(style)
        self.dragging = False
        self.show()
        
    def input_item_pos(self, item):
        x = self.x()
        y = item.y() + item.height()/2 + self.y()
        return x, y

    def output_item_pos(self, item):
        x = self.x() + self.width() - 2
        y = item.y() + item.height()/2 + self.y()
        return x, y
        
    #class manual_drag:            
    def mousePressEvent(self, event):
        self.group = QtGui.QGraphicsItemGroup(self.proxy, self.scene)
        for n in self.noodlets:
            n.setZValue(20)
            self.group.addToGroup(n)
        self.proxy.setZValue(19)
            
        self.dragging = True
        self.drag_pos = (event.x(), event.y())
        #print("draging... ({0}, {1}) ".format(*self.drag_pos), end='', flush=True)
        
    def mouseMoveEvent(self, event):
        if self.dragging:
            x = self.x(); y = self.y()
            #self.scene.update(x-10, y-10, self.width() + 20, self.height()+20)
            #for n in self.noodlets:
                #n.update()
            x += (event.x() - self.drag_pos[0])
            y += (event.y() - self.drag_pos[1])
            self.move(x, y)
            
    def mouseReleaseEvent(self, event):
        self.scene.destroyItemGroup(self.group)
        for n in self.noodlets:
            n.setZValue(10)
        self.proxy.setZValue(0)
        self.dragging = False
        #rint("drop")
        
class NodeView(QtGui.QGraphicsView):
    def __init__(self, scene):
        super(NodeView, self).__init__(scene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.show()

class NodeScene(QtGui.QGraphicsScene):
    def __init__(self):
        super(NodeScene, self).__init__()
        self.node1 = NodeBox("jippee", self, 0, 0)
        self.node2 = NodeBox("wheee", self, 300, 0)
        self.node3 = NodeBox("gogogo", self, 600, 150)        

class NoodlesWindow(QtGui.QMainWindow):    
    def __init__(self):
        super(NoodlesWindow, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        style = str(open("static/qt-style.css", "r").read())
        self.nodeScene = NodeScene()
        self.nodeView = NodeView(self.nodeScene)

        self.nodeView.setStyleSheet(style)
        
        self.sourceView = SourceView()
        
        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.addTab(self.nodeView, "Graph view")
        self.tabWidget.addTab(self.sourceView, "Source view")
        self.setCentralWidget(self.tabWidget)
        
        self.setGeometry(300, 300, 1024, 600)
        self.setWindowTitle('Noodles')    
        self.setWindowIcon(QtGui.QIcon('../static/noodles-icon.png'))
        
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

        self.sourceView.backend.stop()
                

def main():
    app = QtGui.QApplication(sys.argv)
    
#    Qode.backend.CodeCompletionWorker.providers.append(
#        backend.DocumentWordsProvider())
#    Qode.backend.serve_forever()
    
    win = NoodlesWindow()
    sys.exit(app.exec_())



