from graphics import Image


class Button():
    """A class to create buttons for the game."""

    def __init__(self, position, icon_file):
        self.normal = Image(position, "img/b_normal.png")
        self.highlight = Image(position, "img/b_highlight.png")
        self.select = Image(position, "img/b_select.png")

        self.sprite = self.normal
        self.icon = Image(position, icon_file)

    def draw(self, win):
        """Draw button onto a GraphWin object."""
        self.sprite.draw(win)
        self.icon.undraw()
        self.icon.draw(win)
        win.update()

    def onHighlight(self, win):
        """Mimic the behavior of a normal button when mouse hovered over it."""
        self.sprite.undraw()
        self.sprite = self.highlight
        self.draw(win)

    def onLeave(self, win):
        """A button at "normal" state (no highlight or select)."""
        self.sprite.undraw()
        self.sprite = self.normal
        self.draw(win)

    def onSelect(self, win):
        """When the button is pressed."""
        self.sprite.undraw()
        self.sprite = self.select
        self.draw(win)
