from PySide import QtGui, QtCore
from PySide.QtCore import Qt

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

