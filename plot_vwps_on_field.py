import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from osgeo import osr, ogr, gdal
import tqdm

from PythonClient.adaptive_path_planning.parameters import *


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
    #cv2.circle(rgb_img_points, (point1[0], point1[1]), 10, [0, 0, 255], -1)
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
# ortho_dir = '/home/mikrestenitis/Databases/WeedMap Dataset/2018-weedMap-dataset-release/Orthomosaic/RedEdge/{}'.format(
# 	field)
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

# # remove black background
# file_name = "D:\AirSim\PythonClient\\adaptive_path_planning\collected_data\Airsim\\004\\type_polygon_test\\variable\\time_interval_0.5\\velocity_4\\viewpoints_map.jpg"
# src = cv2.imread(file_name, 1)
# tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
# b, g, r = cv2.split(src)
# rgba = [b, g, r, alpha]
# dst = cv2.merge(rgba, 4)
# cv2.imwrite("test.png", dst)


# # remove black background
# file_name1 = "D:\AirSim\PythonClient\\adaptive_path_planning\ASLdataset\RedEdge\\001\groundtruth.tif"
# src1 = cv2.imread(file_name1, 1)
# tmp1 = cv2.cvtColor(src1, cv2.COLOR_BGR2GRAY)
# _, alpha1 = cv2.threshold(tmp1, 0, 255, cv2.THRESH_BINARY)
# b1, g1, r1 = cv2.split(src1)
# rgba1 = [b1, g1, r1, alpha1]
# dst1 = cv2.merge(rgba1, 4)
# cv2.imwrite("test_gth.png", dst1)

# im = plt.imread(os.path.join('collected_data/Airsim/', field, 'type_polygon_{}'.format(type_polygon), mission,  # +'_blur_{}'.format(speed_to_K(velocity)),
#                          'time_interval_{}'.format(time_interval), 'velocity_{}'.format(velocity),
#                          'viewpoints_map.jpg'), rgb_img_points)


im = plt.imread(
    "D:\AirSim\PythonClient\\adaptive_path_planning\collected_data\Airsim\\004\\type_polygon_test\\variable\\time_interval_0.5\\velocity_4\\viewpoints_map.jpg")
# im = plt.imread("test.png")
plt.imshow(im)
pointx = []
pointy = []
# for i in tqdm.tqdm(range(num_waypoints)):
#     point = get_wp_pixels(waypoints[i, :2])
#     pointx.append(point[0])
#     pointy.append(point[1])
# plt.scatter(pointx, pointy, s=10, c=speed, cmap='RdYlBu')

#clb = plt.colorbar(orientation="horizontal", aspect=50, pad=0.05)
# for i in range(0, 8, 2):
#     plt.annotate('{}'.format(i), (pointx[i], pointy[i]), fontsize=13, c="y")
# clb.ax.set_title("Speed")
plt.axis('off')
plt.savefig("filename.png", transparent=True)
plt.show()




# # import the Python Image
# # processing Library
# from PIL import Image
#
# # Giving The Original image Directory
# # Specified
# Original_Image = Image.open("D:\AirSim\PythonClient\\adaptive_path_planning\ASLdataset\RedEdge\\004\composite-png\\second002_gt.png")
#
# # Rotate Image By 180 Degree
# rotated_image1 = Original_Image.rotate(-5)
#
# # # This is Alternative Syntax To Rotate
# # # The Image
# # rotated_image2 = Original_Image.transpose(Image.ROTATE_90)
# #
# # # This Will Rotate Image By 60 Degree
# # rotated_image3 = Original_Image.rotate(60)
#
# rotated_image1.show()
# rotated_image1.save("rotated.png")
# # rotated_image2.show()
# # rotated_image3.show()


import numpy as np
import matplotlib.pyplot as plt
import cv2

# Read the image with Opencv
img = cv2.imread("D:\AirSim\PythonClient\\adaptive_path_planning\collected_data\Airsim\\004\\type_polygon_test\\variable\\time_interval_0.5\\velocity_4\\viewpoints_map.jpg")
# Change the color from BGR to RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Orgird to store data
x, y = np.ogrid[0:img.shape[0], 0:img.shape[1]]
# In Python3 matplotlib assumes rgbdata in range 0.0 to 1.0
img = img.astype('float32')/255
fig = plt.Figure()
# gca do not work thus use figure objects inbuilt function.
ax = fig.add_subplot(projection='3d')

# minus 50 to place the image in the middle
ax.plot_surface(x, y, np.atleast_2d(0) + 5, rstride=5, cstride=5, facecolors=img, label="TEST")


for i in tqdm.tqdm(range(num_waypoints)):
    point = get_wp_pixels(waypoints[i, :2])
    pointx.append(point[0])
    pointy.append(point[1])
ax.scatter(pointx, pointy, 6)


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
fig.savefig('output_image')


