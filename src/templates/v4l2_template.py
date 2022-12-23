#!/usr/bin/env python3

import sys
import time
import cv2

window_title = "USB Camera"

pipeline = " ! ".join(["v4l2src device=/dev/video0",
                       "video/x-raw, width=640, height=480, framerate=30/1",
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ])

h264_pipeline = " ! ".join(["v4l2src device=/dev/video0",
                            "video/x-h264, width=1280, height=720, framerate=30/1, format=H264",
                            "avdec_h264",
                            "videoconvert",
                            "video/x-raw, format=(string)BGR",
                            "appsink sync=false"
                            ])




def show_camera():

    video_capture = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
    width = 640
    height = 480
    fourcc = int(video_capture.get(cv2.CAP_PROP_FOURCC))
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    now = time.time()
    save_name = time.strftime('%m%d_%H%M%S', time.localtime(now))
    savepath = '/home/nw/Documents/temp/{}.avi'.format(save_name)
    out = cv2.VideoWriter(savepath, fourcc, fps, (width, height), True)


    if video_capture.isOpened():
        try:
            # window_handle = cv2.namedWindow(
            #     window_title, cv2.WINDOW_AUTOSIZE)
            # Window
            while True:
                ret_val, frame = video_capture.read()
                out.write(frame)

                # if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
                #     cv2.imshow(window_title, frame)
                # else:
                #     break
                keyCode = cv2.waitKey(10) & 0xFF
                # Stop the program on the ESC key or 'q'
                if keyCode == 27 or keyCode == ord('q'):
                    break

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
            print('end')
    else:
        print("Error: Unable to open camera")


if __name__ == "__main__":

    show_camera()
