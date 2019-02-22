from flask import Flask, render_template
from flask_socketio import SocketIO
import numpy as np

# Graph
from collections import defaultdict 
class Graph: 
    def __init__(self): 
        self.graph = defaultdict(list) 

    def addEdge(self,u,v): 
        self.graph[u].append(v) 
  
    def BFS(self, s, color): 
  
        visited = [False] * 31
        queue = [] 
        queue.append(s) 
        visited[s] = True
  
        while queue: 
            s = queue.pop(0)
            # print (s, end = " ") 
            if color == "red":
                if s == 6 or s == 12 or s == 18 or s == 24 or s == 30:
                    return True

            if color == "blue":
                if s == 26 or s == 27 or s == 28 or s == 29 or s == 30:
                    return True
  

            for i in self.graph[s]: 
                if visited[i] == False: 
                    queue.append(i) 
                    visited[i] = True
        # print(" ")
        return False

redgraph = Graph()
bluegraph = Graph()
# End Graph


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

slots = list()
slots.append(list())
slotnumber = 0
currentturn = 0
haswinner = False

def findredwin():
    global haswinner
    try:
        if redgraph.BFS(1, "red") or redgraph.BFS(7, "red") or redgraph.BFS(13, "red") or redgraph.BFS(19, "red") or redgraph.BFS(25, "red"):
            haswinner = True
            return True    
    except:
        pass
    return False

def findbluewin():
    global haswinner
    try:
        if bluegraph.BFS(1, "blue") or bluegraph.BFS(2, "blue") or bluegraph.BFS(3, "blue") or bluegraph.BFS(4, "blue") or bluegraph.BFS(5, "blue"):
            haswinner = True
            return True    
    except:
        pass
    return False




@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('init')
def init_game(json, methods=['GET', 'POST']):
    global slots, slotnumber, currentturn, redgraph, bluegraph
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

    redgraph = Graph()
    bluegraph = Graph()
    socketio.emit("inited", data)


@socketio.on("move")
def make_move(json, methods=['GET', 'POST']):
    global haswinner
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
        redgraph.addEdge(point1, point2)
    
    if(playcolor == "BLUE"):
        bluegraph.addEdge(point1, point2)
    
    isredwinner = findredwin()
    print("red ", isredwinner)
    if haswinner and isredwinner:
        socketio.emit("WIN", {
            "message": "RED WINS",
            "player": "RED"
        })
        return
    
    isbluewinner = findbluewin()
    print("blue ", isbluewinner)
    print("has winner ", haswinner)
    if haswinner and  isbluewinner:
        socketio.emit("WIN", {
            "message": "BLUE WINS",
            "player": "BLUE"
        })
        return

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