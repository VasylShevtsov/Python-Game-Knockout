"""
Author: Vasyl "Basil" Shevtsov
Date: 08/13/2022
Assignment: Final Project
Purpose: Play a game of knockout.

Citations and acknowledgments:
* Idea and gameplay rules from the iMessage GamePigeon game of Knockout developed by Vitalii Zlotskii.
* Suggestions on programming approaches and ideas for the game from Professor Janet Davis
* Feedback on gameplay ideas from Grant Didway
* sleep() function https://www.programiz.com/python-programming/time/sleep
* random.sample() function https://stackoverflow.com/questions/3998908/how-do-i-perform-a-random-event-in-python-by-picking-a-random-variable
* combinations function https://www.geeksforgeeks.org/python-all-possible-pairs-in-list/
* any() function https://www.geeksforgeeks.org/python-check-if-any-element-in-list-satisfies-a-condition/ 
"""
from itertools import combinations
from graphics import *
import knockout_graphics as GameInterface
import time
import random

class Ball():
    """A circular ball gamepiece
    """
    def __init__(self, x, y, win, color = False, radius = 10):
        """Create a ball

        Args:
            x (int): x coordinate on the screen
            y (int): y coordinate on the screen
            win (GraphWin): Graphics window to move ball on
            color (bool, optional): Color of the ball. Defaults to False.
            radius (int, optional): Radius of the ball. Defaults to 10.
        """
        self.win = win
        self.alive = True
        self.x = x
        self.y = y
        self.launchRadius = 200 #maximum strength of a launch
        self.coord = Point(x,y)
        self.direction = 0
        self.xVel = 0
        self.yVel = 0
        self.alive = True
        self.radius = radius
        self.ball = GameInterface.BallDrawing(self.x, self.y, self.win, radius, color)
        self.moving = False
        self.color = color

        #game physics constants
        self.fricConst = 0.8
        self.fricCoeff = 4
        self.velCoeff = 2.2
        self.velBase = 1.013
        self.tolerance = 0.3
        self.probabilityCoeff = 4

    def updateLocation(self, newX, newY):
        """Moves the ball on the screen

        Args:
            newX (int): New x coordinate to move to
            newY (int): New y coordinate to move to
        """
        self.x = newX
        self.y = newY
        self.ball.moveDrawing(self.x, self.y)

    def chooseLocation(self):
        """Lets the user click on the screen to choose a launch direction and velocity

        Returns:
            None: leaves the method if the ball is dead
        """
        if not self.alive:
            return None
        self.ball.cicrle.setFill("orange") #show the user which ball they are launching
        self.click = self.win.getMouse()

        self.xVel = self.click.getX() - self.x #launch velocity is the dx and dy between current pos and click
        self.yVel = self.click.getY() - self.y

        self.launchLimit() #maximum launch velocity cutoff

        self.xVel /= self.velCoeff # scale down the initial velocity
        self.yVel /= self.velCoeff

        self.moving = True
        self.ball.cicrle.setFill(self.color)

    def botLocation(self, ball):
        """Automatic velocity assignment for computer player balls.

        Args:
            ball (Ball): The ball to aim at

        Returns:
            None: Aborts the method if the computer ball is dead
        """
        if not self.alive:
            return None

        self.xVel = (ball.x - self.x) * random.uniform(1, 2) #add random aiming error
        self.yVel = (ball.y - self.y) * random.uniform(1, 2)
        self.launchLimit()
        self.xVel /= self.probabilityCoeff # scale down the initial velocity
        self.yVel /= self.probabilityCoeff

        self.moving = True
        
    def launchLimit(self):
        """Sets the launch velocity to a given maximum if it exceeds it.
        """
        
        distFromCenter = (self.xVel ** 2 + self.yVel ** 2) ** (1/2)

        if distFromCenter > self.launchRadius:
            slope = self.yVel / self.xVel

            # use equations for a circle and the eqation for a straight line
            # to solve for the intersection of the two functions
            # to correctly solve for the x and y velocities that intersect the
            # maximum launch radius
            if self.xVel > 0:
                newxVel = self.launchRadius / (((slope ** 2) + 1)**0.5)
            if self.xVel < 0:
                newxVel = -(self.launchRadius / (((slope ** 2) + 1)**0.5))
            
            newyVel = slope * newxVel

            self.yVel = newyVel
            self.xVel = newxVel

    def knockout(self):
        """Set the ball object as dead and not moving and hide it
        """
        self.alive = False
        self.moving = False
        self.ball.hide()
        print("knockout!")

    def launchBall(self):
        """One step to incrementally move the ball a certain amount based on the given game physics constants
        """
        # Tested at a maximum launch radius of 200
        # Personally I found the values to work good at: 
        # Friction Constant = 0.8, Friction Coefficient = 4, Velocity Coefficient = 2.2, Velocity Base = 1.013, Miniscule Movement Tolerance: 0.3
        # The fricConst helps the object slide a little further when the input is a very short distance.
        # The fricCoeff helps with extending the slowdown to be more gradual, affects mostly mid-length launches.
        # The velCoeff divides the initial value to be smaller. Helps to lower the initial "kick"
        # The velBase works well for slowing down objects at far distances, and has less effect on close distances.
        # The tolerance allows the balls to stop moving once they reach a slow enough speed.


        if (self.xVel > self.tolerance or self.xVel < -self.tolerance\
             or self.yVel > self.tolerance or self.yVel < -self.tolerance) \
                and self.alive:

            self.updateLocation(self.x + (self.xVel / self.fricCoeff), \
                self.y + (self.yVel / self.fricCoeff))

            #check if the ball got knocked out:
            if self.x >= 700 or self.y >= 700 or self.x <= 0 or self.y <= 0:
                self.knockout()

            #horizontal motion
            if self.xVel > self.tolerance or self.xVel < -self.tolerance:
                if self.xVel > 0:
                    self.xVel -= round((self.velBase ** (self.xVel)), 5)
                    self.xVel += self.fricConst
                else:
                    self.xVel += round((self.velBase ** (-self.xVel)), 5)
                    self.xVel -= self.fricConst

            #vertical motion
            if self.yVel > self.tolerance or self.yVel < -self.tolerance:
                if self.yVel > 0:
                    self.yVel -= round((self.velBase ** (self.yVel)), 5)
                    self.yVel += self.fricConst
                else:
                    self.yVel += round((self.velBase ** (-self.yVel)), 5)
                    self.yVel -= self.fricConst
        else:
            self.moving = False

    def collision(self, other):
        """Simulates a collision between two balls.

        Args:
            other (Ball): second ball to collide with
        """
        #we can just swap values because objects are of equal mass!
        #horizontal component
        vel1x = self.xVel
        vel2x = other.xVel
        self.xVel = vel2x
        other.xVel = vel1x

        #vertical component
        vel1y = self.yVel
        vel2y = other.yVel
        self.yVel = vel2y
        other.yVel = vel1y
    
class KnockoutGame:
    """This models the Knockout game functionality.
    """
    def __init__(self):
        """Create a knockout game
        """
        self.mode = True
        self.gameMode()
        if self.mode:
            print("\nPlayer 1, your pieces are purple.\nPlayer 2, your pieces are green.\nGood luck!\n")
            time.sleep(3)
        else:
            print("\nYour pieces are purple.\nYour computer opponet is green.\nGood luck!\n")
            time.sleep(3)

        self.interface = GameInterface.Interface()
        self.ball1 = Ball(176, 233, self.interface.win, "Purple")
        self.ball2 = Ball(351, 200, self.interface.win, "Purple")
        self.ball3 = Ball(526, 233, self.interface.win, "Purple")
        self.ball4 = Ball(175, 467, self.interface.win, "Green")
        self.ball5 = Ball(350, 500, self.interface.win, "Green")
        self.ball6 = Ball(525, 467, self.interface.win, "Green")

    def gameMode(self):
        """Ask the user whether they want a multiplayer or singleplayer game.
        """
        mode = ''
        print("\nYou're playing Knockout!")
        while True:
            mode = input("Multiplayer (m) or Single-Player? (s) ")
            if mode == "m":
                self.mode = True
                break
            if mode == "s":
                self.mode = False
                break
            print('Please enter either "m" or "s" ')

    def playTurnMultiplayer(self):
        """Simulates one turn of a multiplayer game until all objects are still or the game ends.
        """
        lst = [self.ball1, self.ball2, self.ball3, self.ball4, self.ball5, self.ball6]
        for item in lst:
            item.chooseLocation()

        while any(ball.moving for ball in lst):
            
            #move every ball
            for item in lst:
                item.launchBall()

            #check whether each pair of balls has collided at all
            
            pairs = list(combinations(lst, 2))
            for pair in pairs:
                self.collisionBehavior(pair[0], pair[1])

    def playTurnSingleplayer(self):
        """Simulates one turn of a singleplayer game until all objects are still or the game ends.
        """
        lst = [self.ball1, self.ball2, self.ball3, self.ball4, self.ball5, self.ball6]

        playerBalls = [self.ball1, self.ball2, self.ball3]
        botBalls = [self.ball4, self.ball5, self.ball6]

        for ball in playerBalls: #make a list of player balls that are alive
            if not ball.alive:
                playerBalls.remove(ball)
        
        for ball in playerBalls:
            ball.chooseLocation()
    
        for ball in botBalls: #computer randomly chooses an active player ball to aim at
            ball.botLocation(random.choice(playerBalls))


        while any(ball.moving for ball in lst):
            
            #move every ball
            for ball in lst:
                ball.launchBall()

            #check whether each pair of balls has collided at all

            pairs = list(combinations(lst, 2))
            for pair in pairs:
                self.collisionBehavior(pair[0], pair[1])

    def proximity(self, ball1, ball2):
        """Checks whether the balls are are overlapping/colliding

        Args:
            ball1 (Ball): First ball to compare
            ball2 (Ball): Second ball to compare

        Returns:
            Bool: True if overlapping, False if not
        """
        distance = ((ball2.x - ball1.x)**2 + (ball2.y - ball1.y)**2)**0.5
        if distance < ball1.radius * 2:
            return True
        return False

    def collisionBehavior(self, ball1, ball2):
        """Consolidates the collision physics into one function that checks for a collision and adjusts if necessary

        Args:
            ball1 (Ball): First ball to compare
            ball2 (Ball): Second ball to compare
        """
        if self.proximity(ball1, ball2) and ball1.alive and ball2.alive:
                ball1.collision(ball2)
                ball1.launchBall()
                ball2.launchBall()

                # if the balls don't have enough velocity to escape each
                # other's hitboxes we give them a small nudge
                if self.proximity(ball1, ball2):
                    ball1.xVel *= 2
                    ball2.yVel *= 2

    def gameplay(self):
        """This is the method that plays the game
        """
        if self.mode:
            while (self.ball1.alive or self.ball2.alive or self.ball3.alive) and \
                (self.ball4.alive or self.ball5.alive or self.ball6.alive):
                self.playTurnMultiplayer()
            if (self.ball1.alive or self.ball2.alive or self.ball3.alive):
                print("\nPlayer 1 wins!")
            elif (self.ball4.alive or self.ball5.alive or self.ball6.alive):
                print("\nPlayer 2 wins!")
            else:
                print("\nIts a tie!")
        else:
            while (self.ball1.alive or self.ball2.alive or self.ball3.alive) and \
                (self.ball4.alive or self.ball5.alive or self.ball6.alive):
                self.playTurnSingleplayer()
            if (self.ball1.alive or self.ball2.alive or self.ball3.alive):
                print("\nYou won!")
            elif (self.ball4.alive or self.ball5.alive or self.ball6.alive):
                print("\nThe compter won!")
            else:
                print("\nIts a tie!")

        self.interface.close()
        
def main():
    game = KnockoutGame()
    game.gameplay()

if __name__ == '__main__':
    main()