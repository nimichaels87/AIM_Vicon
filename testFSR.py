import FSR
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    file =  "/home/asus/Desktop/AFO Mocap Test - FSR Data/newAFODesignMocapTest3.csv"
    data = FSR.FSR(file)
    print("FSR 1 Readings:")
    print(data.get_fsr1())
    #print(len(data.get_fsr1()))
    print("FSR 2 Readings:")
    print(data.get_fsr2())
    print("FSR 3 Readings:")
    print(data.get_fsr3())

    print("CoP Readings (X & Y) at instance 2 (Flat Foot)")
    #[cenX, cenY]= (data.get_CoP(2))
    #print(cenX)
    #print(cenY)
    print(data.get_CoP_at_instance(2))
    print("CoP Readings (X & Y) at instance 20 (Toe Down)")
    print(data.get_CoP_at_instance(20))
    print("CoP Readings (X & Y) at instance 56 (Heel Down)")
    print(data.get_CoP_at_instance(56))

    #print(data.get_fsr_locations())
    #print(data.get_fsr_locations()[1])
    #print(data.get_fsr_locations()[1][0])

    ### Plot AFO CoP position data within subplots

    fsrCoP = data.get_CoP_List()
    CoP_X = []
    CoP_Y = []
    CoP_Z = []
    for i in range(0, len(fsrCoP)):
        CoP_X.append(fsrCoP[i][0])
        CoP_Y.append(fsrCoP[i][1])
        CoP_Z.append(fsrCoP[i][2])

    fig, ax = plt.subplots(3, 1, figsize=(9, 3), sharex=True)

    ax[0].plot(CoP_X, color='blue', label='AFO')
    ax[0].set_ylabel('X-Coord')
    ax[0].legend()
    ax[1].plot(CoP_Y, color='green', label='AFO')
    ax[1].set_ylabel('Y-Coord')
    ax[1].legend()
    ax[2].plot(CoP_Z, color='orange', label='AFO')
    ax[2].set_ylabel('Z-Coord')
    ax[2].legend()
    plt.show()
