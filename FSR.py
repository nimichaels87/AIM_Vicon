import matplotlib.pyplot as plt
import serial
import numpy as np
import csv

class FSR(object):
    def __init__(self, file_path):
        self._file_path = file_path
        self._fsr_locations = [[-23.269, 250.84, -28.715], [26.331, 225.478, -28.715], [3.553, 73.573, -28.715]]
        self._marker_locations = [[-80.236, 264.052, 0], [81.969, 250.269, 0], [0, 0, 0]]

        # Take FSR data directly from csv file and store it into lists for each individual FSR
        tmpFSR1 = []
        tmpFSR2 = []
        tmpFSR3 = []
        with open(self._file_path) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                tmpFSR1.append(int(row[0]))
                tmpFSR2.append(int(row[1]))
                tmpFSR3.append(int(row[2]))
        self._fsr1 = tmpFSR1
        self._fsr2 = tmpFSR2
        self._fsr3 = tmpFSR3



    def get_fsr1(self):
        """
        Get the FSR1 class object
        :return: fsr1
        :type:  List
        """
        return self._fsr1

    def get_fsr2(self):
        """
        Get the FSR2 class object
        :return: fsr2
        :type:  List
        """
        return self._fsr2

    def get_fsr3(self):
        """
        Get the FSR3 class object
        :return: fsr3
        :type:  List
        """
        return self._fsr3

    def get_fsr_locations(self):
        """
        Retrieve the XY-coordinate positions of each FSR
        :return:
        """
        return self._fsr_locations

    def get_CoP_List(self):
        CoP_List = []
        for i in range(0, (len(self._fsr1))):
            CoP_List.append(self.get_CoP_at_instance(i))
        return CoP_List

    def get_CoP_at_instance(self, instance):
        """
        Return the Center-of-Pressure location of the FSRs
        for a given instance in time
        :param instance: time-stamp
        :return:
        """
        dataList = [self._fsr1[instance], self._fsr2[instance], self._fsr3[instance]]
        [cenX, cenY, cenZ] = self.calc_CoP(dataList, self._fsr_locations)
        return [cenX, cenY, cenZ]

    def calc_CoP(self, sensor, location):
        """
            calculate the CoP of the foot based on the FSR location
            and force
            CoP_x = sum_i(F_i * x_i)/sum_i(F_i)
            CoP_y = sum_i(F_i * y_i)/sum_i(F_i)
            :return:
            """
        fsrs = sensor
        defaultX = (-23.269 + 26.331 + 3.553)/3.0
        defaultY = (250.84 + 225.478 + 73.573)/3.0
        defaultZ = 0.0
        total_force = 0
        centerX = 0
        centerY = 0
        #print location
        for fsr, loc in zip(fsrs, location):
            # print fsr
            # print loc
            total_force += fsr
            centerX += fsr * loc[0]
            centerY += fsr * loc[1]
        if total_force == 0:
            return [defaultX, defaultY, defaultZ]
        else:
            return [centerX / total_force, centerY / total_force, defaultZ]

