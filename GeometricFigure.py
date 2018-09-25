#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Created on Wed Aug  1 16:27:33 2018

    @author: Javier Serrano Casas
"""

# Import Geospatial Data Abstraction Library
from gdal import ogr

class GeometricFigure(object):
    """
        Class to work and get results from a geometric figure.

        :param polygon:      Class object to operations with wkbPolygon
        :type polygon:       ogr.wkbPolygon
        :param lineString:   Class object to operations with wkbLineString
        :type lineString:    ogr.wkbLineString
    """

    polygon = ogr.Geometry(ogr.wkbPolygon)
    lineString = ogr.Geometry(ogr.wkbLineString)
    
    def __init__(self, wkt):
        """
            Default Constructor

            :param wkt:   Text markup language for representing vector geometry objects
            :type wkt:    Polygon format

            :return:      None
        """

        self.polygon = ogr.CreateGeometryFromWkt(wkt)
        self.lineString = self.polygon.GetGeometryRef(0)


    def sidesNumber(self):
        """
            Method that returns sides number of polygon

            :return: sides number of this geometric figure
        """

        return self.lineString.GetPointCount()-1


    def figureType(self):
        """
            Method that returns figure type

            :return: figure type
        """

        if self.sidesNumber() == 3:
           return "Triangle"
        if self.sidesNumber() == 4:
           return "Quadrilateral"
        if self.sidesNumber() == 5:
           return "Pentagon"
        if self.sidesNumber() == 6:
           return "Hexagon"
        if self.sidesNumber() > 6:
           return "Polygon"


    def calculateArea(self):
        """
            Method that calculates polygon area

            :return: polygon area
        """

        return self.polygon.GetArea()
   
     
    def calculatePerimeter(self):
        """
            Method that calculates polygon perimeter

            :return: polygon perimeter
        """

        return self.lineString.Length()
    
    
    def getVertex(self, index):
        """
            Method that returns indicated vertex

            :param index: index of desired vertex
            :return: Vertex[index]
        """

        if index >= self.lineString.GetPointCount()-1 or index < 0:
            raise IndexError("Index out of range")

        point = ogr.Geometry(ogr.wkbPoint)
        p = self.lineString.GetPoint_2D(index)
        point.AddPoint(p[0], p[1])  

        return point
    
    
    def centroidFigure(self):
        """
            Method that returns the central point

            :return: central point
        """

        return self.polygon.Centroid()
    
    
    def isInside(self, wkt):
        """
            Method that checks if a point is inside the figure

            :param wkt: Geometry to checks
            :return: Boolean with result if a wkt Geometry is inside the figure
        """

        point = ogr.CreateGeometryFromWkt(wkt)
        return self.polygon.Contains(point)
    
    
    def printFigure(self):
        """
            Method that prints figure points

            :return:    None
        """

        for i in range(self.lineString.GetPointCount()):
            print ( "\t", self.lineString.GetPoint_2D(i))
    
    
    def lineToPolygon(self):
        """
            Method that transforms lineString geometry to polygon

            :return: None
        """

        ring = ogr.Geometry(ogr.wkbLinearRing)
        for i in range(self.lineString.GetPointCount()):
            ring.AddPoint(self.lineString.GetX(i), self.lineString.GetY(i))      
        self.polygon.Empty()
        self.polygon.AddGeometry(ring)
     
        
    def addPointIn(self, wkt_point, pos):
        """
            Method that add new vertex in indicated position

            :param wkt_point: Geometry like new vertex
            :param pos: position to insert new vertex
            :return: None
        """

        aux = ogr.Geometry(ogr.wkbLineString)
        point = ogr.CreateGeometryFromWkt(wkt_point)
        for i in range(self.lineString.GetPointCount()):
            if(i == pos):
                aux.AddPoint(point.GetX(), point.GetY())
            aux.AddPoint(self.lineString.GetX(i), self.lineString.GetY(i))       
        self.lineString = aux.Clone()
        self.lineToPolygon()
        

    def midpointSide(self, side):
        """
            Method that calculates the middle point of a side
            Being the parameter "side" from 0 to the number of sides - 1

            :param side: Line to calculates the middle point
            :return: middle point of side
        """

        A = self.getVertex(side)
        B = self.getVertex((side + 1) % self.sidesNumber())
        middlePoint = ogr.Geometry(ogr.wkbPoint)
        middlePoint.AddPoint(0.5*B.GetX() + 0.5*A.GetX(), 0.5*B.GetY() + 0.5*A.GetY())

        return middlePoint
    
    
    def calculateMediatrix(self, side):
        """
            Method that calculates the mediatrix of a line

            :param side: Line to calculates the mediatrix
            :return: mediatrix
        """

        m = self.midpointSide(side)
        A = self.getVertex(side)
        B = self.getVertex((side + 1) % self.sidesNumber())

        # Perpendicular of AB vector
        v = [-(B.GetY() - A.GetY()), B.GetX() - A.GetX()]

        # LineEquation --> [x = v2, y = -v1, constant = P2*v1 - P1*v2]
        lineE = [v[1], -v[0], (m.GetY()*v[0]) - (m.GetX()*v[1])]

        # From the line equation I get any two points
        line = ogr.Geometry(ogr.wkbLineString)

        if lineE[0] == 0:   # Not division by zero
            line.AddPoint( 10, - lineE[2] / float(lineE[1]) )
            line.AddPoint( -10, - lineE[2] / float(lineE[1]) )
        elif lineE[1] == 0:  # Not division by zero
            line.AddPoint( -lineE[2] / float(lineE[0]),  10)
            line.AddPoint( -lineE[2] / float(lineE[0]), -10)
        else:
            line.AddPoint( -((lineE[1] * 10) + lineE[2]) / float(lineE[0]), 10)
            line.AddPoint( -((lineE[1] * -10) + lineE[2]) / float(lineE[0]), -10)

        return line
        
    
    def heightTriangle(self, iVertex):
        """
            Method that returns height line of a triangle given by parameter a vertex

            :param iVertex: vertex index to calculates height line
            :return: height line of geometric figure
        """

        if self.sidesNumber() != 3:
            raise ValueError("This object isn't a triangle")

        A = self.getVertex(iVertex)
        B = self.getVertex((iVertex + 1) % self.sidesNumber())
        C = self.getVertex((iVertex + 2) % self.sidesNumber())

        lineHeight = ogr.Geometry(ogr.wkbLineString)
        lineHeight.AddPoint(A.GetX(), A.GetY())
        lineCB = ogr.Geometry(ogr.wkbLineString)
        lineCB.AddPoint(C.GetX(), C.GetY())
        lineCB.AddPoint(B.GetX(), B.GetY())
        
        t = lineCB.Distance(A) / C.Distance(B)
        D = [((B.GetY() - C.GetY())*t) + A.GetX(), -((B.GetX() - C.GetX())*t) + A.GetY()]
        lineHeight.AddPoint(D[0], D[1])

        return lineHeight
       
        
    def getOrthocenter(self):
        """
            Method that calculates orthocenter point from triangle

            :return: orthocenter point of geometric figure
        """

        if self.sidesNumber() != 3:
            raise ValueError("This object isn't a triangle")  

        line1 = self.heightTriangle(0)
        line2 = self.heightTriangle(1)

        return line1.Intersection(line2)



if __name__ == "__main__":
    wkt_tri = "POLYGON ((1 1, 3 5, 5 1, 1 1))"
    wkt_cua = "POLYGON ((0 0 ,0 5, 5 5, 5 0, 0 0))"
    wkt_pent = "POLYGON ((-5 0, 0 2, 5 0, 1 -4, -1 -4, -5 0))"
    wkt_hex = "POLYGON ((-4 0, -1 4, 1 4, 4 0, 1 -4, -1 -4, -4 0))"
    wkt_pol = "POLYGON ((-5 2, -3 5, 2 7, 5 1, 4 -2, -1 -3, -4 -1, -5 2))"

    polyCua = GeometricFigure(wkt_cua)
    polyTri = GeometricFigure(wkt_tri)
    print ("Polygon:")
    polyCua.printFigure()
    print ("\n")
    polyCua.addPointIn("POINT (8.0 1.5)", 2)
    print ("Polygon after the point is added: ")
    polyCua.printFigure()

    print ("\nThis polygon has", polyCua.sidesNumber(), "sides")
    print ("This polygon is a", polyCua.figureType())
    print ("This polygon has", polyCua.calculateArea(), "of area")
    print ("This polygon has", polyCua.calculatePerimeter(), "of perimeter")
    print ("The center polygon is: ", polyCua.centroidFigure())
    print ("The vertex with index 3 is: ", polyCua.getVertex(3))
    print ("Point: (2.0, 0.5) is inside of polygon: ", polyCua.isInside("POINT (2.0 0.5)"))
    print ("\nThe middle point of side 2 is: ", polyCua.midpointSide(3))
    print ("Mediatrix of side 3: ", polyCua.calculateMediatrix(3))
    print ("Height line in vertex 0 is: ",polyTri.heightTriangle(0))
    print ("Height line in vertex 1 is: ",polyTri.heightTriangle(1))
    print ("Height line in vertex 2 is: ",polyTri.heightTriangle(2))
    print ("Orthocenter point is: ",polyTri.getOrthocenter())