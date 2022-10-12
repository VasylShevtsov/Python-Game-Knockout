"""
Author: Vasyl "Basil" Shevtsov
Date: 08/13/2022
Assignment: Final Project
Purpose: Model the graphics for the game of Knockout

Citations and acknowledgments:
* Graphics module and documentation by John Zelle
* Idea and gameplay rules from the iMessage GamePigeon game of Knockout developed by Vitalii Zlotskii.
* Suggestions on programming approaches and ideas for the game from Professor Janet Davis
* Feedback on gameplay ideas from Grant Didway
"""

import graphics
from graphics import Point

class BallDrawing:
    """A drawing of a ball"""

    def __init__(self, x, y, win, radius = 10, color = False):
        """Create the ball drawing

        Args:
            x (int): x coordinate location
            y (int): y coordinate location
            win (GraphWin): graphics window to draw in
            radius (int, optional): Radius of the ball. Defaults to 10.
            color (bool or str, optional): Fill color of the ball as a string. Defaults to False.
        """
        self.win = win
        self.x = x
        self.y = y
        self.drawn = True
        self.cicrle = graphics.Circle(Point(x,y), radius)
        if color != False:
            self.cicrle.setFill(color)
        self.cicrle.draw(self.win)

    def moveDrawing(self, newX, newY):
        """Moves the drawing of the ball to a new location

        Args:
            newX (int): the new x coordinate
            newY (int): the new y coordinate
        """
        dx = newX - self.x
        dy = newY - self.y
        self.cicrle.move(dx,dy)
        self.x = newX
        self.y = newY

    def hide(self):
        """Undraws the circle
        """
        self.cicrle.undraw()
        self.drawn = False

class Interface:
    """Graphics interface for the Knockout game.
    """
    def __init__(self):
        """Create a graphis window
        """
        self.win = graphics.GraphWin("Knockout!", 700, 700)
        self.win.setBackground("Dark Blue")
        self.win.setCoords(-50,-50,750,750)
        self.iceberg()

    def iceberg(self):
        """Draws an iceberg for the balls to slide on
        """
        ice = graphics.Rectangle(Point(0,0), Point(700,700))
        ice.setFill("White")
        ice.draw(self.win)

    def close(self):
        """Waits for a user click before closing the screen
        """
        self.win.getMouse()
        self.win.close()
    