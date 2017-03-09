"""
Tips & Techniques: Chapter 8 exercise for GforH course on PyQGIS

# it is not best practice to import *
# instead, only import the methods and attributes you need
"""

# OGR Layers
gml_lyr = QgsVectorLayer('vector_layer.gml', 'GML Layer', 'ogr')

# Memory Layers using URI
mem_layer = QgsVectorLayer("LineString?crs=epsg:4326&field=id:integer", "&field=road_name:string&index=yes", "Roads", "memory")
QgsMapLayerRegistry.instance().addMapLayer(mem_layer)

# Memory Layer - add features
mem_layer.startEditing()
points = [QgsPoint(-150, 61), QgsPoint(-151, 62)]
feature = QgsFeature()
feature.setGeometry(QgsGeometry.fromPolyline(points))
feature.setAttribute([1, 'QGIS Lane'])
mem_layer.addFeature(feature, True)
mem_layer.commitChanges()

# Adding a layer using iface
# when developing a standalone application using QGIS API,
# you will not have access to iface objects
lyr = iface.addVectorLayer('vector_layer.shp', 'layer', 'ogr')
lyr = iface.addRasterLayer('raster_layer.tif', 'layer')
# Loading a Raster layer
raster_lyr = QgsRasterLayer('raster_layer.tif', 'Raster Layer')
QgsMapLayerRegistry.instance().addMapLayer(raster_lyr)

# Databases

# Adding PostgreSQL/PostGIS Layer
db_lyr = QgsVectorLayer("dbname='gis_data' host=localhost port=5432 srid=4326 type=MULTILINESTRING table='public'.'street' (the_geom) sql=", 'streets3', 'postgres')

# Working with Symbology
renderer = rendererV2()
symbol = renderer.symbol()
symbol.setColor(QColor(Qt.Red))
symbol.setColor(Qcolor('red'))
symbol.setColor(QColor('#ff0000'))
symbol.setColor(QColor(255, 0, 0, 255))
iface.mapCanvas().refresh()
iface.legendInterface().refreshLayerSymbology(layer)

# Transparency
symbol.setAlpha(0.5)

# Custom Symbols
# this uses QgsMarkerSymbolV2, QgsLineSymbolV2, and QgsFillSymbolV2
sym = QgsMarkerSymbolV2.createSimple({'name':'circle', 'color': 'blue', 'size': '8', 'outline_width': '2'})
renderer = layer.rendererV2()
renderer.setSymbol(sym)

sym = QgsLineSymbolV2.createSimple({'penstyle': 'dash', 'color': 'green', 'width': '4'})
renderer = layer.rendererV2()
renderer.setSymbol(sym)

sym = QgsFillSymbolV2.createSimple({'style':'diagonal_x', 'color': 'blue'})
renderer = layer.rendererV2()
renderer.setSymbol(sym)

# Symbol Layers
lyr = iface.activeLayer()
renderer = lyr.rendererV2()
symbol = renderer.symbol()
# count layer elements or curent layer symbology
symbol.symbolLayerCount()
# access individual elements
sym0 = symbol.symbolLayer(0)
# examine the element properties
sym0.properties()
# change an element with setCustom
sym0.setCustomDashVector([10, 5])

# Using Styles
# Saving a style (either QML or SLD)
layer = iface.activeLayer()
layer.saveNamedStyle('/tmp/mystyle.qml')
# apply layer style (either QML or SLD)
layer.loadNamedStyle('/tmp/mystyle.qml')
iface.mapCanvas().refresh()
iface.legendInterface().refreshLayerSymbology(layer)

# Selecting and working with Features 
for feature in layer.getFeatures():
    print feature.id()









