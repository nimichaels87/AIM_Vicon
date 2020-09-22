import Vicon
import FSR
import numpy as np

if __name__ == '__main__':
    fsrFile = "/home/asus/Desktop/AFO Mocap Test - FSR Data/newAFODesignMocapTest3.csv"
    forceAndViconFile = "/home/asus/Desktop/AFO Mocap Test - Force Plate Data/nathan_foot/test1/220200/new_AFO_design_Mocap_test3.csv"
    viconData = Vicon.Vicon(forceAndViconFile)
    markers = viconData.get_markers()


    ### Initialize FSR data object
    fsrData = FSR.FSR(fsrFile)

    ### Perform Linear Regression Fit to shrink Vicon Marker-Position data down to 76 data points
    mkr1 = viconData.get_markers().mocapLinearFit_PointCore("nathan_Rfoot1", 100)
    mkr2 = viconData.get_markers().mocapLinearFit_PointCore("nathan_Rfoot2", 100)
    mkr3 = viconData.get_markers().mocapLinearFit_PointCore("nathan_Rfoot3", 100)

    ### DEBUG - Use Mocap Marker Position data to calculate the AFO CoP
    fsrMkrCoP = fsrData.turn_CoP_from_Mkrs_into_Point(mkr1, mkr2, mkr3)

    markers.smart_sort()  # sort the markers into bodies by the names
    markers.play(fsrMkrCoP)