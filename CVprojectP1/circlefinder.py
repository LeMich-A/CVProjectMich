import cv2 as cv
import numpy as np


def detect_and_draw_circles(frame, framecnt):
    # Convert the frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Apply GaussianBlur to reduce noise
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    # Use HoughCircles to detect circles
    circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=50)
    
    if circles is not None:
        # Convert coordinates to integers
        circles = np.uint16(np.around(circles))
        
        # Initialize lists to store center coordinates
        centers = []
        
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            # Draw the circle outline
            cv.circle(frame, center, circle[2], (0, 255, 0), 2)
            # Draw the center of the circle
            cv.circle(frame, center, 2, (0, 0, 255), 3)
            # Append center coordinates to the list
            centers.append(center)
        
        # Visualize the best circle
        best_circle = circles[0][0]  # Assuming the first circle is the best
        circ = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
        cv.circle(circ, (best_circle[0], best_circle[1]), best_circle[2], [0, 255, 0], 2)
        cv.circle(circ, (best_circle[0], best_circle[1]), 5, [0, 0, 255], -1)
        cv.putText(circ, f'Center: ({best_circle[0]}, {best_circle[1]})', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv.imshow('Best Circle', circ)
        cv.imwrite(f"Frame_Dump/Best_Circle_Detected{framecnt}.png", circ)
        cv.waitKey(10)

        return centers[0]

    else:
        return None




