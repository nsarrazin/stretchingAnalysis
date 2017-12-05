import numpy as np
import networkx as nx
import functools

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

pointShape =   np.array(
               [[None, None, None, None, 1, 2, None, None, None, None],
                [None, None, None, None, 3, 4, None, None, None, None],
                      [None, None, 5, 6, 7, 8, 9, 10, None, None],
                    [None, 11, 12, 13, 14, 15, 16, 17, 18, None],
                      [19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
                      [29, 30, 31, 32, 33, 34, 35, 36, 37, 38],
                    [None, 39, 40, 41, 42, 43, 44, 45, 46, None],
                  [None, None, 47, 48, 49, 50, 51, 52, None, None],
                [None, None, None, 53, 54, 55, 56, None, None, None]])

def getPos(IDPoint):
    y, x = np.where(pointShape == IDPoint)
    return int(y),int(x)

def getNeighbours(IDPoint, flat=True):
    x,y= getPos(IDPoint)
    # The algorithm seems to fail for certain edge cases, values were filled
    # manually but this isn't ideal, fix ASAP
    NClose = pointShape[x-1:x+2, y-1:y+2]
    if IDPoint == 1:
        NClose = np.array([[None, None, None], [None, 1, 2],[None, 3, 4]])
    if IDPoint == 2:
        NClose = np.array([[None, None, None], [1,2,None], [3,4,None]]) #Manually fixed the upper points
    if IDPoint == 19:
        NClose = np.array([[None, None, 11], [None, 19, 20], [None, 29, 30]])
    if IDPoint == 29:
        NClose = np.array([[None, 19, 20], [None, 29, 30], [None, None, 39]])
    if flat:
        NClose = NClose.flatten()
        NClose = list(NClose[NClose != np.array(None)])
        NClose.remove(IDPoint)
    return NClose

def buildAvgGraph(listGraph):
    listDic=[]
    for graph in listGraph:
        coordDict = nx.get_node_attributes(graph, 'pos')
        listDic.append(coordDict)

    dicVal = {}
    missingValues = []
    for i in range(1,57):
        listVal = []
        n=-1
        for dic in listDic:
            n+=1
            try:
                val = dic[i]
                listVal.append(val)
            except KeyError as e:
                missingValues.append(i)
                print(e, str(listGraph[n]))
                continue
        dicVal[i] = listVal
    #
    # dicList = {k:[ listDic[j][k] for j in range(len(listDic)) ] for k in listDic[0].keys()}
    T = {k:( functools.reduce(np.add, v)/len(v) ) for k,v in dicVal.items()}
    avgGraph = nx.Graph()

    # print(set(missingValues), [str(x) for x in listGraph])

    for i in set(missingValues):
        del T[i]

    for i in T.keys():
        avgGraph.add_node(i, pos = T[i])

    for i in listDic[0].keys():
        for j in getNeighbours(int(i)):
            try:
                iCoord = T[i]
                jCoord = T[j]
                distance = np.linalg.norm(np.array(iCoord)-np.array(jCoord))
                avgGraph.add_edge(i,j, dist=distance)
            except KeyError:
                continue
    return avgGraph

def plotSensorGraph(graphList):
    data = []
    for graph in graphList:
        dicPos = nx.get_node_attributes(graph, 'pos')
        xList = [i[0] for i in list(dicPos.values())]
        yList = [i[1] for i in list(dicPos.values())]
        zList = [i[2] for i in list(dicPos.values())]

        trace = go.Scatter3d(
        x=xList,
        y=yList,
        z=zList,
        mode='markers',
        marker=dict(
            size=12,
            line=dict(
                width=0.5
            ),
            opacity=0.8
                )
            )
        data.append(trace)


    layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),)

    fig = go.Figure(data=data, layout=layout)
    plot(fig, filename='ayyy.html')

def buildDeltaGraph(baseGraph, subjectGraph):
    deltaGraph = nx.Graph()

    baseGraphDist = nx.get_edge_attributes(baseGraph, 'dist')
    subjGraphDist = nx.get_edge_attributes(subjectGraph, 'dist')

    s1 = set(nx.nodes(baseGraph))
    s2 = set(nx.nodes(subjectGraph))

    pointList = s1.intersection(s2)

    for i in pointList:
        deltaGraph.add_node(i)

    for key in baseGraphDist.keys():
        try:
            relativeDistance = (subjGraphDist[key]-baseGraphDist[key])/(baseGraphDist[key])
            deltaGraph.add_edge(*key, rDist = relativeDistance)
        except:
            continue

    return deltaGraph

def plotDeltaGraph(graph, title, returnData=False):
    def getColor(dist):
        if dist > 0:
            red=224 - (224-49)*dist
            green =243 - (243-54)*dist
            blue =248- (248-149)*dist
        else:
            red = 253 + (253 - 165)*dist
            green = 174 +(174 - 0)*dist
            blue = 97 + (97 - 38)*dist
        return red,green,blue
    xNodes = []
    yNodes = []
    relative = True

    for i in graph.nodes():
        y, x = getPos(i)
        xNodes.append(x)
        yNodes.append(-y)

    rDist = nx.get_edge_attributes(graph, 'rDist')

    mDist = max(rDist.values())
    maxThick = 7
    data = []

    for i in graph.edges():
        dist = rDist[i]
        t = (dist)/mDist
        r,g,b = getColor(t)
        t = (np.sqrt(np.abs(t)))*maxThick #we use a square root to reduce thickness difference and better show color diff.
        edge_trace = go.Scatter(
                                x=[],
                                y=[],
                                line=go.Line(width=t, color="rgb({},{},{})".format(r,g,b)),
                                hoverinfo='none',
                                mode='lines')

        y0, x0 = getPos(i[0])
        y1, x1 = getPos(i[1])
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [-y0, -y1, None]
        data.append(edge_trace)

    trace0 = go.Scatter(
        x = xNodes,
        y = yNodes,
        name = 'Sensor',
        mode = 'markers',
        marker = dict(
            size = 10,
            color = 'rgba(100, 100, 100, .8)',
            line = dict(
                width = 2,
                color = 'rgba(0, 0, 0, .8)'
            )))
    data.append(trace0)

    if not returnData:
        layout = go.Layout(
            title=title,
            showlegend=False,
            hovermode= 'closest',
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                autotick=True,
                ticks='',
                showticklabels=False
            ))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename='graphs/'+str(title)+'.html')
    else:
        return data
