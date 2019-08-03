from graphics import Image
import time


class Frog():
    """A class for the frog object that the player can control."""
    def __init__(self, position, step):

        # dict of sprites
        self.sprites = {"up_sprite": Image(position, "img/frog_up.png"),
                        "down_sprite": Image(position, "img/frog_down.png"),
                        "left_sprite": Image(position, "img/frog_left.png"),
                        "right_sprite": Image(position, "img/frog_right.png")}
        self.death = "img/death.png"
        self.base = position

        # At start, the frog face up
        self.current_sprite = self.sprites["up_sprite"]

        # Status variable
        self.dead = False
        self.step = step

    # For all move function, move all frog ssprites at once.
    def moveUp(self):
        """Move all sprites of frog up."""
        for sprite in self.sprites.values():
            sprite.move(0, -self.step)
        self.current_sprite = self.sprites["up_sprite"]

    def moveDown(self):
        """Move all sprites of frog down."""
        for sprite in self.sprites.values():
            sprite.move(0, self.step)
        self.current_sprite = self.sprites["down_sprite"]

    def moveLeft(self):
        """Move all sprites of frog left."""
        for sprite in self.sprites.values():
            sprite.move(-self.step, 0)
        self.current_sprite = self.sprites["left_sprite"]

    def moveRight(self, *args):
        """Move all sprites of frog right."""
        # If one args exist, move frog by that amount instead
        if len(args) == 1:
            for name, sprite in self.sprites.items():
                sprite.move(args[0], 0)
        else:
            for sprite in self.sprites.values():
                sprite.move(self.step, 0)
            self.current_sprite = self.sprites["right_sprite"]

    def getLeft(self):
        """Return left bound of frog hitbox."""
        left_hb = (self.current_sprite.getAnchor().getX() -
                   self.current_sprite.getWidth()/2)
        return int(left_hb)

    def getRight(self):
        """Return right bound of frog hitbox."""
        right_hb = (self.current_sprite.getAnchor().getX() +
                    self.current_sprite.getWidth()/2)
        return int(right_hb)

    def getWidth(self):
        return self.current_sprite.getWidth()

    def reset(self):
        """Reset frog to the base position. Update after reset."""
        self.undraw()
        self.sprites = {"up_sprite": Image(self.base, "img/frog_up.png"),
                        "down_sprite": Image(self.base, "img/frog_down.png"),
                        "left_sprite": Image(self.base, "img/frog_left.png"),
                        "right_sprite": Image(self.base, "img/frog_right.png")}
        self.current_sprite = self.sprites["up_sprite"]

    def onDeath(self, win):
        """Animation for the frog when it's dead."""
        self.undraw()
        death_sprite = Image(self.current_sprite.getAnchor(), self.death)
        death_sprite.draw(win)
        start_time = time.time()
        # Pause the screen for one sec while the frog's ghost floats up.
        while time.time() - start_time < 1:
            death_sprite.move(0, -0.01)
        death_sprite.undraw()

    def draw(self, win):
        """Update the current sprite of the frog."""
        self.current_sprite.draw(win)
        win.update()

    def undraw(self):
        """Undraw the current sprite of the frog."""
        self.current_sprite.undraw()
