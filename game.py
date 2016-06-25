# Under MIT License, see LICENSE.txt

from .util.geometry import Pose, Position
from .util.constant import PLAYER_PER_TEAM
import math


class Game():
    def __init__(self, is_team_yellow):
        self.ball = Ball()
        self.field = Field(self.ball)
        self.referee = None  # TODO Add referee
        self.blue_team, self.yellow_team = self.create_teams()

        if is_team_yellow:
            self.friends = self.yellow_team
            self.enemies = self.blue_team
        else:
            self.friends = self.blue_team
            self.enemies = self.yellow_team

        self.delta = None

    def create_teams(self):
        blue_team = Team(is_team_yellow=False)
        yellow_team = Team(is_team_yellow=True)

        return blue_team, yellow_team

    def update_game_state(self, referee_command):
        pass
        # TODO: Réviser code, ça semble louche
        # blue_team = referee_command.teams[0]
        # self.blue_team.score = blue_team.goalie_count
        # yellow_team = referee_command.teams[0]
        # self.yellow_team.score = yellow_team.goalie_count

        # command = Referee.Command(referee_command.command.name)
        # self.referee.command = command

        # TODO: Correctly update the referee with the data from the referee_command

    def update(self, vision_frame, delta):
        self.delta = delta
        self._update_ball(vision_frame, delta)
        self._update_players(vision_frame, delta)

    def _update_ball(self, vision_frame, delta):
        ball_position = Position(vision_frame.detection.balls[0].x,
                                 vision_frame.detection.balls[0].y,
                                 vision_frame.detection.balls[0].z)
        self.field.move_ball(ball_position, delta)

    def _update_players(self, vision_frame, delta):
        blue_team = vision_frame.detection.robots_blue
        yellow_team = vision_frame.detection.robots_yellow

        self._update_players_of_team(blue_team, self.blue_team, delta)
        self._update_players_of_team(yellow_team, self.yellow_team, delta)

    def _update_players_of_team(self, players, team, delta):
        for player in players:
            player_position = Position(player.x, player.y, player.height)
            player_pose = Pose(player_position, player.orientation)
            team.move_and_rotate_player(player.robot_id, player_pose)


class Field():
    def __init__(self, ball):
        self.ball = ball

    def move_ball(self, position, delta):
        self.ball.set_position(position, delta)


class Ball():
    def __init__(self):
        self._position = Position()
        self.velocity = Position()

    @property
    def position(self):
        return self._position

    def set_position(self, pos, delta):
        if pos != self._position:
            self.velocity.x = (pos.x - self._position.x)/delta
            self.velocity.y = (pos.y - self._position.y)/delta
            print(math.sqrt(self.velocity.x**2 + self.velocity.y**2))
            print(delta)

            self._position = pos


class Team():
    def __init__(self, is_team_yellow):
        self.players = [Player(self, i) for i in range(PLAYER_PER_TEAM)]
        self.is_team_yellow = is_team_yellow
        self.score = 0

    def has_player(self, player):
        has_player = False

        for team_player in self.players:
            if team_player == player:
                has_player = True

        return has_player

    def move_and_rotate_player(self, player_id, pose):
        for player in self.players:
            if player.has_id(player_id):
                player.pose = pose


class Player():
    def __init__(self, team, id):
        self.id = id
        self.team = team
        self.pose = Pose()

    def has_id(self, id):
        return self.id == id
