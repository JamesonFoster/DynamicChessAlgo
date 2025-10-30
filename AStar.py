import math
import time
import random as ran

class IntSect: #different name for vertex
    intersections = []  
    def __init__(self, name, x=0, y=0): #set up vertex
        self.name = name
        self.x = x # position on x
        self.y = y #position on y
        self.connections = []  # list of Roads that this intersection connects to
        self.queues = {} # dictionary that holds queues for each road
        IntSect.intersections.append(self) # for every intersection created add it to the total count

    def makeConnect(self, road):
        self.connections.append(road) #adds road to its list of connections
        if road.conn1 is None: #will determain which connection to make to the road
            road.conn1 = self  #because the road can only have 2 connections
        else:                  #connection 1 for roads will always be the primary 
            road.conn2 = self  #connection and 2 will default always if 1 is filled
        self.queues[road] = Queue()

    def travel_road(self, start, heading):  
        if heading in self.connections and start in self.connections:   # Checks to see if selected road is connected here
            selected_car = self.queues[start].dequeue()                 # Get car traveling and dequeue it from this intersection
            if not heading.Oneway or self == heading.A:                 # Checks if the road is actually travelable
                if selected_car != None:                                # checks to make sure there are cars present
                    print(f'{selected_car.name} leaving {self} heading down {heading.name} (is one way: {heading.Oneway}) (Traverse Time: {get_text_time(heading.time)})')
                    heading.travel(self, selected_car)                  # sends the car down the road to the next intersection
            else:
                print(f'Debug: {selected_car.name} tried to go down a oneway (Road: {heading.name})!')  # ADD ERROR HANDLING HERE!!      
    
    # Method that spawns/moves cars at intersections
    def add_car(self, road, car):   
        if road in self.queues:             # Checks if the road is actually connected to this intersection
            self.queues[road].enqueue(car)  # Adds cars to the queue of the selected road
            car.location = self             # Sets car's current location to this intersection
            delay = self.type.getwait(car)
            car.add_time(delay)            
            print(f' {car.name} arrived at intersection {self.name} DELAY: {delay * 3600} seconds')
        else:
            print("Debug: Road not connected to target intersection!")
            
    @classmethod
    def get_nodes(cls):
        return cls.intersections
        
    def __repr__(self):
        return f"Intersection({self.name})"

class Road: #different name for edge
    def __init__(self, length, speed, name, Oneway=False):
        self.len = length
        self.spe = speed
        self.wei = length / speed  # calculates weight of travel automatically
        self.conn1 = None # primary connection
        self.conn2 = None # secondary connection
        self.name = name
        self.Oneway = Oneway  

    def getOther(self, current):
        return self.conn2 if self.conn1 == current else self.conn1
    
    def travel_road(self, start, heading):  
        if heading in self.connections and start in self.connections:   # Checks to see if selected road is connected here
            selected_car = self.queues[start].dequeue()                 # Get car traveling and dequeue it from this intersection
            if not heading.Oneway or self == heading.A:                 # Checks if the road is actually travelable
                if selected_car != None:                                # checks to make sure there are cars present
                    print(f'{selected_car.name} leaving {self} heading down {heading.name} (is one way: {heading.Oneway}) (Traverse Time: {get_text_time(heading.time)})')
                    heading.travel(self, selected_car)                  # sends the car down the road to the next intersection
            else:
                print(f'Debug: {selected_car.name} tried to go down a oneway (Road: {heading.name})!')  # ADD ERROR HANDLING HERE!!

class Car: #main interactive object
    def __init__(self, startpos):
        self.pos = startpos
        self.location = startpos
        self.time = 0
        self.path = None

    def traverse(self):
        print(f'-------------- Trip Summary --------------')
        for I in self.path:                                          # for each road in the set path
            self.location.travel_road(self.location, I)         # Move car from its current intersection to the next via provided road
            self.location = I                                   # Set the new road as it's current position
        print(self.path)
        print("DONE!")
        print(f'Time to complete: {get_text_time(self.time)}')

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
            #finds the node in toExp with the best f_score
            current = min(toExp, key=lambda node: f_score.get(node, float('inf')))

            if current == target: #if the current position is == to target
                # Reconstruct the path
                path = []
                while current in came_from:
                    prev, road = came_from[current]
                    path.append(current)
                    self.time += road.wei
                    current = prev
                path.reverse() # reverses the path so its in actual order
                self.path = path
                return f'Time to get there: {self.time * 60} minutes.'

            toExp.remove(current)
            self.time = 0

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

def get_text_time(time):
    hours = time
    minutes = (time * 60) % 60
    seconds = (time * 3600) % 60
    return ("%d:%02d:%02d" % (hours, minutes, seconds)) 
    # Queue using FIFO
class Queue:
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        return self.items.pop(0) if self.items else None
    def __len__(self):
        return len(self.items)
    def __repr__(self):
        return f"Queue({self.items})"
        

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
for i in range(1000):
    car = Car(i4)
    lister.append(car)

setuptime = time.time()
print(f"Time: {setuptime - starttime:.6f} seconds\n")
# Find path to Target
for i in lister:
    i.goTarget(it)
    i.traverse()
runtime = time.time()
print(f"Time: {runtime - setuptime:.6f} seconds\n")