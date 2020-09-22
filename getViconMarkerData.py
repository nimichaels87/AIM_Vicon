import Vicon
import numpy as np

if __name__ == '__main__':
    #file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/old_AFO_design_Mocap_test1.csv"
    #file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test1.csv"
    file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"
    data = Vicon.Vicon(file)
    markers = data.get_markers()
    mkr1 = data.get_markers().get_marker("nathan_Rfoot1")
    mkr2 = data.get_markers().get_marker("nathan_Rfoot2")
    mkr3 = data.get_markers().get_marker("nathan_Rfoot3")
    newMKR1x = []
    newMKR1y = []
    newMKR1z = []
    print("MKR1-X: ")
    print(mkr1[1].x)
    print("MKR1-Y: ")
    print(mkr1[1].y)
    print("MKR1-Z: ")
    print(mkr1[1].z)
    print("")
    print("MKR2-X: ")
    print(mkr2[1].x)
    print("MKR2-Y: ")
    print(mkr2[1].y)
    print("MKR2-Z: ")
    print(mkr2[1].z)
    print("")
    print("MKR3-X: ")
    print(mkr3[1].x)
    print("MKR3-Y: ")
    print(mkr3[1].y)
    print("MKR3-Z: ")
    print(mkr3[1].z)
    markers.smart_sort() # sort the markers into bodies by the names
    markers.play()


    # mkr1 = data.get_markers().get_marker("nathan_Rfoot1")
    # mkr2 = data.get_markers().get_marker("nathan_Rfoot2")
    # mkr3 = data.get_markers().get_marker("nathan_Rfoot3")
    # newMKR1x = []
    # newMKR1y = []
    # newMKR1z = []
    # print(mkr3[100].x)
    # print(mkr3[100].y)
    # print(mkr3[100].z)
    # mocapBoxNum = ((len(mkr1))/100) + 1
    #
    # for j in range(1, mocapBoxNum + 1):
    #     strtJter = (j-1)*100
    #     if j < mocapBoxNum:
    #         endJter = j*100
    #     else:
    #         endJter = len(mkr1) - 1
    #     tmpXList = [];
    #     tmpYList = [];
    #     tmpZList = [];
    #     for k in range(strtJter, endJter):
    #         tmpXList.append(float(mkr1[k].x))
    #         tmpYList.append(float(mkr1[k].y))
    #         tmpZList.append(float(mkr1[k].z))
    #
    #     newMKR1x.append(np.mean(tmpXList))
    #     newMKR1y.append(np.mean(tmpYList))
    #     newMKR1z.append(np.mean(tmpZList))

    #print(len(newMKR1x))
    #print(mkr1[1:5])
    #print(type(float(mkr1[1].x)))
    #print(type(len(mkr1)))

    #[mkr3_X, mkr3_Y, mkr3_Z] = data.get_markers().mocapLinearFit("nathan_Rfoot3", 100)
    #print(mkr3_X)
