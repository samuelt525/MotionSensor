import cv2
import math
import os

# import sys
# from PyQt6.QtCore import QSize, Qt, QUrl, pyqtSlot, pyqtSignal
# from PyQt6.QtMultimedia import QMediaPlayer
# from PyQt6.QtQuickWidgets import QQuickWidget
# from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QLineEdit, QFormLayout, QWidget, QWidgetItem, QGroupBox, QHBoxLayout, QLabel, QSpinBox, QSlider, QProgressBar, QRadioButton
# from PyQt6.QtGui import QPixmap

if os.path.exists("./output_video.mp4"):
    os.remove("./output_video.mp4")
if os.path.exists("./skip_output_video.mp4"):
    os.remove("./skip_output_video.mp4")

def getVideoBounds(filepath):

    cap = cv2.VideoCapture(filepath)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    return frame_width, frame_height, fps


def processVideo(filepath, progressBar, outputFPS, rescaleRatio, userXLB, userXUB, userYLB, userYUB, counter, outputPath):

    # Open the video file
    cap = cv2.VideoCapture(filepath)
    
    # Get the video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(total_frames)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    progress_index = 0
  
    # Specify the desired framerate
    desired_fps = outputFPS
 
    motion_threshold = 0.05 * (height * width)
    motion_stats = []
    # print(f'total pixels = {width*height}, motion_threshold={0}')

    # Create a video writer object to output the processed video
    out = cv2.VideoWriter(outputPath + 'output_video' + str(counter) + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), desired_fps, (width, height))

    # Initialize variables for motion detection
    no_motion_frames = 0
    scale_factor = min(1280/width, 720/height)

    # Create a background subtractor object
    back_sub = cv2.createBackgroundSubtractorMOG2()

    # Loop through all frames in the video
    for i in range(total_frames):

        # Read the current frame
        ret, frame = cap.read()

        if not ret:  # check if the frame is empty
            continue
        
        progress_index += 1
        #progressBar.setValue(int(100 * progress_index / total_frames))
        
        frame = cv2.resize(frame, (int(width*scale_factor), int(height*scale_factor)))
        
        # Apply background subtraction to the current frame
        fg_mask = back_sub.apply(frame)

        # Remove noise from the foreground mask
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

        # Count the number of non-zero pixels in the foreground mask
        motion_count = cv2.countNonZero(fg_mask)
        motion_stats.append(motion_count)

        # If there is motion in the frame, reset the no motion frames counter
        if motion_count > 14000:
            no_motion_frames = 0
            # # Draw a rectangle around the areas with motion
            # contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # for contour in contours:
            #     x, y, w, h = cv2.boundingRect(contour)
            #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        else:
            no_motion_frames += 1

        # If there have been more than 10 consecutive frames with no motion, skip this frame
        if no_motion_frames > 10:
            # skip_frame_counter += 1
            # skip.write(frame)
            continue

        # Write the current frame to the output video
        out.write(frame)
        # output_frame_counter += 1

    # Release the video writer object
    out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__': 
    prog_bar = 0
    processVideo("/Users/humaid/Documents/seniordesign/code/main/MotionTracker54/C0078_720p60_40s.mp4", prog_bar, 60, 100, 0, 2160, 0, 3840)
# if __name__ == '__main__': 

#     # Create a new application instance
#     app = QApplication(sys.argv)

#     # Create a new window
#     window = QWidget()

#     # Set the window properties
#     window.setWindowTitle("My PyQT6 Application")
#     window.setGeometry(100, 100, 400, 300)

#     # Show the window
#     window.show()
#     prog_bar = QProgressBar()
#     processVideo("/Users/humaid/Documents/seniordesign/code/main/MotionTracker54/C0078_720p60_40s.mp4", prog_bar, 60, 100, 0, 2160, 0, 3840)

#     # Start the event loop
#     sys.exit(app.exec())


