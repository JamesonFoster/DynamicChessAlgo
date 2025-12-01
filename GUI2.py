import tkinter as tk
import tkintermapview as tkm
import TrafficProgram as TP
import random as ran
import math
from PIL import ImageTk, Image

#NEED TO BE CHANGED BASED ON WHERE IMAGES ARE SAVED
CAR_IMAGES = [TP.path + '\\redcar.png', 
           TP.path + '\\blackcar.png',
           TP.path + '\\browncar.png',
           TP.path + '\\bluecar.png']

def calibrate_coordinates(cx1, cy1, cx2, cy2, cx3, cy3, dx1, dy1, dx2, dy2, dx3, dy3):
        
    y_scale =  math.sqrt(((dx2-dx1)**2) + ((dy2 - dy1)**2)) / math.sqrt(((cx2-cx1)**2) + ((cy2 - cy1)**2)) 
    x_scale =  math.sqrt(((dx3 - dx2)**2) + ((dy3 - dy2)**2)) / math.sqrt(((cx3 - cx2)**2) + ((cy3 - cy2)**2))

    return x_scale, y_scale

def calculate_points(x, y, xs, ys):
    x = -93.25078388 + (x * xs) 
    y =  33.2647510 + (y * ys) 
    
    return y, x

xs, ys = calibrate_coordinates(0, 0, 0, 1000, 1000, 1000, -93.2507388, 33.2647510, -93.2507388,33.2979728, -93.2130162, 33.2979728)

coordinates = []

#========================HIGHLIGHT ROAD FUNCTION=======================#
def highlight_road(car, map_widget):
    #If text file is X=Lat, Y=Lon, use (node.x, node.y).
    position_list = [(node.x, node.y) for node in car.path]
    
    #Add current position
    position_list.insert(0, (car.pos.x, car.pos.y))
    for coord in position_list:
        x = calculate_points(coord[0], coord[1], xs, ys)
        coordinates.append(x)
    map_widget.set_path(coordinates, color="#00F2FF", width=4)

    #Add end text marker
    if len(car.path) > 0:
        map_widget.set_marker(coordinates[-1][0], coordinates[-1][1], text="Destination")
#========================GET ANGLE FUNCTION============================#
def get_angle(x1, y1, x2, y2):
    dx = y2 - y1
    dy = x2 - x1
    angle_radian = math.atan2(dy, dx)
    return math.degrees(angle_radian)

#========================ROTATE IMAGE FUNCTION=========================#
def rotate_image(image, angle):
    # Formula: angle - 90 add or subtract 180 based on image look. IF NEEDED
    rotation_needed = angle - 90
    return image.rotate(rotation_needed, expand=True)
#==========================ANIMATION FUNCTION==========================#
def animate_marker_along_path():
    global current_point_index, car_base_img, marker, car_to_animate

    try:
        if not car_to_animate or not marker or not car_to_animate.path:
            print("Animation setup error.")
            return
        # Continue animation if there are more points
        if current_point_index > len(coordinates) :
            print("Trip Finished")
            return

        #Current and Next Node for position update
        
        current_node = coordinates[current_point_index]
        next_node = coordinates[current_point_index + 1]


        #Calculate angle based on the segment to next node
        angle = get_angle(current_node[0], current_node[1], next_node[0], next_node[1])

        #Move marker to the next point
        marker.set_position(next_node[0], next_node[1])

        #Rotate Image
        if car_base_img:
            rotated_pil = rotate_image(car_base_img, angle)
            rotated_tk = ImageTk.PhotoImage(rotated_pil)
            
            #Update Marker Icon
            marker.change_icon(rotated_tk)
            
            #Keep reference so python doesn't delete the image
            marker.image = rotated_tk 
        
        current_point_index += 1
        # Setup next animation step
        root.after(animation_delay, animate_marker_along_path)
    except Exception as e:
        print(f"Error during animation: {e}")
#==============================GUI SETUP===============================================================#
def GUI_setup():
    root = tk.Tk()
    root.title("Magnolia Map View")
    root.geometry("1920x1080")
    map_widget = tkm.TkinterMapView(root, width=810, height=1080, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    map_widget.set_position(33.2900999, -93.2369201)
    map_widget.set_zoom(14)
    return root, map_widget



root, map_widget = GUI_setup()



def changeType():
    print("yes")


root.title('Search Star')



for i in TP.itemp:
    button = tk.Button(root, text=i.name, width=25, command=changeType)
    button.pack()



#Clear existing markers and paths
map_widget.delete_all_marker()
map_widget.delete_all_path()
#Ensure GUI is updated immediately after clearing the canvas
map_widget.update_idletasks()

#Animation Variables
current_point_index = 0
animation_delay = 500
car_to_animate = None
car_base_img = None

#Find a car to animate
if TP.Car.cars:
    print(f"Found {len(TP.Car.cars)} cars.")
    
    # Get first car
    car_to_animate = next(iter(TP.Car.cars))
    
    if car_to_animate.path and len(car_to_animate.path) >= 2:
        
        #Draw path
        highlight_road(car_to_animate, map_widget)

        #Load Image
        r = ran.randint(0, 3)
        try:
            pil_image = Image.open(CAR_IMAGES[r])
            w, h = pil_image.size
            pil_image = pil_image.resize((int(w/8), int(h/8)))
            car_base_img = pil_image 
        except Exception as e:
            print(f"Image Load Error: {e}")
            car_base_img = None

        # Initial Placement
        
        start_node = coordinates[0]
        next_node = coordinates[1]

        initial_angle = get_angle(start_node[0], start_node[1], next_node[0], next_node[1])
        
        if car_base_img:
            rot_pil = rotate_image(car_base_img, initial_angle)
            tk_img = ImageTk.PhotoImage(rot_pil)

            marker = map_widget.set_marker(start_node[0], start_node[1], icon=tk_img)
            #marker.image = tk_img  # Keep reference
        else:
            # Fallback if image fails
            marker = map_widget.set_marker(start_node[0], start_node[1])

        current_point_index = 0
        # Start moving after 1 second
        
        
    else:
        print("Car has no path.")
else:
    print("No cars in simulation.")



top_left_bound = (33.3017057, -93.2609527)
bottom_right_bound = (33.2595144, -93.2098834)
map_widget.fit_bounding_box(top_left_bound, bottom_right_bound)
root.after(1000, animate_marker_along_path)



#==================================================================================================================



root.mainloop()