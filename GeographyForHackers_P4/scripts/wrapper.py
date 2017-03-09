import os

from PyQt4.QtGui import *

from qgis.utils import iface
from qgis.core import *

from osgeo import ogr
from osgeo import gdal


def addLayer(uri, name=None):
    """ Generic attempt to add a layer by attempting to open it in various ways"""
    # try to open using ogr
    lyr = ogr.Open(uri)
    if lyr:
        return addOgrLayer(uri, name)
    else:
        # try to open using gdal
        lyr = gdal.Open(uri)
        if lyr:
            return addGdalLayer(uri, name)
        else:
            return None


def addOgrLayer(layerpath, name=None):
    """ Add an OGR layer and return a reference to it.
        If name is not passed, the filename will be used
        in the legend.

        User should check to see if layer is valid before
        using it."""
    if not name:
        (path, filename) = os.path.split(layerpath)
        name = filename

    lyr = QgsVectorLayer(layerpath, name, 'ogr')
    return QgsMapLayerRegistry.instance().addMapLayer(lyr)


def addGdalLayer(layerpath, name=None):
    """Add a GDAL layer and return a reference to it"""
    if not name:
        (path, filename) = os.path.split(layerpath)
        name = filename

    lyr = QgsRasterLayer(layerpath, name)
    return QgsMapLayerRegistry.instance().addMapLayer(lyr)


def removeLayer(layer):
    QgsMapLayerRegistry.instance().removeMapLayer(layer.id())


def createRGBA(color):
    (red, green, blue, alpha) = color.split(',')
    return QColor.fromRgb(int(red), int(green), int(blue), int(alpha))


def changeColor(layer, color):
    """ Change the color of a layer using Qt named colors, RGBA, or hex notation."""
    if ',' in color:
        # assume rgba color
        color = createRGBA(color)
        transparency = color.alpha() / 255.0
    else:
        color = QColor(color)
        transparency = None

    renderer = layer.rendererV2()
    symb = renderer.symbol()
    symb.setColor(color)
    if transparency:
        symb.setAlpha(transparency)
    layer.setCacheImage(None)
    iface.mapCanvas().refresh()
    iface.legendInterface().refreshLayerSymbology(layer)

