from PySide import QtGui, QtCore
from PySide.QtCore import Qt

import random

class NoodletSignal(QtCore.QObject):
    pressed  = QtCore.Signal((int,str))
    released = QtCore.Signal((int,str))

class Noodlet(QtGui.QGraphicsWidget):    
    def __init__(self, x, y):
        super(Noodlet, self).__init__()
        self.signal = NoodletSignal()
        
        self.noodlet = (random.randint(0, 65536), "dummy")
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        
        self.setPos(x, y)
        self.setScale(0.6)

        self.outer_path = QtGui.QPainterPath()
        self.outer_path.addEllipse(-16, -16, 32, 32)
        self.inner_path = QtGui.QPainterPath()
        self.inner_path.addEllipse(-9, -9, 18, 18)
        
        self.bg_color = QtGui.QColor(90,90,200)
        self.inner_line_color = Qt.white
        self.outer_line_color = Qt.black        
        
    def boundingRect(self):
        return QtCore.QRectF(-16, -16, 48, 48)
        
    def paint(self, painter, option, widget):
        painter.setRenderHints(painter.Antialiasing)
        painter.fillPath(self.inner_path, QtGui.QBrush(self.bg_color))
        painter.strokePath(self.inner_path, QtGui.QPen(QtGui.QBrush(self.inner_line_color), 1))
        painter.strokePath(self.outer_path, QtGui.QPen(QtGui.QBrush(self.outer_line_color), 1))
        
    def shape(self):
        return self.outer_path

    def mousePressEvent(self, event):
        self.signal.pressed.emit(*self.noodlet)
                    
    def mouseReleaseEvent(self, event):
        self.signal.released.emit(*self.noodlet)
        
    def hoverEnterEvent(self, event):
        self.bg_color = QtGui.QColor(200,60,60)
        self.update()
    
    def hoverLeaveEvent(self, event):
        self.bg_color = QtGui.QColor(90,90,200)
        self.update()

