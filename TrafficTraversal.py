import time
import random

class Car:
    def __init__(self, start, temporary, name):
        self.name = name                                        # name of car 
        self.location = start                                   # Intersection the car starts on
        self.position = start.connections[0]                    # road the car is starting on
        self.time = 0                                           # Keeps track of total travel time 
        self.location.add_car(self.position, self)              # initializes the car on the intersection and start location
        self.path = temporary
        self.traverse(self.path)                                # Move the car down the traversal path
        
    # Method to add time to current travel time
    def add_time(self, time):
        self.time += time
        
    # Traverse the provided path
    def traverse(self, path):
        print(f'-------------- {self.name} Trip Summary --------------')
        for I in path:                                          # for each road in the set path
            self.location.travel_road(self.position, I)         # Move car from its current intersection to the next via provided road
            self.position = I                                   # Set the new road as it's current position
        print("DONE!")
        print(get_text_time(self.time))


# Intersection class
class Intersection:
    intersections = []                                          # Array to keep track of count of all intersections

    def __init__(self, name, type, X, Y):
        self.Xpos = X
        self.Ypos = Y
        self.type = type
        self.name = name                                        # name of intersection
        self.connections = []                                   # array of roads connected
        self.queues = {}                                        # dictionary that holds queues for each road
        Intersection.intersections.append(self)                 # for every intersection created add it to the total count

    # Attach a road to the node
    def add_road(self, road):  
        self.connections.append(road)                           # Append the road to the array of connected roads
        self.queues[road] = Queue()                             # Create a queue for cars coming from this road
        
    # Method that sends cars from start roads queue down the road to the next intersection
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
        

# Road class
class Road:
    def __init__(self, speed_limit, length, Oneway=False, name=""):
        self.name = name                    # name of road
        self.time = length / speed_limit    # time to travel in HH.HHH
        self.Oneway = Oneway                # is the road one way?
        self.A = None                       # Both of these are used to store the intersections at each end of the road
        self.B = None                       # Initially set as None until the connect method is run
        
    # Moves cars from one intersection to the next by adding it to the targeted intersection's queue
    def travel(self, start, car):
        if start == self.A:             # Checks if intersection A called this function
            self.B.add_car(self, car)   # Adds car to intersection B
        if start == self.B:             # Checks if intersection B called this function
            self.A.add_car(self, car)   # Adds car to intersection A
        car.add_time(self.time)         # Add traverse time to selected car's total travel time

    # Method that connects ends of roads to the intersections
    def connect(self, IntersectionA, IntersectionB):
        self.A = IntersectionA
        self.B = IntersectionB
        IntersectionA.add_road(self)
        IntersectionB.add_road(self)
        
    def __repr__(self):
        return f"Road({self.name}, oneway={self.Oneway})"


# Traffic light class
class traffic_light:
    def __init__(self, time, randomization=True):
        self.waittime = time
        if randomization:
            self.random_initial_time = random.randrange(0, self.waittime)
        else:
            self.random_initial_time = 0
        
    def getwait(self, car):
        arrival = car.time * 3600
        state_changes = (arrival + self.random_initial_time) / self.waittime
        if int(state_changes) % 2 == 0:
            remaining = state_changes % 1 * self.waittime
            return remaining / 3600
        else:
            return 0
            

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


# Converts HH.HHH float to HH:MM:SS string
def get_text_time(time):
    hours = time
    minutes = (time * 60) % 60
    seconds = (time * 3600) % 60
    return ("%d:%02d:%02d" % (hours, minutes, seconds)) 


# ---------------- Example Simulation ----------------
starttime = time.time()

# Create Intersections
A = Intersection("A", traffic_light(60), 0, 0)
B = Intersection("B", traffic_light(60), 0, 0)
C = Intersection("C", traffic_light(60), 0, 0)
D = Intersection("D", traffic_light(60), 0, 0)
E = Intersection("E", traffic_light(60), 0, 0)

# Create roads 
R1 = Road(speed_limit=60, length=1.9, Oneway=False, name="Main Street")
R2 = Road(speed_limit=60, length=4.1, Oneway=False, name="Ridgeview")
R3 = Road(speed_limit=20, length=3.2, Oneway=False, name="Edgefield")
R4 = Road(speed_limit=60, length=1.9, Oneway=False, name="Tanglewood")
R5 = Road(speed_limit=60, length=4.1, Oneway=False, name="Willow Street")
R6 = Road(speed_limit=20, length=3.2, Oneway=False, name="SunnyMeadows")
R7 = Road(speed_limit=20, length=3.2, Oneway=False, name="Grafton")

# Connect Roads and Intersections
R1.connect(A, C)
R2.connect(A, B)
R3.connect(C, D)
R4.connect(D, B)
R5.connect(D, A)
R6.connect(D, E)
R7.connect(E, A)

setuptime = time.time()

# Add a car at intersection A
car1 = Car(A, [R2, R4, R5, R1, R3, R6], "steve")

print(f"Time: {setuptime - starttime:.6f} seconds\n")
