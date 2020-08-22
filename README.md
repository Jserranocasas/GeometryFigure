# Geometry Figure
Class to work with a geometric figure and you get results like __orthocenter__ point, 
__height__ __line__ of a triangle or to calculate __mediatrix__. This class use Geospatial Data
Abstraction Library commonly referred to as __gdal__.

![alt text](https://i.imgur.com/kinVvZSm.png)
***
[Examples to work with gdal in python](https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html)

[Gdal library methods](https://gdal.org/python/osgeo.ogr.Geometry-class.html)

## What can you do with this code?
* You can get sides number of a polygon.
```python
self.lineString.GetPointCount()-1
```
- You can know what type of figure it is (Triangle, Quadrilateral, Pentagon, etc...).
```python
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
```
+ You can calculate the area of a polygon.
```python
self.polygon.GetArea()
```
- You can calculate the perimeter of a polygon.
```python
self.lineString.Length()
```
+ You can get center point of a polygon.
```python
self.polygon.Centroid()
```
- You can determine if a point is inside or out of polygon
```python
point = ogr.CreateGeometryFromWkt(wkt)
return self.polygon.Contains(point)
```
+ You can add a new point to the polygon
```python
aux = ogr.Geometry(ogr.wkbLineString)
point = ogr.CreateGeometryFromWkt(wkt_point)
for i in range(self.lineString.GetPointCount()):
    if(i == pos):
        aux.AddPoint(point.GetX(), point.GetY())
    aux.AddPoint(self.lineString.GetX(i), self.lineString.GetY(i))       
self.lineString = aux.Clone()
self.lineToPolygon()
```
- You can get the middle point of a side
```python
A = self.getVertex(side)
B = self.getVertex((side + 1) % self.sidesNumber())
middlePoint = ogr.Geometry(ogr.wkbPoint)
middlePoint.AddPoint(0.5*B.GetX() + 0.5*A.GetX(), 0.5*B.GetY() + 0.5*A.GetY())
```
+ You can calculate the mediatrix of a line.
```python
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
```
- You can get height line from triangle.
```python
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
```
+ You can get orthocenter point from triangle.
```python
if self.sidesNumber() != 3:
    raise ValueError("This object isn't a triangle")  

line1 = self.heightTriangle(0)
line2 = self.heightTriangle(1)

return line1.Intersection(line2)
```
