#!/usr/bin/env python
# //==============================================================================
# /*
#     Software License Agreement (BSD License)
#     Copyright (c) 2020, AIMVicon
#     (www.aimlab.wpi.edu)

#     All rights reserved.

#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions
#     are met:

#     * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.

#     * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.

#     * Neither the name of authors nor the names of its contributors may
#     be used to endorse or promote products derived from this software
#     without specific prior written permission.

#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#     FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#     COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#     INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#     BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#     LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#     LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#     ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#     POSSIBILITY OF SUCH DAMAGE.

#     \author    <http://www.aimlab.wpi.edu>
#     \author    <nagoldfarb@wpi.edu>
#     \author    Nathaniel Goldfarb
#     \version   0.1
# */
# //==============================================================================


import Devices
from lib.GaitCore.Core.Point import Point
from lib.GaitCore.Core.Newton import Newton
import numpy as np

class ForcePlate(Devices.Devices):

    def __init__(self, name, forces, moments, CoP):
        self.force = Point(forces["Fx"]["data"], forces["Fy"]["data"], forces["Fz"]["data"])
        self.moment = Point(moments["Mx"]["data"], moments["My"]["data"], moments["Mz"]["data"])
        self.CoP = Point(CoP["Cx"]["data"], CoP["Cy"]["data"], CoP["Cz"]["data"])
        sensor = Newton(self.CoP, self.force, self.moment, None)
        super(ForcePlate, self).__init__(name, sensor, "IMU")

    def get_forces(self):
        """

        :return: the force from the force plate
        :rtype: Point
        """
        return self._sensor.force

    def get_moments(self):
        """

        :return: the Moment from the force plate
        :rtype: Point
        """
        return self._sensor.moment

    def get_CoP(self):
        """

        :return: the CoP from the force plate
        :rtype: Point
        """
        return self._sensor.angle

    def get_CoP_LinearRegressionFit(self, timeMag):
        """
        Uses a Linear-Regression Fit to get a reduced list of CoP values
        :param timeMag:
        :return:
        """
        CoPList = self.get_CoP()
        fPlateBoxNum = ((len(CoPList.x)) / timeMag) + 1
        avgFCoP_X = []
        avgFCoP_Y = []
        avgFCoP_Z = []
        for i in range(1, fPlateBoxNum + 1):
            strtIter = (i - 1) * timeMag
            if i < fPlateBoxNum:
                endIter = i * timeMag
            else:
                endIter = len(CoPList.x) - 1
                #print(endIter)
            tmpListX = CoPList.x[strtIter:endIter]
            tmpListY = CoPList.y[strtIter:endIter]
            tmpListZ = CoPList.z[strtIter:endIter]
            avgFCoP_X.append(np.mean(tmpListX))
            avgFCoP_Y.append(np.mean(tmpListY))
            avgFCoP_Z.append(np.mean(tmpListZ))
        return [avgFCoP_X, avgFCoP_Y, avgFCoP_Z]

