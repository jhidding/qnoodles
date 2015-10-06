import os
from PySide import QtGui, QtCore
from PySide.QtCore import Qt

os.environ['QT_API'] = 'pyside'

from pyqode.core import api as QodeApi
from pyqode.core import modes as QodeModes
from pyqode.core import panels as QodePanels
from pyqode.core import backend as QodeBackend

class SourceView(QodeApi.CodeEdit):
    def __init__(self):
        super(SourceView, self).__init__()
        self.backend.start(QodeBackend.server.__file__)
        self.modes.append(QodeModes.CodeCompletionMode())
        self.modes.append(QodeModes.PygmentsSyntaxHighlighter(self.document()))
        self.modes.append(QodeModes.CaretLineHighlighterMode())
        self.panels.append(QodePanels.LineNumberPanel())
        
        margin = self.modes.append(QodeModes.RightMarginMode())
        margin.position = 80
        margin.color = Qt.GlobalColor.gray
        
        self.font_name = "Inconsolata"
        self.font_size = 12
        self.file.open(__file__)

