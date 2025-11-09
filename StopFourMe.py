import time
import random
from AStar import IntSect, Road, Car
#Four way stop sign class.
class StopFourMe(IntSect):
    def __init__(self, name, x=0, y=0):
        super().__init__(name, x, y)
        self.time = .5
        self.ghosts = 3
    #logic for four-way stop delay
    def getTime(self, car):
        for i in range(self.ghosts):
            Gdest = random.randint(1,len(self.connections)) # each ghost car gets a random destination road

            Csource = car.path[car.path.index(self) - 1] # index of the previous intersection in path
            Cdest = car.path[car.path.index(self) + 1] # index of the next intersection in path

            for road in self.connections:
                if road.getOther(self) == Csource: #get road that car came from
                    CsourceRoad = road
                if road.getOther(self) == Cdest: #get road car is going to
                    CdestRoad = road
    def multi_arrival(self):
        c1 = car
        #c2 = ghostCar
        #c3 = ghostCar
        #c4 = ghostCar
    
    def the_slow_down(self, car_stopping, road_stopping_on): #Takes the car stopping "Your car" 
        cars_ahead_count = 0 
        
        #Count the total number of cars waiting at the entire intersection.
        #This count is the number of turns that will happen before your car's turn.
        for road in self.connections:
            cars_ahead_count += len(self.queues[road]) 
        cars_ahead_of_me = cars_ahead_count - 1
        
        #Calculate the total delay
        total_delay = cars_ahead_of_me * self.time
        
        return total_delay
def get_text_time(time):
    hours = time
    minutes = (time * 60) % 60
    seconds = (time * 3600) % 60
    return ("%d:%02d:%02d" % (hours, minutes, seconds))
    # Queue using FIFO 

        

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
i1 = StopFourMe("i1", 0, 0)
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
for i in range(1):
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
