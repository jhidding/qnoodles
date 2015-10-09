import sys, os
from PySide import QtGui, QtCore
from PySide.QtCore import Qt

from .noodlet import Noodlet

class MySeparator(QtGui.QWidget):
    """
    Qt doesn't have a `QSeparator` widget. This draws a horizontal line.
    """
    
    def __init__(self, parent=None):
        super(MySeparator, self).__init__(parent)
        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setFixedHeight(8)
        
    def paintEvent(self, event):
        pt = QtGui.QPainter(self)
        pt.setRenderHints(pt.Antialiasing)
        w, h = self.size().toTuple()
        
        pen = QtGui.QPen(QtGui.QBrush(Qt.black), 1)
        pt.drawLine(4, h/2, w-4, h/2)
        
class MyFrame(QtGui.QWidget):
    """
    The standard `QFrame` doesn't have the fine-grained control over
    appearance, different colors, rounded corners etc, that we need.
    Maybe if I understand better how Qt+CSS works we can revert to using
    `QFrame`.
    """
    
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
        pen = QtGui.QPen(QtGui.QBrush(Qt.black), 0.5)
        path.addRoundedRect(1, 1, w-2, h-2, 8, 8)
        pt.fillPath(path, brush)
        pt.strokePath(path, pen)

def _make_widget(noodlet):
    """
    Arguments:
        noodlet - named tuple which should have `name`, `dtype`, `widget`
            attributes.
            
    Returns:
        a QWidget
    """
    
    w = QtGui.QLabel("{name} [{dtype}]".format(name=noodlet.name, dtype=noodlet.dtype.__name__))
    if noodlet.direction == 'out':
        w.setAlignment(QtCore.Qt.AlignRight)
    
    w.setProperty('labelClass', 'noodlet')
    w.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
    w.setContentsMargins(5, 2, 5, 2)
    return w
    
class NodeBox(MyFrame):
    """
    The NodeBox is the widget that displays a Node and its childs. It also
    creates the Noodlets needed for this node, but those are added to the
    QGraphicsScene independently. This seems necesary for the noodlets to
    recieve the mouse events.
    Only during the dragging of a node are the Noodlets grouped with the node
    so that they move in unison with the node. Once the mouse button is
    released the group is descroyed so that the noodlets recieve their own
    events once more.
    """
    def __init__(self, node, scene):
        super(NodeBox, self).__init__()
        self.scene = scene
        self.data  = node
        
        style = str(open("static/qt-style.css", "r").read())
        #self.setFrameStyle(self.StyledPanel | self.Plain)
        self.box = QtGui.QVBoxLayout()
        self.setLayout(self.box)
        
        self.title = QtGui.QLabel(node.name, self)
        self.title.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.title.setProperty('labelClass', 'title')
        self.box.addWidget(self.title)
                    
        #self.items = [QtGui.QPushButton("Blah {0}".format(i), self) for i in range(3)]
        self.input_items = [_make_widget(i) for i in self.data.input_noodlets()]
        for i in self.input_items:
            self.box.addWidget(i)
           
        self._sep = MySeparator() 
        self.box.addWidget(self._sep)
        self.output_items = [_make_widget(i) for i in self.data.output_noodlets()]

        for i in self.output_items:
            self.box.addWidget(i)
        
        self.proxy = scene.addWidget(self)
        self.proxy.setZValue(0)
        self.move(*node.location)
        
        #self.group = QtGui.QGraphicsItemGroup(self.proxy, scene)
        #self.group.addToGroup(self.proxy)
        
        self.noodlets = [Noodlet(*self.output_item_pos(i)) for i in self.output_items] \
                      + [Noodlet(*self.input_item_pos(i)) for i in self.input_items]
                      
        for n in self.noodlets:
            scene.addItem(n)
            n.signal.pressed.connect(scene.noodletPressed)
            n.signal.released.connect(scene.noodletReleased)
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

