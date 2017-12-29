"""Main interface for hand-tracking Pong, multiprocessing version.

Uses multiprocessing code from Victor Dibia's
https://github.com/victordibia/handtracking/blob/master/detect_multi_threaded.py
"""

import tensorflow as tf
from multiprocessing import Queue, Pool
from pong import Pong
from handtracking.utils import detector_utils
import cv2


def update_pong_with_boxes_scores(boxes, scores, pong, height):
    if scores[0] > 0.5:
        ftop, _, fbottom, _ = boxes[0]
        top, bottom = ftop * height, fbottom * height
        target = (top + bottom) / 2.
        pong.set_target_for_player(pong.paddle1, target)
        print('setting target', target)
    else:
        print('unsetting target')
        pong.unset_target_for_player(pong.paddle1)


def worker(input_q, output_q, cap_params, frame_processed):
    print(">> loading frozen model for worker")
    detection_graph, sess = detector_utils.load_inference_graph()
    sess = tf.Session(graph=detection_graph)
    while True:
        frame = input_q.get()
        if (frame is not None):
            # actual detection
            boxes, scores = detector_utils.detect_objects(
                frame, detection_graph, sess)
            # draw bounding boxes
            detector_utils.draw_box_on_image(
                cap_params['num_hands_detect'], cap_params["score_thresh"], scores, boxes, cap_params['im_width'], cap_params['im_height'], frame)
            output_q.put((frame, boxes[0], scores[0]))
            frame_processed += 1
        else:
            output_q.put(frame)
    sess.close()


def main():
    input_q = Queue(maxsize=5)
    output_q = Queue(maxsize=5)

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    height, width, _ = frame.shape
    pong = Pong(
        h=height,
        w=width,
        default_ball_dx=width // 100,
        default_ball_dy=height // 100,
        default_paddle_speed=height // 100,
        default_half_paddle_height=height // 10)
    i = 0

    # parallelize
    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = (width, height)
    cap_params['score_thresh'] = 0.5
    cap_params['num_hands_detect'] = 1
    cap_params['pong'] = pong
    pool = Pool(2, worker, (input_q, output_q, cap_params, frame_processed))

    while True:
        i += 1
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # flip across vertical axis

        # wait for keys
        key = cv2.waitKey(100)
        pong.on_key(key)

        input_q.put(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        frame, box, score = output_q.get()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        update_pong_with_boxes_scores([box], [score], pong, height)

        # update game
        ended = pong.update()
        pong.draw(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if pong.is_key(key, 'q') or ended:
            break


if __name__ == '__main__':
    main()
