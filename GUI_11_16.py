#GUI
import tkinter as tk
import tkintermapview as tkm
import TrafficProgram as TP
import random as ran
from PIL import ImageTk, Image
import time

carPics = ['C:\\Users\\Corinne\\Desktop\\DSA\\TrafficProgram\\redcar.png', 
           'C:\\Users\\Corinne\\Desktop\\DSA\\TrafficProgram\\blackcar.png',
           'C:\\Users\\Corinne\\Desktop\\DSA\\TrafficProgram\\browncar.png',
           'C:\\Users\\Corinne\\Desktop\\DSA\\TrafficProgram\\bluecar.png']

coordinates = []
def highlight_road(car):

    # Add the path to the map
    # The set_path() method returns a MapPath object cyan line width
    position_list = [(i.x,i.y) for i in car.path] #list of coordinates of intersections in car's path
    position_list.insert(0, (car.pos.x, car.pos.y))
    map_widget.set_path(position_list, color="#00F2FF", width=4)

    # Optional: You can add markers to the start/end points
    map_widget.set_marker(TP.itemp[0].x, TP.itemp[0].y, text="Start")
    map_widget.set_marker(TP.itemp[-1].x, TP.itemp[-1].y, text="End")

root = tk.Tk()
root.title("Magnolia Map View")
root.geometry("1920x1080")

map_widget = tkm.TkinterMapView(root, width=1920, height = 1080, corner_radius = 0)
map_widget.pack(fill="both", expand=True)
map_widget.place(relx=0.5, rely = 0.5, anchor= tk.CENTER)

map_widget.set_position(33.2900999, -93.2369201)
map_widget.set_zoom(15) #Adjust this if we want to zoom in on a point/intersection

for x, y in coordinates:
    map_widget.set_marker(x, y, text=f"X: {x:.2f}, Y: {y:.2f}")
        
for car in TP.Car.cars:
    r = ran.randint(1, 4) - 1
    img1 = Image.open(carPics[r])
    [w, h] = img1.size
    n = 8
    newW = int(w/n)
    newH = int(h/n)
    
    img1 = img1.resize((newW, newH))
    img = ImageTk.PhotoImage(img1)
    highlight_road(car)

top_left_bound = (33.3017057, -93.2609527)
bottom_right_bound = (33.2595144, -93.2098834)
map_widget.fit_bounding_box(top_left_bound, bottom_right_bound)

marker = map_widget.set_marker(TP.itemp[0].x, TP.itemp[0].y, icon=img)
current_point_index = 0
animation_delay = 500 # milliseconds (adjust for speed)

def animate_marker_along_path():
    global current_point_index
    
    for car in TP.Car.cars:
        # Check if we have reached the end of the path
        if current_point_index < len(car.path) - 1:
            
            current_point_index += 1
            next_pos = car.path[current_point_index]
            marker.set_position(next_pos.x, next_pos.y)
            # Optional: update map view to follow the marker
            # map_widget.set_position(next_pos[0], next_pos[1])
            # Schedule the next movement
            root.after(animation_delay, animate_marker_along_path)
        else:
            print("Animation complete.")
            # Optional: reset the path
            # current_point_index = 0
            # root.after(animation_delay, animate_marker_along_path)
            return False
        

# Call the function to highlight the road
#highlight_road()
#(33.2900999, -93.2369201) Wilson hall, SAU Magnolia
# Start the animation after a short initial delay
root.after(20000, animate_marker_along_path)

root.mainloop()

a = True


    
