"""
Map Tools: Chapter 8 exercise for Geography for Hackers course in PyQGIS

"""

from PyQt4.QtCore import pyqtSignal, Qt
from PyQt4.QtGui import QColor
from qgis.core import QgsGeometry, QgsPoint
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand


class ConnectTool(QgsMapToolEmitPoint):
    """ Map tool to conect points """
    
    line_complete = pyqtSignal(QgsPoint, QgsPoint)
    start_point = None
    end_point = None
    rubberband = None
    
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, canvas)
    
    def canvasMoveEvent(self, event):
        if self.start_point:
            point = self.toMapCoordinates(event.pos())
            if self.rubberband:
                self.rubberband.reset()
            else:
                self.rubberband = QgsRubberBand(self.canvas, False)
                self.rubberband.setColor(QColor(Qt.red))
            # set the geometry for the rubberband
            point = [self.start_point, point]
            self.rubberband.setToGeometry(QgsGeometry.fromPolyline(points), None)
    
    def canvasPressEvent(self, e):
        if self.end_point is None: 
            self.start_point = self.toMapCoordinates(e.pos())
        else:
            self.end_point = self.toMapCoordinates(e.pos())
            # kill the rubberband
            self.rubberband.reset()
            # line is done, emit a signal
            self.line_complete.emit(self.start_point, self.end_point)
            # reset the points
            self.start_point = None
            self.end_point = None
