from handleGeo.ConvCoords import ConvCoords

import time
import xml.etree.cElementTree as ET
import json
import sys
import random
import airsim
import numpy as np
import math
import threading
import sched

from get_new_speed import GetViewpointImage, GetSpeed

# --- Path definition -- #
from parameters import *

os.makedirs(save_path, exist_ok=True)


def GetmultirotorState(DroneName):
    getdata = client.getMultirotorState(DroneName)
    time.sleep(0.1)  # sleep to avoid BufferError
    return getdata


class Thread_class(threading.Thread):
    def __init__(self, running):
        threading.Thread.__init__(self)
        self.running = running
        self.daemon = True
        self.start()

    def run(self):
        while self.running:
            self.update_path()

    def update_path(self):
        global getpose
        global resulting_path
        global ned_dist
        global corner_radius
        global ViewWPs_WGS84, ViewWPs_WGS84_orientantion
        global turn

        try:

            getpose = GetmultirotorState('Drone1')

            current_ned = np.array(
                (getpose.kinematics_estimated.position.x_val, getpose.kinematics_estimated.position.y_val))
            nextWP_ned = np.array((path_No1[0].x_val, path_No1[0].y_val))
            ned_dist = np.linalg.norm(current_ned - nextWP_ned)

            # print(
            # 	f'Curent position: [{getpose.kinematics_estimated.position.x_val}, {getpose.kinematics_estimated.position.y_val}], '
            # 	f'Next waypoint: [{path_No1[0].x_val}.{path_No1[0].y_val}], Distance: {ned_dist}')

            if ned_dist < distance_threshold:
                del path_No1[0]
                print("WPs to go:", len(path_No1))

            if ned_dist < corner_radius:
                resulting_path = client.moveOnPathAsync(path_No1, 1, 500, airsim.DrivetrainType.ForwardOnly,
                                                        airsim.YawMode(False, 0), vehicle_name='Drone1')
                turn = True  # Drone is in Turn
            else:
                if mission_type == 'constant':
                    resulting_path = client.moveOnPathAsync(path_No1, velocity, 500,
                                                            airsim.DrivetrainType.ForwardOnly,
                                                            airsim.YawMode(False, 0), vehicle_name='Drone1')

                    turn = False
                else:  # mission_type == 'variable'

                    """ Dummy adaptive mission """
                    # time.sleep(0.5)
                    # new_speed = random.uniform(4, 7)
                    # print('Speed adjusted to: {:.4f}'.format(new_speed))
                    #
                    # resulting_path = client.moveOnPathAsync(path_No1, new_speed, 500, airsim.DrivetrainType.ForwardOnly,
                    #                                         airsim.YawMode(False, 0), vehicle_name='Drone1')
                #
                """Adaptive mission """
                """CONTROL SPEED"""
                # -- Step #1: Get current viewpoint -- #
                # print("ViewWP:", ViewWPs_WGS84[-1][0][0])
                waypoint = ViewWPs_WGS84[-1][0][0]  # [50.61460849406916, 6.989823076008492]
                orientation = ViewWPs_WGS84_orientantion[-1]  # 39.97415723366056
                # -- Step #2: Get new velocity -- #
                img = viewpoint.get_image(waypoint, orientation)
                new_speed = speed_adj.calculate_speed_adj(img)
                print('Speed adjusted to: {:.4f}'.format(new_speed))
                # -- Step #3: Update speed on path -- #
                resulting_path = client.moveOnPathAsync(path_No1, new_speed, 500, airsim.DrivetrainType.ForwardOnly,
                                                        airsim.YawMode(False, 0), vehicle_name='Drone1')

        except:
            pass


if __name__ == '__main__':

    """
########################################################################################################################
    ---------------------------------------------- CPP -------------------------------------------------------------
########################################################################################################################
    """

    """Define sensor specifications"""
    # RedEdge-M Image Sensor specs
    HFOV = 46
    hRes = 1280
    ImageWidth = 1280
    ImageHeight = 960
    SensorWidth = 13.2
    SensorHeight = 8
    FocalLength = 5.4


    def GSD(altitude):
        return ((2 * altitude * getTanFromDegrees(HFOV / 2)) / hRes) * 100


    def getTanFromDegrees(degrees):
        return math.tan(degrees * math.pi / 180)


    def covered(altitude):
        return 2 * altitude * getTanFromDegrees(HFOV / 2)


    def GSDh(altitude):
        return ((altitude * 100) * (SensorHeight / 10)) / ((FocalLength / 10) * ImageHeight)


    def GSDw(altitude):
        return ((altitude * 100) * (SensorWidth / 10)) / ((FocalLength / 10) * ImageWidth)


    """ ---------------------------------------  PARAMETERS ---------------------------------------------------------"""

    geoCoords = []
    geoObstacles = []

    # READ input variables
    file = open(json_path)
    data = json.load(file)

    if QGIS:  # If QGIS is True, read polygon data as QGIS format
        polygon_file = open(qgis_path)
        polygon_data = json.load(polygon_file)
        field_name = polygon_data['name']

        # Polygon
        for p in polygon_data['features']:
            for i in range(len(p['geometry']['coordinates'][0][0])):
                geoCoords.append([p['geometry']['coordinates'][0][0][i][1], p['geometry']['coordinates'][0][0][i][0]])

        # LineString
        # for p in polygon_data['features']:
        #     for i in range(len(p['geometry']['coordinates'][0])):
        #         geoCoords.append([p['geometry']['coordinates'][0][i][1], p['geometry']['coordinates'][0][i][0]])

    else:  # If QGIS is False, read polygon data from .json
        for i in data['polygon']:
            geoCoords.append([i.get("lat"), i.get("long")])

    if len(data['obstacles']) > 0:
        geoObstacles = [[] for _ in range(len(data['obstacles']))]
        for i in range(len(data['obstacles'])):

            for j in data['obstacles'][i]:
                geoObstacles[i].append([j.get("lat"), j.get("long")])

    altitude = data['altitude']
    sidelap = data['sidelap']
    # frontlap = data['frontlap']

    scanDist = float("{:.2f}".format(covered(altitude) * (1 - sidelap / 100)))
    print("Scanning Distance:", scanDist)

    print("GSD:", float("{:.2f}".format(GSD(altitude))))
    # print("GSD:", float("{:.2f}".format(max(GSDh(altitude), GSDw(altitude)))))

    droneNo = data['droneNo']
    portions = data['rPortions']
    pathsStrictlyInPoly = data['pathsStrictlyInPoly']

    randomInitPos = False  # If false define in .json the initialPos of the drones as WGS84 format
    notEqualPortions = False
    initial_positions = []
    if randomInitPos is False:
        for i in data['initialPos']:
            initial_positions.append([i.get("lat"), i.get("long")])

    """ ----------------------------------------- End of parameters ------------------------------------------------ """

    """
########################################################################################################################
    ----------------------------------------------  AirSim -------------------------------------------------------------
########################################################################################################################
    """

    # connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True, "Drone1")
    client.armDisarm(True, "Drone1")

    z = -altitude
    path_No1 = []

    getpose = client.getMultirotorState('Drone1')

    names = []

    """
    # ------------------ Read path from TurnWPs.txt --------------------------------------------------------------------
    """

    TurnWPs = []
    file1 = open(turnwps_path, 'r')
    Lines = file1.readlines()
    # Strips the newline character
    for line in Lines:
        TurnWPs.append(line.strip().split(" "))
    TurnWPs_helper = []
    for WP in TurnWPs:
        TurnWPs_helper.append([float(WP[0]), float(WP[1])])
    TurnWPs_NED = ConvCoords(geoCoords, geoObstacles).convWGS84ToNED(TurnWPs_helper)
    No_wp = 0
    for WP_NED in TurnWPs_NED:
        path_No1.append(airsim.Vector3r(WP_NED[0], WP_NED[1], z))
        names.append('No{}'.format(No_wp))
        No_wp += 1

    # # Visualize waypoints
    """ Press T for path visualization"""
    client.simPlotLineStrip(points=path_No1, color_rgba=[1.0, 1.0, 0.0, 1.0], thickness=30, is_persistent=True)
    # client.simPlotStrings(strings=names, positions=path_No1, color_rgba=[1.0, 1.0, 0.0, 1.0])

    airsim.wait_key('Press any key to takeoff')
    f1 = client.takeoffAsync(vehicle_name="Drone1").join()

    print("make sure we are hovering at {} meters...".format(-z))
    hovering = client.moveToZAsync(z, 5, vehicle_name='Drone1').join()

    # ##################################################################################################################
    """
                                    Adaptive path planning based on vegetation knowledge 
    """


    # ##################################################################################################################

    def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z  # in radians


    def getStateOnPath(DroneName, wp_interval):

        # Get position & orientation
        # getdata = GetmultirotorState(DroneName)  # client.getMultirotorState(DroneName)

        wp_interval_helper.append(
            [getpose.kinematics_estimated.position.x_val, getpose.kinematics_estimated.position.y_val])
        Pitch, Roll, Yaw = euler_from_quaternion(getpose.kinematics_estimated.orientation.x_val,
                                                 getpose.kinematics_estimated.orientation.y_val,
                                                 getpose.kinematics_estimated.orientation.z_val,
                                                 getpose.kinematics_estimated.orientation.w_val)

        print("Current Drone's speed:", math.sqrt(
            getpose.kinematics_estimated.linear_velocity.x_val ** 2 + getpose.kinematics_estimated.linear_velocity.y_val ** 2 + getpose.kinematics_estimated.linear_velocity.z_val ** 2))
        ViewWPs_WGS84.append(ConvCoords(geoCoords, geoObstacles).NEDToWGS84([[wp_interval_helper[-1]]]))
        ViewWPs_WGS84_orientantion.append(np.degrees(Yaw))

        file_orientation.write(''.join(
            '{}'.format(np.degrees(Yaw))))
        file_orientation.write('\n')

        file_viewWPs_NED.write(''.join(
            '{}, {}'.format(getpose.kinematics_estimated.position.x_val, getpose.kinematics_estimated.position.y_val)))
        file_viewWPs_NED.write('\n')

        file_exec_real_speed.write(''.join('{}'.format(math.sqrt(
            getpose.kinematics_estimated.linear_velocity.x_val ** 2 + getpose.kinematics_estimated.linear_velocity.y_val ** 2 + getpose.kinematics_estimated.linear_velocity.z_val ** 2))))
        file_exec_real_speed.write('\n')

        if turn is True:
            file_exec_speed.write(''.join('{}'.format(2)))
            file_exec_speed.write('\n')
        else:
            file_exec_speed.write(''.join('{}'.format(velocity)))
            file_exec_speed.write('\n')


    """
    Parameters
    """
    turn = False
    corner_radius = corner_radius
    mission_type = mission_type
    velocity = initial_velocity  # Define the speed of the mission
    time_interval = time_interval  # This is the time interval witch an image is taken e.g. 1 frame per time_interval seconds
    print(" --- 1 frame per {} seconds --- ".format(time_interval))
    path_No1_full = path_No1.copy()
    ViewWPs_WGS84 = []  # store current ViewWP
    ViewWPs_WGS84_orientantion = []  # store current ViewWP's orientation

    # Write ViewWPs's orientation from origin point (0,0)
    file_name_orientation = "ViewWPs_Orientation.txt"
    completeName_orientation = os.path.join(save_path_wps, file_name_orientation)
    file_orientation = open(completeName_orientation, "w")

    # Write ViewWPs in NED
    file_name_viewWPs_NED = "ViewWPs_NED.txt"
    completeName_viewWPs_NED = os.path.join(save_path_wps, file_name_viewWPs_NED)
    file_viewWPs_NED = open(completeName_viewWPs_NED, "w")

    # Write ViewWPs
    file_name_viewWPs = "ViewWPs.txt"
    completeName_viewWPs = os.path.join(save_path_wps, file_name_viewWPs)

    # Write execution time - flight time
    file_name_exec_time = "Flight_time.txt"
    completeName_exe_time = os.path.join(save_path_wps, file_name_exec_time)
    file_exec_time = open(completeName_exe_time, "w")

    # Write dummy speed
    file_name_speed = "Dummy_Speed.txt"
    completeName_speed = os.path.join(save_path_wps, file_name_speed)
    file_exec_speed = open(completeName_speed, "w")

    # Write real speed
    file_name_real_speed = "Real_Speed.txt"
    completeName_real_speed = os.path.join(save_path_wps, file_name_real_speed)
    file_exec_real_speed = open(completeName_real_speed, "w")

    if mission_type == 'variable':
        # --- Initialize speed classes  --- #
        viewpoint = GetViewpointImage()
        speed_adj = GetSpeed(weights_path, backbone)
        # -- Dummy prediction to initialize model -- #
        dummy_img = np.random.randint(0, 255, (1280, 960, 3))
        speed_adj.get_prediction(dummy_img)

    print("DroneNo 1 is flying on path...")

    # For ForwardOnly mode (Heading towards path)
    resulting_path = client.moveOnPathAsync(path_No1, 2, 500, airsim.DrivetrainType.ForwardOnly,
                                            airsim.YawMode(False, 0), vehicle_name='Drone1')

    print("WPs to go:", len(path_No1))

    # Wait until first WP is reached
    movetopath = True
    while movetopath:

        get_inital_pose = client.getMultirotorState('Drone1')

        current_ned = np.array(
            (get_inital_pose.kinematics_estimated.position.x_val, get_inital_pose.kinematics_estimated.position.y_val))
        nextWP_ned = np.array((path_No1[0].x_val, path_No1[0].y_val))
        ned_dist = np.linalg.norm(current_ned - nextWP_ned)

        # print(f'Curent position: [{get_inital_pose.kinematics_estimated.position.x_val}, {get_inital_pose.kinematics_estimated.position.y_val}], '
        #	  f'Next waypoint: [{path_No1[0].x_val}.{path_No1[0].y_val}], Distance: {ned_dist}')

        if ned_dist < distance_threshold:
            # start measuring execution time
            start = time.time()

            # start measuring execution time via AirSim (same)
            # get_time = client.getMultirotorState('Drone1')
            # start_date_time = datetime.fromtimestamp(get_time.timestamp // 1000000000)
            # print(" --- First WP !! - Drone starts to follow the path at {} ---".format(start_date_time))

            del path_No1[0]
            print("WPs to go:", len(path_No1))
            movetopath = False
            onpath = True
            time.sleep(0.1)  # sleep in order not to access the 2nd while statement (same as 1st)

    wp_interval = [[] for _ in range(len(portions))]
    wp_interval_helper = []
    s = sched.scheduler(time.time, time.sleep)

    # Start Thread for updating the path -- Background process
    Thread_class(True)

    while onpath:

        # Start an event at scheduler
        s.enter(time_interval, 1, getStateOnPath, ('Drone1', wp_interval_helper))
        s.run()

        # print("Current_ViewWP:", ViewWPs_WGS84[-1][0][0])
        # print("Current ViewWP's orientation", ViewWPs_WGS84_orientantion[-1])
        """ ---------------------------------------------------- """
        if mission_type == 'variable' and ned_dist > corner_radius:
            if turn is True:
                resulting_path = client.moveOnPathAsync(path_No1, velocity, 500, airsim.DrivetrainType.ForwardOnly,
                                                        airsim.YawMode(False, 0), vehicle_name='Drone1')
                turn = False  # Drone is in Turn
            else:

                # """ Dummy adaptive mission """
                # time.sleep(0.5)
                # new_speed = random.uniform(4, 7)
                # print('Speed adjusted to: {:.4f}'.format(new_speed))
                #
                # resulting_path = client.moveOnPathAsync(path_No1, new_speed, 500, airsim.DrivetrainType.ForwardOnly,
                #                                         airsim.YawMode(False, 0), vehicle_name='Drone1')

                """ Real adaptive mission """
                """CONTROL SPEED"""
                # -- Step #1: Get current viewpoint -- #
                # print("ViewWP:", ViewWPs_WGS84[-1][0][0])
                waypoint = ViewWPs_WGS84[-1][0][0]  # [50.61460849406916, 6.989823076008492]
                orientation = ViewWPs_WGS84_orientantion[-1]  # 39.97415723366056
                # -- Step #2: Get new velocity -- #
                img = viewpoint.get_image(waypoint, orientation)
                new_speed = speed_adj.calculate_speed_adj(img)
                print('Speed adjusted to: {:.4f}'.format(new_speed))
                # -- Step #3: Update speed on path -- #
                resulting_path = client.moveOnPathAsync(path_No1, new_speed, 500, airsim.DrivetrainType.ForwardOnly,
                                                        airsim.YawMode(False, 0), vehicle_name='Drone1')
        """ ---------------------------------------------------- """

        if len(path_No1) == 0:
            # End of execution time
            end = time.time()

            # End of execution time via AirSim (same)
            # get_time = client.getMultirotorState('Drone1')
            # end_date_time = datetime.fromtimestamp(get_time.timestamp // 1000000000)
            # print(" --- Path has finished at {} ---".format(end_date_time))

            # Execution time
            Execution_time = end - start
            print(" -------------- Overall execution time is {} sec".format(Execution_time))
            file_exec_time.write(''.join('Overall execution time is {} sec'.format(Execution_time)))

            # exec_time = end_date_time - start_date_time

            # print(" -------------- Overall execution time from timestamp is {} {}".format(exec_time.total_seconds(),
            #																			  exec_time.microseconds))

            onpath = False
            wp_interval[droneNo - 1].append(wp_interval_helper)

    # close files
    file_exec_time.close()
    file_orientation.close()
    file_viewWPs_NED.close()
    file_exec_speed.close()
    file_exec_real_speed.close()

    view_points = []
    WGS84_Coords_interval = [[] for _ in range(len(portions))]
    for i in range(droneNo):
        WGS84_Coords_interval[i].append(ConvCoords(geoCoords, geoObstacles).NEDToWGS84(wp_interval[i]))

        # For Geoplaner (Write ViewWaypoints in .gpx file compatible with geoplaner.com)
        root = ET.Element("gpx", version="1.1", creator="http://www.geoplaner.com",
                          xmlns="http://www.topografix.com/GPX/1/1",
                          schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd")
        rte = ET.SubElement(root, "rte")

        ET.SubElement(rte, "name").text = "Route1"
        file_viewWPs = open(completeName_viewWPs, "w")
        for j in range(len(WGS84_Coords_interval[i])):
            for k in range(len(WGS84_Coords_interval[i][j])):
                for l in range(len(WGS84_Coords_interval[i][j][k])):
                    print(WGS84_Coords_interval[i][j][k][l][0], ",", WGS84_Coords_interval[i][j][k][l][1], ";")
                    file_viewWPs.write(''.join(
                        '{}, {}'.format(WGS84_Coords_interval[i][j][k][l][0], WGS84_Coords_interval[i][j][k][l][1])))

                    file_viewWPs.write('\n')

                    elem = ET.SubElement(rte, "rtept", lat=str(WGS84_Coords_interval[i][j][k][l][0]),
                                         lon=str(WGS84_Coords_interval[i][j][k][l][1]))
                    ET.SubElement(elem, "ele").text = "WP" + str(l)
                    ET.SubElement(elem, "name").text = "WP" + str(l)

                tree = ET.ElementTree(root)
                tree.write("" + str(i + 1) + ".gpx",
                    xml_declaration="1.0",
                    encoding="UTF-8")

    file_viewWPs.close()
    for i in range(len(wp_interval)):
        for j in range(len(wp_interval[i])):
            for k in range(len(wp_interval[i][j])):
                # print(wp_interval[i][j][k][0], wp_interval[i][j][k][1])
                view_points.append(airsim.Vector3r(wp_interval[i][j][k][0], wp_interval[i][j][k][1], z))
                names.append("No {}".format(k))
    client.simPlotPoints(points=view_points, size=30, is_persistent=True)
    # client.simPlotStrings(strings=names, positions=path_No1, color_rgba=[1.0, 1.0, 0.0, 1.0])

    airsim.wait_key('Press any key to reset to original state')
    client.armDisarm(False, "Drone1")
    client.reset()

    # that's enough fun for now. let's quit cleanly
    client.enableApiControl(False, "Drone1")
