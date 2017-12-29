"""Main interface for hand-tracking Pong."""

from pong import Pong
import cv2


def main():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    height, width, _ = frame.shape
    pong = Pong(
        h=height,
        w=width,
        default_ball_dx=width // 100,
        default_ball_dy=height // 100,
        default_paddle_speed=height // 100)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)  # flip across vertical axis

        key = cv2.waitKey(1)
        pong.on_key(key)

        # update game
        ended = pong.update()
        pong.draw(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if pong.is_key(key, 'q') or ended:
            break


if __name__ == '__main__':
    main()
