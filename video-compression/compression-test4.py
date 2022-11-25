from scenedetect import SceneManager, open_video, ContentDetector
import sys
import csv

def find_scenes(video_path, threshold=60):
    video = open_video(video_path)
    scene_manager = SceneManager()

    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # Detect all scenes in video from current position to end.
    scene_manager.detect_scenes(video, frame_skip=1, show_progress=True)
    
    # `get_scene_list` returns a list of start/end timecode pairs for each scene that was found.
    return scene_manager.get_scene_list()

if __name__ == '__main__':
    sceneList = find_scenes(sys.argv[1], int(sys.argv[2]))
    # print(sceneList[0])

    for i, scene in enumerate(sceneList):
        print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (i+1,scene[0].get_timecode(), scene[0].get_frames(),scene[1].get_timecode(), scene[1].get_frames(),))

    with open('sample.txt', 'w') as file:
        for i, scene in enumerate(sceneList):
            file.write('Scene %2d: Start %s / Frame %d, End %s / Frame %d\n' % (i+1, scene[0].get_timecode(), scene[0].get_frames(), scene[1].get_timecode(), scene[1].get_frames(),))
