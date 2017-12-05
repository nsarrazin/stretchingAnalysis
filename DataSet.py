import csv
from scipy.spatial import Delaunay
from FrameData import FrameData

class DataSet:
    def __init__(self, csvpath, postDic):
        with open(csvpath) as csvfile:
            datadump = csv.reader(csvfile, delimiter=',')
            self.data = list(datadump)

        self.postDic = postDic

    def getFrame(self, timeframe):
        frame = FrameData.fromList(self.data, timeframe)
        return frame

    def getValidPoints(self):
        listLabels = []
        for posture in self.postDic.values():
            for tf in posture:
                frame = self.getFrame(tf)
                listLabels.append(list(frame.dictPoint.keys())) #extract non-null points for every frame

        result = set(listLabels[0])
        for s in listLabels[1:]:
            result.intersection_update(s) #find intersection of all those lists

        return result

    def pointIntersect(self, tf1, tf2):
        frame1 = self.getFrame(tf1)
        frame2 = self.getFrame(tf2)

        s1 = set(list(frame1.dictPoint.keys()))
        s2 = set(list(frame2.dictPoint.keys()))

        return s1.intersection(s2)
