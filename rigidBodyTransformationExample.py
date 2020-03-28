import Vicon
from lib.GaitCore.Core.Point import Point

if __name__ == '__main__':
    #file = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"
    file = "/home/asus/AIM_Vicon/Examples/ExampleData/subject_03 Cal 03.csv"
    data = Vicon.Vicon(file)
    markers = data.get_markers()
    markers.smart_sort()

    frames = {}
    # Do severial bodies, use the marker location on the rigidbody
    frames["hip"] = [Point(0.0, 0.0, 0.0),
                     Point(70.0, 0, 0.0),
                     Point(0, 42.0, 0),
                     Point(35.0, 70.0, 0.0)]

    frames["RightThigh"] = [Point(0.0, 0.0, 0.0),
                            Point(56.0, 0, 0.0),
                            Point(0, 49.0, 0),
                            Point(56.0, 63.0, 0.0)]

    frames["RightShank"] = [Point(0.0, 0.0, 0.0),
                            Point(56.0, 0, 0.0),
                            Point(0, 42.0, 0),
                            Point(56.0, 70.0, 0.0)]

    markers.auto_make_transform(frames)

    # Get just one transform and the RMSE error
    # Can be used to get the transformation between ANY two sets of markers
    #m = markers.get_rigid_body("ben:hip")
    #f = [m[0][frame], m[1][frame], m[2][frame], m[3][frame]]
    #T, err = Markers.cloud_to_cloud(hip_marker, f)
