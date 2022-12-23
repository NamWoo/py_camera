# py_camera

Camera 를 python - opencv로 불러와 실행하는 기본 구성 코드를 정리한다. *(자꾸 까먹어서 repo를 새로 박아놓자;;)*

1. 기본 opencv 에서 `lsusb` 로 보이는 Camera 번호에 맞춰 열기
2. `v4l2src`로 불러오는 방법
3. `gsteamer` 로 불러오는 방법

내부 이론? 또는 pipeline 에 대한 정의는 나중에 다시 정리하자.


>TODO: v4l2-ctl --list-device 카메라 번호랑 셋팅 정보 파이썬으로 한번에 불러오기

---


## V4l2src

```python 

def v4l2src_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    framerate=30,
    ):
    return (
        "v4l2src device=%d !"
        "video/x-raw, width=%d, height=%d, framerate=%d/1 !"
        "videoconvert !"
        "video/x-raw, format=(string)BGR !"
        "appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate
        )
    )
```


## gstreamer

```python

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
    ):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
```