#######################################################
#    Author:      Shu Hwai Teoh
#    email:       teoh0@purdue.edu
#    ID:          ee364e13
#    Date:        Apr. 03, 2019
#######################################################
import os
import sys
import numpy as np
import imageio
from scipy.spatial import Delaunay
from scipy.interpolate import RectBivariateSpline
from matplotlib.path import Path
# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################

def loadTriangles(leftPointFilePath: str, rightPointFilePath: str) -> tuple:
    with open(leftPointFilePath, "r") as f:
        leftSource=f.read().split()
    leftPoints = [[float(leftSource[i]), float(leftSource[i + 1])] for i in range(0,len(leftSource) - 1,2)]
    leftPoiArray = np.array(leftPoints)
    tri = Delaunay(leftPoiArray)
    leftTri = leftPoiArray[tri.simplices]

    with open(rightPointFilePath, "r") as f:
        rightSource = f.read().split()
    rightPoints = [[float(rightSource[i]), float(rightSource[i + 1])] for i in range(0,len(rightSource) - 1,2)]
    rightPoiArray = np.array(rightPoints)
    rightTri = rightPoiArray[tri.simplices]

    return [Triangle(i) for i in leftTri],[Triangle(i) for i in rightTri]

def _calH(leftTri,rightTri,alpha):
    targetPoints=[l.vertices*(1-alpha)+r.vertices*alpha for l,r in zip(leftTri,rightTri)]
    targetTri=[Triangle(i) for i in targetPoints]
    lHs=[]
    rHs=[]
    for i in range(len(leftTri)):
        la=np.array([[leftTri[i]._0[0],leftTri[i]._0[1],1.0,0,0,0],[0,0,0,leftTri[i]._0[0],leftTri[i]._0[1],1.0]\
            ,[leftTri[i]._1[0], leftTri[i]._1[1], 1.0, 0, 0, 0],[0, 0, 0, leftTri[i]._1[0], leftTri[i]._1[1], 1.0]\
            ,[leftTri[i]._2[0], leftTri[i]._2[1], 1.0, 0, 0, 0],[0, 0, 0, leftTri[i]._2[0], leftTri[i]._2[1], 1.0]])
        tb=np.array([[targetTri[i]._0[0]],[targetTri[i]._0[1]],[targetTri[i]._1[0]],[targetTri[i]._1[1]],[targetTri[i]._2[0]],[targetTri[i]._2[1]]])
        lH=np.linalg.solve(la,tb)
        lHs.append(np.linalg.inv(np.insert(lH.reshape(2, 3), 2, [0.0, 0.0, 1.0], 0)))
        #lHs.append(np.insert(lH.reshape(2,3),2,[0.0,0.0,1.0],0))
        ra = np.array([[rightTri[i]._0[0], rightTri[i]._0[1], 1.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, rightTri[i]._0[0], rightTri[i]._0[1], 1.0] \
                          ,[rightTri[i]._1[0], rightTri[i]._1[1], 1.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, rightTri[i]._1[0], rightTri[i]._1[1], 1.0] \
                          ,[rightTri[i]._2[0], rightTri[i]._2[1], 1.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, rightTri[i]._2[0], rightTri[i]._2[1], 1.0]])
        rH = np.linalg.solve(ra, tb)
        rHs.append(np.linalg.inv(np.insert(rH.reshape(2, 3), 2, [0.0, 0.0, 1.0], 0)))
        #rHs.append(np.insert(rH.reshape(2, 3), 2, [0.0, 0.0, 1.0], 0))
    return targetTri, lHs, rHs

class Triangle:
    def __init__(self,vertices):
        if len(vertices)!=3 or len(vertices[0])!=2 or len(vertices[1])!=2 or len(vertices[2])!=2 or \
                type(vertices[0][0])!=np.float64:
            raise ValueError("Vertices dimensions or types are not valid.")
        self.vertices=vertices
        self._0=vertices[0]
        self._1 = vertices[1]
        self._2 = vertices[2]
    # def _calArea(self,x1,y1,x2,y2,x3,y3):
    #     return abs((x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))/2)

    def getPoints(self):
        xCoors=np.array((self._0[0],self._1[0],self._2[0]),dtype=float)
        yCoors = np.array((self._0[1], self._1[1], self._2[1]), dtype=float)
        xs,ys=np.meshgrid(np.arange(np.uint(np.min(xCoors)),np.uint(np.max(xCoors))+1),np.arange(np.uint(np.min(yCoors)),np.uint(max(yCoors))+1))
        points=list(zip(xs.flatten(),ys.flatten()))
        pointList=[]
        p = Path([self._0, self._1, self._2])
        boolArray=p.contains_points(points)
        for i in range(boolArray.shape[0]):
            if boolArray[i]==True:
                pointList.append(points[i])
        return np.array(pointList,dtype=float)

        # x, y = np.meshgrid(np.arange(np.uint(max(self._0[0],self._1[0],self._2[0]))+1), np.arange(np.uint(max(self._0[1], self._1[1], self._2[1]))+1))  # make a canvas with coordinates
        # x, y = x.flatten(), y.flatten()
        # points = np.vstack((x, y)).T
        # p = Path([self._0,self._1,self._2])
        # grid = p.contains_points(points)
        # mask = grid.reshape(np.uint(max(self._0[0],self._1[0],self._2[0]))+1, np.uint(max(self._0[1], self._1[1], self._2[1]))+1)
        # # for i in mask:
        #     if i:
        #         pointList.append(points[k])
        # return np.array(pointList,dtype=float)

        # areaT = self._calArea(self._0[0],self._0[1],self._1[0],self._1[1],self._2[0],self._2[1])
        # for i in points:
        #     x, y = i
        #     if (not(x==self._0[0] and y==self._0[1])) and not((x==self._1[0] and y==self._1[1])) and not(x==self._2[0] and y==self._2[1]):
        #         area1=self._calArea(x,y,self._1[0],self._1[1],self._2[0],self._2[1])
        #         area2=self._calArea(self._0[0],self._0[1],x,y,self._2[0],self._2[1])
        #         area3=self._calArea(self._0[0],self._0[1],self._1[0],self._1[1],x,y)
        #         if (area1+area2+area3)==areaT:
        #             pointList.append(i)
        # return np.array(pointList,dtype=float)

        # xc=np.mean(xCoors)
        # yc=np.mean(yCoors)
        # binMaskTri=np.ones(xs.shape,dtype=bool)
        # for p in range(3):
        #    pp=(p+1)%3
        #    if xCoors[p]==xCoors[pp]:
        #        inside=xs*(xc-xCoors[p])/abs(xc-xCoors[p]) > xCoors[p]*(xc-xCoors[p])/abs(xc-xCoors[p])
        #    else:
        #        slope=(yCoors[pp]-yCoors[p])/(xCoors[pp]-xCoors[p])
        #        poly=np.poly1d([slope,yCoors[p]-xCoors[p]*slope])
        #        inside=ys*(yc-poly(xc)/abs(yc-poly(xc))) > poly(xs)*(yc-poly(xc)/abs(yc-poly(xc)))
        #    binMaskTri*=inside
        # return np.array(zip(xs[binMaskTri],ys[binMaskTri]))

class Morpher:
    def __init__(self, leftImage, leftTriangles, rightImage, rightTriangles):
        if type(leftImage)!=np.ndarray or type(leftTriangles)!=list or type(rightImage)!=np.ndarray or type(rightTriangles)!=list:
            raise TypeError("Arguments of Morpher are not numpy arrays or lists.")
        self.leftImage=leftImage
        self.leftTriangles=leftTriangles
        self.rightImage=rightImage
        self.rightTriangles=rightTriangles

    def getImageAtAlpha(self, alpha):
        tarTri, lHs, rHs = _calH(self.leftTriangles, self.rightTriangles,alpha)
        x,y=self.leftImage.shape
        result = np.zeros((x,y))
        leftFunc=RectBivariateSpline(np.arange(0,x),np.arange(0,y),self.leftImage,kx=1,ky=1)
        rightFunc=RectBivariateSpline(np.arange(0,x),np.arange(0,y),self.rightImage,kx=1,ky=1)
        for k,v in enumerate(tarTri):
            for tarPoint in v.getPoints():
                r=np.matmul(rHs[k],np.array(([tarPoint[0]],[tarPoint[1]],[1.0])))
                rr=rightFunc.ev(r[1],r[0])
                l=np.matmul(lHs[k],np.array(([tarPoint[0]],[tarPoint[1]],[1.0])))
                ll=leftFunc.ev(l[1],l[0])
                result[int(tarPoint[1])][int(tarPoint[0])]=(1-alpha)*ll+(alpha)*rr
        return np.array(result,dtype=np.uint8)

    # for k,v in enumerate(tarTri):
    #     points=v.getPoints()
    #     pointsT= np.vstack((points.T, np.ones(points.shape[0])))
    #     r = np.matmul(rHs[k], pointsT)
    #     rr = rightFunc.ev(r[1], r[0])
    #     l = np.matmul(lHs[k], pointsT)
    #     ll = leftFunc.ev(l[1], l[0])
    #     for k, v in zip(points, (ll*(1-alpha) + rr*alpha)):
    #         result[int(k[1]), int(k[0])] = v



if __name__ == "__main__":
    lTri, rTri=loadTriangles("/home/ecegridfs/a/ee364e13/Documents/labs-teoh0/Lab12/TestData/points.left.txt","/home/ecegridfs/a/ee364e13/Documents/labs-teoh0/Lab12/TestData/points.right.txt")
    # a=Triangle(np.array(((999.0,1245.6),(1128.6,1079.0),(1079.0,1439.0)),dtype=float))
    # b=a.getPoints()
    # print("1")
    lIm = np.array(imageio.imread("/home/ecegridfs/a/ee364e13/Documents/labs-teoh0/Lab12/TestData/LeftGray.png"))
    rIm = np.array(imageio.imread("/home/ecegridfs/a/ee364e13/Documents/labs-teoh0/Lab12/TestData/RightGray.png"))
    a=Morpher(lIm, lTri, rIm, rTri)
    result=a.getImageAtAlpha(0.25)
    imageio.imwrite('result25.png', result[:,:])







