from graphics import Point
from moving import BigLog
from random import randrange


class TrafficControl():
    """An object to control traffics on the road.
       controller = TrafficControl()"""

    def __init__(self, obj_distribution, safe=True):

        self.obj_distribution = obj_distribution
        # List of object that will appear in order, eg: [Truck, Car, Rocket]
        # will give Truck in lane 1, Car in lane 2 and Rocket in lane 3.

        self.n_lane = len(self.obj_distribution)
        self.safe_lane = safe

    def setNLane(self, n_lane):
        """Set the number of lanes"""
        # Extend the self.obj_distribution list
        if n_lane > self.n_lane:
            for i in range(n_lane - self.n_lane):
                self.obj_distribution.insert(0, self.obj_distribution[-i-1])
        self.n_lane = n_lane

    def generateTraffic(self, start_lane, win):
        """Place vehicles and moving objects onto the screen randomly."""
        top_screen = 84
        unit = 42

        # The dictionary with lane number as keys.
        # Values are lists of Moving objects that will be added later.
        self.object_group = {i + start_lane: [] for i in range(self.n_lane)}

        # Start lane is the lane where the controller start drawing object
        for lane_index in range(start_lane, self.n_lane + start_lane):
            Class = self.obj_distribution[lane_index - start_lane]

            # Random position for first object
            x = randrange(unit*2)

            # Set number of objects on the lane
            n_object = 3
            if Class == BigLog:
                n_object = 2

            # Create n_object Moving objects
            for _ in range(n_object):
                # Position of the object based on random x position and lane
                moving_object = Class(Point(x,
                                            top_screen+unit*(lane_index+1/2)))
                moving_object.draw(win)
                self.object_group[lane_index].append(moving_object)

                # Generate another random x for the next object
                x = (self.object_group[lane_index][-1].getRight() +
                     randrange(unit*4, unit*6) +
                     self.object_group[lane_index][-1].getWidth()/2)

    def moveTraffic(self, right_bound, left_bound=0):
        """Move objects on lane. If objects move past the right bound
           or left bound, move it to the other side."""
        for lane, moving_objects in self.object_group.items():
            for obj in moving_objects:
                obj.move()
            # If objects on that lane is moving left:
            # |   <-        <-       <-   | (object visual)
            # |    0         1       2    | (position in list)
            # | in_front                  | (position of in_front)
            if moving_objects[0].getDirection() == "Left":
                # The object closest to the left bound is the one at position 0
                in_front = moving_objects[0]
                if in_front.getRight() < left_bound:
                    # Pick position based on position of the obj at the back
                    move_to = moving_objects[-1].getRight()+randrange(200, 300)

                    if move_to < right_bound:
                        move_to = right_bound + randrange(200, 300)
                    move_to += in_front.getWidth()

                    moving_objects.pop(0)
                    moving_objects.append(in_front)
                    in_front.move(move_to)

            # If objects on that lane is moving right:
            # |  ->      ->       ->     | (object visual)
            # |  0       1        2      | (position in list)
            # |                in_front  | (position of in_front)
            else:
                # The object closest to the right bound is at final position
                in_front = moving_objects[-1]
                if in_front.getLeft() > right_bound:

                    # Pick position relative to position of the obj at the back
                    move_to = moving_objects[0].getLeft() - randrange(200, 300)
                    if move_to > left_bound:
                        move_to = left_bound - randrange(200, 300)
                    move_to -= in_front.getWidth()

                    moving_objects.pop()
                    moving_objects.insert(0, in_front)

                    # Actually move the object.
                    # move_to is the the point to move the object to.
                    # right_bound-move_to is the magnitude of the path to move.
                    # Negative since we move to the left.
                    in_front.move(-(right_bound - move_to))

    def checkCollision(self, frog_lane, frog):
        """Check if the frog collided with any object on the lane it is on."""

        for moving_object in self.object_group[frog_lane]:
            # If the frog hitbox collides with one of the object hitbox
            if (frog.getLeft() in range(moving_object.getLeft(),
                                        moving_object.getRight())
                or frog.getRight() in range(moving_object.getLeft(),
                                            moving_object.getRight())):
                return moving_object
        return None
