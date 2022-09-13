import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from osgeo import osr, ogr, gdal
import tqdm

from parameters import *


def world_to_pixel(geo_matrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ul_x = geo_matrix[0]
    ul_y = geo_matrix[3]
    x_dist = geo_matrix[1]
    y_dist = geo_matrix[5]
    pixel = int((x - ul_x) / x_dist)
    line = -int((ul_y - y) / y_dist)
    return pixel, line


def get_wp_pixels(waypoint):
    # waypoint = [waypoint[0].astype(np.float64), waypoint[1].astype(np.float64)]
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(waypoint[0], waypoint[1])
    point.Transform(transform)
    x, y = world_to_pixel(ds.GetGeoTransform(), point.GetX(), point.GetY())
    return [x, y]


def get_angle(orientation):
    if orientation <= 0:
        angle = 90 - abs(orientation)
    else:
        angle = 90 + orientation
    return angle


def get_waypoints(wp_file, orien_file):
    with open(wp_file) as file:
        lines = file.readlines()
        lines = [line.replace(';', '') for line in lines]
        lines = [line.rstrip() for line in lines]
        points_X = [float(p.split(',')[0]) for p in lines]
        points_Y = [float(p.split(',')[1]) for p in lines]
        # waypoints = np.column_stack((points_X, points_Y))
    with open(orien_file) as file:
        lines = file.readlines()
        lines = [line.replace(';', '') for line in lines]
        orien = [float(line.rstrip()) for line in lines]
    waypoints = np.column_stack((points_X, points_Y, orien))
    return waypoints


def get_speed(speed_file):
    with open(speed_file) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        speed = [float(p.split(',')[0]) for p in lines]
        cov_ratio = [float(p.split(',')[1]) for p in lines]
    return speed  # , cov_ratio


def plot_points(point1, angle, speed, window_size, rgb_img_points):
    # cv2.circle(rgb_img_points, (point1[0], point1[1]), 10, [0, 0, 255], -1)
    # if i % 5 == 0: # plot every x points
    rect = ((point1[0], point1[1]), (window_size[0], window_size[1]), angle)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(rgb_img_points, [box], 0, (0, 255, 0), 10)

    return rgb_img_points


# -- Input parameters -- #
data_dir = data_dir
field = field
type_polygon = type_polygon
mission = mission_type
time_interval = time_interval
velocity = initial_velocity

i = 0
window_size = (640, 480)  # (212, 160) #(1280, 960)

mission_dir = os.path.join(data_dir, field, 'type_polygon_{}'.format(type_polygon), mission,
                           'time_interval_{}'.format(time_interval),
                           'velocity_{}'.format(velocity))

wp_file = os.path.join(mission_dir, 'ViewWPs.txt')
orientation_file = os.path.join(mission_dir, 'ViewWPs_Orientation.txt')
speed_file = os.path.join(mission_dir, 'Speed_Records_ext.txt')
save_dir = os.path.join('collected_data/Airsim/', field, 'type_polygon_{}'.format(type_polygon), mission,
                        # +'_blur_{}'.format(speed_to_K(velocity)),
                        'time_interval_{}'.format(time_interval), 'velocity_{}'.format(velocity), 'images')
os.makedirs(save_dir, exist_ok=True)

# -- Orthomosaic with georeference -- #
ortho_dir = 'D:/AirSim/PythonClient/adaptive_path_planning/ASLdataset/RedEdge/{}'.format(
    field)

img_path = os.path.join(ortho_dir,
                        'reflectance-tif/transparent_reflectance_{}.tif')  # 'reflectance-tif/transparent_reflectance_{}.tif'
# -- Orthomosaic to crop images -- #
rgb_img = cv2.imread(
    os.path.join(ortho_dir, 'composite-png/RGB.png'))  # 'groundtruth/second002_gt' , 'composite-png/RGB.png'
rgb_img_points = np.copy(rgb_img)


# Extract target reference from the tiff file
ds = gdal.Open(img_path.format('red'))
target = osr.SpatialReference(wkt=ds.GetProjection())
source = osr.SpatialReference()
source.ImportFromEPSG(4326)
transform = osr.CoordinateTransformation(source, target)

# -- Get Waypoints -- #
waypoints = get_waypoints(wp_file, orientation_file)  # [:3]
speed = get_speed(speed_file)
num_waypoints = waypoints.shape[0]
print('Number of ViewWPs: {}'.format(num_waypoints))

for i in tqdm.tqdm(range(num_waypoints)):
    # -- Get pixel coordinates -- #
    point = get_wp_pixels(waypoints[i, :2])
    # -- Calculate orientation -- #
    # angle = get_angle(waypoints[i,2])
    angle = waypoints[i, 2]
    rgb_img_points = plot_points(point, angle, speed[i], window_size, rgb_img_points)
    i += 1

cv2.imwrite(os.path.join('collected_data/Airsim/', field, 'type_polygon_{}'.format(type_polygon), mission,
                         # +'_blur_{}'.format(speed_to_K(velocity)),
                         'time_interval_{}'.format(time_interval), 'velocity_{}'.format(velocity),
                         'viewpoints_map.jpg'), rgb_img_points)