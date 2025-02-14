import cv2 as cv
import numpy as np
import random
import subprocess
import os
from calibCam import calibCamera

filedir = 'calibration_data/'

cap = cv.VideoCapture(0)
####################################READ INPUT VIDEO STREAM###########################################
state,frame = cap.read()
h, w = frame.shape[:2]
output = cv.VideoWriter("output.avi", cv.VideoWriter_fourcc(*'MPEG'), 30, (w, h)) 
while cap.isOpened():
    state, frame = cap.read()
    if state == True:
        output.write(frame)
        cv.imshow('video feed',frame)
        #press s to save video
        if cv.waitKey(1) & 0xFF == ord('s'): 
            break
output.release()  
cap.release()    
cv.destroyAllWindows()
output_file = 'output.mp4'
def convertVidFormat(output_file):
    command = ['ffmpeg', '-y', '-i', 'output.avi', '-vcodec', 'libx264', output_file]
    subprocess.run(command)


convertVidFormat(output_file)

########################Read in output video from live stream and perform camera calibration###########################
cap2 = cv.VideoCapture('output.mp4')
num_frames = 20
rvec = []
tvec = []
while cap2.isOpened():
    # Get total number of frames
    total_frames = int(cap2.get(cv.CAP_PROP_FRAME_COUNT))

    # Generate random frame indices
    frame_indices = random.sample(range(total_frames), num_frames)

    # Process sampled frames
    for idx in frame_indices:
        # Set the frame position
        cap2.set(cv.CAP_PROP_POS_FRAMES, idx)
        ret, frame2 = cap2.read()

 
        if ret:
            # Write the frame to a temporary file
            cv.imwrite("temp_frame.png", frame2)
            # Pass the file path to the calibCamera function
            output_dat = calibCamera("temp_frame.png")
            if output_dat is not None:
                rvecs, tvecs, mtx, roi, dist = output_dat
                rvec.append(rvecs)
                tvec.append(tvecs)
            else:
                continue

        else:
            print("Error reading frame")
            break

    # Termination condition: Exit loop if all frames have been processed

    print("All frames processed. Exiting the loop.")
    break

np.save(filedir+'optimalIntrinsic.npy', mtx)
np.save(filedir+'rvecs.npy', rvec)
np.save(filedir+'tvecs.npy', tvec)
np.save(filedir+'roi.npy', roi)
np.save(filedir+'dist.npy', dist)
# Release the video capture objects
cap.release()
os.remove('temp_frame.png')
os.remove('output.avi')
os.remove('output.mp4')