"""Manager for the Pong game."""

import cv2
import numpy as np


class Pong:

    padding = 100

    def __init__(
            self,
            h: int=600,
            w: int=600,
            default_half_paddle_width: int=5,
            default_half_paddle_height: int=20):
        self.ball = {
            'cx': w // 2,
            'cy': h // 2,
            'dx': 3,
            'dy': 2,
            'r': 3
        }
        self.paddle1 = {
            'cx': self.padding,
            'cy': h // 2,
            'dy': 0,
            'half_paddle_width': default_half_paddle_width,
            'half_paddle_height': default_half_paddle_height
        }
        self.paddle2 = {
            'cx': w - self.padding,
            'cy': h // 2,
            'dy': 0,
            'half_paddle_width': default_half_paddle_width,
            'half_paddle_height': default_half_paddle_height
        }
        self.h = h
        self.w = w

    def update(self):
        """Update all positions and velocities."""
        by = self.ball['cy']
        if by <= self.padding or by >= self.h - self.padding:
            self.ball['dy'] *= -1

        # TODO: remove me
        bx = self.ball['cx']
        if bx <= self.padding or bx >= self.w - self.padding:
            self.ball['dx'] *= -1

        if self.hit(self.ball, self.paddle1) \
                or self.hit(self.ball, self.paddle2):
            self.ball['dx'] *= -1

        self.ball['cx'] += self.ball['dx']
        self.ball['cy'] += self.ball['dy']

        self.paddle1['cy'] += self.paddle1['dy']
        self.paddle2['cy'] += self.paddle2['dy']

    def hit(self, ball, paddle):
        return False

    def draw(self, frame):
        """In-place modification of frame"""
        assert frame.shape[:2] == (self.h, self.w), 'Frame shape mismatch'
        self.draw_paddle(frame, self.paddle1)
        self.draw_paddle(frame, self.paddle2)
        self.draw_ball(frame, self.ball)

    def draw_paddle(self, frame, paddle):
        cx, cy = paddle['cx'], paddle['cy']
        p1 = (cx - paddle['half_paddle_width'], cy - paddle['half_paddle_height'])
        p2 = (cx + paddle['half_paddle_width'], cy + paddle['half_paddle_height'])
        cv2.rectangle(frame, p1, p2, (255, 255, 255), thickness=-1)

    def draw_ball(self, frame, ball):
        p = (ball['cx'], ball['cy'])
        cv2.circle(frame, p, ball['r'], (255, 255, 255), thickness=-1)


def main():
    width = height = 600
    pong = Pong()

    while True:
        # update game
        frame = np.zeros((width, height))
        pong.update()
        pong.draw(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
