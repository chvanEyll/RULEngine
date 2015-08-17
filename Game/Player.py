from ..Util.Pose import Pose, Position
from ..Command import Command
from time import time


class Player(object):
    """ Player is container of proprieties (id, current pose and color team) and can generate player command. """
    def __init__(self, id, is_yellow=True):
        assert(isinstance(id, int)), 'Player.id should be int.'
        assert(0 <= id <= 6), 'Player.id should be between 0 and 6.'
        assert(isinstance(is_yellow, bool)), 'Player.is_yellow should be bool.'

        self.id = id
        self.pose = Pose()
        self.is_yellow = is_yellow
        self._last_cmd_time = time()
        self._delay_btw_cmd = 50        # ms

    def has_id(self, id):
        """ Return self.id == id """
        assert(isinstance(id, int)), 'Player.has_id should be int (not {})'.format(type(id))
        assert(0 <= id <= 8), 'Player.has_id should be between 0 and 8 (not {})'.format(id)
        return self.id == id

    # def act_move(self, n_pose):
    #     """ Return command player for moving to next pose """
    #     assert(isinstance(n_pose, Pose)), 'Player.actMove should be Pose object (not {})'.format(type(n_pose))
    #     return Command.MoveToAndRotate(self, n_pose)
    #
    # def act_strafe(self, n_position):
    #     """ Return command player for strafing to next position """
    #     assert(isinstance(n_position, Position)), 'Player.actStrafe should be Position object (not {})'.format(type(n_position))
    #     return Command.MoveTo(self, n_position)
    #
    # def act_kick(self, kick_speed=5):
    #     """ Return raw command player for kicking NOW """
    #     assert(isinstance(kick_speed, int)), 'Player.actKick should be int object (not {})'.format(type(kick_speed))
    #     assert(0 <= kick_speed <= 8), 'Player.actKick should be between 0+ and 8 (not {})'.format(kick_speed)
    #     if self._is_ready():
    #         return Command.Kick(self, kick_speed)
    #     else:
    #         return self.act_stop()
    #
    # def act_stop(self):
    #     """ Return raw command player for stopping any movement """
    #     return Command.Stop(self)
    #
    # def _is_ready(self):
    #     """ Return (now > last + delay)?(last = now and True):False """
    #     now = int(round(time() * 1000))
    #     last = int(round(self._last_cmd_time * 1000))
    #     delay = self._delay_btw_cmd
    #     if now > last + delay:
    #         self._last_cmd_time = time()
    #         return True
    #     else:
    #         return False
