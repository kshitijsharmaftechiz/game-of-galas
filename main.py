from flask import Flask, render_template
from flask_socketio import SocketIO
import numpy as np

# Graph
# from collections import defaultdict 
# class Graph: 
#     def __init__(self): 
#         self.graph = defaultdict(list) 

#     def addEdge(self,u,v): 
#         self.graph[u].append(v) 
  
#     def BFS(self, s): 
  
#         visited = [False] * (len(self.graph)) 
#         queue = [] 
#         queue.append(s) 
#         visited[s] = True
  
#         while queue: 
#             s = queue.pop(0) 
#             print (s, end = " ") 
  
#             for i in self.graph[s]: 
#                 if visited[i] == False: 
#                     queue.append(i) 
#                     visited[i] = True

# End Graph


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

slots = list()
slots.append(list())
slotnumber = 0
currentturn = 0

w, h = 30, 30
RedMatrix = [[0 for x in range(w)] for y in range(h)]
BlueMatrix = [[0 for x in range(w)] for y in range(h)]

# def findredwin():
#     global RedMatrix
#     g = Graph()
#     for i in range(0, 30):
#         for j in range(0, 30):
#             if(RedMatrix[i][j] == 1):
#                 g.addEdge(i, j)

#     print("BFS")
#     try:
#         g.BFS(0)
#         g.BFS(1)
#         g.BFS(2)
#         g.BFS(3)
#         g.BFS(4)
#         g.BFS(5)
#     except:
#         pass




@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('init')
def init_game(json, methods=['GET', 'POST']):
    global slots, slotnumber, currentturn
    print(slotnumber)
    print("initializing game: " + str(json))
    if len(slots[slotnumber]) == 2:
        slotnumber = slotnumber + 1
        slots.append(list())

    if len(slots[slotnumber]) == 0:
        data = {
            "playid": json["playid"],
            "playcolor": "RED",
            "slotindex": 0,
            "slotnumber": slotnumber,
            "currentturn": currentturn
        }
        slots[slotnumber].append(data)
    elif len(slots[slotnumber]) == 1:
        data = {
            "playid": json["playid"],
            "playcolor": "BLUE",
            "slotindex": 1,
            "slotnumber": slotnumber,
            "currentturn": currentturn
        }
        slots[slotnumber].append(data)

    print()
    print(slots)
    print()
    print("Responding " + str(data))
    socketio.emit("inited", data)


@socketio.on("move")
def make_move(json, methods=['GET', 'POST']):
    print("make move " + str(json))
    playid = json["playid"]
    slotnumber = json["slotnumber"]
    slotindex = json["slotindex"]
    playcolor = json["playcolor"]
    line = json["line"]

    if slotindex == 0:
        slotindex = 1
    else: 
        slotindex = 0

    point1 = json["dots"]["p1"]
    point2 = json["dots"]["p2"]

    if(playcolor == "RED"):
        RedMatrix[point1-1][point2-1] = 1
        RedMatrix[point2-1][point1-1] = 1
    
    if(playcolor == "BLUE"):
        BlueMatrix[point1-1][point2-1] = 1
        BlueMatrix[point2-1][point1-1] = 1
    
    # isredwinner = findredwin()
    # print(isredwinner)

    playid = slots[slotnumber][0]["playid"]

    data = {
        "playid": playid,
        "slotnumber": slotnumber,
        "slotindex": slotindex,
        "playcolor": playcolor,
        "line": line
    }

    socketio.emit("moved", data)


if __name__ == '__main__':
    socketio.run(app, debug=True)