from graphics import Point, Image, update
from traffic_control import TrafficControl
from moving import (Truck, Rocket, Car, RaceTruck, RaceCar,
                    SmallLog, MedLog, BigLog, TwoTurtle, ThreeTurtle)
from frog import Frog
from screen import GameScreen
import time


def createFrog(frog_step, frog_lane, win):
    """Create and return a frog object"""
    base = Point(frog_step*6.5, 84 + frog_step * (frog_lane - 1/2))
    frog = Frog(base, frog_step)
    frog.draw(win)
    return frog


def drawPavements(unit, n_street, n_river, win):
    """Draw safe pavements that frog can rest on."""

    # Top pavement
    pavement1 = Image(Point(win.getWidth()/2, 84+unit*1/2), "img/pavement.png")
    pavement1.draw(win)

    # Mid pavement
    pavement2 = pavement1.clone()
    pavement2.move(0, unit * (n_river+1))
    pavement2.draw(win)

    # Bottom pavement
    pavement3 = pavement2.clone()
    pavement3.move(0, unit * (n_street+1))
    pavement3.draw(win)


def drawLives(n_lives, bottom_screen, win):
    """Draw small icons indicating the number of lives given to the user."""
    sample = Image(Point(12, win.getHeight() - bottom_screen + 10),
                   "img/lives.png")

    lives_list = []

    for i in range(n_lives):
        lives = sample.clone()
        lives.move(i*22, 0)
        lives.draw(win)
        lives_list.append(lives)

    return lives_list


def moveFrog(score, frog, frog_step, current_lane, base_lane, win):
    """Move the frog based on the command the user presses."""
    WIDTH = win.getWidth()
    key_pressed = win.checkKey()

    if key_pressed:
        frog.undraw()

        if key_pressed == "Up":
            # If the frog is not yet at top lane
            if current_lane != 0:
                frog.moveUp()
                current_lane -= 1
                # Add 50 to the score every time the user moves up
                score += 50

        elif key_pressed == "Down":
            # If the frog is not yet at the base lane
            if current_lane != base_lane:
                frog.moveDown()
                current_lane += 1
                # Minus 100 everytime they move down.
                score -= 100

        elif key_pressed == "Left":
            # Prevent the frog from moving off screen
            if frog.getLeft() - frog_step > 0:
                frog.moveLeft()

        elif key_pressed == "Right":
            # Prevent the frog from moving off screen
            if frog.getRight() + frog_step < WIDTH:
                frog.moveRight()

        frog.draw(win)

    return current_lane, score


def createTraffic(n_street, n_river, win):
    """Draw traffics when the game first created."""

    # How obstacles are distributed onto the screen.
    obstacles = [Truck, Rocket, Car, RaceTruck, RaceCar]
    aids = [MedLog, TwoTurtle, BigLog, SmallLog, ThreeTurtle]

    street_controller = TrafficControl(obstacles)
    street_controller.setNLane(n_street)
    street_controller.generateTraffic(n_river + 2, win)

    river_controller = TrafficControl(aids, safe=False)
    river_controller.setNLane(n_river)
    river_controller.generateTraffic(1, win)

    return street_controller, river_controller


def deathAnimation(frog, lives_list, win):
    """Play death animation when the frog dies."""
    frog.undraw()
    frog.onDeath(win)
    lives_list.pop().undraw()

    # Reset frog to the base lane
    frog.reset()
    win.lastKey = ""
    frog.draw(win)


def play(win, street_controller, river_controller, n_street, n_river):
    unit = 42
    WIDTH = win.getWidth()
    bottom_screen = 42

    frog = createFrog(unit, n_river + n_street + 3, win)
    base_lane = n_street + n_river + 2
    current_lane = base_lane
    lives_list = drawLives(3, bottom_screen, win)

    won = False
    score = 0

    # Parameter to calculate how long it takes for the user to finish the game.
    start_time = time.time()
    while len(lives_list) > 0 and not won:
        # Move frog
        current_lane, score = moveFrog(score, frog, unit, current_lane,
                                       base_lane, win)

        # Move traffic
        street_controller.moveTraffic(WIDTH)
        river_controller.moveTraffic(WIDTH)

        # If frog is on street lanes
        if current_lane in range(base_lane - n_street, base_lane):
            collided = street_controller.checkCollision(current_lane, frog)
            if collided is not None:
                deathAnimation(frog, lives_list, win)
                score -= 100
                current_lane = base_lane

        # If frog is on river lanes
        elif current_lane in range(1, n_river + 1):
            collided = river_controller.checkCollision(current_lane, frog)

            # If frog doesn't collide on river, it dies
            if collided is None:
                deathAnimation(frog, lives_list, win)
                current_lane = base_lane
                score -= 500

            # Else frog move with the speed of the log/turtle
            else:
                if (collided.getDirection() == "Left" and
                    frog.getLeft() >= 0 or
                    collided.getDirection() == "Right" and
                   frog.getRight() <= WIDTH):
                    frog.moveRight(collided.getSpeed())

        elif current_lane == 0:
            won = True
            score += 500
        update(30)

    # Calculate score
    end_time = time.time()
    score += 1000/(end_time-start_time)
    if score < 0:
        score = -score*0.1
    return round(score)


def main():
    n_street = 5
    n_river = 5
    unit = 42

    win = GameScreen(n_street=n_street, n_river=n_river)
    win.setBackground()
    choice = win.welcomeScreen()

    while choice != "Quit":
        if choice == "Play":
            street_controller, river_controller = createTraffic(n_street,
                                                                n_river, win)
            drawPavements(unit, n_street, n_river, win)
            score = play(win, street_controller, river_controller,
                         n_street, n_river)
            win.addHighscoreScreen(score)

        choice = win.highscoreScreen()
    win.close()


if __name__ == "__main__":
    main()
