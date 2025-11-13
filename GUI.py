#GUI
import tkinter as tk
import tkintermapview as tkm

def create_map_gui(coordinates):
    root = tk.Tk()
    root.title("SAU Map View")
    root.geometry("1920x1080")

    map_widget = tkm.TkinterMapView(root, width=1920, height = 1080, corner_radius = 0)
    map_widget.pack(fill="both", expand=True)

    if coordinates:
        map_widget.set_position(coordinates[0][0], coordinates[0][1])
        map_widget.set_zoom(0) #Adjust this if we want to zoom in on a point/intersection

        for x, y in coordinates:
            map_widget.set_marker(x, y, text=f"X: {x:.2f}, Y: {y:.2f}")
        
    root.mainloop()

#Example
sample_coordinates = [(33.2900999, -93.2369201),(34,118),(51,0.27)]
create_map_gui(sample_coordinates)