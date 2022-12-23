#!/usr/bin/env python3

import sys
import time
import cv2
import subprocess

window_title = "USB Camera"
w, h, fps = 640, 480, 30

def check_usb_camera_list()->list:
    """usb 카메라의 dev/video* 번호를 확인한다."""
    video_list = []
    dev_list = subprocess.check_output(["v4l2-ctl", "--list-device"]).decode().split('\n\n')
    for dev_raw in dev_list:
        if dev_raw != '':
            dev_raw2 = dev_raw.split('\n')
            if dev_raw2[0][:15] == 'H264 USB Camera':
                dev_raw3 = dev_raw2[1].replace('\t','')
                video_list.append(dev_raw3)
    return video_list

dev_num = check_usb_camera_list()

pipeline_cmd = ["v4l2src device={}".format(dev_num[0]),
                       "video/x-raw, width={}, height={}, framerate={}/1".format(w, h, fps),
                       "videoconvert",
                       "video/x-raw, format=(string)BGR",
                       "appsink"
                       ]


pipeline = " ! ".join(pipeline_cmd)

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
