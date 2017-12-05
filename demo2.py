from FrameData import FrameData
from networkx import info, get_edge_attributes
from utils import buildAvgGraph, buildDeltaGraph, plotDeltaGraph, plotSensorGraph

listGraph = []
IDDict = {'rest' : [1, 3, 5, 7, 9, 11, 13, 15, 17],
            'draw' : [2],
            'multidevice' : [4],
            'text' : [6],
            'cocoon' : [8],
            'swipe' : [10],
            'smartlean' : [12],
            'trance' : [14],
            'takeitin' : [16],
            # 'strunch' : [18]
             }

def retListGraph(IDList, ds, twoPart=True):
    listGraph=[]
    for i in IDList:
        try:
            frame = FrameData.fromCSV("/home/nsarrazin/prog/thesis/postures/"+str(ds)+"/1/"+str(ds)+"."+str(i)+".csv")
            # print(i, frame.tf)
            listGraph.append(frame.returnGraph())
        except:
            print("ERROR Frame {} - {} - 1".format(str(ds), str(i)))
        if twoPart:
            try:
                frame2 = FrameData.fromCSV("/home/nsarrazin/prog/thesis/postures/"+str(ds)+"/2/"+str(ds)+"."+str(i)+".2.csv")
                # print(i, frame2.tf)
                listGraph.append(frame2.returnGraph())
            except Exception as e:
                print("ERROR Frame {} - {} - 2 : {}".format(str(ds), str(i), str(e)))

    return listGraph

# test = retListGraph(list(range(1,19)), 5)
# 53x > 53
# 53 > 48

# 54x > 54
# 54 >49

# 54xx > 54
# 54x > None

dataset = 2
restL = retListGraph(IDDict["rest"], dataset)
rest = buildAvgGraph(restL)
plotDict = {}

for i in IDDict.keys():
    plotDict[i] = []

for i in IDDict.keys():
    if i == "rest":
        continue

    subjL = retListGraph(IDDict[i], dataset)
    subj = buildAvgGraph(subjL)

    d1 = buildDeltaGraph(rest, subj)
    plotDeltaGraph(d1, i)
    # plotDict[i].append(data)

strunch = FrameData.fromCSV("/home/nsarrazin/prog/thesis/postures/2/1/2.18.csv")
strunch = strunch.returnGraph()
d1 = buildDeltaGraph(rest, strunch)
plotDeltaGraph(d1, "strunch")


# strunch2 = FrameData.fromCSV("/home/nsarrazin/prog/thesis/postures/4/1/4.18.csv")
# strunch2 = strunch2.returnGraph()
##
# rest2 = FrameData.fromCSV("/home/nsarrazin/prog/thesis/postures/4/1/4.17.csv")
# rest2 = rest2.returnGraph()

# rest2 = FrameData.fromCSV("/home/nsarrazin/prog/thesis/postures/4/1/4.17.csv")
# rest2 = rest2.returnGraph()


# plotSensorGraph([strunch, strunch2, rest, rest2])
# graph =-

# plotSensorGraph([draw, rest])
# for i in range(2,6):
# listGraph = retListGraph(list(range(1,19)), 3, twoPart=True)
#
# plotSensorGraph(listGraph)
# frame2 = FrameData.fromCSV("/home/nsarrazin/prog/thesis/postures/"+str(ds)+"/2/"+str(ds)+"."+str(i)+".2.csv")

#mislabeled data :
# 5th 2nd half
# 4th 1st half
#
