"""
FirstScript: Chapter 7 exercise for GforH course on PyQGIS

# it is not best practice to import *
# instead, only import the methods and attributes you need
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *


class FirstScript:
    
    def __init__(self, iface):
        self.iface = iface
    
    def load_layer(self):
        wb = QgsVectorLayer('/home/medo/Desktop/research/analysis/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp', 'countries', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(wb)

    def change_color(self):
        active_layer = self.iface.activeLayer()
        renderer = active_layer.rendererV2()
        symbol = renderer.symbol()
        symbol.setColor(QColor(Qt.red))
        self.iface.mapCanvas().refresh()
        self.iface.legendInterface().refreshLayerSymbology(active_layer)

    def open_attribute_table(self):
        self.iface.showAttributeTable(self.iface.activeLayer())
