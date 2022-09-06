# -- Path parameters -- #
json_path = 'D:\Conv-CAO\Coverage Path Planning\Adaptive_Coverage_Path_Planning\inputVariables.json'
save_path_wps = 'D:\Conv-CAO\Coverage Path Planning\Adaptive_Coverage_Path_Planning\\results'
turnwps_path = 'D:\Conv-CAO\Coverage Path Planning\Adaptive_Coverage_Path_Planning\CPP\\002\\TurnWPs.txt'

# -- Model parameters -- #
weights_path = 'D:\Conv-CAO\Coverage Path Planning\Adaptive_Coverage_Path_Planning\weights0500.hdf5'
backbone = 'efficientnetb1'

# -- Orthophoto parameters -- #
ortho_georef_img = 'D:/AirSim/PythonClient/adaptive_path_planning/ASLdataset/RedEdge/002/reflectance-tif/transparent_reflectance_red.tif'
ortho_rgb_img = 'D:/AirSim/PythonClient/adaptive_path_planning/ASLdataset/RedEdge/002/composite-png/RGB.png'

# Path planning parameters
QGIS = True  # read data from QGIS - GEOJSON file exported from QGIS
qgis_path = 'D:\Conv-CAO\Coverage Path Planning\Adaptive_Coverage_Path_Planning\CPP\\002\Polygon002.geojson'
mission_type = 'constant'  # 'constant'  # or 'variable'
initial_velocity = 4
time_interval = 0.5
distance_threshold = 0.3
if mission_type == 'constant':
    corner_radius = initial_velocity + 3
elif mission_type == 'variable':
    corner_radius = initial_velocity + 1 + 3  # if mission_type = 'variable': corner_radius = max_speed + 3

# How & Where to save your results
data_dir = save_path_wps  # save path
field = '002'  # name of the field
type_polygon = 'name_of_polygon'  # name of the polygon

import os

save_path = os.path.join(data_dir, field, 'type_polygon_{}'.format(type_polygon), mission_type,
                         'time_interval_{}'.format(time_interval),
                         'velocity_{}'.format(initial_velocity))

# e.g. for the above parameters your results will be saved in a folder located in 'data_dir'\002\name_of_polygon\constant\time_interval_0.5\velocity_4
