from scenedetect import SceneManager, open_video, ContentDetector, split_video_ffmpeg
import sys
import csv

def find_scenes(videoPath, threshold=10, frameSkip=0, showProgress=True):
    video = open_video(videoPath)

    # sceneManager
    sceneManager = SceneManager()
    
    # Detector Settings
    sceneManager.add_detector(ContentDetector(threshold=threshold, min_scene_len=1200))

    # Detect all scenes in video from current position to end.
    sceneManager.detect_scenes(video, frame_skip=frameSkip, show_progress=showProgress)
    
    sceneList = sceneManager.get_scene_list()

    for i, scene in enumerate(sceneList):
        print('Scene %2d: Start %s / Frame %d, End %s / Frame %d' %
              (i+1, scene[0].get_timecode(), scene[0].get_frames(), scene[1].get_timecode(), scene[1].get_frames(),))

    # write timecodes to file - maybe change to html output
    with open('timecode.txt', 'w') as file:
        for i, scene in enumerate(sceneList):
            file.write('Scene %2d: Start %s / Frame %d, End %s / Frame %d\n' %
                       (i+1, scene[0].get_timecode(), scene[0].get_frames(), scene[1].get_timecode(), scene[1].get_frames(),))

    # use ffmpeg for splitting video files
    # TODO add func to output to directory and prevent overwrites on multiple runs
    split_video_ffmpeg(videoPath, sceneList, show_progress=True)

    return sceneList

if __name__ == '__main__':

    sceneListMain = find_scenes(sys.argv[1], int(sys.argv[2]))

    # print(sys.argv)

    # TODO deal with more args
    # if len(sys.argv) < 2:
    #     raise AttributeError('Video File Path not provided.')
    # elif len(sys.argv) == 2:
    #     sceneList = find_scenes(sys.argv[1])
    # elif len(sys.argv) == 3:
    #     sceneList = find_scenes(sys.argv[1], int(sys.argv[2]))
    # elif len(sys.argv) == 4:
    #     # sceneList = find_scenes(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    #     if sys.argv[3].isnumeric():
    #         sceneList = find_scenes(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    #     else:
    #         sceneList = find_scenes(sys.argv[1], int(sys.argv[2]), show_progress=bool(sys.argv[3]))
    # elif len(sys.argv) == 5:
    #     sceneList = find_scenes(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), False)
