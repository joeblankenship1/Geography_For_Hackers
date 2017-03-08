"""
FirstScript: Chapter 7 exercise for GforH course on PyQGIS

# it is not best practice to import *
# instead, only import the methods and attributes you need
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *


class FirstScript:
    """Class to load and render the assigned Vector layer"""

    def __init__(self, iface):
        self.iface = iface

    def load_layer(self):
        """Load the Vector layer and add it to map canvas"""
        wb = QgsVectorLayer('vector_file.shp', 'countries', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(wb)

    def change_color(self):
        """Change the color of the active layer to red. Update the legend"""
        active_layer = self.iface.activeLayer()
        renderer = active_layer.rendererV2()
        symbol = renderer.symbol()
        symbol.setColor(QColor(Qt.red))
        self.iface.mapCanvas().refresh()
        self.iface.legendInterface().refreshLayerSymbology(active_layer)

    def open_attribute_table(self):
        """Open the attribute table for the active layer"""
        self.iface.showAttributeTable(self.iface.activeLayer())


def run_script(iface):
    """Run the script by instantiating FirstScript and calling methods"""
    fs = FirstScript(iface)
    fs.load_layer()
    fs.change_color()
    fs.open_attribute_table()
