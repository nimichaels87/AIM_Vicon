import Vicon
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    trial1_file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test1.csv"
    trial2_file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"
    viconData_T1 = Vicon.Vicon(trial1_file)
    viconData_T2 = Vicon.Vicon(trial2_file)
    fp_T1 = viconData_T1.get_force_plate(1).get_CoP()
    fp_T2 = viconData_T2.get_force_plate(1).get_CoP()
    print(fp_T2.x[1])
    #print(fp.y)
    #print(fp.z)
    print(len(fp_T2.x))
    #fpX = fp.x
    #fpY = fp.y
    #fpZ = fp.z
    #print(fpX[:10])
    #print(fpX[:20])
    #print(fpX[5:20])

    #testArr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #print(testArr[5:10])
    #print(testArr[1:9])
    #print(np.mean(testArr))

    iterArr = []
    #print(float(len(fp.x))/1000)
    #print(len(fp.x)/1000)
    boxNum = ((len(fp_T2.x))/1000) + 1
    #print(boxNum)
    for i in range(1, boxNum+1):
        strtIter = (i - 1)*1000
        if i < boxNum:
            endIter = i*1000
        else:
            endIter = len(fp_T2.x)-1
            print(endIter)
        tmpList = fp_T2.x[strtIter:endIter]
        iterArr.append(np.mean(tmpList))

    #print(len(iterArr))
    #print(iterArr)

    [fpX_1, fpY_1, fpZ_1] = viconData_T1.get_force_plate(1).get_CoP_LinearRegressionFit(1000)
    [fpX_2, fpY_2, fpZ_2] = viconData_T2.get_force_plate(1).get_CoP_LinearRegressionFit(1000)

    ## Test printing CoP data for a single trial
    fig, ax = plt.subplots(3, 1, figsize=(9, 3), sharex=True)

    ax[0].plot(fpX_2, color='blue', label='Force-Plate')
    ax[0].set_ylabel('X-Coord')
    ax[0].legend()
    ax[1].plot(fpY_2, color='green', label='Force-Plate')
    ax[1].set_ylabel('Y-Coord')
    ax[1].legend()
    ax[2].plot(fpZ_2, color='orange', label='Force-Plate')
    ax[2].set_ylabel('Z-Coord')
    ax[2].legend()
    plt.show()

    ## Show force-plate CoP data for both trials
    fig, ax2 = plt.subplots(3, 2, figsize = (12, 8), sharex=True)
    ax2[0, 0].plot(fpX_1, color='blue', label='Force-Plate')
    ax2[0, 0].grid()
    ax2[0, 0].title.set_text('Trial #1 Force-Plate CoP position wrt Origin')
    ax2[0, 0].set_ylabel('X-Coord (mm)')
    ax2[0, 1].plot(fpX_2, color='blue', label='Force-Plate')
    ax2[0, 1].grid()
    ax2[0, 1].title.set_text('Trial #2 Force-Plate CoP position wrt Origin')

    ax2[1, 0].plot(fpY_1, color='green', label='Force-Plate')
    ax2[1, 0].grid()
    ax2[1, 0].set_ylabel('Y-Coord (mm)')
    ax2[1, 1].plot(fpY_2, color='green', label='Force-Plate')
    ax2[1, 1].grid()

    ax2[2, 0].plot(fpZ_1, color='orange', label='Force-Plate')
    ax2[2, 0].grid()
    ax2[2, 0].set_xlabel('Time (sec)')
    ax2[2, 0].set_ylabel('Z-Coord (mm)')
    ax2[2, 1].plot(fpZ_2, color='orange', label='Force-Plate')
    ax2[2, 1].grid()
    ax2[2, 1].set_xlabel('Time (sec)')
    plt.show()