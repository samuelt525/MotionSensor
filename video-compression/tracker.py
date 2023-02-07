import cv2
import math

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton

class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    # print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids


def getVideoBounds(filepath):

    cap = cv2.VideoCapture(filepath)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    return frame_width, frame_height, fps


def processVideo(filepath, progressBar, outputFPS, rescaleRatio, userXLB, userXUB, userYLB, userYUB):
    # Create tracker object
    tracker = EuclideanDistTracker()

    # Open the video file
    cap = cv2.VideoCapture(filepath)

    # Get the frames per second (fps) of the video
    frame_index = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Original framerate:", fps)
    print("Total frames: ", total_frames)

    # Specify the desired framerate
    desired_fps = outputFPS

    # Get the frame dimensions (width, height)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, desired_fps, (frame_width, frame_height))

    # TODO Multiply by Ratio for the new frame_width, frame_height

    # Object detection from Stable camera
    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

    # Read the frames of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_index += 1
        progressBar.setValue(int(100 * frame_index / total_frames))
        app.processEvents()
        print(int(100 * frame_index / total_frames))

        # height, width, _ = frame.shape

        # Write the frame to the output video

        # print(height, width)

        # Extract Region of interest
        # print(type(userXLB), type(userXUB), type(userYLB), type(userYUB))
        roi = frame[userXLB:userXUB, userYLB:userYUB]

        # 1. Object Detection
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 500:
                # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        # 2. Object Tracking
        boxes_ids = tracker.update(detections)
        out.write(frame)
        for box_id in boxes_ids:
            x, y, w, h, detection_id = box_id
            cv2.putText(roi, str(detection_id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # cv2.imshow("roi", roi)
        # cv2.imshow("Frame", frame)
        # cv2.imshow("Mask", mask)

        key = cv2.waitKey(30)
        if key == 27:
            break

    # Release the video writer object
    out.release()

    cap.release()
    cv2.destroyAllWindows()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(320,250)
        self.setWindowTitle("test")
 
        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(50, 50, 250, 30)

        button = QPushButton("Start Process", self)
        button.clicked.connect(self.update)
        button.move(50,100)

    def update(self):
        processVideo("./C0078_clip10sec.mp4", self.prog_bar, 30, 100, 0, 2160, 0, 3840)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

