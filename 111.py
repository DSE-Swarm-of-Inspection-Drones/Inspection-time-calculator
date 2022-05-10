import matplotlib.pyplot as plt
import numpy as np
import math

wing_area = 122.6 * 2  # [m2]
fuselage_area = 2 * np.pi * 4.05 * 37.57  # [m2]
total_tail_area = 105  # [m2]
total_area = (wing_area + fuselage_area + total_tail_area)  # [m2]
big_area = fuselage_area * 0.6 + wing_area * 0.5 + total_tail_area
small_area = total_area - big_area
area = {"Large100":total_area, "Large60":big_area, "IR": big_area, "Small100":total_area, "Small40": small_area}  # Field of View [deg]

FOV = {"Large100":46.8, "Large60":46.8, "IR": 24.6, "Small100":12, "Small40": 12}  # Field of View [deg]
n_pixels = {"Large100":[8192, 5460], "Large60":[8192, 5460] , "IR": [1024, 96], "Small100":[5120, 2880], "Small40": [5120, 2880]}  # number of pixels [3840, 2160]
refresh_rate = {"Large100":1.4, "Large60": 1.4, "IR": 240, "Small100":120, "Small40": 120}
size_crack = {"Large100":1, "Large60":1, "IR": 5, "Small100":1, "Small40": 1}  # [mm]
shutter_speed = {"Large100":0.0005, "Large60":0.0005, "IR": 1/240, "Small100":1/1000, "Small40": 1/1000}  #[s], shutter speed of IR camera is uncertain and may need to be confirmed

styles = {"Large100":'dashed', "Large60":'dashed', "IR": 'dotted', "Small100": 'solid', "Small40": 'solid'}
labels = {"Large100": "Zenmuse, total surface", "Large60":"Zenmuse, upper surface", "IR": "IR camera, upper surface", "Small100":"Hero10, total surface",  "Small40": "Hero10, lower surface"}
inspection_list = ["Large100", "Large60", "IR", "Small100", "Small40"]   # [visual, IR]
for i in range(len(inspection_list)):
    speed = np.arange(0.01, 1, 0.001)  # [m/s]
    inspection_type = inspection_list[i]
    blur_size_accepted = size_crack[inspection_type]/3  # [mm]
    blur_length = speed * shutter_speed[inspection_type] * 1000 # [mm]
    size_pixel = blur_size_accepted - blur_length # [mm]
    sidelength = size_pixel * n_pixels[inspection_type][0] # [mm]


    t_inspection = (area[inspection_type]/(sidelength/1000))/speed # [s]
    d_aircraft = (sidelength/(FOV[inspection_type]/180*np.pi))/1000 # [m]

    min_value = 1000000000

    for i in range(len(t_inspection)):
        t = t_inspection[i]
        if t < 0:
            t_inspection[i] = t_inspection[i-1]
            speed[i] = speed[i-1]
        if t > 10**5:
            t_inspection[i] = t_inspection[i-1]
            speed[i] = speed[i-1]
        if t > 0 and t < min_value:
            min_value = t

    idx = (np.where(t_inspection==min_value)[0])
    print(f'minimum time = {min_value} seconds ({min_value/60} minutes)   \nfastest possible speeeeed = {speed[idx][0]} meters per second\ndrone to aircraft distance = {d_aircraft[idx][0]} meters\namount of drones = {math.ceil(min_value/60/30)} drones')
    # max_speed = n_pixels[inspection_type][1]*size_pixel[idx][0]/1000*refresh_rate[inspection_type]
    plt.loglog(speed, t_inspection, label=labels[inspection_type], linestyle=styles[inspection_type])

plt.title('Inspection time ')
plt.legend()
plt.grid()
plt.xlabel('Speed [m/s]')
plt.ylabel('Inspection time [s]')
plt.show()
