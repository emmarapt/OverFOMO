# -- Path parameters -- #
json_path = 'D:\AirSim\PythonClient\\adaptive_path_planning\mCPP\inputVariables.json'
save_path_wps = 'D:\AirSim\PythonClient\\adaptive_path_planning\\results'
turnwps_path = 'D:\AirSim\PythonClient\\adaptive_path_planning\TurnWPs.txt'

# -- Model parameters -- #
weights_path = 'D:\AirSim\PythonClient\\adaptive_path_planning\weights0500.hdf5'
backbone = 'efficientnetb1'

# -- Orthophoto parameters -- #
ortho_georef_img = 'D:/AirSim/PythonClient/adaptive_path_planning/ASLdataset/RedEdge/001/reflectance-tif/transparent_reflectance_red.tif'
ortho_rgb_img = 'D:/AirSim/PythonClient/adaptive_path_planning/ASLdataset/RedEdge/001/composite-png/RGB.png'

# Path planning parameters
QGIS = True  # read data from QGIS - GEOJSON file exported from QGIS
qgis_path = 'D:/AirSim/PythonClient/adaptive_path_planning/qgis/000/better_best/Polygon000.geojson'
mission_type = 'constant'  # 'constant'  # or 'variable'
initial_velocity = 4
time_interval = 0.5
distance_threshold = 0.3
if mission_type == 'constant':
	corner_radius = initial_velocity + 3
elif mission_type == 'variable':
	corner_radius = initial_velocity + 1 + 3  # if mission_type = 'variable': corner_radius = max_speed + 3
##
data_dir = 'D:/AirSim/PythonClient/adaptive_path_planning/ASLdataset'
field = '004'
type_polygon = 'name_of_polygon'


import os
save_path = os.path.join(data_dir, field, 'type_polygon_{}'.format(type_polygon), mission_type, 'time_interval_{}'.format(time_interval),
						   'velocity_{}'.format(initial_velocity))
