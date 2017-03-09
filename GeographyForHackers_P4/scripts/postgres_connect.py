"""
PostgreSQL Connect: Chapter 8 exercise for GforH course on PyQGIS

You can also use psycopg2 or SQLAlchemy (which I highly recommend)

# it is not best practice to import *
# instead, only import the methods and attributes you need
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *


def run_script(iface):
    # get the active layer
    layer = iface.activeLayer()
    # get the underlying data provider
    provider = layer.dataProvider()
    if provider.name() == 'postgres':
        # get the URI containing the connection parameters
        uri = QgsDataSourceURI(provider.dataSourceUri())
        print uri.uri()
        #create a PostgreSQL connection
        db = QSqlDatabase.addDatabase('QPSQL')
        # check if valid
        if db.isValid():
            print "QPSQL db is valid"
            # set params for connection
            db.setHostName(uri.host())
            db.setDatabaseName(uri.database())
            db.setPort(int(uri.port()))
            db.setUserName(uri.username())
            db.setPassword(uri.password())
            # open the connection
            if db.open():
                print "Opened %s" % uri.uri()
                # a simple query
                query = db.exec_("""select * from qgis_sample.airports order by name""")
                # loop and print name
                while query.next():
                    record = query.record()
                    print record.field('name').value().toString()
                else:
                    err = db.lastError()
                    print err.driverText()
