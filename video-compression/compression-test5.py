import cv2
import numpy as np

# Open the video file
cap = cv2.VideoCapture("C0078_clip10sec.mp4")

# Get the frames per second (fps) of the video
fps = cap.get(cv2.CAP_PROP_FPS)
print("Original framerate:", fps)

# Get the frame dimensions (width, height)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Set the threshold for motion detection
threshold = 254

# Specify the desired framerate
desired_fps = 30

# Initialize variables for detecting motion
first_frame = None
motion_detected = False

# Create a video writer object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, desired_fps,
                      (frame_width, frame_height))

# Read the frames of the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the frame
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # If this is the first frame, initialize the first frame
    if first_frame is None:
        first_frame = gray
        continue

    # Calculate the absolute difference between the current frame and the first frame
    frame_delta = cv2.absdiff(first_frame, gray)

    # Threshold the delta image to highlight the pixels that have changed
    thresh = cv2.threshold(frame_delta, threshold, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in any holes
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours in the thresholded image
    contours = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = contours[0] if len(contours) == 2 else contours[1]

    # Iterate through the contours
    for c in contours:
        # Ignore contours that are too small
        if cv2.contourArea(c) < ((frame_height/50) * (frame_width/100)):
            continue

        x, y, w, h = cv2.boundingRect(c)

        # Set the motion_detected flag
        motion_detected = True

    # if motion is detected, write the frame to the output video
    if motion_detected:
        out.write(frame)

    # reset the motion_detected flag
    motion_detected = False

    cv2.imshow("frame1", gray)
    cv2.imshow("frame2", frame)
    cv2.imshow("frame3", thresh)

    key = cv2.waitKey(30)
    if key == 27:
        break


# Release the video writer object
out.release()

cap.release()
cv2.destroyAllWindows()
