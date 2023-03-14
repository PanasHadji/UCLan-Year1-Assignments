# Arkanoid.py
# Author: Panagiotis Hadjidemetriou (G20965620)
# Email: PHadjidemetriou1@uclan.ac.uk
# Description: The Arkanoid.py program demonstrates an arcade game from the 1980's.
# The player controls a rectangular craft at the bottom of the screen, moving it left and right,
# to deflect a ball and eliminate a number of bricks by hitting them with the ball. If the player
# wins when all the bricks are destroyed and loses if the ball touches the bottom of the screen.
# *invalid command name "animation" while executing "animation" ("after" script)* appears after the
# player restarts the game, but it doesn't affect the program.


# Importing the tkinter and random libraries
from tkinter import *
from random import randint

# Declaring and assigning some constant variables and arrays
WIDTH = 800
HEIGHT = 600
DELAY = 20

DEFAULT_SPEED = 4
DEFAULT_BALL_RADIUS = 10
DEFAULT_COLORS = ['red', 'green', 'blue', 'yellow', 'cyan', '']

x = WIDTH / 2
x2 = WIDTH / 2
y = HEIGHT / 2

# Creating the games window
win = Tk()
win.title('Arkanoid Game')

canvas = Canvas(win, width=WIDTH, height=HEIGHT, bg='black')
canvas.pack()


# Creating a 'Ball' class that collects given data and creates,moves,draws and removes the balls
# in the game. (The code is reused from BallAsClass.py provided under Week03, step0304)
class Ball:

    # A function that collects given data and assigns it to a specific characteristic of the ball that we want to create
    def __init__(self, ball_x, ball_y, speed_x, speed_y, radius, color, outline):
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.color = color
        self.outline = outline
        self.canvas_object = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=self.color,
                                                outline=self.outline)

    # A function that moves the ball and changes its speed if it collides with the windows borders
    def move_ball(self):
        self.ball_x = self.ball_x + self.speed_x  # Updates the balls X

        if self.ball_x >= WIDTH - self.radius:
            self.speed_x = -abs(self.speed_x)  # If the ball touches the left or right border of the
        if self.ball_x <= self.radius:  # window its speed on the X axis inverts
            self.speed_x = abs(self.speed_x)

        self.ball_y = self.ball_y + self.speed_y  # Updates the balls Y

        if self.ball_y >= HEIGHT - self.radius:
            self.speed_y = 0  # If the ball touches the bottom of the screen its speed on the Y axis
            self.speed_x = 1  # becomes zero and the speed on the Y axis becomes 1. If it touches the
        if self.ball_y <= self.radius:  # top of the screen its speed on the Y axis inverts
            self.speed_y = abs(self.speed_y)

    # A function that draws the ball using the collected data
    def draw_ball(self):
        canvas.coords(self.canvas_object, self.ball_x - self.radius, self.ball_y - self.radius,
                      self.ball_x + self.radius,
                      self.ball_y + self.radius)

    # A function that deletes the balls from the window
    def remove(self):
        canvas.delete(self.canvas_object)


# Creating a 'Craft' class that collects given data and creates, draws and removes the bottom
# rectangle that the player moves (Code inspired from BallAsClass.py provided under Week03, step0304)
class Craft:

    # A function that collects given data and assigns it to a specific characteristic of the players' rectangle that we want to create
    def __init__(self, rect_x, rect_y, width, height, color, outline):
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.width = width
        self.height = height
        self.color = color
        self.outline = outline
        self.canvas_object = canvas.create_rectangle(x - width, y - height, x + width, y + height, fill=self.color,
                                                     outline=self.outline)

    # A function that draws the players' rectangle using the collected data
    def draw_rect(self):
        canvas.coords(self.canvas_object, self.rect_x - self.width, self.rect_y - self.height,
                      self.rect_x + self.width,
                      self.rect_y + self.height)

    # A function that deletes the players' rectangle from the window
    def remove(self):
        canvas.delete(self.canvas_object)


# Creating a 'Brick' class that collects given data and creates, draws and removes the top
# bricks that the player has to destroy (Code inspired from BallAsClass.py provided under Week03, step0304)
class Brick:

    # A function that collects given data and assigns it to a specific characteristic of the bricks that we want to create
    def __init__(self, brick_x, brick_y, brick_width, brick_height, color, outline):
        self.brick_x = brick_x
        self.brick_y = brick_y
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.color = color
        self.outline = outline
        self.canvas_object = canvas.create_rectangle(x - brick_width, y - brick_height, x + brick_width,
                                                     y + brick_height, fill=self.color,
                                                     outline=self.outline)

    # A function that draws the bricks using the collected data
    def draw_bricks(self):
        canvas.coords(self.canvas_object, self.brick_x - self.brick_width, self.brick_y - self.brick_height,
                      self.brick_x + self.brick_width,
                      self.brick_y + self.brick_height)

    # A function that deletes the bricks from the window
    def remove(self):
        canvas.delete(self.canvas_object)


# Creating a 'Score' class that collects given data and creates, draws and removes a text
# that we want to display in the game (Code inspired from BallAsClass.py provided under Week03, step0304)
class Score:

    #  A function that collects given data and assigns it to a specific characteristic of the text that we want to display
    def __init__(self, text_x, text_y, points, text_font, color):
        self.text_x = text_x
        self.text_y = text_y
        self.points = points
        self.text_font = text_font
        self.color = color
        self.canvas_text = canvas.create_text(self.text_x, self.text_y)

    # A function that displays the text using the collected data
    def draw_score(self):
        canvas.itemconfig(self.canvas_text, text=self.points, font=self.text_font,
                          fill=self.color)

    # A function that deletes the text from the window
    def remove(self):
        canvas.delete(self.canvas_text)


# Declaring an array and creating a 'Ball' type object (bg_ball) that we use in the next function
bg_balls = []
bg_ball = Ball(randint(0, WIDTH), 0, 0, randint(1, 10), randint(0, 1), '', '')


# A function that uses the 'Ball' object and creates 30 balls storing them in the bg_balls array
# (Code is reused from TwoBalls.py provided under Week03, step0305)
def background():
    global bg_ball  # Makes bg_ball a global variable to use it from outside the function

    for i in range(0, 30):  # The X, Y speed and radius of the balls are randomizes
        bg_ball = Ball(randint(0, WIDTH), 0, 0, randint(1, 10), randint(1, 3), 'white', '')
        bg_balls.append(bg_ball)


# Declaring and assigning variables and arrays that we use in the next function
rectangle_width = 50
rectangle_height = 7

drawn_rectangles = []
drawn_cubes = []
MAX_SIZE = 1

# Declaring and creating a 'Craft' type object (first) and drawing it in the window
first = Craft(x, HEIGHT - rectangle_height, rectangle_width, rectangle_height, DEFAULT_COLORS[4], 'white')
first.draw_rect()


# A function repeatedly draws and removes 'Craft' type objects giving the illusion that the players' rectangle is moving
# (Code inspired from MoreMouseInputWithLists.py provided under Week02, step0204)
def delete_prev_craft():
    # Declaring and creating a 'Craft' type object (new_rectangle), drawing it and storing it in the
    # drawn_rectangles array
    new_rectangle = Craft(x, HEIGHT - rectangle_height, rectangle_width, rectangle_height, DEFAULT_COLORS[4],
                          outline='black')
    new_rectangle.draw_rect()

    drawn_rectangles.append(new_rectangle)

    # If the length of the (drawn_rectangles) array is bigger than 1, a new object (prev_rectangle) is declared and
    # assigned to the first object of the array that got removed. Then it deletes the new object
    if len(drawn_rectangles) > MAX_SIZE:
        prev_rectangle = drawn_rectangles.pop(0)
        Craft.remove(prev_rectangle)


# Creating 5 'Craft' type objects that we use in the next function
cube1 = Craft(x, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
cube2 = Craft(x - 20, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
cube3 = Craft(x - 40, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
cube4 = Craft(x + 20, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
cube5 = Craft(x + 40, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')


# A function that draws and removes the previous (invisible) objects inside the players' rectangle
# so that we can use them later for the rectangle-ball collision
# (Code inspired from MoreMouseInputWithLists.py provided under Week02, step0204)
def delete_prev_cube():
    global cube1, cube2, cube3, cube4, cube5

    # Takes the 5 objects above and creates them again inside the function
    cube1 = Craft(x, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
    cube2 = Craft(x - 20, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
    cube3 = Craft(x - 40, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
    cube4 = Craft(x + 20, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
    cube5 = Craft(x + 40, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')

    # draws the 5 objects and stores them inside the drawn_cubes array
    cube1.draw_rect()
    cube2.draw_rect()
    cube3.draw_rect()
    cube4.draw_rect()
    cube5.draw_rect()

    drawn_cubes.append(cube1)
    drawn_cubes.append(cube2)
    drawn_cubes.append(cube3)
    drawn_cubes.append(cube4)
    drawn_cubes.append(cube5)

    # If the length of the (drawn_cubes) array is bigger than 5, then we create 5 new objects that get assigned to the
    # 5 first components of the array that got removed starting from the fifth and ending to the first
    if len(drawn_cubes) > 5:
        prev_cube1 = drawn_cubes.pop(4)
        prev_cube2 = drawn_cubes.pop(3)
        prev_cube3 = drawn_cubes.pop(2)
        prev_cube4 = drawn_cubes.pop(1)
        prev_cube5 = drawn_cubes.pop(0)

        Craft.remove(prev_cube1)
        Craft.remove(prev_cube2)
        Craft.remove(prev_cube3)
        Craft.remove(prev_cube4)
        Craft.remove(prev_cube5)


# An event function that repeatedly assigns the mouses' X position to the players' rectangle and
# the 5 cubes inside it X positions, while using the two functions above to display the moving
# players' rectangle (Code inspired from MouseInput.py provided in week02, step0203)
def craft_movement(event):
    global x  # Assigns the mouses' X position to the events X and uses 'global' to change the 'x'
    mouse_x = event.x  # variable used for the rectangle and cube coordinates

    if mouse_x <= 50:  # If the mouses X position is smaller or equal to 50 then x equals to 50
        x = 50  # and the two function from above get called to draw the objects

        delete_prev_craft()
        delete_prev_cube()
    elif mouse_x >= 750:  # If the mouses X position is larger or equal to 750 then x equals to 750
        x = 750  # and the two function from above get called to draw the objects

        delete_prev_craft()
        delete_prev_cube()
    else:  # Else, the object (first) gets deleted of the screen, the mouses' X position
        first.remove()  # equals to the events x, x equals to the mouses x position
        mouse_x = event.x  # and the two function from above get called to draw the objects
        x = mouse_x

        delete_prev_craft()
        delete_prev_cube()


# Declaring a (trail_balls2) array and a constant that we use in the next function
trail_balls = []
MAX_TRAIL = 10


# A function that creates 10 smaller balls behind our main balls to make it look like the balls are
# leaving a trail behind them.
# (Code inspired from MoreMouseInputWithLists.py provided under Week02, step0204
#  and AnimationOverXandY.py provided in Week03, step0302)
def ball_trail(ball_object):
    global MAX_TRAIL  # Using 'global' to access (MAX_TRAIL) from outside the function

    new_ball = Ball(x2, y, 0, DEFAULT_SPEED, 2,  # Creating a 'Ball' type object
                    '', 'gray')
    if ball_object.speed_x > 0:  # If the balls X speed is bigger than 0, then new_balls X position equals to the balls X position minus its radius
        new_ball.ball_x = ball_object.ball_x - ball_object.radius
    if ball_object.speed_x < 0:  # If the balls X speed is smaller than 0, then new_balls X position equals to the balls X position plus its radius
        new_ball.ball_x = ball_object.ball_x + ball_object.radius
    if ball_object.speed_x == 0:  # If the balls X speed equals to 0, then
        if ball_object.speed_y > 0:  # If the ball_objects' Y speed is bigger than 0, then new_balls X position equals to the balls X position
            new_ball.ball_x = ball_object.ball_x  # and Y position equals to the balls Y position minus its radius
            new_ball.ball_y = ball_object.ball_y - ball_object.radius
        if ball_object.speed_y < 0:  # If the ball_objects' Y speed is smaller than 0, then new_balls X position equals to the balls X position
            new_ball.ball_x = ball_object.ball_x  # and Y position equals to the balls Y position plus its radius
            new_ball.ball_y = ball_object.ball_y + ball_object.radius
    elif ball_object.speed_y == 0:  # If the ball_objects' Y speed equals to 0, then new_balls X position equals to the balls X position
        new_ball.ball_x = ball_object.ball_x
    else:  # Else,
        if ball_object.speed_y > 0:  # If the ball_objects' Y speed is bigger than 0, then new_balls Y position equals to the balls Y position minus its radius
            new_ball.ball_y = ball_object.ball_y - ball_object.radius
        if ball_object.speed_y < 0:  # If the ball_objects' Y speed is smaller than 0, then new_balls Y position equals to the balls Y position plus its radius
            new_ball.ball_y = ball_object.ball_y + ball_object.radius

    new_ball.draw_ball()
    # Draws (new_ball) and stores it inside the (trail_balls) array
    trail_balls.append(new_ball)

    # If the length of the (trail_balls) array is bigger than (MAX_TRAIL), a new object (prev_trail) is declared and
    # assigned to the first object of the array that got removed. Then it deletes the new object
    if len(trail_balls) > MAX_TRAIL:
        prev_trail = trail_balls.pop(0)
        Craft.remove(prev_trail)


# Creating different 'Score' type objects that we will use as the text that gets displayed in different times during the game
score = Score(50, 570, 0, ('Arial Bold', 16), 'white')
final_score = Score(x, y + 50, 'Final score: ' + str(score.points), ('Arial Bold', 16), 'gray')
lost = Score(x, y, 'YOU LOST!!', ('Arial Bold', 40), 'gray')
won = Score(x, y, 'YOU WIN!!', ('Arial Bold', 40), 'gray')

welcome = Score(x, y - 100, 'Welcome to the Arkanoid Game', ('Arial Bold', 35), 'gray')
level1 = Score(200, y, 'Press "1" for level 1', ('Arial Bold', 24), 'gray')
level2 = Score(200, y + 50, 'Press "2" for level 2', ('Arial Bold', 24), 'gray')
other = Score(313, y + 100, 'Press "R" to restart and "X" to quit', ('Arial Bold', 24), 'gray')
restart = Score(x, y + 100, 'Press "R" to restart or "X" to quit', ('Arial Bold', 16), 'gray')
if_restarted = Score(350, y + 150, '*If you restarted the game please tap on the game screen before choosing a level*',
                     ('Arial Bold', 12),
                     'gray')

# Creating the same objects as the once above but with randomized color and a 2 pixel offset to create a
# 3D illusion and add aesthetics to tha game
final_score_fk = Score(x + 2, y + 52, 'Final score: ' + str(score.points), ('Arial Bold', 16),
                       DEFAULT_COLORS[randint(0, 4)])
lost_fk = Score(x + 2, y + 2, 'YOU LOST!!', ('Arial Bold', 40), DEFAULT_COLORS[randint(0, 4)])
won_fk = Score(x + 2, y + 2, 'YOU WIN!!', ('Arial Bold', 40), DEFAULT_COLORS[randint(0, 4)])

welcome_fk = Score(x + 2, y - 98, 'Welcome to the Arkanoid Game', ('Arial Bold', 35), DEFAULT_COLORS[randint(0, 4)])
level1_fk = Score(202, y + 2, 'Press "1" for level 1', ('Arial Bold', 24), DEFAULT_COLORS[randint(0, 4)])
level2_fk = Score(202, y + 52, 'Press "2" for level 2', ('Arial Bold', 24), DEFAULT_COLORS[randint(0, 4)])
other_fk = Score(315, y + 102, 'Press "R" to restart and "X" to quit', ('Arial Bold', 24),
                 DEFAULT_COLORS[randint(0, 4)])
restart_fk = Score(x + 2, y + 102, 'Press "R" to restart or "X" to quit', ('Arial Bold', 16),
                   DEFAULT_COLORS[randint(0, 4)])
if_restarted_fk = Score(352, y + 152,
                        '*If you restarted the game please tap on the game screen before choosing a level*',
                        ('Arial Bold', 12),
                        'white')

# Creating two 'Ball' type objects (ball), (ball2) that we will use as our balls in the game
ball = Ball(x2 + 20, y, 0, DEFAULT_SPEED, DEFAULT_BALL_RADIUS,
            DEFAULT_COLORS[0], 'yellow')

ball2 = Ball(x2 - 20, y, 0, DEFAULT_SPEED - 2, DEFAULT_BALL_RADIUS,
             DEFAULT_COLORS[2], 'cyan')

# Declaring and assigning variables and an array that we will use in the next function
br_width = 19
br_height = 10
x_space = 22
y_space = 10

bricks = []


# A function that uses the pythagorean thorium to measure the distance between two objects (in this case ball and brick)
# and if the distance is smaller or equal to the balls radius plus the bricks' height then it returns as (True)
# (Code inspired by the solutions of Exercise0301.md and Exercise0302.md provided under Week03, xtras)
def collision_with_brick(ob1, ob2):
    dx = int((ob2.brick_x - ob1.ball_x) ** 2)
    dy = int((ob2.brick_y - ob1.ball_y) ** 2)
    distance = int((dx + dy) ** 0.5)

    if distance <= ob1.radius + ob2.brick_height + 5:
        hit = True
        return hit


# A function that uses the pythagorean thorium to measure the distance between two objects (in this case ball and players' rectangle)
# and if the distance is smaller or equal to the balls radius plus the rectangles' width minus 2 then it returns as (True)
# (Code inspired by the solutions of Exercise0301.md and Exercise0302.md provided under Week03, xtras)
def collision_with_cube(ob1, ob2):
    dx = int((ob2.rect_x - ob1.ball_x) ** 2)
    dy = int((ob2.rect_y - ob1.ball_y) ** 2)
    distance = int((dx + dy) ** 0.5)

    if distance <= ob1.radius + ob2.width - 2:
        hit = True
        return hit


# A function that draws 5 rows of 20 'Brick' type objects with every line a different color
# (Code inspired from NestedLoops.py provided under Week01, step0106)
def draw_bricks():
    global x_space, y_space  # Using 'global' to access two variables (x_space, y_space) from outside the function

    if len(bricks) >= 100:  # If the length of the (bricks) array is bigger or equal to 100 then the function stops executing
        return
    else:  # Else, it draws 5 rows of 20 bricks using a for loop and a nested for loop
        for i in range(0, 5):
            for j in range(0, 20):
                brick = Brick(x_space, y_space, br_width, br_height,
                              DEFAULT_COLORS[i], 'gray')

                brick.draw_bricks()  # A 'Brick' type object gets created, drawn and stored in the (bricks) array
                bricks.append(brick)
                x_space += 40  # Every loop the value of (x_space) increases by 40

            x_space = 22  # Every loop the value of (x_space) becomes 22 again and
            y_space += 24  # the value of (y_space) increases by 24


# An event function that according to the key pressed by the player, returns a variable to use it in the flow of the game
# (Code reused from MoreKeyboardInput.py provided under Week02, step0202)
def on_key_press(event):
    global case, select  # Using 'global' to access the (case) variable from outside the function
    if event.char == 'r' or event.char == 'R':
        case = 3  # If the player pressed 'r' on the keyboard it returns the value of (case) as 3
        return case
    if event.char == '1' and select:
        case = 1  # If the player pressed '1' on the keyboard it returns the value of (case) as 1
        return case
    if event.char == '2' and select:
        case = 2  # If the player pressed '2' on the keyboard it returns the value of (case) as 2
        return case
    if event.char == 'x' or event.char == 'X':
        quit()  # If the player pressed 'x' on the keyboard it ends the program


# Declaring and assigning variables that we will use in functions for the games flow
case = 0
select = True
won_or_lost = True


# A function that is responsible for everything that gets constantly updated in level 1 while the game is running.
# These things are: drawing and removing objects, ball physics, collisions and text display.
# (Code inspired from AnimationOverXandY.py provided under Week03, step0302)
def animation():
    global ball, ball2, cube1, cube2, cube3, cube4, cube5, bg_ball, won_or_lost, case, MAX_TRAIL, DEFAULT_COLORS
    # Using 'global' to access objects and variables from outside the function

    ball.draw_ball()
    ball.move_ball()
    ball_trail(ball)  # (ball) is drawn and is moving with a trail
    if case == 2:  # if the value of (case) is equal to 2, 'level 2'
        ball2.draw_ball()  # (ball2) is drawn and is moving with a trail
        ball2.move_ball()
        ball_trail(ball2)
        MAX_TRAIL = 20
        DEFAULT_COLORS = ['red', 'hot pink', 'orange', 'SeaGreen2', 'cyan', '']
    else:  # Else, (ball2) gets removed, 'level 1'
        ball2.remove()

    draw_bricks()  # The bricks and score are drawn
    score.draw_score()

    # For loop that loops through all the components of the (bricks) array to constantly check for collisions
    for array_num in range(0, len(bricks)):
        if collision_with_brick(ball, bricks[array_num]):  # If there is a collision between the ball and a brick, then
            if ball.ball_x <= bricks[array_num].brick_x - bricks[array_num].brick_width:
                ball.speed_x = -ball.speed_x  # If the balls X position is smaller and equal to the bricks' X position minus its width
                # the balls X speed inverts
            elif ball.ball_x > bricks[array_num].brick_x + bricks[array_num].brick_width:
                ball.speed_x = -ball.speed_x  # If the balls X position is bigger than the bricks' X position plus its width
                # the balls X speed inverts
            else:
                ball.speed_y = -ball.speed_y  # Else, the balls y speed inverts

            bricks[array_num].remove()  # The brick that the ball collided with gets deleted of the window
            bricks[array_num].brick_x = 1000  # and its X position is set to '1000' to avoid invisible collisions
            score.points += 10  # The value of the score gets increased by 10 and the value of the objects (final_score)
            final_score.points = 'Final score: ' + str(score.points)  # and (final_score_fk) are equal to the score
            final_score_fk.points = 'Final score: ' + str(score.points)

    if collision_with_cube(ball, cube1):  # If the ball collides with (cube1) is X speed becomes 0 and Y speed -10
        ball.speed_x = 0
        ball.speed_y = -10
    if collision_with_cube(ball,
                           cube2):  # If the ball collides with (cube2) is X speed becomes a random integer between -7 and -3, and Y speed -10
        ball.speed_x = randint(-7, -3)
        ball.speed_y = -10
    if collision_with_cube(ball,
                           cube3):  # If the ball collides with (cube3) is X speed becomes a random integer between 3 and 7, and Y speed -10
        ball.speed_x = -10
        ball.speed_y = -10
    if collision_with_cube(ball, cube4):  # If the ball collides with (cube4) is X speed becomes 0 and Y speed -10
        ball.speed_x = randint(3, 7)
        ball.speed_y = -10
    if collision_with_cube(ball, cube5):  # If the ball collides with (cube5) is X speed becomes 10 and Y speed -10
        ball.speed_x = +10
        ball.speed_y = -10

    # The next two blocks of code are exactly the same as the two above, but check the second balls collisions and physics in level 2
    if case == 2:
        for array_num2 in range(0, len(bricks)):
            if collision_with_brick(ball2, bricks[array_num2]):
                if ball2.ball_x <= bricks[array_num2].brick_x - bricks[array_num2].brick_width:
                    ball2.speed_x = -ball2.speed_x

                elif ball2.ball_x > bricks[array_num2].brick_x + bricks[array_num2].brick_width:
                    ball2.speed_x = -ball2.speed_x

                else:
                    ball2.speed_y = -ball2.speed_y

                bricks[array_num2].remove()
                bricks[array_num2].brick_x = 1000

                score.points += 10
                final_score.points = 'Final score: ' + str(score.points)
                final_score_fk.points = 'Final score: ' + str(score.points)

        for d in range(0, 1):
            if collision_with_cube(ball2, cube1):
                ball2.speed_x = 0
                ball2.speed_y = -10
            if collision_with_cube(ball2, cube2):
                ball2.speed_x = randint(-7, -3)
                ball2.speed_y = -10
            if collision_with_cube(ball2, cube3):
                ball2.speed_x = -10
                ball2.speed_y = -10
            if collision_with_cube(ball2, cube4):
                ball2.speed_x = randint(3, 7)
                ball2.speed_y = -10
            if collision_with_cube(ball2, cube5):
                ball2.speed_x = +10
                ball2.speed_y = -10

    if (ball.speed_y == 0 or ball2.speed_y == 0) and won_or_lost:
        ball.ball_x = 900
        ball2.ball_x = 900  # If one of the balls have X speed equal to 0 and (won_or_lost) is True
        lost.draw_score()  # then both balls X position is set to 900 and text gets displayed on the screen. The Player loses.
        final_score.draw_score()
        restart.draw_score()

        lost_fk.draw_score()
        final_score_fk.draw_score()
        restart_fk.draw_score()
        won_or_lost = False
    elif score.points == 1000 and won_or_lost:
        won.draw_score()
        final_score.draw_score()  # If the value of the score is equal to 1000 and (won_or_lost) is True
        restart.draw_score()  # then text gets displayed on the screen. The Player wins.

        won_fk.draw_score()
        final_score_fk.draw_score()
        restart_fk.draw_score()
        won_or_lost = False

    if len(bg_balls) < 29:  # If the length of the (bg_balls) array is smaller than 29 the (background) function gets executed
        background()

    for j in range(0, 30):  # For loop that draws and moves the 30 (bg_balls) that where created above,
        bg_balls[j].move_ball()
        bg_balls[
            j].draw_ball()  # and if the bg_balls touch the bottom of the screen, they appear at the top in a random position
        if bg_balls[j].ball_y >= 580:  # with a random Y speed
            bg_balls[j].ball_y = 10
            bg_balls[j].ball_x = randint(5, 795)
            bg_balls[j].speed_y = randint(1, 10)

    canvas.after(DELAY, animation)  # This sets the time that the function updates during runtime


# This is the main function that controls the switching from the menu to the levels and restarting/quiting the game
def check_game():
    global case, select, win, canvas, DELAY, welcome, level1, level2, \
        other, if_restarted, welcome_fk, level1_fk, level2_fk, other_fk, \
        if_restarted_fk  # Using 'global' to access variables and objects from outside the function

    if case == 0:
        welcome.draw_score()
        level1.draw_score()  # If (case) equals to 0 then text gets displayed on the window and waits for
        level2.draw_score()  # the user to click on a button. This is the main manu.
        other.draw_score()
        if_restarted.draw_score()

        welcome_fk.draw_score()
        level1_fk.draw_score()
        level2_fk.draw_score()
        other_fk.draw_score()
        if_restarted_fk.draw_score()

    if case > 0:
        welcome.remove()
        level1.remove()
        level2.remove()  # If (case) is larger than 0 everything from the main menu gets deleted
        other.remove()
        if_restarted.remove()

        welcome_fk.remove()
        level1_fk.remove()
        level2_fk.remove()
        other_fk.remove()
        if_restarted_fk.remove()

    if case == 1 and select:
        animation()  # If (case) equals to 1 and (select) is True
        select = False  # then the (animation) function gets executed and (select) equals to False

    if case == 2 and select:
        animation()  # If (case) equals to 2 and (select) is True
        select = False  # then the (animation2) function gets executed and (select) equals to False

    if case == 3:  # If (case) equals to 3 the window gets destroyed
        win.destroy()
        global WIDTH, HEIGHT, DEFAULT_COLORS, DEFAULT_SPEED, DEFAULT_BALL_RADIUS, x, \
            x2, y, rectangle_height, rectangle_width, drawn_rectangles, drawn_cubes, MAX_SIZE, \
            first, br_width, br_height, x_space, y_space, bricks, score, final_score, lost, won, won_fk, restart, \
            ball, ball2, cube1, cube2, cube3, cube4, cube5, bg_ball, bg_balls, final_score_fk, lost_fk, restart_fk, \
            won_or_lost  # Using 'global' to access variables and objects from outside the function

        # Everything that is outside a function is written again and was put in the global statement
        # so that when the window gets destroyed we have the code here. This is the restart process of the game.
        win = Tk()
        win.title('Arkanoid Game')

        canvas = Canvas(win, width=WIDTH, height=HEIGHT, bg='black')
        canvas.pack()

        WIDTH = 800
        HEIGHT = 600
        DELAY = 20

        DEFAULT_SPEED = 4
        DEFAULT_BALL_RADIUS = 10
        DEFAULT_COLORS = ['red', 'green', 'blue', 'yellow', 'cyan', '']

        x = WIDTH / 2
        x2 = WIDTH / 2
        y = HEIGHT / 2

        rectangle_width = 50
        rectangle_height = 7

        drawn_rectangles = []
        drawn_cubes = []
        MAX_SIZE = 1

        bg_balls = []
        bg_ball = Ball(randint(0, WIDTH), 0, 0, randint(1, 10), randint(1, 2), '', '')

        first = Craft(x, HEIGHT - rectangle_height, rectangle_width, rectangle_height, DEFAULT_COLORS[4], 'white')
        first.draw_rect()

        cube1 = Craft(x, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
        cube2 = Craft(x - 20, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
        cube3 = Craft(x - 40, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
        cube4 = Craft(x + 20, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')
        cube5 = Craft(x + 40, HEIGHT - rectangle_height, rectangle_width / 5, rectangle_height, DEFAULT_COLORS[5], '')

        br_width = 19
        br_height = 10
        x_space = 22
        y_space = 10

        bricks = []

        score = Score(50, 570, 0, ('Arial Bold', 16), 'white')
        final_score = Score(x, y + 50, 'Final score: ' + str(score.points), ('Arial Bold', 16), 'gray')
        lost = Score(x, y, 'YOU LOST!!', ('Arial Bold', 40), 'gray')
        won = Score(x, y, 'YOU WIN!!', ('Arial Bold', 40), 'gray')

        welcome = Score(x, y - 100, 'Welcome to the Arkanoid Game', ('Arial Bold', 35), 'gray')
        level1 = Score(200, y, 'Press "1" for level 1', ('Arial Bold', 24), 'gray')
        level2 = Score(200, y + 50, 'Press "2" for level 2', ('Arial Bold', 24), 'gray')
        other = Score(313, y + 100, 'Press "R" to restart and "X" to quit', ('Arial Bold', 24), 'gray')
        restart = Score(x, y + 100, 'Press "R" to restart or "X" to quit', ('Arial Bold', 16), 'gray')
        if_restarted = Score(350, y + 150,
                             '*If you restarted the game please tap on the game screen before choosing a level*',
                             ('Arial Bold', 12),
                             'gray')
        final_score_fk = Score(x + 2, y + 52, 'Final score: ' + str(score.points), ('Arial Bold', 16),
                               DEFAULT_COLORS[randint(0, 4)])
        lost_fk = Score(x + 2, y + 2, 'YOU LOST!!', ('Arial Bold', 40), DEFAULT_COLORS[randint(0, 4)])
        won_fk = Score(x + 2, y + 2, 'YOU WIN!!', ('Arial Bold', 40), DEFAULT_COLORS[randint(0, 4)])

        welcome_fk = Score(x + 2, y - 98, 'Welcome to the Arkanoid Game', ('Arial Bold', 35),
                           DEFAULT_COLORS[randint(0, 4)])
        level1_fk = Score(202, y + 2, 'Press "1" for level 1', ('Arial Bold', 24), DEFAULT_COLORS[randint(0, 4)])
        level2_fk = Score(202, y + 52, 'Press "2" for level 2', ('Arial Bold', 24), DEFAULT_COLORS[randint(0, 4)])
        other_fk = Score(315, y + 102, 'Press "R" to restart and "X" to quit', ('Arial Bold', 24),
                         DEFAULT_COLORS[randint(0, 4)])
        restart_fk = Score(x + 2, y + 102, 'Press "R" to restart or "X" to quit', ('Arial Bold', 16),
                           DEFAULT_COLORS[randint(0, 4)])
        if_restarted_fk = Score(352, y + 152,
                                '*If you restarted the game please tap on the game screen before choosing a level*',
                                ('Arial Bold', 12),
                                'white')
        ball = Ball(x2 + 20, y, 0, DEFAULT_SPEED, DEFAULT_BALL_RADIUS,
                    DEFAULT_COLORS[0], 'yellow')
        ball2 = Ball(x2 - 20, y, 0, DEFAULT_SPEED - 2, DEFAULT_BALL_RADIUS,
                     DEFAULT_COLORS[2], 'cyan')
        win.bind('<Motion>', craft_movement)
        win.bind('<KeyPress>', on_key_press)

        case = 0  # (case) is set back to 0, (select) back to True and (won_or_lost) back to True
        select = True
        won_or_lost = True
        check_game()  # The (check_game) function gets executed

        win.mainloop()  # This is keeping the window open while the game is running
        return case, select  # Returns the variables (case) and (select)

    canvas.after(DELAY, check_game)  # This sets the time that the function updates during runtime


check_game()  # The (check_game) function gets executed
win.bind('<Motion>', craft_movement)  # The mouses motion gets bound with the (craft_movement) function
win.bind('<KeyPress>', on_key_press)  # Any key on the keyboard gets bound with the (on_key_press) function
win.mainloop()  # This is keeping the window open while the game is running
