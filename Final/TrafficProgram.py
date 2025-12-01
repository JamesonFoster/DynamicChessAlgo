import math
import time
import random as ran
import turtle as turt
import os


#path = str(os.getcwd())


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
        self.lastUse = time.time()
        self.deltaTuse = 0
    def getConnOrder(self):
        self.connections.sort(key = self.Order)
    def Order(self, node): # return the degree of a node WRT another node
        if node != None:
            x1 = self.x
            y1 = self.y
            x2 = node.x
            y2 = node.y
            r = ((x2 - x1)**2 + (y2 - y1)**2)**(1/2)
            theta = math.degrees(math.acos((x2-x1)/r))            
            return theta
        else:
            return -1
    def spawnGhosts(self, new):
        m = new - self.lastUse
        if m < self.deltaTuse:
            ghosts = self.ghosts + self.ghosts* math.ceil(new - self.lastUse) 
        #percentage of ghosts based on time since last use
        else:
            ghosts = self.ghosts - self.ghosts* math.ceil(new - self.lastUse) 
        return ghosts + 1
    def getTime(self, car):
        newUse = time.time()
        #print(len(self.connections))
        self.ghosts = self.spawnGhosts(newUse)
        #update time difference since last use
        self.deltaTuse = newUse - self.lastUse
        #update time of last use
        self.lastUse = newUse
        temp = car.path[car.path.index(self)] 
        if temp == car.path[-1]: #if temp is equal to last node in path
            Cdest = temp #the car destination is the current node
        else:
            Cdest = car.path[car.path.index(self) + 1] #the car destination is the next node
        for _ in range(self.ghosts):
            Gdest = ran.randint(0,len(self.connections)-1) # each ghost car gets a random destination road
            if self.connections[Gdest].getOther(self) == Cdest: # if the ghost car's destination is same as car's at this node
                self.time += ((5/60)/60) # add 5 seconds for yeild
        ord = self.Order(Cdest)     
        dist = (ord/360) * 2*math.pi * 0.0094697 #50 ft radius, the arc length the car travels in the roundabout
        if ord == 0:
            dist = math.pi * 0.0094697 # going straight so half of the roundabout is driven
        elif ord < 0:
            dist = 0
        delay = dist/self.speed #delay in hours
        self.time += delay
        return self.time
#*****************************************************************************************************
#==============================================4 Way Stop=============================================
class StopFour(IntSect):
    # Position order to check for right car
    POSITION_ORDER = ['North', 'East', 'South', 'West']
    def __init__(self, name, x, y):
        self.name = name
        self.time = 0
        self.x = x # position on x
        self.y = y #position on y
        self.connections = []
        self.queues = {}
        self.is_stop_sign_controlled = True
        self.ghosts = 2
        self.lastUse = time.time()
        self.deltaTuse = 0

    def traffic_control(self):
        #Overrides the parent method to specify the type of control.
        return
    def determine_order_of_entry(self, simultaneous_cars):
        if not simultaneous_cars:
            return "No cars stopped.", []
        if len(simultaneous_cars) == 1:
            return f"Only one car ({simultaneous_cars[0]}). It goes first.", []
        print(f"\n Order for simultaneous arrival: {simultaneous_cars}")
        #Map car positions to their index in the defined order (0-3)
        car_indices = {pos: self.POSITION_ORDER.index(pos) for pos in simultaneous_cars}
        # Find the car that has no other simultaneous car to its immediate right
        #This car is the one that goes first.
        goes_first = None
        for current_car, current_index in car_indices.items():
            # Calculate the index of the car to the right
            right_index = (current_index + 1) % len(self.POSITION_ORDER)
            car_to_right = self.POSITION_ORDER[right_index]
            # If the car to the right is NOT among the simultaneous cars, then the current_car has the right-of-way.
            if car_to_right not in simultaneous_cars:
                goes_first = current_car
                break # Dis da boi
        # Handle the edge case where all four cars stop at the same time
        if goes_first is None and len(simultaneous_cars) == 4:
            return "All cars stopped at the same time, one must go first", []
        if goes_first:
            remaining_cars = [car for car in simultaneous_cars if car != goes_first]
            return f"{goes_first} goes first (No car to its right).", remaining_cars
        else:
            # Should only happen if there's a problem with the logic, but included as a guard. Hopefully :)
            return "Could not determine the order based on the 'car to the right' rule.", simultaneous_cars
    def spawnGhosts(self, new):
        m = new - self.lastUse
        if m < self.deltaTuse:
            ghosts = self.ghosts + self.ghosts* math.ceil(new - self.lastUse) 
        #percentage of ghosts based on time since last use
        else:
            ghosts = self.ghosts - self.ghosts* math.ceil(new - self.lastUse) 
        return ghosts + 1
    def getTime(self, car):
        newUse = time.time()
        #print(len(self.connections))
        self.ghosts = self.spawnGhosts(newUse)
        #update time difference since last use
        self.deltaTuse = newUse - self.lastUse
        #update time of last use
        self.lastUse = newUse
        temp = car.path[car.path.index(self)] 
        if temp == car.path[-1]: # If temp is equal to last node in path
            Cdest = temp # The car destination is the current node
        else:
            Cdest = car.path[car.path.index(self) + 1] # The car destination is the next node
        for _ in range(self.ghosts):
            Gdest = ran.randint(0,len(self.connections)-1) # Each ghost car gets a random destination road
            if self.connections[Gdest].getOther(self) == Cdest: # If the ghost car's destination is same as car's at this node
                self.time += ((5/60)/60) # Add 5 seconds for stop
        return self.time
# Traffic light class
class traffic_light(IntSect):
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x # position on x
        self.y = y #position on y
        self.connections = []  # list of Roads that this intersection connects to
        self.ghosts = 2
        self.queues = {} # dictionary that holds queues for each road
        self.chancetime = 0.05
        self.time = (ran.random() * self.chancetime)
    def getTime(self, car):
        self.time = (ran.random() * self.chancetime)
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
    cars =set()
    def __init__(self, startpos):
        self.pos = startpos
        self.location = startpos
        self.time = 0
        self.path = None
        Car.cars.add(self)
    def traverse(self):
        print(f'-------------- Trip Summary --------------')
        if self.path != None:
            for I in self.path:                                          # for each road in the set path
                if I != None:
                    self.location.travel_road(self.location, I)         # Move car from its current intersection to the next via provided road
                    self.location = I                                   # Set the new road as it's current position
        print(self.path)
        print("DONE!")
        print(f'Time to complete: {get_text_time(self.time)}')
    def est(self, currpos, target): # estimates distance to target from current pos
        if currpos is None or target is None:
            return float('inf')
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
xmax = 0
xmin = 0
ymax = 0
ymin = 0
rtemp = []
itemp = []
with open( "test.txt", "r") as file:
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
                dp1 = float(li)
            elif fc == 1:
                dp2 = float(li)
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
                dp1 = li #name
            elif fc == 1:
                dp2 = float(li) #x point
            elif fc == 2:
                dp3 = float(li) # y point
            elif fc == 3:
                dp4 = int(li) # type
                if dp4 == 2:
                    newint = StopFour(dp1,dp2,dp3)
                elif dp4 == 1:
                    newint = RoundAbt(dp1, dp2, dp3)
                elif dp4 == 3:
                    newint = traffic_light(dp1,dp2,dp3)
                else:
                    newint = IntSect(dp1, dp2, dp3)
                itemp.append(newint)
            elif fc >= 4:
                conn = None
                for i in rtemp:
                    if i.name == li:
                        conn = i
                        break
                if conn:
                    if xmax < dp2:
                        xmax = dp2
                    elif xmin > dp2:
                        xmin = dp2
                    if ymax < dp3:
                        ymax = dp3
                    elif ymin > dp3:
                        ymin = dp3
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


'''
#Visual Stuff (Turtle Edition)
turt.speed(999999)
turt.hideturtle()
screen = turt.Screen()
winhei = ((ymax - ymin) + 5)
winwid = ((xmax - xmin) + 5)
staty = (ymax + ymin) / 2
statx = (xmax + xmin) / 2
turt.Screen = screen
screen.setworldcoordinates(xmin - 5,ymin - 5,xmax + 5,ymax + 5)
screen.tracer(0)

for i in itemp:
    turt.up()
    turt.setposition(i.x,i.y)
    turt.dot(9)
for i in rtemp:
    turt.width(3)
    if i.conn1 != None:
        getx1 = i.conn1.x
        gety1 = i.conn1.y
    if i.conn2 != None:
        getx2 = i.conn2.x
        gety2 = i.conn2.y
    turt.setposition(getx1,gety1)
    turt.down()
    turt.setposition(getx2,gety2)
    turt.up()

screen.update()
runtime = time.time()
print(f"Time: {runtime - starttime:.6f} seconds\n")
stoper = input("Press Enter when Finished: ")'''