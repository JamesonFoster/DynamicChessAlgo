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
        self.time = 0
        self.ghosts = 2
        self.queues = {} # dictionary that holds queues for each road
        IntSect.intersections.append(self) # for every intersection created add it to the total count

    def getTime(self, car):
        return self.time

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


#************************************************Roundabout**********************************************
class RoundAbt(IntSect): #remove AStar. once combined
    def __init__(self, name, x, y):
        
        super().__init__(name, x, y)

        self.ghosts = 2
        self.speed = 15 #mph
        self.use = 0

    def getConnOrder(self):
        self.connections.sort(key = self.Order)

    def Order(self, connection): # return the degree of a node WRT another node
        
        x1 = self.x
        y1 = self.y
        x2 = connection.getOther(self).x
        y2 = connection.getOther(self).y

        r = ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)
        theta = math.degrees(math.acos((x2-x1)/r)) 
        print(f"theta: {theta}")
        return theta
    
    def spawnGhosts(self):
        ghosts = 0

        ghosts *= self.use

        return ghosts
    def getTime(self, car):
        self.use += 1
        self.ghosts = self.spawnGhosts()
        
        Csource = car.path[car.path.index(self) - 1] # index of the previous intersection in path
        
        #cars cannot have roundabouts as destination
        Cdest = car.path[car.path.index(self) + 1] # index of the next intersection in path

        for road in self.connections:
                if road.getOther(self) == Csource: #get road that car came from
                    CsourceRoad = road
                if road.getOther(self) == Cdest: #get road car is going to
                    CdestRoad = road

        for _ in range(self.ghosts):
            #Gsource = random.randint(1, len(self.connections)) # cars may enter roundabout to turn around so source can equal destination
            Gdest = ran.randint(1,len(self.connections)) # each ghost car gets a random destination road
            
            
            if self.connections[Gdest] == CdestRoad: # if the ghost car's destination is same as car's at this node
                self.time += ((5/60)/60) # add 5 seconds for yeild
            
        
        ord = self.Order(CdestRoad)
        print(ord)
        
        dist = (ord/360) * 2*math.pi * 0.0094697 #50 ft radius, the arc length the car travels in the roundabout
        if ord == 0:
            dist = math.pi * 0.0094697 # going straight so half of the roundabout is driven
            
        delay = dist/self.speed #delay in hours
        
        self.time += delay

        return self.time
#*****************************************************************************************************


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
                for I in self.path:
                    
                    self.time += I.getTime(car = self)
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
readmode = 0  # 0 = roads, 1 = intersections, 2 = cars
fc = 0 
rtemp = []
itemp = []

with open("test.txt", "r") as file:
    for line in file:
        li = line.strip()
        if li == "----Intersect----":
            readmode = 1
            fc = 0
            continue
        elif li == "----Cars----":
            readmode = 2
            fc = 0
            continue
        # Roads
        if readmode == 0:
            if fc == 0:
                dp1 = int(li)
            elif fc == 1:
                dp2 = int(li)
            elif fc == 2:
                dp3 = li
            elif fc == 3:
                dp4 = li.lower() == "true"
                newroad = Road(dp1, dp2, dp3, dp4)
                print(f"{newroad.name} created")
                rtemp.append(newroad)
                fc = -1
            fc += 1
        # Intersections
        elif readmode == 1:
            if li == "--stop--":
                fc = 0
                continue
            if fc == 0:
                dp1 = li
            elif fc == 1:
                dp2 = int(li)
            elif fc == 2:
                dp3 = int(li)
                newint = IntSect(dp1, dp2, dp3)
                itemp.append(newint)
            elif fc >= 3:
                conn = None
                for i in rtemp:
                    if i.name == li:
                        conn = i
                        break
                if conn:
                    newint.makeConnect(conn)
                    print(f"{newint.name} connected to {conn.name}")
                else:
                    print("Error No connection for", li)
            fc += 1
        # Cars
        elif readmode == 2:
            if fc == 0:
                conn1 = None
                for i in itemp:
                    if i.name == li:
                        conn1 = i
                        break
                if conn1:
                    newCar = Car(conn1)
                else:
                    print("ERROR NO CONNECTION")
            elif fc == 1:
                conn2 = None
                for i in itemp:
                    if i.name == li:
                        conn2 = i
                        break
                if conn2:
                    newCar.goTarget(conn2)
                    newCar.traverse()
                else:
                    print("ERROR NO CONNECTION")
            fc = (fc + 1) % 2

runtime = time.time()
print(f"Time: {runtime - starttime:.6f} seconds\n")