import math
import time
import random as ran

class IntSect: #different name for vertex
    def __init__(self, name, x=0, y=0): #set up vertex
        self.name = name
        self.x = x # position on x
        self.y = y #position on y
        self.connections = []  # list of Roads that this intersection connects to

    def makeConnect(self, road):
        self.connections.append(road) #adds road to its list of connections
        if road.conn1 is None: #will determain which connection to make to the road
            road.conn1 = self  #because the road can only have 2 connections
        else:                  #connection 1 for roads will always be the primary 
            road.conn2 = self  #connection and 2 will default always if 1 is filled

class Road: #different name for edge
    def __init__(self, length, speed, name):
        self.len = length
        self.spe = speed
        self.wei = length / speed  # calculates weight of travel automatically
        self.conn1 = None # primary connection
        self.conn2 = None # secondary connection
        self.name = name

    def getOther(self, current):
        return self.conn2 if self.conn1 == current else self.conn1

class Car: #main interactive object
    def __init__(self, startpos):
        self.pos = startpos

    def est(self, currpos, target): # estimates distance to target from current pos
        dx = currpos.x - target.x
        dy = currpos.y - target.y
        distance = math.sqrt((dx*dx) + (dy*dy))
        max_speed = 100  # Assume 100 miles is max
        return distance / max_speed

    def goTarget(self, target):
        toExp = [self.pos]  # list of nodes to explore
        came_from = {}         # for reconstructing path

        g_score = {self.pos: 0} 
        f_score = {self.pos: self.est(self.pos, target)}

        while toExp:
            #finds the node in toExp with the lowest f_score
            current = min(toExp, key=lambda node: f_score.get(node, float('inf')))

            if current == target: #if the current position is == to target
                # Reconstruct the path
                path = []
                while current in came_from:
                    prev, road = came_from[current]
                    path.append((road.name, current.name))
                    weiRec += road.wei
                    current = prev
                path.reverse() # reverses the path so its in actual order
                return f'{path}. Time to get there: {weiRec * 60} minutes.'

            toExp.remove(current)
            weiRec = 0

            for road in current.connections:
                neighbor = road.getOther(current)
                tent_g = g_score[current] + road.wei

                if neighbor not in g_score or tent_g < g_score[neighbor]:
                    came_from[neighbor] = (current, road)
                    g_score[neighbor] = tent_g
                    f_score[neighbor] = tent_g + self.est(neighbor, target)

                    if neighbor not in toExp:
                        toExp.append(neighbor)

        return None  # there is not a path able to get to target
        

# -------------------------
# Map setup with coordinates
# -------------------------
starttime = time.time()
# Roads
r1 = Road(5, 60, "ChillBurger Street")      # 5/60 = 0.0833 hr
r2 = Road(6, 60, "uuJi")                    # 6/60 = 0.1 hr
r3 = Road(1, 1, "1 Mine Stopped")           # 1/1 = 1 hr
r4 = Road(10, 75, "Life is a Highway")      # 10/75 = 0.1333 hr
r5 = Road(4, 40, "45454Road")               # 4/40 = 0.1 hr

# Intersections with (x, y) positions
i1 = IntSect("i1", 0, 0)
i2 = IntSect("i2", 5, 0)
i3 = IntSect("i3", 10, 0)
i4 = IntSect("i4", -5, 0)
it = IntSect("Target", 14, 0)  # Destination

# Connect roads to intersections
i1.makeConnect(r1) # i1 to chillburger
i2.makeConnect(r1) # i2 to chillburger

i3.makeConnect(r2) # i3 to uuJi
i2.makeConnect(r2) # i2 to uuJi

i3.makeConnect(r5) # i3 to 45454
it.makeConnect(r5) # Target to 45454

i1.makeConnect(r3) # i1 to 1 Mine
i4.makeConnect(r3) # i4 to 1 Mine

i1.makeConnect(r4) # i1 to Life
i3.makeConnect(r4) # i3 to Life

# Car starts at i4
lister = []
j = 0
for i in range(10):
    j = ran.randrange(0,4)
    if j <= 1:
        car = Car(i1)
    elif j <= 2:
        car = Car(i2)
    elif j <= 3:
        car = Car(i3)
    else:
        car = Car(i4)
    lister.append(car)

setuptime = time.time()
print(f"Time: {setuptime - starttime:.6f} seconds\n")
# Find path to Target
for i in lister:
    print(i.goTarget(it))
runtime = time.time()
print(f"Time: {runtime - setuptime:.6f} seconds\n")