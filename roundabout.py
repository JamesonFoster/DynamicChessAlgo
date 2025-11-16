#simulate roundabout
import time
import random as ran
import math
from AStar import IntSect

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
            print(f'Theta: {theta}')
            
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
        print(f'GHOSTS: {self.ghosts}')

        #update time difference since last use
        self.deltaTuse = newUse - self.lastUse
        #update time of last use
        self.lastUse = newUse
        
        Csource = car.path[car.path.index(self) - 1] # index of the previous intersection in path
        temp = car.path[car.path.index(self)] 

        if temp == car.path[-1]: #if temp is equal to last node in path
            Cdest = temp #the car destination is the current node
            
        else:
            Cdest = car.path[car.path.index(self) + 1] #the car destination is the next node


        for _ in range(self.ghosts):
            
            Gdest = ran.randint(0,len(self.connections)-1) # each ghost car gets a random destination road
            print(f'Gdest: {self.connections[Gdest].name}')
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