import numpy as np
import networkx as nx

import csv

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

from Point import Point
from utils import getNeighbours

class FrameData:
    def __init__(self, dictpoint, tf, IDList, path=""):
        self.dictPoint = dictpoint
        self.IDList = IDList
        self.tf = tf
        self.path = path
    @classmethod
    def fromList(cls, dataList, tf):
        tf = tf
        FrameDict = {}
        IDList = []

        l1 = list(filter(None, dataList[5]))
        l1.pop(0)

        IDList = l1

        for i in range(0, len(IDList)):
            x = 1 + i*3
            y = 1 + i*3 + 1
            z = 1 + i*3 + 2

            coord = [float(dataList[tf][x]), float(dataList[tf][y]),float(dataList[tf][z])]
            ID = IDList[i]
            pt = Point(coord, ID)

            if pt.isNull():
                continue
            FrameDict[l1[i]] = pt

        return cls(FrameDict, tf, IDList)


    @classmethod
    def fromCSV(cls, filepath):
        FrameDict = {}
        with open(filepath) as csvfile:
            datadump = csv.reader(csvfile, delimiter=',')
            data = list(datadump)

        tf=data[1][1]
        l1 = list(filter(None, data[5]))
        l1.pop(0)

        for i in range(0, len(l1)):
            x = 1 + i*3
            y = 1 + i*3 + 1
            z = 1 + i*3 + 2

            coord = [float(data[8][x]), float(data[8][y]),float(data[8][z])]
            ID = l1[i]
            pt = Point(coord, ID)

            if pt.isNull():
                continue
            if pt.ID == "56x":
                pt.ID = "56"
                FrameDict["51"] = FrameDict["56"]
            if pt.ID == "55x":
                pt.ID = "55"
                FrameDict["50"] = FrameDict["55"]
            if pt.ID == "53x":
                pt.ID = "53"
                FrameDict["48"] = FrameDict["53"]
            if pt.ID == "54x":
                pt.ID = "54"
                FrameDict["49"] = FrameDict["54"]
            if pt.ID == "54xx":
                pt.ID = "54"
                FrameDict["49"] = FrameDict["54"]
            if pt.ID == "45x":
                pt.ID = "45"
                FrameDict["52"] = FrameDict["45"]
            if pt.ID == "1x":
                pt.ID = "1"
                FrameDict["3"] = FrameDict["1"]
            FrameDict[pt.ID] = pt

        try:
            del FrameDict["r"]
            del FrameDict["t"]
            # del FrameDict["1"]
            # del FrameDict["2"]
            # del FrameDict["3"]
            # del FrameDict["4"]
            # del FrameDict["No_Label_002842"]
        except:
            print("WARNING: Missing R or T points")
        return cls(FrameDict, tf, l1, path=filepath)


    def getPoint(self, ID):
        try:
            return self.dictPoint[ID]
        except:
            return None

    def returnGraph(self):
        structure = nx.Graph(name=self.path[41:-4])
        listpoints = sorted([int(x) for x in self.dictPoint.keys()])

        for i in listpoints:
            structure.add_node(i, pos=self.dictPoint[str(i)].pos)

        for i in listpoints:
            for j in getNeighbours(int(i)):
                try:
                    iPoint = self.dictPoint[str(i)]
                    jPoint = self.dictPoint[str(j)]
                    dist = iPoint.getDistance(jPoint)
                    structure.add_edge(i,j, dist=dist)
                except KeyError:
                    # print(str(j))
                    continue
        return structure

    def plotFrame(self):
        x,y,z = [], [], []
        for point in self.dictPoint.values():
            x.append(point.pos[0])
            y.append(point.pos[1])
            z.append(point.pos[2])

        trace = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=12,
            line=dict(
                width=0.5
            ),
            opacity=0.8
                )
            )

        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            ),
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot(fig, filename='plotBack - '+str(self.tf))

    def plotXYZ(self, X,Y,Z):
        trace = go.Scatter3d(x=X,
        y=Y,
        z=Z,
        mode='markers',
        marker=dict(
            size=12,
            line=dict(
                width=0.5
            ),
            opacity=0.8
                )
            )

        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            ),
            scene = dict(
                aspectratio=dict(x=1, y=1, z=1),
            xaxis = dict(
                nticks=4, range = [-3000,3000],),
            yaxis = dict(
                nticks=4, range = [-3000,3000],),
            zaxis = dict(
                nticks=4, range = [0,2000],),),
        )
        fig = go.Figure(data=[trace], layout=layout)
        plot(fig, filename='plotBack - '+str(self.tf))
