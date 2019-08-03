from graphics import GraphWin, Rectangle, Point, Image, Text, Entry, color_rgb
from button import Button
import time


class GameScreen(GraphWin):
    """A class for the game's screen."""
    def __init__(self, title="Frogger", unit=42, top=84, bottom=42,
                 n_street=5, n_river=5):

        width = unit*14
        height = top + bottom + unit * (n_street + n_river + 3)

        super().__init__(title, width, height, autoflush=True)

        # The Background objects
        self.river = Rectangle(Point(0, 0), Point(self.width,
                                                  top + unit * (n_river + 1)))
        self.river.setWidth(0)
        self.river.setFill(color_rgb(0, 0, 66))

        self.street = Rectangle(Point(self.width, top + unit * (n_river + 1)),
                                Point(0, self.height))
        self.street.setWidth(0)
        self.street.setFill(color_rgb(0, 0, 0))

        self.config(bg="black")

    def setBackground(self):
        """Draw a black-blue background."""
        self.river.draw(self)
        self.street.draw(self)

    def clearScreen(self, start_item=2):
        """Clear all objects on screen except the background."""
        for item in self.items[start_item:]:
            item.undraw()

    def welcomeScreen(self):
        """Draw the welcome screen and return the button the user presses."""
        title = Image(Point(self.width/2, self.height/2-150), "img/title.png")
        title.draw(self)
        return self.getButton("Play", "Highscore")

    def addHighscoreScreen(self, score):
        """Draw a pop-up prompting the user to enter their name and
           add their info to the highscores list if score is high enough."""

        def drawEnterbox():
            enterbox = Rectangle(Point(0, self.height/2 - 70),
                                 Point(self.width, self.height/2 + 70))

            enterbox.setFill("black")
            enterbox.draw(self)

            score_text = Text(Point(self.width/2, self.height/2 - 35), score)
            score_text.setFace("courier")
            score_text.setSize(25)
            score_text.setStyle("bold")
            score_text.setTextColor("white")
            score_text.draw(self)

            name_text = Text(Point(70, self.height/2 + 10), "NAME")
            name_text.setFace("courier")
            name_text.setSize(30)
            name_text.setStyle("bold")
            name_text.setTextColor("white")
            name_text.draw(self)

            name_entry = Entry(Point(self.width/2+50, self.height/2+10), 25)
            name_entry.setFace("courier")
            name_entry.setSize(20)
            name_entry.setTextColor("yellow")
            name_entry.setStyle("bold")
            name_entry.draw(self)

            while True:
                if self.getKey() == "Return":
                    break
            name = name_entry.getText()

            # If the user didn't enter a name, put NONAME in.
            if name == "":
                name = "NONAME"

            # Abbreviate name if name is longer than 26 characters.
            if len(name) > 26:
                print(name)
                name = name[:13] + "..." + name[-13:]
            return name

        # Compare and add score to the text file.
        entries = self.readScores()
        # Entries is a list: [[name1, score1], [name2, score2],...]
        name = drawEnterbox()
        for entry in range(8):
            try:
                # If the score is bigger than one of the score in the list
                if score > entries[entry][1]:
                    entries.insert(entry, [name, score])
                    break
            except IndexError:
                # Happens when the list of score hasn't had 8 entries yet.
                entries.append([name, score])
                break

        with open("doc/highscores.txt", "w") as file:
            # Only accept 8 highest scores.
            for entry in range(8):
                try:
                    file.write("%s-%s\n" %
                               (entries[entry][0], entries[entry][1]))
                except IndexError:
                    break
        self.clearScreen()

    def highscoreScreen(self):
        """Print a highscore screen. Return the button the user presses."""

        # Print the title "HIGHSCORE"
        title = Text(Point(self.width/2, 100), "H I G H  S C O R E")
        title.setSize(30)
        title.setTextColor("white")
        title.setStyle("bold")
        title.setFace("courier")
        title.draw(self)

        # Print the leaderboard nicely formatted.
        entries = self.readScores()
        counter = 1
        color = ["red", "pink", "yellow", "orange", "green",
                 "blue", "purple", "magenta"]
        for entry in entries:
            text = "{0:.<30}{1:<5}".format(entry[0], entry[1])
            print_text = Text(Point(self.width/2, 100 + (counter*50)),
                              str(counter) + ". " + text)
            print_text.setSize(15)
            print_text.setTextColor(color[counter-1])
            print_text.setStyle("bold")
            print_text.setFace("courier")
            print_text.draw(self)
            counter += 1

        return self.getButton("Play", "Quit", 250)

    def getButton(self, b1_name, b2_name, h_offset=150):
        """Button effect for two buttons on screen.
           Button name have to match the sprite file name (no extension)."""

        # Create a two buttons
        button_1 = Button(Point(self.width/2 - 150, self.height/2 + h_offset),
                          "img/%s.png" % b1_name.lower())
        button_2 = Button(Point(self.width/2 + 150, self.height/2 + h_offset),
                          "img/%s.png" % b2_name.lower())

        button_1.draw(self)
        button_2.draw(self)

        # Only register when user presses left or right
        valid_keys = ["Left", "Right"]
        is_on = button_1

        while not self.closed:
            # Highlight the current button
            is_on.onHighlight(self)
            command = self.getKey()
            # If the user presses Left or Right
            if command in valid_keys:
                # Change current button to normal and switch to other button.
                if is_on == button_1:
                    button_1.onLeave(self)
                    is_on = button_2
                else:
                    button_2.onLeave(self)
                    is_on = button_1

            elif command == "Return":
                # When Enter, change current button to select state.
                is_on.onSelect(self)
                # Pause for a split second for the effect.
                time.sleep(0.1)
                # Return the button
                if is_on == button_1:
                    self.clearScreen()
                    return b1_name.title()
                else:
                    self.clearScreen()
                    return b2_name.title()
                break
        return b2_name.title()

    def readScores(self):
        """Read and return a list of scores in the highscore text file."""
        entries = []
        with open("doc/highscores.txt", "r") as file:
            for line in file:
                try:
                    name, score = line.split("-")
                    entries.append([name, int(score)])
                except (ValueError):
                    pass
        return entries
