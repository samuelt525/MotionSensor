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


def processVideo(filepath, progressBar, outputFPS, rescaleRatio, sensitivityRatio, userXLB, userXUB, userYLB, userYUB, outputPath):

    # Open the video file
    cap = cv2.VideoCapture(filepath)
    
    # Get the video properties
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    progress_index = 0
  
    # Specify the desired framerate
    desired_fps = outputFPS
 
    motion_stats = []
    no_motion_frames = 0
    
    scale_factor = 100
    if rescaleRatio in range(1, 101):
        scale_factor = rescaleRatio
    else:
        raise ValueError("Value is out of range (1-100)")

    filename = os.path.splitext(os.path.basename(filepath))[0]
    # Create a video writer object image.pngto output the processed video
    out = cv2.VideoWriter(outputPath + '/' + filename + '-output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), desired_fps, (int(width * scale_factor / 100), int(height * scale_factor / 100)))
    # out = cv2.VideoWriter(outputPath, cv2.VideoWriter_fourcc(*'mp4v'), desired_fps, (int(width * scale_factor / 100), int(height * scale_factor / 100)))

    # Create a background subtractor object
    back_sub = cv2.createBackgroundSubtractorMOG2()
    
    if sensitivityRatio in range(1, 101):
        motion_count_threshold = round((100-sensitivityRatio) / 100 * (height * width))
    else:
        raise ValueError("Sensitivity Value is out of range (1-100). Recommended 20.")
    print(height*width)
    print(motion_count_threshold)

    # Loop through all frames in the video
    for i in range(total_frames):

        # Read the current frame
        ret, frame = cap.read()

        if not ret:  # check if the frame is empty
            continue
        
        progress_index += 1
        progressBar.setValue(int(100 * progress_index / total_frames))
        
        frame = cv2.resize(frame, (math.ceil(width * scale_factor / 100), math.ceil(height * scale_factor / 100)))
        
        # Apply background subtraction to the current frame
        fg_mask = back_sub.apply(frame)

        # Remove noise from the foreground mask
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))

        # Count the number of non-zero pixels in the foreground mask
        motion_count = cv2.countNonZero(fg_mask)
        motion_stats.append(motion_count)

        # If there is motion in the frame, reset the no motion frames counter

        if motion_count > motion_count_threshold:
            no_motion_frames = 0
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
    processVideo("/Users/humaid/Documents/seniordesign/code/main/MotionTracker54/Motorcycle.mp4", prog_bar, 120, 100, 10, 0, 782, 0, 1392, "/Users/humaid/Documents/seniordesign/code/main/MotionTracker54/Motorcycle-output10.mp4")
    # processVideo("/Users/samueltsui/Documents/GitHub/MotionSensor/video-compression/C0078_clip1min60fps.mp4", prog_bar, 60, 100, 0, 2160, 0, 3840, "/Users/samueltsui/Desktop")


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


