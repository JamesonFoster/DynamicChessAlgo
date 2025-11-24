import tkinter as tk
import tkintermapview as tkm
import TrafficSim as TP
import random as ran
import math
from PIL import ImageTk, Image
#Make longer or shorter based on desired path length
PATH_COORDINATES = [
    (33.2900999, -93.2369201), # Start
    (33.2915, -93.2360),
    (33.2920, -93.2355),
    (33.2925, -93.2340),
    (33.2930, -93.2325),
    (33.2935, -93.2310),
    (33.2940, -93.2300)  # End
]
#NEED TO BE CHANGED BASED ON WHERE IMAGES ARE SAVED
CAR_IMAGES = [
    r'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\CarPNGs\\redcar.png', 
    r'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\CarPNGs\\blackcar.png',
    r'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\CarPNGs\\browncar.png',
    r'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\CarPNGs\\bluecar.png'
]
#========================HIGHLIGHT ROAD FUNCTION=======================#
def highlight_road(car, map_widget):
    #If text file is X=Lat, Y=Lon, use (node.x, node.y).
    position_list = [(node.x, node.y) for node in car.path]
    
    #Add current position
    position_list.insert(0, (car.pos.x, car.pos.y))
    
    map_widget.set_path(position_list, color="#00F2FF", width=4)

    #Add start/end text markers
    if len(car.path) > 0:
        start = car.path[0]
        map_widget.set_marker(start.x, start.y, text="Start")
        end = car.path[-1]
        map_widget.set_marker(end.x, end.y, text="End")
#========================CLEAR VISUALS FUNCTION========================#
def clear_existing_visuals():
    global marker
    if marker:
        map_widget.delete(marker)
        marker = None
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
        if current_point_index >= len(car_to_animate.path) - 1:
            print("Trip Finished")
            return

        #Current and Next Node for position update
        current_node = car_to_animate.path[current_point_index]
        next_node = car_to_animate.path[current_point_index + 1]

        #Calculate angle based on the segment to next node
        angle = get_angle(current_node.x, current_node.y, next_node.x, next_node.y)

        #Move marker to the next point
        marker.set_position(next_node.x, next_node.y)

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
#==============================GUI SETUP================================#
def GUI_setup():
    root = tk.Tk()
    root.title("Magnolia Map View")
    root.geometry("1920x1080")
    map_widget = tkm.TkinterMapView(root, width=1920, height=1080, corner_radius=0)
    map_widget.pack(fill="both", expand=True)

    map_widget.set_position(33.2900999, -93.2369201)
    map_widget.set_zoom(15)
    return root, map_widget

root, map_widget = GUI_setup()

map_widget.delete_all_marker()
map_widget.delete_all_path()

#Animation Variables
current_point_index = 0
animation_delay = 500
car_to_animate = None
car_base_img = None
marker = None

# Find a car to animate
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
        clear_existing_visuals()
        start_node = car_to_animate.path[0]
        next_node = car_to_animate.path[1]

        initial_angle = get_angle(start_node.x, start_node.y, next_node.x, next_node.y)

        if car_base_img:
            rot_pil = rotate_image(car_base_img, initial_angle)
            tk_img = ImageTk.PhotoImage(rot_pil)

            marker = map_widget.set_marker(start_node.x, start_node.y, icon=tk_img)
            marker.image = tk_img  # Keep reference
        else:
            # Fallback if image fails
            marker = map_widget.set_marker(start_node.x, start_node.y)

        current_point_index = 0
        # Start moving after 1 second
        root.after(1000, animate_marker_along_path)
        
    else:
        print("Car has no path.")
else:
    print("No cars in simulation.")

root.mainloop()