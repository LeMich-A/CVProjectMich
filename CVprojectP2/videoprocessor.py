# import cv2 as cv
# import os
# from matplotlib import pyplot as plt
# from circlefinder import detect_and_draw_circles  # Assuming the function is in circlefinder module

# filename = "coinTrack.avi"
# capture = cv.VideoCapture(filename)
# framecnt = 0
# frame_count_list = []
# center_xlist = []  
# center_ylist = []
# center_zlist = []  # List to store z-axis coordinates
# plt.ion()  # Turn on interactive mode

# if not os.path.exists('Frame_Dump'):
#     os.mkdir('Frame_Dump')
# else:
#     print("Directory already exists, proceeding with overwriting directory\n")

# try:
#     while capture.isOpened():
#         state, frame = capture.read()
#         if state:
#             framecnt += 1
#             # Saving the frame as an image with a filename instead of a string
#             frame_filename = f'Frame_Dump/frame_{framecnt:04d}.jpg'
#             cv.imwrite(frame_filename, frame)

#             # Call detect_and_draw_circles function to get center coordinates
#             coordinates = detect_and_draw_circles(frame, framecnt)

#             # If center coordinates are found, append them to the lists
#             if coordinates is not None:
#                 x, y, z = coordinates
#                 frame_count_list.append(framecnt)
#                 center_xlist.append(x)
#                 center_ylist.append(y)
#                 center_zlist.append(z)  # Append z-coordinate to the list
#                 # Plot the center coordinates with respect to frame count
#                 plt.clf()  # Clear the previous plot
#                 plt.plot(frame_count_list, center_xlist, label='Center X Coordinate', marker='o', linestyle='-')
#                 plt.plot(frame_count_list, center_ylist, label='Center Y Coordinate', marker='o', linestyle='-')
#                 plt.plot(frame_count_list, center_zlist, label='Center Z Coordinate', marker='o', linestyle='-')
#                 plt.xlabel('Frame Count')
#                 plt.ylabel('Center Position')
#                 plt.legend()
#                 plt.title('Center Position over Frame Count')
#                 plt.draw()
#                 plt.pause(0.1)  # Adjust the pause duration as needed
#             else:
#                 print("No circles detected in frame ", framecnt)

#             print('FrameCount:' + str(framecnt) + '\n')
#         else:
#             print("No remaining frames to process\n")
#             break

# except KeyboardInterrupt:
#     print("Interrupted by user")

# finally:
#     plt.ioff()  # Turn off interactive mode
#     capture.release()
#     plt.show()



import cv2 as cv
import os
from matplotlib import pyplot as plt
from circlefinder import detect_and_draw_circles  # Assuming the function is in circlefinder module

filename = "coin.mov"
capture = cv.VideoCapture(filename)
framecnt = 0
frame_count_list = []
center_xlist = []  
center_ylist = []
center_zlist = []  # List to store z-axis coordinates
plt.ion()  # Turn on interactive mode
# Set the desired size of the video window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

if not os.path.exists('Frame_Dump'):
    os.mkdir('Frame_Dump')
else:
    print("Directory already exists, proceeding with overwriting directory\n")
try:
    while capture.isOpened():
        state, frame = capture.read()
        if state:
            framecnt += 1
            # Resize the frame to the desired window size
            frame = cv.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
            cv.imshow('Video', frame)


            # Call detect_and_draw_circles function to get center coordinates
            coordinates = detect_and_draw_circles(frame, framecnt)

            # If center coordinates are found, append them to the lists
            if coordinates is not None:
                x, y, z = coordinates
                frame_count_list.append(framecnt)
                center_xlist.append(x)
                center_ylist.append(y)
                center_zlist.append(z)  # Append z-coordinate to the list
                # Plot the center coordinates with respect to frame count
                plt.clf()  # Clear the previous plot
                plt.plot(frame_count_list, center_xlist, label='Center X Coordinate', marker='o', linestyle='-')
                plt.plot(frame_count_list, center_ylist, label='Center Y Coordinate', marker='o', linestyle='-')
                plt.plot(frame_count_list, center_zlist, label='Center Z Coordinate', marker='o', linestyle='-')
                plt.xlabel('Frame Count')
                plt.ylabel('Center Position')
                plt.legend()
                plt.title('Center Position over Frame Count')
                plt.draw()
                plt.pause(0.1)  # Adjust the pause duration as needed
            else:
                print("No circles detected in frame ", framecnt)

            print('FrameCount:' + str(framecnt) + '\n')
            key = cv.waitKey(10)
            if key & 0xFF == ord('q') or key == 27:  # Press 'q' or 'Esc' to exit
                break
        else:
            print("No remaining frames to process\n")
            break

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    capture.release()
    cv.destroyAllWindows()
