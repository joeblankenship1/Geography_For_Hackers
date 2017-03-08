"""
Console Commands: Chapter 6 exercises for GforH course on PyQGIS
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor

# load Vector layer
wb = QgsVectorLayer('layer_location.shp', 'countries', 'ogr')
if wb.isValid():
    QgsMapLayerRegistry.instance().addMapLayer(wb)

# to remove layer
QgsMapLayerRegistry.instance().removeMapLayer(wb.id())

renderer = wb.rendererV2()
renderer

#change symbology
symbol = renderer.symbol()
symbol.dump()

symbol.setColor(QColor('#800000'))
iface.mapCanvas().refresh()

wb.setCacheImage(None)
iface.mapCanvas().refresh()

# import Raster layer

nat_earth = QgsRasterLayer('raster_layer.tif', 'Natural Earth')
QgsMapLayerRegistry.instance().addMapLayer(nat_earth)

# remove Raster layer
QgsMapLayerRegistry.instance().removeMapLayer(nat_earth.id())

# print QGIS data providers
for provider in QgsProviderRegistry.instance().providerList():
    print providers

