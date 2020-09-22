import Vicon
import FSR
import matplotlib.pyplot as plt
import numpy as np
import Markers as MK
from lib.GaitCore.Core.Point import Point


if __name__ == "__main__":
    #fsrFile_trial1 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/oldAFODesignMocapTest1.csv"
    #fsrFile_trial3 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/oldAFODesignMocapTest2.csv"
    #viconFile_trial1 = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test1.csv"
    #viconFile_trial3 = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/old_AFO_design_Mocap_test2.csv"

    fsrFile_trial1 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/newAFODesignMocapTest1.csv"
    fsrFile_trial3 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/newAFODesignMocapTest3.csv"
    viconFile_trial1 = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test1.csv"
    viconFile_trial3 = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"

    ## Initialize FSR and Vicon Data objects for each trial
    fsrData_trial1 = FSR.FSR(fsrFile_trial1)
    fsrData_trial3 = FSR.FSR(fsrFile_trial3)
    viconData_trial1 = Vicon.Vicon(viconFile_trial1)
    viconData_trial3 = Vicon.Vicon(viconFile_trial3)

    ### Calculate AFO CoP position with respect to World Frame for both Trials
    markerNameList = ["nathan_Rfoot1", "nathan_Rfoot2", "nathan_Rfoot3"]
    trueRefFrame = [Point(-80.236, 264.052, 56), Point(0, 0, 56), Point(81.969, 250.269, 56)]
    #trueRefFrame = [Point(0, 0, 56), Point(80.236, -264.052, 56), Point(162.204, -13.783, 56)]
    [afoCoP_X_1, afoCoP_Y_1, afoCoP_Z_1] = fsrData_trial1.transformAFOCoP_into_WorldFrame(viconData_trial1,
                                                                                          markerNameList, trueRefFrame)
    [afoCoP_X_3, afoCoP_Y_3, afoCoP_Z_3] = fsrData_trial3.transformAFOCoP_into_WorldFrame(viconData_trial3,
                                                                                          markerNameList, trueRefFrame)

    ### Linear Fit Regression of the Force-Plate CoP data for each trial
    [avgFPCoP_X_1, avgFPCoP_Y_1, avgFPCoP_Z_1] = viconData_trial1.get_force_plate(1).get_CoP_LinearRegressionFit(1000)
    [avgFPCoP_X_3, avgFPCoP_Y_3, avgFPCoP_Z_3] = viconData_trial3.get_force_plate(1).get_CoP_LinearRegressionFit(1000)

    ### Make subplots showing the AFO-v-Force-Plate CoP comparisions for each trial
    fig, ax = plt.subplots(3, 2, figsize=(12,6), sharex=True)
    # Plot X-Coordinate Positions
    ax[0, 0].plot(afoCoP_X_1, color='blue', label='AFO')
    ax[0, 0].plot(avgFPCoP_X_1, color='red', label='Force-Plate')
    ax[0, 1].plot(afoCoP_X_3, color='blue', label='AFO')
    ax[0, 1].plot(avgFPCoP_X_3, color='red', label='Force-Plate')
    ax[0, 0].set_title('Trial #1 CoP Position readings wrt Origin', fontsize=15)
    ax[0, 1].set_title('Trial #2 CoP Position readings wrt Origin', fontsize=15)
    ax[0, 0].set_ylabel('X-Pos (mm)', fontsize=13)
    ax[0, 0].legend(bbox_to_anchor=(0, -.005, 1, -.005), ncol=2, mode="expand", borderaxespad=0.)
    ax[0, 1].legend(bbox_to_anchor=( 0, -.005, 1, -.005),  ncol=2,  mode="expand", borderaxespad=0.)
    ax[0, 0].grid()
    ax[0, 1].grid()
    # Plot Y-Coordinate Positions
    ax[1, 0].plot(afoCoP_Y_1, color='green', label='AFO')
    ax[1, 0].plot(avgFPCoP_Y_1, color='purple', label='Force-Plate')
    ax[1, 1].plot(afoCoP_Y_3, color='green', label='AFO')
    ax[1, 1].plot(avgFPCoP_Y_3, color='purple', label='Force-Plate')
    ax[1, 0].set_ylabel('Y-Pos (mm)', fontsize=13)
    ax[1, 0].legend(bbox_to_anchor=(0, -.005, 1, -.005), ncol=2, mode="expand", borderaxespad=0.)
    ax[1, 1].legend(bbox_to_anchor=(0, -.005, 1, -.005), ncol=2, mode="expand", borderaxespad=0.)
    ax[1, 0].grid()
    ax[1, 1].grid()
    # Plot Z-Coordinate Positions
    ax[2, 0].plot(afoCoP_Z_1, color='orange', label='AFO')
    ax[2, 0].plot(avgFPCoP_Z_1, color='black', label='Force-Plate')
    ax[2, 1].plot(afoCoP_Z_3, color='orange', label='AFO')
    ax[2, 1].plot(avgFPCoP_Z_3, color='black', label='Force-Plate')
    ax[2, 0].set_ylabel('Z-Pos (mm)', fontsize=13)
    ax[2, 0].legend(bbox_to_anchor=(0, -.105, 1, -.105), ncol=2, mode="expand", borderaxespad=0.)
    ax[2, 1].legend(bbox_to_anchor=(0, -.105, 1, -.105), ncol=2, mode="expand", borderaxespad=0.)
    ax[2, 0].grid()
    ax[2, 1].grid()
    plt.show()

    ### Make subplots showing CoP position between AFO and Force plates acrpss X-Y Axis
    f, ax2 = plt.subplots(2, 2, figsize=(12,8))
    ax2[0, 0].plot(avgFPCoP_X_1, avgFPCoP_Y_1)
    ax2[0, 0].set_title("Force-Plate CoP - Trial 1", fontsize=15)
    ax2[0, 0].grid()
    ax2[0, 0].set_ylabel('Y-Coord (mm)', fontsize=13)
    ax2[0, 0].set_xlim([-35, -335])
    #ax2[0, 0].set_xlim([-150, -250])
    ax2[0, 0].set_ylim([150, 450])

    ax2[0, 1].plot(avgFPCoP_X_3, avgFPCoP_Y_3)
    ax2[0, 1].set_title("Force-Plate CoP - Trial 2", fontsize=15)
    ax2[0, 1].grid()
    ax2[0, 1].set_xlim([-35, -335])
    ax2[0, 1].set_ylim([150, 450])

    ax2[1, 0].plot(afoCoP_X_1, afoCoP_Y_1)
    ax2[1, 0].set_title("AFO CoP - Trial 1", fontsize=15)
    ax2[1, 0].grid()
    ax2[1, 0].set_xlabel('X-Coord (mm)', fontsize=13)
    ax2[1, 0].set_ylabel('Y-Coord (mm)', fontsize=13)
    ax2[1, 0].set_xlim([-35, -335])
    ax2[1, 0].set_ylim([150, 450])

    ax2[1, 1].plot(afoCoP_X_3, afoCoP_Y_3)
    ax2[1, 1].set_title("AFO CoP - Trial 2", fontsize=15)
    ax2[1, 1].grid()
    ax2[1, 1].set_xlabel('X-Coord (mm)', fontsize=13)
    ax2[1, 1].set_xlim([-35, -335])
    ax2[1, 1].set_ylim([150, 450])
    plt.show()
