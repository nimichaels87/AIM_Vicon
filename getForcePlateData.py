import Vicon
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"
    data = Vicon.Vicon(file)
    fp = data.get_force_plate(1).get_CoP()
    print(fp.x[1])
    #print(fp.y)
    #print(fp.z)
    print(len(fp.x))
    fpX = fp.x
    fpY = fp.y
    fpZ = fp.z
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
    boxNum = ((len(fp.x))/1000) + 1
    #print(boxNum)
    for i in range(1, boxNum+1):
        strtIter = (i - 1)*1000
        if i < boxNum:
            endIter = i*1000
        else:
            endIter = len(fp.x)-1
            print(endIter)
        tmpList = fp.x[strtIter:endIter]
        iterArr.append(np.mean(tmpList))

    #print(len(iterArr))
    #print(iterArr)

    #[avgFCoP_X, avgFCoP_Y, avgFCoP_Z] = data.get_force_plate(1).get_CoP_LinearRegressionFit(1000)
    fig, ax = plt.subplots(3, 1, figsize=(9, 3), sharex=True)

    ax[0].plot(fpX, color='blue', label='X-Coord')
    ax[0].set_ylabel('X-Coord')
    #ax[0].legend()
    ax[1].plot(fpY, color='green', label='Y-Coord')
    ax[1].set_ylabel('Y-Coord')
    #ax[1].legend()
    ax[2].plot(fpZ, color='orange', label='AFO')
    ax[2].set_ylabel('Z-Coord')
    #ax[2].legend()
    plt.show()