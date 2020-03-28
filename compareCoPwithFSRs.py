import Vicon
import FSR
import matplotlib.pyplot as plt
import numpy as np
import Markers as MK
from lib.GaitCore.Core.Point import Point


if __name__ == "__main__":
    fsrFile = "/home/asus/Desktop/AFO Mocap Test - FSR Data/newAFODesignMocapTest3.csv"
    forceAndViconFile = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"

    ### Get Vicon Marker and Force-Plate Data
    viconData = Vicon.Vicon(forceAndViconFile)

    ### Perform Linear Regression Fit to shrink Vicon Marker-Position data down to 76 data points
    mkr1 = viconData.get_markers().mocapLinearFit_PointCore("nathan_Rfoot1", 100)
    mkr2 = viconData.get_markers().mocapLinearFit_PointCore("nathan_Rfoot2", 100)
    mkr3 = viconData.get_markers().mocapLinearFit_PointCore("nathan_Rfoot3", 100)

    #print(type(mkr1[1]))
    #print(mkr1[1])
    #print(len(mkr1))

    ### Get Force-Plate Force Data
    fpForce = viconData.get_force_plate(1).get_forces()

    ### Get Force-Plate Center of Pressure Data
    fCoP = viconData.get_force_plate(1).get_CoP()

    ### Linear Fit Regression of the Force-Plate CoP data
    [avgFCoP_X, avgFCoP_Y, avgFCoP_Z] = viconData.get_force_plate(1).get_CoP_LinearRegressionFit(1000)

    ### Initialize FSR data object
    fsrData = FSR.FSR(fsrFile)
    fsrCoP = fsrData.get_CoP_List()

    ### Calculate Transformation Matrices between World Frame and AFO Frame during the test
    trueRefFrame = [Point(-81.969, -250.269, 56),#28.715), #Point(-80.236, 264.052, 28.715),
                    Point(80.236, -264.052, 56),#28.715), #Point(81.969, 250.269, 28.715),
                    Point(0, 0, 56)]#28.715)]
    t_Matrices = []     # Stores Transformation Matrices at each time-instances
    err_Terms = []      # Stores RMS-Error at each time-instances
    t_Inverse = []      # Stores Inverted Transformation Matrices for each time-instances
    for i in range(0, len(fsrCoP)):
        currentRefFrame = [mkr1[i], mkr2[i], mkr3[i]]
        T, err = MK.cloud_to_cloud(trueRefFrame, currentRefFrame)
        T_Inv = np.linalg.inv(T)  ## Invert the transformation matrix
        t_Matrices.append(T)
        err_Terms.append(err)
        t_Inverse.append(T_Inv)
    
    print("Transformation at Flat-Foot Position & RMS Error:")
    print(t_Matrices[2])
    print(err_Terms[2])
    print("")
    print("Transformation at Toe-Down Position:")
    print(t_Matrices[20])
    print(err_Terms[20])
    print("")
    print("Transformation at Heel-Down Position:")
    print(t_Matrices[56])
    print(err_Terms[56])
    print("")
    print("Inverse-Transformation at Heel-Down Position:")
    print(t_Inverse[1])



    ### Use Transformation Matrices to determine AFO CoP position within the World-frame
    p_world_to_afo = []
    for j in range(0, len(t_Inverse)):
        T_Inv = t_Inverse[j]
        tmpVal = fsrCoP[j]
        p_afo = np.array([fsrCoP[j][0], fsrCoP[j][1], fsrCoP[j][2], 1])
        #newPosition_FOUR_BY_ONE = np.dot(T_Inv, p_afo)#T_Inv.dot(p_afo)
        #newPosition_FOUR_BY_ONE = np.dot(t_Matrices[j], p_afo)
        newPosition_FOUR_BY_ONE = np.dot(np.identity(4),np.dot(t_Matrices[j], p_afo))
        newPosition_THREE_BY_ONE = [newPosition_FOUR_BY_ONE[0], newPosition_FOUR_BY_ONE[1], newPosition_FOUR_BY_ONE[2]]
        p_world_to_afo.append(newPosition_THREE_BY_ONE)


    print("Position of AFO CoP @ Flat-Foot Position:")
    print(p_world_to_afo[2])
    print("Position of AFO CoP @ Toe-Down Position:")
    print(p_world_to_afo[20])
    print("Position of AFO CoP @ Heel-Down Position:")
    print(p_world_to_afo[56])
    print("")


    ###  Put AFO position values into seperate lists corresponding to X, Y, & Z coordinates
    p_X = []
    p_Y = []
    p_Z = []
    for k in range(0, len(p_world_to_afo)):
        p_X.append(p_world_to_afo[k][0])
        p_Y.append(p_world_to_afo[k][1])
        p_Z.append(p_world_to_afo[k][2])

    #print("Test")
    #print(p_X)
    #print("")
    ###
    flatFootArr = [avgFCoP_X[2], avgFCoP_Y[2], avgFCoP_Z[2]]
    toeDownArr = [avgFCoP_X[20], avgFCoP_Y[20], avgFCoP_Z[20]]
    heelDownArr = [avgFCoP_X[56], avgFCoP_Y[56], avgFCoP_Z[56]]
    print("")
    print("Position of Force-Plate CoP @ Flat-Foot Position:")
    print(flatFootArr)
    print("Position of Force-Plate CoP @ Toe-Down Position:")
    print(toeDownArr)
    print("Position of Force-Plate CoP @ Heel-Down Position:")
    print(heelDownArr)
    # Print out comparison of CoP position data between AFO and Force-plate


    ### Make subplots comparing CoP X, Y, Z coordinates between the AFO and Force-Plate Data
    fig, ax = plt.subplots(3, 1, figsize=(9,3), sharex=True)

    ax[0].plot(p_X, color='blue', label='AFO')
    ax[0].plot(avgFCoP_X, color='red', label='Force-Plate')
    ax[0].set_ylabel('X-Coord')
    ax[0].legend()
    ax[1].plot(p_Y, color='green', label='AFO')
    ax[1].plot(avgFCoP_Y, color='purple', label='Force-Plate')
    ax[1].set_ylabel('Y-Coord')
    ax[1].legend()
    ax[2].plot(p_Z, color='orange', label='AFO')
    ax[2].plot(avgFCoP_Z, color='black', label='Force-Plate')
    ax[2].set_ylabel('Z-Coord')
    ax[2].legend()
    plt.show()


