# Hand-Tracking Pong
"Real-time" Hand-Tracking Pong. As of the moment, object detection inference time is the bottleneck, at 1-2 FPS on a Macbook Pro (i5, 2.5GHz, 8GB) with detections on 160x90 images.

![ezgif-2-1afdbb1a75](https://user-images.githubusercontent.com/2068077/34434701-ae270e00-ec3c-11e7-81da-5a274c7ebf99.gif)

The original hand tracker utilities and model are taken from Victor Dibia's [Hand Tracking repository](https://github.com/victordibia/handtracking).

## Installation

1. [Setup a Python virtual environment](https://www.digitalocean.com/community/tutorials/common-python-tools-using-virtualenv-installing-with-pip-and-managing-packages#a-thorough-virtualenv-how-to) with Python 3.5.

2. Install all Python dependencies.

```
pip install -r requirements.txt
```

> For Ubuntu users, install `libsm6` for OpenCV to work:
> ```
> apt install libsm6
> ```

Installation is complete. To get started, launch the demo. I recommend running the multi-threaded version.

```
python main_multi.py
```
