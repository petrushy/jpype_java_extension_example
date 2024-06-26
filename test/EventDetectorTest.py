# -*- coding: utf-8 -*-

import MyOrekitProject
import jpype

# orekit_jpype.initVM(vmargs='-Xcheck:jni,-verbose:jni,-verbose:class,-XX:+UnlockDiagnosticVMOptions', additional_classpaths=['custom_jars/orekit_addons.jar'])
#orekit_jpype.initVM(additional_classpaths=['custom_jars/orekit_addons.jar'])
MyOrekitProject.initVM()

from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.bodies import OneAxisEllipsoid, GeodeticPoint
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.orbits import KeplerianOrbit
from org.orekit.utils import Constants
from org.orekit.propagation.analytical import KeplerianPropagator
from org.orekit.utils import PVCoordinates, IERSConventions
from org.orekit.propagation.events.handlers import EventHandler, ContinueOnEvent
from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.orekit.propagation.events import EventDetector, AdaptableInterval
from org.hipparchus.ode.events import Action
from org.orekit.propagation.events import AbstractDetector
from org.orekit.propagation.events import NewElevationDetector
from org.orekit.custom import EventCounter

from math import radians
import math
import unittest
import sys

import logging
logging.basicConfig(level=logging.DEBUG)

from orekit_jpype.pyhelpers import setup_orekit_curdir, download_orekit_data_curdir
#download_orekit_data_curdir()

setup_orekit_curdir()
from jpype import JImplements, JOverride, JFloat, JDouble

mycounter = EventCounter()

@JImplements(AdaptableInterval)
class MyAdaptableInterval():
    @JOverride
    def currentInterval(self, s):
        return float(AbstractDetector.DEFAULT_MAXCHECK)


@JImplements(EventDetector)
class MyElevationDetector():
    passes = 0

    def __init__(self, elevation, topo):
        self.elevation = elevation
        self.topo: TopocentricFrame = topo

    @JOverride
    def init(self, s, T):
        pass

    @JOverride
    def getThreshold(self):
        return float(AbstractDetector.DEFAULT_THRESHOLD)

    @JOverride
    def getMaxCheckInterval(self):
        return MyAdaptableInterval()

    @JOverride
    def getMaxIterationCount(self):
        return AbstractDetector.DEFAULT_MAX_ITER

    @JOverride
    def g(self, s):
        tmp = self.topo.getElevation(s.getPVCoordinates().getPosition(), s.getFrame(), s.getDate()) - self.elevation
        return tmp

    @JOverride
    def resetState(self, oldState):
        return oldState

    def getElevation(self):
        return self.elevation

    def getTopocentricFrame(self):
        return self.topo

    @JOverride
    def getHandler(self):
        return mycounter


class EventDetectorTest(unittest.TestCase):

    def testOwnElevationDetector(self):
        initialDate = AbsoluteDate(2014, 1, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
        inertialFrame = FramesFactory.getEME2000()  # inertial frame for orbit definition
        position = Vector3D(-6142438.668, 3492467.560, -25767.25680)
        velocity = Vector3D(505.8479685, 942.7809215, 7435.922231)
        pvCoordinates = PVCoordinates(position, velocity)
        initialOrbit = KeplerianOrbit(pvCoordinates,
                                      inertialFrame,
                                      initialDate,
                                      Constants.WGS84_EARTH_MU)

        kepler = KeplerianPropagator(initialOrbit)

        ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                                 Constants.WGS84_EARTH_FLATTENING,
                                 ITRF)

        # Station
        longitude = radians(45.0)
        latitude = radians(25.0)
        altitude = 0
        station1 = GeodeticPoint(latitude, longitude, float(altitude))
        sta1Frame = TopocentricFrame(earth, station1, "station 1")

        elevation = math.radians(5.0)

        detector = MyElevationDetector(elevation, sta1Frame)
        kepler.addEventDetector(detector)

        finalState = kepler.propagate(initialDate.shiftedBy(60 * 60 * 24.0 * 15))

        print(detector.passes)
        self.assertEqual(52, mycounter.getCount())

    def testNewJavaElevationDetector(self):
        initialDate = AbsoluteDate(2014, 1, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
        inertialFrame = FramesFactory.getEME2000()  # inertial frame for orbit definition
        position = Vector3D(-6142438.668, 3492467.560, -25767.25680)
        velocity = Vector3D(505.8479685, 942.7809215, 7435.922231)
        pvCoordinates = PVCoordinates(position, velocity)
        initialOrbit = KeplerianOrbit(pvCoordinates,
                                      inertialFrame,
                                      initialDate,
                                      Constants.WGS84_EARTH_MU)

        kepler = KeplerianPropagator(initialOrbit)

        ITRF = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                                 Constants.WGS84_EARTH_FLATTENING,
                                 ITRF)

        # Station
        longitude = radians(45.0)
        latitude = radians(25.0)
        altitude = 0
        station1 = GeodeticPoint(latitude, longitude, float(altitude))
        sta1Frame = TopocentricFrame(earth, station1, "station 1")

        elevation = math.radians(5.0)

        counter_new = EventCounter()
        detector = NewElevationDetector(sta1Frame).withConstantElevation(elevation).withHandler(counter_new)
        kepler.addEventDetector(detector)

        finalState = kepler.propagate(initialDate.shiftedBy(60 * 60 * 24.0 * 15))

        self.assertEqual(52, counter_new.getCount())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(EventDetectorTest)
    ret = not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(ret)
