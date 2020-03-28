import Vicon
import Markers as MK
from lib.GaitCore.Core.Point import Point

if __name__ == '__main__':
    file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"
    data = Vicon.Vicon(file)
    markers = data.get_markers()
    markers.smart_sort()
    m = markers.get_rigid_body("nathan_Rfoot") # returns an array of markers
    ## Get the X corr of a marker 2 in frame 100
    xTest = m[2][100].x
    print(xTest)
    print(m[2][100].y)
    print(m[2][100].z)
    print(m[2][100])
    print(type(m[2]))
    #print(type(m))             Returns <type 'list'>
    #print(type(m[2][100]))     Returns <class 'lib.GaitCore.Core.Point.Point'>
    f = [m[0][100], m[1][100], m[2][100]]

    print(f)
    testTerm = [Point(0.0, 0.0, 0.0),
                Point(0.0, 0.0, 0.0),
                Point(0.0, 0.0, 0.0)]
    print(testTerm)
    print(testTerm[0])
    T, err = MK.cloud_to_cloud(testTerm, f)
    print(T)

