# for presenting using videos

import time
from pathlib import Path

import cv2


def capture_frames(capture_interval):

    # Define the list of video files for simulating four roads of intersection
    video_files = [
        Path("road_videos/road1.mp4"),
        Path("road_videos/road2.mp4"),
        Path("road_videos/road3.mp4"),
        Path("road_videos/road4.mp4"),
    ]
    # Define the directory to save frames
    frames_dir = Path("frames")
    frames_dir.mkdir(parents=True, exist_ok=True)

    # If capture_interval is zero, capture and save the first frame from each video and return
    if capture_interval == 0:
        for i, video_file in enumerate(video_files):
            cap = cv2.VideoCapture(str(video_file))
            ret, frame = cap.read()
            cap.release()
            if ret:
                frame_filename = frames_dir / f"frame_road({i + 1}).jpg"
                cv2.imwrite(str(frame_filename), frame)
                print(f"First frame from video {i + 1} saved: {frame_filename}")
        return

    # Delete previous frames
    for prev_frame in frames_dir.glob("frame_road(*).jpg"):
        prev_frame.unlink()

    # Otherwise, capture only one frame from each video and then return
    for i, video_file in enumerate(video_files):
        cap = cv2.VideoCapture(str(video_file))
        cap.set(
            cv2.CAP_PROP_POS_MSEC, capture_interval * 1000
        )  # Set the position to 30 seconds (30,000 milliseconds)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame_filename = frames_dir / f"frame_road({i + 1}).jpg"
            cv2.imwrite(str(frame_filename), frame)
            print(f"Frame from video {i + 1} saved: {frame_filename}")
