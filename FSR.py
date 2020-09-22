import serial
import csv
import Vicon
import matplotlib.pyplot as plt
import numpy as np
import Markers as MK
from lib.GaitCore.Core.Point import Point


class FSR(object):
    def __init__(self, file_path):
        self._file_path = file_path
        #self._fsr_locations = [[26.331, 225.478, -28.715], [-23.269, 250.84, -28.715],  [3.553, 73.573, -28.715]]
        self._fsr_locations = [[26.331, 225.478, -28.715], [-23.269, 250.84, -28.715],  [-3.553, 73.573, -28.715]]
        #self._fsr_locations = [[23.269, 250.84, -28.715], [-26.331, 225.478, -28.715], [3.553, 73.573, -28.715]]

        #self._fsr_locations = [[-23.269, 250.84, -28.715], [26.331, 225.478, -28.715], [3.553, 73.573, -28.715]]
        self._marker_locations = [[-80.236, 264.052, 0], [0, 0, 0], [81.969, 250.269, 0]]

        #self._fsr_locations = [[56.967, -13.212, -28.715], [106.567, -38.574, -28.715], [83.789, -190.479, -28.715]]
        #self._marker_locations = [[0, 0, 0], [80.236, -264.052, 0], [162.204, -13.783, 0]]
        #self._inBallMkrLoc = [-80.236, 264.052, 0]
        #self._outBallMkrLoc = [81.969, 250.269, 0]
        #self._heelMkrLoc = [0, 0, 0]

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

    def get_Mkr_locations(self):
        """
        Get Marker locations relative to AFO frame
        :return:
        """
        return self._marker_locations

    def get_local_CoP_List(self):
        """

        :return:
        """
        CoP_List = []
        for i in range(0, (len(self._fsr1))):
            CoP_List.append(self.get_CoP_at_instance(i))
        return CoP_List

    def get_local_CoP_Coord_Lists(self):
        """
        Alt. function to "get_local_CoP_List()".  Returns calculated CoP positions in local AFO ref frame as seperate
        lists for the X,Y,Z coordinates.  Usefull for plotting the results.
        :return: CoP_X, CoP_Y, CoP_Z:  Lists containing the X,Y,Z coordinate values for the CoP during the trial.
        """
        CoP_X = []
        CoP_Y = []
        CoP_Z = []
        for i in range(0, (len(self._fsr1))):
            [tmpX, tmpY, tmpZ] = self.get_CoP_at_instance(i)
            CoP_X.append(tmpX)
            CoP_Y.append(tmpY)
            CoP_Z.append(tmpZ)
        return [CoP_X, CoP_Y, CoP_Z]

    def get_CoP_at_instance(self, instance):
        """
        Return the Center-of-Pressure location determined by the FSRs in the AFO's local coordinate frame
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
        #defaultX = (56.967 + 106.567 + 83.789)/3.0
        #defaultY = (-13.212 + -38.574 + -190.479)/3.0
        defaultX = (-23.269 + 26.331 + -3.553)/3.0
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


    def transformAFOCoP_into_WorldFrame(self, ViconDataFile, mkrNameList, trueRefFrame):
        """
        Using given Vicon-Marker Positions and Names within world-frame, transform the calculated AFO-CoP position list
        into the "World Frame Coordinates" of the Vicon Testing Lab.  Then, return X, Y, Z position coordinates as lists
        :param ViconDataFile: String containing the file-directory location of the .csv file for a given Vicon Marker
        data set for a specific trial.
        :param mkrNameList: List of strings containing the "names" of each individual "marker" used within the trial,
        as they appear within the ViconDataFile.csv file.
        :param trueRefFrame: The Positions of each of the Mocap Markers if the origin of the AFO ref. frame was lined
        up exactly with the "World" ref. frame.  (This should be tested beforehand to make sure which marker is which)
        :return: afoCoPWorldPos_X, afoCoPWorldPos_Y, afoCoPWorldPos_Z - Lists containing the X,Y,Z position coordinates
        of the AFO's CoP point transformed into the World Frame.
        """
        afoCoP = self.get_local_CoP_List()
        ### Get Vicon Marker and Force-Plate Data
        if isinstance(ViconDataFile, str): viconData = Vicon.Vicon(ViconDataFile)
        else: viconData = ViconDataFile

        ### Perform Linear Regression Fit to shrink Vicon Marker-Position data down to 76 data points
        mkrDataList = []
        for i in range(0, len(mkrNameList)):
            tmpMkr = viconData.get_markers().mocapLinearFit_PointCore((mkrNameList[i]), 100)
            mkrDataList.append(tmpMkr)

        ### Calculate Transformation Matrices between World Frame and AFO Frame during the test
        t_Matrices = []  # Stores Transformation Matrices at each time-instances
        err_Terms = []  # Stores RMS-Error at each time-instances
        t_Inverse = []  # Stores Inverted Transformation Matrices for each time-instances
        for j in range(0, len(afoCoP)):
            currentRefFrame = []
            for k in range(0, len(mkrDataList)):
                markerJ = mkrDataList[k]
                currentRefFrame.append(markerJ[j])
            T, err = MK.cloud_to_cloud(trueRefFrame, currentRefFrame)
            #T, err = MK.cloud_to_cloud(currentRefFrame, trueRefFrame)
            T_Inv = np.linalg.inv(T)  ## Invert the transformation matrix
            t_Matrices.append(T)
            err_Terms.append(err)
            t_Inverse.append(T_Inv)

        ### Use Transformation Matrices to determine AFO CoP position within the World-frame
        p_world_to_afo = []
        for ii in range(0, len(t_Matrices)):
            T_l_to_W = t_Matrices[ii]
            T_Inv = t_Inverse[ii]
            p_afo = np.array([afoCoP[ii][0], afoCoP[ii][1], afoCoP[ii][2], 1])#.reshape((-1,1))
            #newPosition_FOUR_BY_ONE = np.dot(T_Inv, p_afo)
            newPosition_FOUR_BY_ONE = np.dot(t_Matrices[ii], p_afo)
            #newPosition_FOUR_BY_ONE = np.dot(np.identity(4), np.dot(t_Matrices[ii], p_afo))
            newPosition_THREE_BY_ONE = [newPosition_FOUR_BY_ONE[0], newPosition_FOUR_BY_ONE[1], newPosition_FOUR_BY_ONE[2]]
            p_world_to_afo.append(newPosition_THREE_BY_ONE)

        ###  Put AFO-CoP position values into seperate lists corresponding to X, Y, & Z coordinates
        afoCoPWorldPos_X = []
        afoCoPWorldPos_Y = []
        afoCoPWorldPos_Z = []
        for iii in range(0, len(p_world_to_afo)):
            afoCoPWorldPos_X.append(p_world_to_afo[iii][0])
            afoCoPWorldPos_Y.append(p_world_to_afo[iii][1])
            afoCoPWorldPos_Z.append(p_world_to_afo[iii][2])

        return [afoCoPWorldPos_X, afoCoPWorldPos_Y, afoCoPWorldPos_Z]




    def simplify_fsrData(self, raw_fsrData):
        """
        'Simplify' a given set of FSR data values, such that the values returned lie in the range of 0-to-1 instead of
        0-to-1023
        :param raw_fsrData: raw set of data taken from a specific FSR sensor for a given trial
        :return: simpFSRdata:  list of 'simplified' FSR data values
        """
        simpFSRdata = []
        for i in range(0, len(raw_fsrData)):
            simpFSRdata.append(int(raw_fsrData[i])/1023.0)
        return simpFSRdata



    def binarize_fsrData(self, N, noiseCutOff, returnSimpData):
        """
        'Binarizes' FSR data, such that values returned by individual FSRs are reduced to simple "On" or "Off" value
        states, depending on whether or not they lie above a certain Noise Cut-Off value.
        :param N:
        :param noiseCutOff:  The "raw data value' cut-off threshold used to separate raw FSR data values into either
        'noise' or 'Actual data'.  Any values < noiseCutOff are considered to be the result of static "noise" and can be
        dismissed.  Any values >= noiseCutOff are considered to be valid indications of the FSRs being activated.
        :param returnSimpData:  boolean value that tells the function whether or not it should also return the data it
        received from the 'simplify_fsrData()' function
        :return:
        """
        if noiseCutOff > 1:  # Check to make-sure entered Noise Cut-Off value is valid
            noiseCutOff = int(noiseCutOff/1023.0)

        simp_fsr1 = self.simplify_fsrData(self.get_fsr1())
        simp_fsr2 = self.simplify_fsrData(self.get_fsr2())
        simp_fsr3 = self.simplify_fsrData(self.get_fsr3())

        fsr1_conv = np.convolve(simp_fsr1, np.ones(N,)/N, mode='valid')
        fsr2_conv = np.convolve(simp_fsr2, np.ones(N,)/N, mode='valid')
        fsr3_conv = np.convolve(simp_fsr3, np.ones(N,)/N, mode='valid')

        binMapVal_fsr1 = lambda a: int(a > noiseCutOff)
        binMapVal_fsr2 = lambda a: int(a > noiseCutOff)
        binMapVal_fsr3 = lambda a: int(a > noiseCutOff)

        fsr1_Bin = map(binMapVal_fsr1, fsr1_conv)
        fsr2_Bin = map(binMapVal_fsr2, fsr2_conv)
        fsr3_Bin = map(binMapVal_fsr3, fsr3_conv)

        ### Find indices where the 'Toe Down' and 'Heel Down' phases BEGIN in the data set
        toeDwnStrt = fsr3_Bin.index(0) - 1
        HeelDwnStrt = fsr2_Bin.index(0) - 1

        ### Find indices where the 'Toe Down' and 'Heel Down' phases END in the data set.
        ToeDwnPeriod = []
        HeelDwnPeriod = []
        for i in range(0, len(fsr3_Bin)):
            if fsr3_Bin[i] == 0:
                ToeDwnPeriod.append(i)
        for i in range(0, len(fsr2_Bin)):
            if fsr2_Bin[i] == 0:
                HeelDwnPeriod.append(i)
        toeDwnEnd = ToeDwnPeriod[(len(ToeDwnPeriod)) - 1]
        HeelDwnEnd = HeelDwnPeriod[(len(HeelDwnPeriod)) - 1]

        if returnSimpData == True:
            return [fsr1_Bin, fsr2_Bin, fsr3_Bin, toeDwnStrt, toeDwnEnd, HeelDwnStrt, HeelDwnEnd,
                    simp_fsr1, simp_fsr2, simp_fsr3]
        else:
            return [fsr3_Bin, fsr2_Bin, fsr3_Bin, toeDwnStrt, toeDwnEnd, HeelDwnStrt, HeelDwnEnd]





    def plot_Raw_v_Binarized_Data(self, N, noiseCutOff, leftTitleStr, rightTitleStr):
        [fsr1B, fsr2B, fsr3B, tDS, tDE, hDS, hDE, fsr1S, fsr2S, fsr3S] = self.binarize_fsrData(N, noiseCutOff, True)
        print("Toe Down Start:")
        print()
        fig, ax = plt.subplots(3, 2, figsize=(12, 6), sharex=True)
        ax[0, 0].plot(fsr1S, color='blue', label='Inner-Ball')
        ax[0, 0].set_ylabel('Inner-Ball FSR')
        ax[0, 0].title.set_text(leftTitleStr)
        ax[0, 0].grid()
        ax[0, 0].set_ylim([-0.05, 1.05])
        ax[1, 0].plot(fsr2S, color='green', label='Outer-Ball')
        ax[1, 0].set_ylabel('Outer-Ball FSR')
        ax[1, 0].grid()
        ax[1, 0].set_ylim([-0.05, 1.05])
        ax[2, 0].plot(fsr3S, color='orange', label='Heel')
        ax[2, 0].set_ylabel('Heel FSR')
        ax[2, 0].grid()
        ax[2, 0].set_ylim([-0.05, 1.05])
        ax[2, 0].set_xlabel('Time (sec)')

        ax[0, 1].plot(fsr1B, color='blue', label='Inner-Ball')
        ax[0, 1].title.set_text(rightTitleStr)
        ax[0, 1].grid()
        ax[0, 1].set_ylim([-0.05, 1.05])
        ax[1, 1].plot(fsr2B, color='green', label='Outer-Ball')
        ax[1, 1].grid()
        ax[1, 1].set_ylim([-0.05, 1.05])
        ax[2, 1].plot(fsr3B, color='orange', label='Heel')
        ax[2, 1].grid()
        ax[2, 1].set_ylim([-0.05, 1.05])
        ax[2, 1].set_xlabel('Time (sec)')

        ## Extra code intended to label points where the "Toe Down" and "Heel Down" positions begin and end directly
        ## on the plot.  Had trouble getting the arrows and word bubbles to look good on plot, so commented these out.
        # ax[0, 1].annotate('', xy=(tDS, 0), xytext=(tDS, 1), arrowprops=dict(facecolor='black', shrink=0.00025))
        # ax[0, 1].annotate('', xy=(tDE, 0), xytext=(tDE, 1), arrowprops=dict(facecolor='black', shrink=0.00025))
        # ax[0, 1].annotate('', xy=(hDS, 0), xytext=(hDS, 1), arrowprops=dict(facecolor='black', shrink=0.00025))
        # ax[0, 1].annotate('', xy=(hDE, 0), xytext=(hDE, 1), arrowprops=dict(facecolor='black', shrink=0.00025))
        # ax[1, 1].text(tDS, 1.1, 'Toe Down Period', fontsize=9, bbox=dict(boxstyle="round", fc="w"))
        # ax[1, 1].text(tDE, 1.05, 'Toe Down End', fontsize=9, bbox=dict(boxstyle="round", fc="w"))
        # ax[1, 1].text(hDS, 1.1, 'Heel Down Period', fontsize=9, bbox=dict(boxstyle="round", fc="w"))
        # ax[1, 1].text(hDE, 1.05, 'Heel Down End', fontsize=9, bbox=dict(boxstyle="round", fc="w"))

        plt.show()


    ### Following methods were created to help debug AFO CoP position, but ultimately determined to be unnecessary
    def turn_CoP_from_Mkrs_into_Point(self, mkr1, mkr2, mkr3):
        CoP_List = self.get_CoP_from_Markers(mkr1, mkr2, mkr3)
        pntCoP_List = []
        for i in range(0, len(CoP_List)):
            mkrCoP_pnt = Point(CoP_List[i][0], CoP_List[i][1], CoP_List[i][2])
            pntCoP_List.append(mkrCoP_pnt)
        return pntCoP_List

    def get_CoP_from_Markers(self, mkr1, mkr2, mkr3):
        CoP_List = []

        for i in range(0, len(self._fsr1)):
            mrkr_Location = [[mkr1[i].x, mkr1[i].y, mkr1[i].z],
                             [mkr2[i].x, mkr2[i].y, mkr2[i].z],
                             [mkr3[i].x, mkr3[i].y, mkr3[i].z]]
            dataList = [self._fsr1[i], self._fsr2[i], self._fsr3[i]]
            CoP_List.append(self.calc_CoP(dataList, mrkr_Location))
        return CoP_List
