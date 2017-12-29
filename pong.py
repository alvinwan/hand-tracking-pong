"""Manager for the Pong game.

No way to control player 2 just yet.
"""

import cv2
import numpy as np


class Pong:

    padding = 100

    def __init__(
            self,
            h: int=600,
            w: int=600,
            default_half_paddle_width: int=5,
            default_half_paddle_height: int=20,
            default_paddle_lives: int=3,
            default_paddle_speed: int=2,
            default_ball_dx: int=3,
            default_ball_dy: int=2,
            enable_computer_player: bool=True):
        self.ended = False
        self.ball = {
            'cx': w // 2,
            'cy': h // 2,
            'dx': default_ball_dx,
            'dy': default_ball_dy,
            'r': 5
        }
        self.paddle1 = {
            'no': 1,
            'cx': self.padding,
            'cy': h // 2,
            'dy': 0,
            'half_paddle_width': default_half_paddle_width,
            'half_paddle_height': default_half_paddle_height,
            'lives': default_paddle_lives,
            'speed': default_paddle_speed * 5
        }
        self.paddle2 = {
            'no': 2,
            'cx': w - self.padding,
            'cy': h // 2,
            'dy': 0,
            'half_paddle_width': default_half_paddle_width,
            'half_paddle_height': default_half_paddle_height,
            'lives': default_paddle_lives,
            'speed': default_paddle_speed,
            'computer': enable_computer_player
        }
        self.h = h
        self.w = w

    def update(self):
        """Update all positions and velocities."""

        # Check if ball needs to bounce vertically
        by = self.ball['cy']
        if by <= self.padding or by >= self.h - self.padding:
            self.ball['dy'] *= -1

        # Check if ball needs to bounce off of paddle. Updates lives accordingly
        bx = self.ball['cx']
        if bx <= self.padding + self.paddle1['half_paddle_width']:
            if not self.hit(self.ball, self.paddle1):
                self.remove_player_life(self.paddle1)
                self.reset()
                return
            self.ball['dx'] *= -1

        if bx >= self.w - self.padding - self.paddle2['half_paddle_width']:
            if not self.hit(self.ball, self.paddle2):
                self.remove_player_life(self.paddle2)
                self.reset()
                return
            self.ball['dx'] *= -1

        # Move balls and paddles
        self.ball['cx'] += self.ball['dx']
        self.ball['cy'] += self.ball['dy']

        self.paddle1['cy'] += self.paddle1['dy']
        self.paddle2['cy'] += self.paddle2['dy']

        # update paddle2 if computer enabled
        if self.paddle2['computer']:
            if self.ball['cy'] > self.paddle2['cy']:
                self.paddle2['dy'] = self.paddle2['speed']
            elif self.ball['cy'] < self.paddle2['cy']:
                self.paddle2['dy'] = -self.paddle2['speed']
            else:
                self.paddle2['dy'] = 0
        return self.ended

    def hit(self, ball, paddle):
        """Assumes the paddle is within x of the paddle."""
        top = paddle['cy'] + paddle['half_paddle_height']
        bottom = paddle['cy'] - paddle['half_paddle_height']
        return bottom <= ball['cy'] - ball['r'] or ball['cy'] + ball['r'] <= top

    def remove_player_life(self, paddle):
        """Decrement player life and check for end of game."""
        paddle['lives'] -= 1
        print(paddle['no'], paddle['lives'])
        if paddle['lives'] <= 0:
            self.end_game()

    def reset(self):
        """Reset the ball."""
        self.ball['cx'] = self.w // 2
        self.ball['cy'] = self.h // 2
        self.ball['dx'] *= -1

    def end_game(self):
        """End the game"""
        self.ended = True

    def draw(self, frame):
        """In-place modification of frame"""
        assert frame.shape[:2] == (self.h, self.w), 'Frame shape mismatch'
        self.draw_arena(frame)
        self.draw_paddle(frame, self.paddle1)
        self.draw_paddle(frame, self.paddle2)
        self.draw_ball(frame, self.ball)

    def draw_arena(self, frame):
        """In-place draw the arena"""
        p1 = (self.padding - self.ball['r'], self.padding + self.ball['r'])
        p2 = (self.w - self.padding - self.paddle1['half_paddle_width'],
              self.h - self.padding + self.paddle2['half_paddle_width'])
        cv2.rectangle(frame, p1, p2, (255, 255, 255), 2)

    def draw_paddle(self, frame, paddle):
        """In-place draw the paddle onto the frame"""
        cx, cy = paddle['cx'], paddle['cy']
        p1 = (cx - paddle['half_paddle_width'], cy - paddle['half_paddle_height'])
        p2 = (cx + paddle['half_paddle_width'], cy + paddle['half_paddle_height'])
        cv2.rectangle(frame, p1, p2, (255, 255, 255), thickness=-1)

    def draw_ball(self, frame, ball):
        """In-place draw the ball onto the frame"""
        p = (ball['cx'], ball['cy'])
        cv2.circle(frame, p, ball['r'], (255, 255, 255), thickness=-1)

    def on_key(self, key):
        if self.is_key(key, 'w'):
            self.paddle1['dy'] = -self.paddle1['speed']
        elif self.is_key(key, 's'):
            self.paddle1['dy'] = self.paddle1['speed']
        else:
            self.paddle1['dy'] = 0

    def is_key(self, key, character):
        return key & 0xFF == ord(character)


def main():
    width = height = 600
    pong = Pong()

    while True:
        key = cv2.waitKey(1)
        pong.on_key(key)

        # update game
        frame = np.zeros((width, height))
        ended = pong.update()
        pong.draw(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if pong.is_key(key, 'q') or ended:
            break


if __name__ == '__main__':
    main()
