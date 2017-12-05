from DataSet import DataSet
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import numpy as np

path = r'/home/nsarrazin/prog/thesis/2(new).csv'
postDic = {'rest' : [741, 2873, 4707, 6409, 8360, 10400, 12208, 14153, 16208,
                     18243, 20099, 21731, 23415, 25227, 26759, 28455, 30247, 31991],
            'draw' : [1409, 18875],
            'multidevice' : [4063, 21087],
            'text' : [5583, 22383],
            'cocoon' : [7219, 24071],
            'swipe' : [9372, 25819],
            'smartlean' : [11252, 27463],
            'trance' : [13017, 28455],
            'takeitin' : [14888, 31267],
            'strunch' : [17111, 32667]
             }

test2 = DataSet(path, postDic)
t1 = 741

for t2 in postDic['rest'][1:]:
    # t2 = 4063
    frameTest = test2.getFrame(t2)
    points = test2.pointIntersect(t1, t2)

    # points = test2.getValidPoints()
    # x,y,z = [], [], []
    posList = []
    for ptID in points:
        pt = frameTest.getPoint(ptID)
        # x.append(pt.pos[0])
        # y.append(pt.pos[1])
        # z.append(pt.pos[2])
        posList.append(pt.pos)

    # frameTest.plotXYZ(x,y,z)
    tree = KDTree(posList)
    nLinks = []
    for i in range(0, 100):
        setr = tree.query_pairs(i)
        nLinks.append(len(setr))

    # plt.plot(range(0,125), nLinks)
    plt.plot(range(0,100), np.gradient(nLinks))
plt.show()
