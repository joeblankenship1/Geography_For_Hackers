"""
Simple Point: Chapter 2 exercise for GforH course on PyQGIS

# Mixing class definitions and non-class functions in the
# same file is not best practice
"""

class Point:
    
    marker_size = 4
    
    def draw(self):
        print "drawing the point"
    
    def move(self, new_x, new_y):
        print "moving the point"
    

def my_function():
    return "this does nothing"
