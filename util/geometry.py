# Under MIT License, see LICENSE.txt
import math as m

__author__ = 'RoboCupULaval'

# TODO: Merge vector and position
class Position(object):
    """ Vector with [x, y, z] """
    def __init__(self, x=0, y=0, z=0):
        assert(isinstance(x, (int, float))), 'x should be int or float.'
        assert(isinstance(y, (int, float))), 'y should be int or float.'
        assert(isinstance(z, (int, float))), 'z should be int or float.'

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def copy(self):
        """
        copy() -> Position

        Return copy of Position.
        """
        return Position(self.x, self.y, self.z)

    # *** OPERATORS ***
    def __add__(self, other):
        """ Return self + other """
        if not isinstance(other, (Position, int, float)):
            return NotImplemented
        else:
            new_x = self.x + (other.x if isinstance(other, Position) else other)
            new_y = self.y + (other.y if isinstance(other, Position) else other)
            return Position(new_x, new_y)

    def __sub__(self, other):
        """ Return self - other """
        if not isinstance(other, (Position, int, float)):
            raise NotImplemented
        else:
            new_x = self.x - (other.x if isinstance(other, Position) else other)
            new_y = self.y - (other.y if isinstance(other, Position) else other)
            return Position(new_x, new_y)

    def __mul__(self, other):
        """ Return self * other """
        if not isinstance(other, (int, float)):
            raise NotImplemented
        else:
            new_x = self.x * other
            new_y = self.y * other
            return Position(new_x, new_y)

    def __truediv__(self, other):
        """ Return self / other """
        if not isinstance(other, (int, float)):
            raise NotImplemented
        else:
            new_x = self.x / other
            new_y = self.y / other
            return Position(new_x, new_y)

    def __eq__(self, other):
        """ Return self == other """
        assert(isinstance(other, Position)), 'other should be Position.'
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """ Return self != other """
        return not self.__eq__(other)

    def __repr__(self):
        """ Return str(self) """
        return "(x={}, y={}, z={})".format(self.x, self.y, self.z)

class Pose(object):
    """  Container of position and orientation """
    def __init__(self, position=Position(), orientation=0.0):
        assert(isinstance(position, Position)), 'position should be Position object.'
        assert(isinstance(orientation, (int, float))), 'orientation should be int or float value.'

        self.position = position
        self.orientation = orientation
        if self.orientation >= m.pi:
            self.orientation -= 2 * m.pi
        elif self.orientation <= -m.pi:
            self.orientation += 2*m.pi

    def __str__(self):
        return '[{}, theta={}]'.format(self.position, self.orientation)
    def __repr__(self):
        return self.__str__()

class Vector(object):
    def __init__(self, length=1.0, direction=0.0):
        """
        :param length: the vector's length
        :param direction: the vector's direction, in radians
        """
        assert (isinstance(length, (int, float))), 'length should be int or float value.'
        assert (isinstance(direction, (int, float))), 'direction should be int or float value.'

        x = length * m.cos(direction)
        y = length * m.sin(direction)
        self._attributes = [length, direction, x, y]

    # *** GETTER / SETTER ***
    def _getlength(self):
        return self._attributes[0]

    def _setlength(self, length):
        assert (isinstance(length, (int, float)))
        self._attributes[0] = length
        self._attributes[2] = length * m.cos(self._attributes[1])
        self._attributes[3] = length * m.sin(self._attributes[1])

    """ Make self.length with setter and getter attributes """
    length = property(_getlength, _setlength)

    def _getdirection(self):
        return self._attributes[1]

    def _setdirection(self, direction):
        assert (isinstance(direction, (int, float)))
        self._attributes[1] = direction
        self._attributes[2] = self._attributes[0] * m.cos(direction)
        self._attributes[3] = self._attributes[0] * m.sin(direction)

    """Make self.direction with setter and getter attributes """
    direction = property(_getdirection, _setdirection)

    def _getx(self):
        return self._attributes[2]

    def _setx(self, x):
        assert (isinstance(x, (int, float))), 'value should be Position or int or float.'
        self._attributes[2] = x
        self._attributes[0] = m.sqrt(x ** 2 + self._attributes[3] ** 2)
        self._attributes[1] = m.atan2(self._attributes[3], x)

    """ Make self.x with setter and getter attributes """
    x = property(_getx, _setx)

    def _gety(self):
        return self._attributes[3]

    def _sety(self, y):
        assert (isinstance(y, (int, float)))
        self._attributes[3] = y
        self._attributes[0] = m.sqrt(y ** 2 + self._attributes[2] ** 2)
        self._attributes[1] = m.atan2(y, self._attributes[2])

    """ Make self.y with setter and getter attributes """
    y = property(_gety, _sety)

    # *** OPERATORS ***
    def __eq__(self, other):
        """
        The == operator
        :param other: The comparison vector
        :return: A boolean stating whether the two Vectors are equal
        """
        assert (isinstance(other, Vector))
        #return self.length == other.length and self.direction == other.direction
        return round(self.length, 10) == round(other.length, 10) and round(self.direction, 10) == round(other.direction,
                                                                                                        10)

    def __ne__(self, other):
        """
        The != operator
        :param other: The comparison vector
        :return: A boolean stating whether the two Vectors are not equal
        """
        assert (isinstance(other, Vector))
        return not self.__eq__(other)

    def __add__(self, other):
        """
        The + operator
        :param other: A Position, a Pose or a Vector
        :return: An object of the same type as the input parameter other
        Note : if other is of type Pose, returns a new Pose whose orientation is the same as the current vector
        """
        assert (isinstance(other, (Position, Pose, Vector)))
        if isinstance(other, Position):
            return Position(other.x + self.x, other.y + self.y)
        elif isinstance(other, Pose):
            p = Position(other.position.x + self.x, other.position.y + self.y)
            return Pose(p, self.direction)
        elif isinstance(other, Vector):
            x = self.x + other.x
            y = self.y + other.y
            return Vector(m.sqrt(x ** 2 + y ** 2), m.atan2(y, x))

    def __radd__(self, other):
        """
        Allows commutativity for Position + Vector and Pose + Vector
        :param other: A Position or a Pose
        :return: An object of the same type as the input parameter other
        Note : if other is of type Pose, returns a new Pose whose orientation is the same as the current vector
        """
        assert (isinstance(other, (Position, Pose)))
        if isinstance(other, Position):
            return Position(other.x + self.x, other.y + self.y)
        elif isinstance(other, Pose):
            p = Position(other.position.x + self.x, other.position.y + self.y)
            return Pose(p, self.direction)

    def __iadd__(self, other):
        """
        The += operator
        :param other: A Vector to add to the current Vector
        :return: The current Vector is modified
        """
        assert (isinstance(other, Vector))
        x = self.x + other.x
        y = self.y + other.y
        self.length = m.sqrt(x ** 2 + y ** 2)
        self.direction = m.atan2(y, x)
        return self

    def __sub__(self, other):
        """
        The - operator
        :param other: A Vector
        :return: The new Vector resulting from the substraction
        """
        assert (isinstance(other, Vector))
        x = self.x - other.x
        y = self.y - other.y
        return Vector(m.sqrt(x ** 2 + y ** 2), m.atan2(y, x))

    def __isub__(self, other):
        """
        The -= operator
        :param other: A Vector to substract from the current Vector
        :return: The current Vector is modified
        """
        assert (isinstance(other, Vector))
        x = self.x - other.x
        y = self.y - other.y
        self.length = m.sqrt(x ** 2 + y ** 2)
        self.direction = m.atan2(y, x)
        return self

    def __neg__(self):
        """
        The unary arithmetic operation -
        :return: the opposite vector
        """
        return self.__mul__(-1)

    def __mul__(self, scalar):
        """
        Scalar Multiplication
        :param scalar: a real number
        :return: a new vector resulting of the scalar multiplication
        """
        assert (isinstance(scalar, (int, float)))
        if scalar >= 0:
            return Vector(length=scalar * self.length, direction=self.direction)
        else:
            return Vector(length=-1 * scalar * self.length, direction=-1 * self.direction)

    def __rmul__(self, scalar):
        """
        Allows commutativity for int*Vector
        :param scalar: a real number
        :return: a new vector resulting of the scalar multiplication
        """
        assert (isinstance(scalar, (int, float)))
        if scalar >= 0:
            return Vector(length=scalar * self.length, direction=self.direction)
        else:
            return Vector(length=-1 * scalar * self.length, direction=-1 * self.direction)

    def __imul__(self, scalar):
        """
        Incremental scalar multiplication
        :param scalar: a real number
        :return: the current resized vector
        """
        assert(isinstance(scalar, (int, float)))
        if scalar >= 0:
            self.length *= scalar
        else:
            self.length *= -1 * scalar
            self.direction *= -1
        return self

    def __str__(self):
        """
        :return: A string containing the Vector's attribute in a readable form
        """
        return "(Length = {}, Direction = {})".format(self.length, self.direction)

    # *** GENERAL METHODS ***
    def dot(self, vector):
        """
        The dot product
        :param vector: The second Vector of the dot product
        :return: The result of the dot product in a float
        """
        return self.length * vector.length * m.cos(self.direction - vector.direction)

    def unit(self):
        """
        :return: A unit Vector whose direction is the same as the current Vector
        """
        return Vector(length=1, direction=self.direction)

    def normal(self, plus90=True):
        """
        :param plus90: A boolean stating if the direction of the normal Vector is equal to the direction of
        the current Vector plus pi/2 (True) or minus pi/2 (False)
        :return: A unit Vector perpendicular to the current Vector
        """
        if plus90:
            return Vector(length=1, direction=self.direction + m.pi / 2)
        else:
            return Vector(length=1, direction=self.direction - m.pi / 2)

    def getangle(self, vector):
        """
        :param vector: The Vector
        :return: The smallest angle between the two Vectors, in radians
        """
        return m.fabs(self.direction - vector.direction)

def get_distance(position_1, position_2):
    """
    Distance between two positions.
    :param position_1: Position
    :param position_2: Position
    :return: float - distance in millimeter
    """
    assert(isinstance(position_1, Position))
    assert(isinstance(position_2, Position))
    return m.sqrt((position_2.x - position_1.x) ** 2 + (position_2.y - position_1.y) ** 2)


def get_angle(main_position, other):
    """
    Angle between position1 and position2 between -pi and pi
    :param main_position: Position of reference
    :param other: Position of object
    :return: float angle between two positions in radians
    """
    assert isinstance(main_position, Position), "TypeError main_position"
    assert isinstance(other, Position), "TypeError other"

    position_x = float(other.x - main_position.x)
    position_y = float(other.y - main_position.y)
    return m.atan2(position_y, position_x)


def cvt_angle_360(orientation):
    """
    Convert radians angle to 0-360 degrees
    :param orientation: float angle in radians
    :return: int angle with 0 to 360 range.
    """
    assert isinstance(orientation, (int, float)), "TypeError orientation"
    orientation = m.degrees(orientation)

    if orientation < 0:
        while True:
            if orientation >= 0:
                break
            else:
                orientation += 360
    elif orientation > 359:
        while True:
            if orientation < 360:
                break
            else:
                orientation -= 360
    return int(orientation)


def cvt_angle_180(orientation):
    """
    Convert radians angle to -180-180 degrees (same as m.degrees())
    :param orientation: float angle in radians
    :return: int angle with 180 to -179 range.
    """
    assert isinstance(orientation, (int, float)), "TypeError orientation"

    orientation = cvt_angle_360(orientation)
    if orientation > 180:
        return orientation-360
    elif orientation <= -180:
        return orientation+360
    else:
        return int(orientation)


def get_nearest(ref_position, list_of_position, number=1):
    dict_position_distance = {}
    for bot_position in list_of_position:
        dst = get_distance(ref_position, bot_position)

        while dst in dict_position_distance.keys():
            dst += 0.1
        dict_position_distance[dst] = bot_position

    list_sorted = []
    for i, bot_dst in enumerate(sorted(dict_position_distance.keys())):
        if i < number:
            list_sorted.append(dict_position_distance[bot_dst])
        else:
            return list_sorted
