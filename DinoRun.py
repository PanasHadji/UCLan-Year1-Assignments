# DinoRun.py
# Author: Panagiotis Hadjidemetriou (G20965620)
# Email: PHadjidemetriou1@uclan.ac.uk
# Description: The DinoRun.py program demonstrates the Chrome Dino game where the
# player guides a pixelated Tyrannosaurus rex across a side-scrolling landscape,
# avoiding obstacles to achieve a higher score. The player avoids obstacles by pressing
# the space bar to make the dinosaur jump. The game becomes faster with time and a bird obstacle
# is added. To collect more points the player can press the 'Down' arrow key when a bag of gold appears
# and the dinosaur is near it to collect the points.


# Importing the tkinter and random libraries
from tkinter import *
from random import randint

# Declaring and assigning some constant variables
WIDTH = 800
HEIGHT = 600
DELAY = 50
FRAME_COUNT = 4

# Creating the games window
win = Tk()
win.title('Moving background in loops')

canvas = Canvas(win, width=WIDTH, height=HEIGHT, bg='DarkOrange3')
canvas.pack()


# ============================================================================================#
# The functions below are responsible for objects other than the ones they're named after for simplicity and recycle of code


# Creating a 'Cactus' class that collects given data and creates,moves,draws the objects in the game.
# The (move_cac) function is specific for the cacti, (move) is for other objects and (move_sun_and_moon) is for the
# sun and the moon.
# (The code is inspired by BallAsClass.py provided under Week03, step0304)
class Cactus:

    # A function that collects given data and assigns it to a specific characteristic of the object that we want to create
    def __init__(self, cac_x, cac_y, speed_x, image, ):
        self.cac_x = cac_x
        self.cac_y = cac_y
        self.speed_x = speed_x
        self.image = image
        self.canvas_object = canvas.create_image(self.cac_x, self.cac_y, image=self.image)

    # A function that moves the cacti and resets their position every time they exit the window and randomises their picture
    def move_cac(self):
        self.cac_x = self.cac_x + self.speed_x  # updates the cactus' X

        if self.cac_x <= -50:  # If the cactus X is smaller than -50, then its X equals to WIDTH+100 and the image is changed randomly
            self.cac_x = WIDTH + 100
            self.canvas_object = canvas.create_image(self.cac_x, self.cac_y, image=cac_img_array[randint(0, 6)])

    # A function that draws the object using the collected data
    def draw_cac(self):
        canvas.coords(self.canvas_object, self.cac_x, self.cac_y)

    # A function that moves the object and resets their position every time they exit the window
    def move(self):
        self.cac_x = self.cac_x + self.speed_x  # updates the objects' X

        if self.cac_x <= -90:  # If the objects X is smaller than -50, then its X equals to WIDTH+100
            self.cac_x = WIDTH + 100

    # A function that moves the sun and moon creating the day/night cycle
    def move_sun_and_moon(self):
        if self.cac_x >= WIDTH / 2 and self.cac_y <= HEIGHT:  # If the X is bigger or equal to WIDTH/2 and Y is smaller or equal to HEIGHT then,
            self.cac_x -= 0.4  # X is constantly decreased by 0.4 and Y by 0.6
            self.cac_y -= 0.6
        if self.cac_x < WIDTH / 2 and self.cac_y <= HEIGHT:  # If the X is smaller than WIDTH/2 and Y is smaller or equal to HEIGHT then,
            self.cac_x -= 0.4  # X is constantly decreased by 0.4 and Y is increased by 0.6
            self.cac_y += 0.6
        if self.cac_x < WIDTH / 2 and self.cac_y > HEIGHT:  # If the X is smaller than WIDTH/2 and Y is bigger than HEIGHT then,
            self.cac_x += 0.4  # X is constantly increased by 0.4 and Y by 0.6
            self.cac_y += 0.6
        if self.cac_x >= WIDTH / 2 and self.cac_y > HEIGHT:  # If the X is bigger or equal to WIDTH/2 and Y is bigger than HEIGHT then,
            self.cac_x += 0.4  # X is constantly increased by 0.4 and Y is decreased by 0.6
            self.cac_y -= 0.6


# Creating a 'Bird' class that collects given data and creates,moves,draws the objects in the game.
# The (move) and (draw) functions are specific for the bird, (move2) and (draw2) functions are specific for the money bag
# (The code is inspired by BallAsClass.py provided under Week03, step0304)
class Bird:

    # A function that collects given data and assigns it to a specific characteristic of the object that we want to create
    def __init__(self, bird_x, bird_y, speed_x, image, ):
        self.bird_x = bird_x
        self.bird_y = bird_y
        self.speed_x = speed_x
        self.image = image
        self.canvas_object = canvas.create_image(self.bird_x, self.bird_y, image=self.image)

    # A function that moves the bird and resets its position every time it exit the window and randomises the chance of it appearing in the next cycle
    def move(self):
        self.bird_x = self.bird_x + self.speed_x  # updates the birds' X

        if self.bird_x <= -50:  # If the objects X is smaller than -50, then its X equals to WIDTH+100 and Y equals to 1000
            self.bird_x = WIDTH + 100
            self.bird_y = 1000
            bird_chance = randint(0, 2)  # random number between 0 and 2

            if bird_chance == 2:  # If the random number is equal to 2 the birds' Y equals to HEIGHT - 220
                self.bird_y = HEIGHT - 220

    # A function that draws the bird using the collected data, and animates it using frames
    def draw(self):
        canvas.coords(self.canvas_object, self.bird_x, self.bird_y)
        canvas.itemconfig(self.canvas_object, image=bird_frames[frame_index])

    # A function that moves the money bag and resets its position every time it exit the window
    def move2(self):
        self.bird_x = self.bird_x + self.speed_x  # updates the money bags' X

        if self.bird_x <= -100:  # If the objects X is smaller than -100, then its X equals to WIDTH+500 and Y equals to 1090
            self.bird_x = WIDTH + 50
            self.bird_y = 1090

    # A function that draws the object using the collected data
    def draw2(self):
        canvas.coords(self.canvas_object, self.bird_x, self.bird_y)


# Creating a 'Score' class that collects given data and creates and draws the text in the game.
# (The code is inspired by BallAsClass.py provided under Week03, step0304)
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


# Creating a 'Dino' class that collects given data and creates,moves,draws the dinosaur in the game.
# (The code is inspired by BallAsClass.py provided under Week03, step0304)
class Dino:

    # A function that collects given data and assigns it to a specific characteristic of the dinosaur that we want to create
    def __init__(self, x, y, image, ):
        self.x = x
        self.y = y
        self.image = image
        self.canvas_object = canvas.create_image(self.x, self.y, image=self.image)

    # A function that draws the dinosaur using the collected data, and animates it using frames
    def draw_dino(self):
        canvas.coords(self.canvas_object, self.x, self.y)
        canvas.itemconfig(self.canvas_object, image=dino_frames[frame_index])

    # A function that is responsible for the jumping mechanic of the dinosaur
    # (The code is inspired by interactive_flappy_wings.py provided under Week06, step0604)
    def dino_jump(self):
        global in_a_jump, jump_index, jump_offsets, dino_y  # Using 'global' to access data from outside the function

        canvas.itemconfig(self.canvas_object, image=dino_frames[0])  # A specific frame is displayed when jumping

        if in_a_jump:  # If (in_a_Jump) is true then,
            jump_offset = jump_offsets[
                jump_index]  # (jump_offset) equals to jump_offsets[jump_index], the dinosaurs Y is increased by the value of the (jump_offset)
            self.y += jump_offset
            canvas.move(self.canvas_object, 0,
                        jump_offset)  # The picture of the dinosaur is moved according to the value above
            jump_index = jump_index + 1  # (jump_index) is increased by one

            if jump_index > len(
                    jump_offsets) - 1:  # If (jump_index) is bigger than the length of (jump_offsets) the, (jump_index) equals to 0 and (in_a_Jump) to false
                jump_index = 0
                in_a_jump = False

    # A function that displays a specific frame when the player loses
    def lost(self):
        canvas.itemconfig(self.canvas_object, image=lost_img)


# ============================================================================================#
# The code below is responsible for accessing the (resources) folder and assigning PNG images to variables
# The last four variable have four images each that we will use to animate them
# (The code is inspired by flappy_wings.py provided under Week06, step0603 and moving_background.py provided under Week07, step0701)
# Some graphics where provided in the resource folder and some were custom-made in an external editor (cloud_black, mountains, stars,
# money, bird). The already provided images where also edited.

cloud_black_img = PhotoImage(file='resources/cloud_black.png')
ground_img = PhotoImage(file='resources/ground.png')
lost_img = PhotoImage(file='resources/dino4.png')
mountains_img = PhotoImage(file='resources/mountains.png')
stars_img = PhotoImage(file='resources/stars.png')
money_img = PhotoImage(file='resources/money.png')

cac_img_array = [PhotoImage(file='resources/cactus-small.png'), PhotoImage(file='resources/cactus-big.png'),
                 PhotoImage(file='resources/cactus-small.png'), PhotoImage(file='resources/cactus-big.png'),
                 PhotoImage(file='resources/cactus-double.png'), PhotoImage(file='resources/cactus-small2.png'),
                 PhotoImage(file='resources/cactus-small3.png')]

sun_frames = [PhotoImage(file='resources/sun%i.png' % i) for i in range(FRAME_COUNT)]
moon_frames = [PhotoImage(file='resources/moon%i.png' % i) for i in range(FRAME_COUNT)]
bird_frames = [PhotoImage(file='resources/bird%i.png' % i) for i in range(FRAME_COUNT)]
dino_frames = [PhotoImage(file='resources/dino%i.png' % i) for i in range(FRAME_COUNT)]

# ============================================================================================#
# The code below is responsible for creating objects with the classes above
# (The code is inspired by BallAsClass.py provided under Week03, step0304)

cloud_black_obj1 = Cactus(WIDTH / 2, HEIGHT / 3, -2, image=cloud_black_img)
cloud_black_obj2 = Cactus(WIDTH / 2 + 100, HEIGHT / 2, -5, image=cloud_black_img)

stars_obj = Cactus(WIDTH / 2 + 1000, HEIGHT / 2, 0, image=stars_img)

sun = Cactus(WIDTH, HEIGHT - 1, 0, image=sun_frames[0])
moon = Cactus(0 / 3, HEIGHT + 1 / 3, 0, image=moon_frames[0])

mountains_obj = Cactus(WIDTH, HEIGHT - 90 - ground_img.height() / 2, -5, image=mountains_img)
ground_obj = Cactus(WIDTH, HEIGHT - ground_img.height() / 2, -13, image=ground_img)

bird = Bird(WIDTH + 150, HEIGHT - 220, -15, image=bird_frames[0])

cactus_array = [Cactus(WIDTH, HEIGHT - 110, -15, cac_img_array[randint(0, 1)]),
                Cactus(WIDTH + 300, HEIGHT - 110, -15, cac_img_array[0]),
                Cactus(WIDTH + 600, HEIGHT - 110, -15, cac_img_array[0])]

money = Bird(WIDTH + 150, HEIGHT - 1090, -15, image=money_img)

dino = Dino(WIDTH / 5, HEIGHT - 110, image=dino_frames[0])
# ============================================================================================#
# Declaring and assigning some variable and arrays that will help us in the functions

started = False
is_paused = False
is_night = False
in_a_jump = False
pick_up = False

jump_offsets = [0, -70, -55, -40, -20, -10, 0, 20, 40, 55, 50, 45, -15]
bg_colors_day = ['DarkOrange3', 'DarkGoldenrod2', 'Gold2', 'Aquamarine', 'LightSkyBlue', 'DeepSkyBlue', 'DodgerBlue',
                 'blue4', 'black', 'black', 'black', 'black', 'black', 'DarkOrange4']

animation_index = 0
frame_index = 0
jump_index = 0
bg_index = 0

timer = 0
cactus_timer = 0
bird_timer = 0

case = 0
bg_changer = 0

dino_y = dino.y

# ============================================================================================#
# Creating our 'Score' objects for the text in the game

score_txt = Score(650, HEIGHT - 10, 'Score: ', ('Source Sans Pro', 16), 'black')
score = Score(710, HEIGHT - 10, 0, ('Source Sans Pro', 16), 'black')

high_score_txt = Score(650, 15, 'High Score: ', ('Source Sans Pro', 16), 'black')
high_score = Score(740, 15, 0, ('Source Sans Pro', 16), 'black')

lost = Score(WIDTH / 2, HEIGHT / 2, 'GAME OVER', ('Arial Bold', 60), 'black')
pause = Score(WIDTH / 2, HEIGHT / 2, 'PAUSE', ('Arial Bold', 60), 'black')
menu = Score(WIDTH / 2, HEIGHT / 2 - 50, 'PRESS "S" TO START', ('Arial Bold', 40), 'black')
info = Score(WIDTH / 3 + 10, HEIGHT - 10,
             'CO1417 Dino | Q: quit, P: pause, R: restart, Space: jump, <Down>: pick up bag', ('Source Sans Pro', 12),
             'black')


# ============================================================================================#


# A function that uses the pythagorean thorium to measure the distance between two objects (in this case cactus and dinosaur)
# and if the distance is smaller or equal to 40, then it returns as (True)
# (Code inspired by the solutions of Exercise0301.md and Exercise0302.md provided under Week03, xtras)
def collision_with_cactus(ob1, ob2):
    dx = ((ob2.cac_x + 10 - ob1.x) ** 2)
    dy = ((ob2.cac_y - 30 - ob1.y) ** 2)
    distance = ((dx + dy) ** 0.5)

    if distance <= 40:
        return True


# A function that uses the pythagorean thorium to measure the distance between two objects (in this case bird or money bag and dinosaur)
# and if the distance is smaller or equal to 40, then it returns as (True)
# (Code inspired by the solutions of Exercise0301.md and Exercise0302.md provided under Week03, xtras)
def collision_with_bird(ob1, ob2):
    dx = ((ob2.bird_x + 10 - ob1.x) ** 2)
    dy = ((ob2.bird_y - ob1.y) ** 2)
    distance = ((dx + dy) ** 0.5)

    if distance <= 40:
        return True


# This is the main function that controls the switching from the start screen to the game and restarting/quiting
# Also it  is responsible for everything that gets constantly updated while the game is running.
# These things are: drawing and removing objects, dinosaur physics, collisions and text display.
# (Code inspired from AnimationOverXandY.py provided under Week03, step0302)
def update():
    global animation_index, cactus_timer, case, jump_offsets, \
        frame_index, in_a_jump, jump_index, timer, dino_y, case, \
        started, is_paused, bg_changer, bg_index, is_night, pick_up, \
        bird_timer  # Using 'global' to access data from outside the function

    if case == 0:  # Menu   # If (case) equals to 0 then, the text of the start screen is visible
        menu.color = 'black'
        menu.draw_score()
        info.draw_score()

    elif case == 5:  # Paused   # If (case) equals to 5 then, the text of the pause screen is visible, and (is_paused) is true
        pause.color = 'black'
        pause.draw_score()
        is_paused = True

    elif case == 6:  # End Pause    # If (case) equals to 6 then, the text of the pause screen is visible, (is_paused) is false and (case) equals to 4
        pause.color = ''
        pause.draw_score()
        case = 4
        is_paused = False

    elif case == 2 and not is_paused:  # Restart    # If (case) equals to 2 and (is_paused) is false then,
        # the text of the start screen is visible, and everything gets back to its starting value and position
        score.points = 0

        lost.color = ''
        lost.draw_score()

        menu.color = 'black'
        menu.draw_score()

        for e in range(3):  # The cacti return to their original values
            cactus_array[e].cac_x += WIDTH + 100
            cactus_array[e].draw_cac()
            cactus_array[e].speed_x = -15

        # The bird returns to its original value
        bird.bird_x += WIDTH + 100
        bird.bird_y = 1000
        bird.draw()
        bird.speed_x = -15

        # The money bag returns to its original value
        money.bird_x += WIDTH + 100
        money.draw2()
        money.speed_x = -15

        # The dinosaur returns to its original value
        dino.y = HEIGHT - 110

        bird_timer = 0
        jump_index = 0
        case = 0
        started = False
        in_a_jump = False

    elif case == 3:  # Lost # If (case) equals to 3, the text of the loose screen is visible, the high score is displayed and (started) equals to false
        lost.color = 'black'
        lost.draw_score()
        dino.lost()

        high_score_txt.draw_score()
        high_score.draw_score()
        started = False

    else:  # If nothing from above is true then the game is running
        menu.color = ''
        menu.draw_score()  # The text of the starting screen disappears

        # ====================================================================================#
        # The code below is responsible for drawing, moving and animating the objects in the game
        # (The code is inspired by flappy_wings.py provided under Week06, step0603 and moving_background.py provided under Week07, step0701)

        stars_obj.draw_cac()

        sun.draw_cac()
        sun.move_sun_and_moon()
        canvas.itemconfig(sun.canvas_object, image=sun_frames[frame_index])

        moon.draw_cac()
        moon.move_sun_and_moon()
        canvas.itemconfig(moon.canvas_object, image=moon_frames[frame_index])

        mountains_obj.draw_cac()
        mountains_obj.move()
        canvas.itemconfig(mountains_obj.canvas_object, image=mountains_img)

        ground_obj.draw_cac()
        ground_obj.move()
        canvas.itemconfig(ground_obj.canvas_object, image=ground_img)

        cloud_black_obj1.draw_cac()
        cloud_black_obj1.move()
        cloud_black_obj2.draw_cac()
        cloud_black_obj2.move()
        money.draw2()
        money.move2()

        # ====================================================================================#

        money_chance = randint(0, 300)  # declaring a random variable from 0 to 300

        if money_chance == 1:  # If the above variable equals to 1 then, the money bags Y equals to Height - 90 and X equals to WIDTH
            money.bird_y = HEIGHT - 90
            money.bird_x = WIDTH

        if pick_up and collision_with_bird(dino,
                                           money):  # If (pick_up) is true and the dinosaur collided with the money bag then,
            money.bird_y = 1090  # The money bags y equals to 1090 and the score is increased by 200
            score.points += 200

        bird_timer += 1  # Increases (bird_timer) by one
        if bird_timer >= 900:  # If (bird_timer) equals to 900 then the bird is drawn and is moving
            bird.draw()
            bird.move()

        for i in range(3):  # Drawing and moving all the cacti constantly at the same time
            cactus_array[i].draw_cac()
            cactus_array[i].move_cac()

            if bird.speed_x <= -22:  # if the birds speed is smaller or equal to -22 then,
                if cactus_timer >= 300:  # If (cactus_timer) is bigger or equal then 300 then,
                    for j in range(3):
                        cactus_array[j].speed_x -= 1  # The speed of the cacti, bird and money bag get decreased by 1
                    cactus_timer = 0  # (cactus_timer) is equal to 0
                    bird.speed_x -= 1
                    money.speed_x -= 1

            # If the dinosaur collides with a cactus or the bird then, (case) equals to 3
            if collision_with_cactus(dino, cactus_array[i]):
                case = 3

        if collision_with_bird(dino, bird):
            case = 3

        # =====================================================================================#
        # The code below is responsible for changing the color of the background to make the day/night cycle.
        # For this we use is variable (bg_changer) as our 'clock', everytime it equals to 142 the background
        # changes and the 'clock' resets. When it's nighttime (bg_index equals to 8) the stars are moved inside the window
        # to create the night sky and when (bg_index equals to 13) they get removed to create the day sky.

        bg_changer += 0.5
        if bg_changer == 142:
            bg_index += 1
            canvas.configure(bg=bg_colors_day[bg_index])
            bg_changer = 0

            if bg_index == 8 and not is_night:
                stars_obj.cac_x -= 1000
                is_night = True

            if bg_index == 13 and is_night:
                stars_obj.cac_x += 1000
                is_night = False

            if bg_index == 13:
                bg_index = -1

        # =====================================================================================#
        # The code below is responsible for the score. Every 100ms the score gets increased by one.
        # for these we use a 'clock' again because our delay is 50ms. When the clocks value is an even number
        # the score is increased by one. If the high score is smaller or equal to the score then its value is equal to the score

        cactus_timer += 1
        if cactus_timer % 2 == 0:
            score.points += 1

        score_txt.draw_score()
        score.draw_score()

        if high_score.points <= score.points:
            high_score.points = score.points

        # ====================================================================================#
        # The code below is responsible for the drawing of the dinosaur during jump and running.
        # also is animates the dinosaur every 100ms with the same way we increase the score above

        if in_a_jump:
            dino.dino_jump()
        else:
            dino.draw_dino()

        timer += 1
        if timer == 2:
            frame_index += 1
            timer = 0
            if frame_index == FRAME_COUNT:
                frame_index = 0

        lost.color = ''

    win.after(DELAY, update)  # Sets the update delay of the function


# ============================================================================================#
# The functions below are responsible for the detection of the key press for jumping and picking the money bag
# (The code is inspired by interactive_flappy_wings.py provided under Week06, step0604)


def jump(
        __self__):  # If the player presses 'space' in_a_jump equals to true, and it doesn't allow it to be true again until its false
    global in_a_jump
    if not in_a_jump:
        in_a_jump = True


def pick(
        __self__):  # If the player presses 'down' pick_up equals to true, and it doesn't allow it to be true again until its false
    global pick_up
    if not pick_up:
        pick_up = True


# ============================================================================================#
# An event function that according to the key pressed by the player, returns a variable to use it in the flow of the game
# (Code reused from MoreKeyboardInput.py provided under Week02, step0202)

def on_key_press(event):
    global case, started, is_paused  # Using 'global' to access data from outside the function

    if event.char == 's' or event.char == 'S':  # If the player pressed 's' on the keyboard it returns the value of (case) as 4 and (started) as true
        if is_paused or case == 3:  # If (is_paused) is true or (case) equals to 3, then it skips the code
            return
        else:
            case = 4
            started = True
            return case, started

    if event.char == 'r' or event.char == 'R':  # If the player pressed 'r' on the keyboard it returns the value of (case) as 2
        if is_paused:  # If (is_paused) is true, then it skips the code
            return
        else:
            case = 2
            return case

    if event.char == 'p' or event.char == 'P':  # If the player pressed 'p' on the keyboard it increases the value of (case) and returns it
        if not started:  # If (started) is false, then it skips the code
            return
        else:
            case += 1
            return case

    if event.char == 'x' or event.char == 'X':
        quit()  # If the player pressed 'x' on the keyboard it ends the program


# ============================================================================================#

win.bind("<space>", jump)  # Binds the space bar with the (jump) function
win.bind('<Down>', pick)  # Binds the down arrow key with the (pick) function
win.bind('<KeyPress>', on_key_press)  # Any key on the keyboard gets bound with the (on_key_press) function

win.after(0, update)  # This keeps the (update) function updated
win.mainloop()  # This is keeping the window open while the game is running
