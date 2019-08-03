from graphics import Image


class MovingObject():
    "A class of uncontrollable object on screen."

    def __init__(self, position):
        self.sprite = Image(position, "img/car.png")
        self.speed = 1

    def draw(self, win):
        "Draw MovingObject object on to GraphWin object."
        self.sprite.draw(win)

    # My attempt at encapsulation (how do you spell it again?)
    # setSpeed to increase/decrease difficulties
    def setSpeed(self, speed):
        "Set the speed of the object."
        self.speed = speed

    def getSpeed(self):
        "Get the speed of the object."
        return self.speed

    def getLeft(self):
        "Return left bound of the object."
        left_hb = self.sprite.getAnchor().getX() - self.sprite.getWidth()/2
        return int(left_hb)

    def getRight(self):
        "Return right bound of the object."
        right_hb = self.sprite.getAnchor().getX() + self.sprite.getWidth()/2
        return int(right_hb)

    def getWidth(self):
        """Return the width of the object."""
        return self.sprite.getWidth()

    def getDirection(self):
        """Return the direction the object is moving."""
        if self.speed < 0:
            return "Left"
        return "Right"

    def move(self, *args):
        """Move object based on its speed."""
        # If one args exist, move object by that value instead.
        if len(args) == 1:
            offset = args[0]
            self.sprite.move(offset, 0)
        else:
            self.sprite.move(self.speed, 0)


class Obstacle(MovingObject):
    """Class for all obstacles. Exists for organization purpose."""
    pass


class RaceCar(Obstacle):
    """RaceCar class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/racecar.png")
        self.speed = -2.5


class RaceTruck(Obstacle):
    """RaceTruck class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/racetruck.png")
        self.speed = 1.5


class Car(Obstacle):
    """Car class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/car.png")
        self.speed = -3


class Rocket(Obstacle):
    """Rocket class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/rocket.png")
        self.speed = 2


class Truck(Obstacle):
    """Truck class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/truck.png")
        self.speed = -2


class Aid(MovingObject):
    """Class for all aid moving objects. Exists for organization purpose."""
    pass


class SmallLog(Aid):
    """SmallLog class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/small_log.png")
        self.speed = 1


class BigLog(Aid):
    """BigLog class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/big_log.png")
        self.speed = 3


class MedLog(Aid):
    """MedLog class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/med_log.png")
        self.speed = 1.5


class TwoTurtle(Aid):
    """TwoTurtle class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/two_turtle.png")
        self.speed = -2.5


class ThreeTurtle(Aid):
    """ThreeTurtle class."""
    def __init__(self, position):
        self.sprite = Image(position, "img/three_turtle.png")
        self.speed = -2
