import numpy as np
import cv2 as cv

#Load in initial camera calibration parameters
savedir = 'calibration_data/'
writeValues=False
cam_mtx = np.load(savedir+'optimalIntrinsic.npy')
rvecs = np.load(savedir+'rvecs.npy')
tvecs = np.load(savedir+'tvecs.npy')
dist = np.load(savedir+'dist.npy')
#load center points from New Camera matrix
cx=cam_mtx[0,2]
cy=cam_mtx[1,2]
fx=cam_mtx[0,0]
print("cx: "+str(cx)+",cy "+str(cy)+",fx "+str(fx))


#MANUALLY INPUT YOUR MEASURED POINTS HERE
#ENTER (X,Y,d*)
#d* is the distance from your point to the camera lens. (d* = Z for the camera center)
#we will calculate Z in the next steps after extracting the new_cam matrix


#world center + 9 world points

total_points_used=9

X_center=14
Y_center=10
Z_center=69
loonie_rad = 26.5/2 #mm
worldPoints=np.array([[X_center,Y_center,Z_center],                      
                       [4,3,69],
                       [14,3,67],
                       [24,3,70],
                       [4,9,70],
                       [14,10,69],
                       [23,10,70],
                       [4,17,70],
                       [14,17,70],
                       [23,17,71]], dtype=np.float32)

#MANUALLY INPUT THE DETECTED IMAGE COORDINATES HERE
pixel_rad = 30 #pixels
#[u,v] center + 9 Image points
imagePoints=np.array([[cx,cy],
                       [180,92],
                       [304,92],
                       [436,90],
                       [180,196],
                       [310,198],
                       [442,200],
                       [178,290],
                       [306,290],
                       [444,288]], dtype=np.float32)
                       

#FOR REAL WORLD POINTS, CALCULATE Z from d*

for i in range(0,total_points_used):
    #start from 1, given for center Z=d*
    #to center of camera
    wX=worldPoints[i,0]-X_center
    wY=worldPoints[i,1]-Y_center
    wd=worldPoints[i,2]

    d1=np.sqrt(np.square(wX)+np.square(wY))
    wZ=np.sqrt(np.square(wd)-np.square(d1))
    worldPoints[i,2]=wZ

print(worldPoints)


#print(ret)
print("Camera Matrix")
print(cam_mtx)


print("New Camera Matrix")
print(cam_mtx)
inverse_newcam_mtx = np.linalg.inv(cam_mtx)
print("Inverse New Camera Matrix")
print(inverse_newcam_mtx)
if writeValues==True: np.save(savedir+'inverse_newcam_mtx.npy', inverse_newcam_mtx)

print(">==> Calibration Loaded")


print("solvePNP")
ret, rvec1, tvec1=cv.solvePnP(worldPoints,imagePoints,cam_mtx,dist)

print("pnp rvec1 - Rotation")
print(rvec1)
if writeValues==True: np.save(savedir+'rvec1.npy', rvec1)

print("pnp tvec1 - Translation")
print(tvec1)
if writeValues==True: np.save(savedir+'tvec1.npy', tvec1)

print("R - rodrigues vecs")
R_mtx, jac=cv.Rodrigues(rvec1)
print(R_mtx)
if writeValues==True: np.save(savedir+'R_mtx.npy', R_mtx)

print("R|t - Extrinsic Matrix")
Rt=np.column_stack((R_mtx,tvec1))
print(Rt)
if writeValues==True: np.save(savedir+'Rt.npy', Rt)

print("newCamMtx*R|t - Projection Matrix")
P_mtx=cam_mtx.dot(Rt)
print(P_mtx)
if writeValues==True: np.save(savedir+'P_mtx.npy', P_mtx)

s_arr=np.array([0], dtype=np.float32)
s_describe=np.array([0,0,0,0,0,0,0,0,0,0],dtype=np.float32)

for i in range(0,total_points_used):
    print("=======POINT # " + str(i) +" =========================")
    
    print("Forward: From World Points, Find Image Pixel")
    XYZ1=np.array([[worldPoints[i,0],worldPoints[i,1],worldPoints[i,2],1]], dtype=np.float32)
    XYZ1=XYZ1.T
    print("{{-- XYZ1")
    print(XYZ1)
    suv1=P_mtx.dot(XYZ1)
    print("//-- suv1")
    print(suv1)
    s=suv1[2,0]    
    uv1=suv1/s
    print(">==> uv1 - Image Points")
    print(uv1)
    print(">==> s - Scaling Factor")
    print(s)
    s_arr=np.array([s/total_points_used+s_arr[0]], dtype=np.float32)
    s_describe[i]=s
    if writeValues==True: np.save(savedir+'s_arr.npy', s_arr)

    print("Solve: From Image Pixels, find World Points")

    uv_1=np.array([[imagePoints[i,0],imagePoints[i,1],1]], dtype=np.float32)
    uv_1=uv_1.T
    print(">==> uv1")
    print(uv_1)
    suv_1=s*uv_1
    print("//-- suv1")
    print(suv_1)

    np.save(savedir+'scalingfactor.npy', s)