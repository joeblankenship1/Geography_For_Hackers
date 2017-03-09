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

# get the name of a feature
nme = feature['CNTRY_NAME']
name = feature[2]

# get the index
idx = feature.fieldNameIndex('cntry_name')

# get features using a rectangle 
rectangle = QgsRectangle(-150, 60, -140, 61)
request = QgsFeatureRequest().setFilterRect(rectangle)
for feature in layer.getFeatures(request):
    # do something

# feature by id 
request = QgsFeatureRequest().setFilterFid(3201)
feature = layer.getFeatures(request).next()
print feature['cntry_name']

# wrap requests in try/except blocks 
request = QgsFeatureRequest().setFilterFid(320021)
try:
    feature = lyr.getFeatures(request).next()
except StopIteration:
    print "Feature not found"

# select all features
layer.selectAll()

# remove selection 
layer.removeSelection()

# Editing Attributes

# edit feature with known fid 
fid = 1
new_name = {2: 'My new name'}
layer.dataProvider().changeAttributeValues({fid: new_name})

# fetching field index for edit 
features = layer.getFeatures(QgsFeatureRequest().setFilterFid(1))
feature = features.next()
new_name = {feature.fieldNameIndex('name'): 'My New Name'}
layer.dataProvider().changeAttributeValues({feature.id: new_name})

# update multiple attributes
layer = iface.activeLayer()
provider = layer.dataProvider()
features = layer.getFeatures(QgsFeatureRequest().setFilter(1))
feature = features.next()
feature['name'] = "My new Name"
feature['city'] = "Lexington"
field_map = provider.fieldNameMap()
attrs = {field_map[key]: feature[key] for key in field_map}
layer.dataProvider().changeAttributeValues({feature.id(): attrs})

# Saving Images

# you can save images as any number of formats - see documentation 
mc = iface.mapCanvas().saveAsImage('/tmp/image.png')

# Getting QGIS Paths

# summary of paths 
print QgsApplication.showSettings()

# path to installed plugin 
QgsApplication.qgisUserDbFilePath()

# full path to plugin 
QFileInfo(QgsApplication.qgisUserDbFilePath()).path()
plugin_dir = os.path.join(QFileInfo(QgsApplication.qgisUserDbFilePath()).path(), 'python/plugins')
plugin_dir
plugin_path = os.path.join(plugin_dir, 'my_plugin')

# Message and Feedback 

# Message Box 
QMessageBox.information(iface.mainWindow(), 'Important Information', 'This is an important message')

# Message Log
QgsMessageLog.logMessage('SuperZoom plugin initialized and ready', 'SuperZoom', QgsMessageLog.INFO)

# Message Bar 
from qgis.gui import QgsMessageBar
iface.messageBar().pushMessage("Title", "message", QgsMessageBar.WARNING, 2)
iface.messageBar().pushMessage("SuperZoom", "You sepcified an invalid zoom level", QgsMessageBar.CRITICAL, 10)

# Refeshing Map Legend 

# refresh map 
iface.mapCanvas().refresh()

# refersh legend 
iface.legendInterface().refreshLayerSymbology(layer)

# Creating a Map Tool 

# see map_tool.py

# using the map tool

# create the tool
map_tool = ConnectTool(self.canvas)

# create an action to enable it
self.connect_action = QAction(QIcon(":/ouricon/connect_icon"), "Connect", self)

# add action to toolar
self.toolbar.addAction(self.connect_action)

# Connect action to method for tool
self.connect_action.triggered.connect(self.connect_pt)

# Create the method for map tool 
def connect_pt(self):
    self.map_canvas.setMapTool(self.tool_connect)

# Create the method for new line
def connect_complete(self, pt1, pt2):
    # create the line from the points 
    QMessageBox.information(None, "Connect Tool", "Creating line from %s to %s" % (pt1.toString(), pt2.toString()))

self.tool_connect.line_complete.connect(self.connect_complete)

# adding tool to custom toolbar

rect_select = self.iface.actionSelectRectangle()
self.toolbar.addAction(rect_select)

# Access existing plugins 

if 'pinpoint' in qgis.utils.plugins:
    pp = qgis.utils.plugins['pinpoint']
    pp.create_pin_layer()
    pp.place_pin(QgsPoint(100,100), 1)

# Setting up a repository

# contents of plugins.xml
# place in location that serves HTTP (GitHub would be good)


    
