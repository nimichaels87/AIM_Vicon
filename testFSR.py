import FSR
import matplotlib.pyplot as plt
from lib.GaitCore.Core.Point import Point
import numpy as np

if __name__ == "__main__":
    fsrfile_v1T1 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/oldAFODesignMocapTest1.csv"
    fsrfile_v1T2 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/oldAFODesignMocapTest2.csv"
    fsrfile_v3T1 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/newAFODesignMocapTest1.csv"
    fsrfile_v3T2 = "/home/asus/Desktop/AFO Mocap Test - FSR Data/newAFODesignMocapTest3.csv"

    ## Create FSR data objects for each 'Trial' containing data sets for all 3 FSRs
    fsrData_v1T1 = FSR.FSR(fsrfile_v1T1)
    fsrData_v1T2 = FSR.FSR(fsrfile_v1T2)
    fsrData_v3T1 = FSR.FSR(fsrfile_v3T1)
    fsrData_v3T2 = FSR.FSR(fsrfile_v3T2)

    ## Test Printing out raw-value FSR readings
    print("FSR 1 Readings:")
    print(fsrData_v3T1.get_fsr1())
    #print(len(data.get_fsr1()))
    print("FSR 2 Readings:")
    print(fsrData_v3T1.get_fsr2())
    print("FSR 3 Readings:")
    print(fsrData_v3T1.get_fsr3())

    print("CoP Readings (X & Y) at instance 2 (Flat Foot)")
    #[cenX, cenY]= (data.get_CoP(2))
    #print(cenX)
    #print(cenY)
    print(fsrData_v3T1.get_CoP_at_instance(2))
    print("CoP Readings (X & Y) at instance 20 (Toe Down)")
    print(fsrData_v3T1.get_CoP_at_instance(20))
    print("CoP Readings (X & Y) at instance 56 (Heel Down)")
    print(fsrData_v3T1.get_CoP_at_instance(56))

    #print(data.get_fsr_locations())
    #print(data.get_fsr_locations()[1])
    #print(data.get_fsr_locations()[1][0])

    ### Initial test for Plotting AFO CoP position in local frame data within subplots
    fsrCoP_v3T1 = fsrData_v3T1.get_local_CoP_List()
    CoP_X_1 = []
    CoP_Y_1 = []
    CoP_Z_1 = []
    for i in range(0, len(fsrCoP_v3T1)):
        CoP_X_1.append(fsrCoP_v3T1[i][0])
        CoP_Y_1.append(fsrCoP_v3T1[i][1])
        CoP_Z_1.append(fsrCoP_v3T1[i][2])

    [CoP_X_2, CoP_Y_2, CoP_Z_2] = fsrData_v3T2.get_local_CoP_Coord_Lists()

    fig, ax = plt.subplots(3, 2, figsize=(12, 6), sharex=True)
    ax[0, 0].plot(CoP_X_1, color='blue', label='AFO')
    ax[0, 0].grid()
    ax[0, 0].title.set_text('Trial #1 AFO CoP Position wrt Local Frame')
    ax[0, 1].plot(CoP_X_2, color='blue', label='AFO')
    ax[0, 1].grid()
    ax[0, 1].title.set_text('Trial #2 AFO CoP Position wrt Local Frame')
    ax[0, 0].set_ylabel('X-Coord (mm)')
    #ax[0, 0].legend()
    ax[1, 0].plot(CoP_Y_1, color='green', label='AFO')
    ax[1, 0].grid()
    ax[1, 1].plot(CoP_Y_2, color='green', label='AFO')
    ax[1, 1].grid()
    ax[1, 0].set_ylabel('Y-Coord (mm)')
    #ax[1, 0].legend()
    ax[2, 0].plot(CoP_Z_1, color='orange', label='AFO')
    ax[2, 0].grid()
    ax[2, 0].set_xlabel('Time (sec)')
    ax[2, 0].set_ylabel('Z-Coord (mm)')
    ax[2, 1].plot(CoP_Z_2, color='orange', label='AFO')
    ax[2, 1].grid()
    ax[2, 1].set_xlabel('Time (sec)')
    #ax[2, 0].legend()
    plt.show()

    ## Test World-Frame transformation for AFO-calculated CoP Point

    markerNameList = ["nathan_Rfoot1", "nathan_Rfoot2", "nathan_Rfoot3"]
    viconFile_trial1 = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test1.csv"
    trueRefFrame = [Point(-80.236, 264.052, 56), Point(0, 0, 56), Point(81.969, 250.269, 56)]
    [afoCoP_X_1, afoCoP_Y_1, afoCoP_Z_1] = fsrData_v3T1.transformAFOCoP_into_WorldFrame(viconFile_trial1, markerNameList, trueRefFrame)

    ## Make subplots showing AFO CoP X,Y,Z coordinate positions
    fig, ax = plt.subplots(3, 1, figsize=(9, 5), sharex=True)

    ax[0].plot(afoCoP_X_1, color='blue', label='AFO')
    ax[0].set_ylabel('X-Coord')
    ax[0].legend()
    ax[1].plot(afoCoP_Y_1, color='green', label='AFO')
    ax[1].set_ylabel('Y-Coord')
    ax[1].legend()
    ax[2].plot(afoCoP_Z_1, color='orange', label='AFO')
    ax[2].set_ylabel('Z-Coord')
    ax[2].legend()
    plt.show()

    ### Plot Raw Sensor Values against 'Binarized' Results
    fsrData_v1T1.plot_Raw_v_Binarized_Data(4, 0.12, "SoleSensorV1 Trial #1 Raw Data", "SoleSensorV1 Trail #2 Binarized Data")
    fsrData_v1T2.plot_Raw_v_Binarized_Data(4, 0.12, "SoleSensorV1 Trial #2 Raw Data", "SoleSensorV1 Trial #2 Binarized Data")
    fsrData_v3T1.plot_Raw_v_Binarized_Data(4, 0.12, "SoleSensorV3 Trial #1 Raw Data", "SoleSensorV3 Trial #1 Binarized Data")
    fsrData_v3T2.plot_Raw_v_Binarized_Data(4, 0.12, "SoleSensorV3 Trial #2 Raw Data", "SoleSensorV3 Trial #2 Binarized Data")