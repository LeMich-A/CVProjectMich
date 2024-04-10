import cv2 as cv
import os
from matplotlib import pyplot as plt
from circlefinder import detect_and_draw_circles

filename = "videos/coin.mov"
capture = cv.VideoCapture(filename)
framecnt = 0
frame_count_list = []
center_xlist = []  
center_ylist = []
plt.ion()  # Turn on interactive mode

if not os.path.exists('Frame_Dump'):
    os.mkdir('Frame_Dump')
else:
    print("Directory already exists, proceeding with overwriting directory\n")

try:
    while capture.isOpened():
        state, frame = capture.read()
        if state:
            framecnt += 1
            # Saving the frame as an image with a filename instead of a string
            frame_filename = f'Frame_Dump/frame_{framecnt:04d}.jpg'
            cv.imwrite(frame_filename, frame)

            centerX, centerY = detect_and_draw_circles(frame, framecnt)

            # If center x-coordinate is found, append it to the list
            if centerX is not None and centerY is not None:
                frame_count_list.append(framecnt)
                center_xlist.append(centerX)
                center_ylist.append(centerY)
                # Plot the center coordinates with respect to frame count
                plt.clf()  # Clear the previous plot
                plt.plot(frame_count_list, center_xlist, label='Center X Coordinate', marker='o', linestyle='-')
                plt.plot(frame_count_list, center_ylist, label='Center Y Coordinate', marker='o', linestyle='-')
                plt.xlabel('Frame Count')
                plt.ylabel('Center Position')
                plt.legend()
                plt.title('Center Position over Frame Count')
                plt.draw()
                plt.pause(0.1)  # Adjust the pause duration as needed

            print('FrameCount:' + str(framecnt) + '\n')
        else:
            print("No remaining frames to process\n")
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    plt.ioff()  # Turn off interactive mode
    capture.release()
    plt.show()
