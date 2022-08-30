""" find parallel ViewWPs """
import geopy as gp
import geopy.distance
from geopy.distance import great_circle


def parallel_ViewWPs(scanDist=2.55/2, ViewWP=[50.61466238436415, 6.989793137702924]):
	distance = geopy.distance.distance(meters=scanDist)  # Define the distance between flight path lines
	start = gp.Point(ViewWP[0], ViewWP[1])
	result = distance.destination(start, 45 + 90)  # no radians here
	return result


result = parallel_ViewWPs()
print(result.latitude, result.longitude)
