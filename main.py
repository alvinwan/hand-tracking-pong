"""Main interface for hand-tracking Pong."""

from pong import Pong
from handtracking.utils import detector_utils
import cv2


def update_pong_with_boxes_scores(boxes, scores, pong, height):
    if scores[0] > 0.5:
        ftop, _, fbottom, _ = boxes[0]
        top, bottom = ftop * height, fbottom * height
        pong.set_target_for_player(pong.paddle1, (top + bottom) / 2.)
    else:
        pong.unset_target_for_player(pong.paddle1)


def main():
    cap = cv2.VideoCapture(0)
    detection_graph, sess = detector_utils.load_inference_graph()
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

    while True:
        i += 1
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # flip across vertical axis

        # wait for keys
        key = cv2.waitKey(100)
        pong.on_key(key)

        boxes, scores = detector_utils.detect_objects(
            frame, detection_graph, sess)

        if boxes is not None and scores is not None:
            # draw bounding boxes
            detector_utils.draw_box_on_image(
                1, 0.5, scores, boxes, width, height, frame)
            update_pong_with_boxes_scores(boxes, scores, pong, height)

        # update game
        ended = pong.update()
        pong.draw(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if pong.is_key(key, 'q') or ended:
            break


if __name__ == '__main__':
    main()
