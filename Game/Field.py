from ..Game.Ball import Ball, Position


class Field(object):
    """ Field contain object ball (for time being).  """
    def __init__(self, ball):
        assert(isinstance(ball, Ball)), 'Field.ball should be Ball object (not {})'.format(type(ball))
        self.ball = ball

    def move_ball(self, position):
        assert(isinstance(position, Position)), \
            'Player.move_ball.position should be Position object (not {})'.format(type(position))
        self.ball.position = position
