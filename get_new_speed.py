import numpy as np
import time
from osgeo import osr, ogr, gdal
import cv2

# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()

import sys
#sys.path.append('/home/mikrestenitis/GANs/Pix2pix')
import keras_tools
keras_tools.keras_allow_growth()


import segmentation_models as sm
sm.set_framework('tf.keras')

from parameters import ortho_georef_img, ortho_rgb_img


class GetViewpointImage():
    '''
    Class to crop an image from the RGB orthomosaic based on an input waypoint
    '''
    def __init__(self):
        self.window_size = (1280, 960)

        # -- Orthomosaic with georeference -- #
        self.ortho_img_path = ortho_georef_img
        # -- Orthomosaic to crop images -- #
        self.rgb_img = cv2.imread(ortho_rgb_img)
        self.rgb_img = cv2.cvtColor(self.rgb_img, cv2.COLOR_BGR2RGB)

        # Extract target reference from the tiff file
        self.ds = gdal.Open(self.ortho_img_path)
        target = osr.SpatialReference(wkt=self.ds.GetProjection())
        source = osr.SpatialReference()
        source.ImportFromEPSG(4326)
        self.transform = osr.CoordinateTransformation(source, target)


    def rotate_image(self, point, angle):
        M = cv2.getRotationMatrix2D((point[0], point[1]), angle, 1.0)
        rotated = cv2.warpAffine(self.rgb_img, M, (self.rgb_img.shape[1], self.rgb_img.shape[0]))
        return rotated

    def world_to_pixel(self, geo_matrix, x, y):
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

    def get_wp_pixels(self, waypoint):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(waypoint[0], waypoint[1])
        point.Transform(self.transform)
        x, y = self.world_to_pixel(self.ds.GetGeoTransform(), point.GetX(), point.GetY())
        return [x, y]



    def crop_image(self, point1, angle):
        # -- Rotate image for cropping -- #
        rotated = self.rotate_image(point1, angle)
        rh, rw = rotated.shape[:2]

        # -- Pad image -- #
        top_pad = 0
        bottom_pad = 0
        left_pad = 0
        right_pad = 0
        if (point1[1] - self.window_size[1] // 2) < 0:
            top_pad = abs(point1[1] - self.window_size[1] // 2)
            print('Out of borders')
        if (point1[1] + self.window_size[1] // 2) > rh:
            bottom_pad = (point1[1] + self.window_size[1] // 2) - rh
            print('Out of borders')
        if (point1[0] - self.window_size[0] // 2) < 0:
            left_pad = abs(point1[0] - self.window_size[0] // 2)
            print('Out of borders')
        if (point1[0] + self.window_size[0] // 2) > rw:
            right_pad = (point1[0] + self.window_size[0] // 2) - rw
            print('Out of borders')
        rotated_pad = cv2.copyMakeBorder(rotated, top_pad, bottom_pad, left_pad, right_pad,
                                         borderType=cv2.BORDER_CONSTANT, value=0)

        # # -- Crop image -- #
        captured_img = rotated_pad[
                       (point1[1] - self.window_size[1] // 2) + top_pad:point1[1] + top_pad + self.window_size[1] // 2,
                       (point1[0] - self.window_size[0] // 2) + left_pad:point1[0] + left_pad + self.window_size[0] // 2, :]

        return captured_img

    def get_image(self, waypoint, orientation):
        # -- Get pixel coordinates -- #
        point = self.get_wp_pixels(waypoint)
        # -- Crop image at viewpoint -- #
        captured_img = self.crop_image(point, orientation)
        return captured_img


class GetSpeed():
    def __init__(self, weights_path, backbone):
        # -- Speed parameters -- #
        self.nominal_speed = 3
        self.Q_max = 2
        self.ratio_min = 0.05
        self.ratio_max = 0.15

        # -- Model parameters -- #
        self.num_classes = 4
        self.backbone = backbone
        self.preprocess_input = sm.get_preprocessing(self.backbone)

        # -- Initialize prediction model -- #
        self.weights_path = weights_path
        self.model = sm.Unet(self.backbone, input_shape=(None, None, 3), classes=self.num_classes, encoder_weights=None,
                        activation='softmax')
        self.model.load_weights(self.weights_path)


    def get_coverage_ratio(self, pred):
        pred = pred.flatten()
        cov_ratio = (np.sum(pred == 1) + np.sum(pred == 2)) / len(pred)
        return cov_ratio

    def find_speed(self, coverage_ratio, norm=True):
        if norm:
            coverage_ratio = (coverage_ratio - self.ratio_min) / (self.ratio_max - self.ratio_min)
        adj = (1 - 2 * coverage_ratio) * self.Q_max
        speed = self.nominal_speed + adj
        return speed


    def calculate_speed_adj(self, img):
        prediction = self.get_prediction(img)
        cov_ratio = self.get_coverage_ratio(prediction)
        new_speed = self.find_speed(cov_ratio)
        return new_speed

    def get_prediction(self, img):
        img = self.preprocess_input(img)
        pred_s = time.time()
        prediction = self.model.predict(np.expand_dims(img, 0))
        print('Prediction time: {}'.format(time.time() - pred_s))
        prediction = np.argmax(prediction.squeeze(), -1)
        return prediction




if __name__ == '__main__':
    start = time.time()

    # -- Waypoint info -- #
    waypoints = [[50.61460849406916, 6.989823076008492], [50.61462313448179, 6.9898392815408465],
                 [50.61463804734468, 6.9898564207929645], [50.614652765873664, 6.989874253873176]]
    orientation = 39.97415723366056

    # -- Create class instances -- #
    viewpoint = GetViewpointImage()
    speed_adj = GetSpeed()

    for waypoint in waypoints:
        # -- Get image on the defined viewpoint -- #
        img = viewpoint.get_image(waypoint, orientation)
        # -- Get new speed -- #
        new_speed = speed_adj.calculate_speed_adj(img)


        print('New speed: {}'.format(new_speed))
    print('Overall execution time: {}'.format(time.time() - start))
