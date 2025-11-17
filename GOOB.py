#GUI
import tkinter as tk
import tkintermapview as tkm
import TrafficProgram as TP
import random as ran
from PIL import ImageTk, Image

path_coordinates = [(33.231,-93.2313),
                        (33.4264436, -94.0455640),
                        (33.321332, -93.1222)] #Input a list of tuples

carPics = [ 'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\redcar.png',
            'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\blackcar.png',
            'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\browncar.png',
            'C:\\Users\\patte\\OneDrive\\Desktop\\DSA Project Group\\bluecar.png' ]
coordinates = []
def highlight_road():

    # Add the path to the map
    # The set_path() method returns a MapPath object         cyan       line width
    new_path = map_widget.set_path(path_coordinates,color="#00F2FF", width=2)

    # Optional: You can add markers to the start/end points
    map_widget.set_marker(path_coordinates[0][0], path_coordinates[0][1], text="Start")
    map_widget.set_marker(path_coordinates[-1][0], path_coordinates[-1][1], text="End")


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
        
cars = [TP.Car((0,0))]
canvas = tk.Canvas(root)
for car in cars:
    r = ran.randint(1, 4) - 1
    img = ImageTk.PhotoImage(Image.open(carPics[r]))
    panel = tk.Label(root, image = img)
    panel.pack(side = "bottom", fill = "none", expand = "yes")

top_left_bound = (33.3017057, -93.2609527)
bottom_right_bound = (33.2595144, -93.2098834)
map_widget.fit_bounding_box(top_left_bound, bottom_right_bound)

marker = map_widget.set_marker(path_coordinates[0][0], path_coordinates[0][1], icon=img)
current_point_index = 0
animation_delay = 500 # milliseconds (adjust for speed)

def animate_marker_along_path():
    global current_point_index

    # Check if we have reached the end of the path
    if current_point_index < len(path_coordinates) - 1:
        current_point_index += 1
        next_pos = path_coordinates[current_point_index]
        marker.set_position(next_pos[0], next_pos[1])
        # Optional: update map view to follow the marker
        # map_widget.set_position(next_pos[0], next_pos[1])

        # Schedule the next movement
        root.after(animation_delay, animate_marker_along_path)
    else:
        print("Animation complete.")
        # Optional: reset the path
        # current_point_index = 0
        # root.after(animation_delay, animate_marker_along_path)

# Call the function to highlight the road
highlight_road()
#(33.2900999, -93.2369201) Wilson hall, SAU Magnolia
# Start the animation after a short initial delay
root.after(1000, animate_marker_along_path)

root.mainloop()

