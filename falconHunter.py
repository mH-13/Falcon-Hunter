import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

hunter_name = ""  # Variable to store the hunter's name

screenWidth = 1000
screenHeight = 600

background_color = (0.08235294117647059, 0.20392156862745098, 0.2823529411764706)  # Initial background color
new_background_color = (0.08235294117647059, 0.20392156862745098, 0.2823529411764706)  # Initial new background color

ResetButton = False
PlayButton = False
CrossButton = False
paused = False
game_over = False
MissedBirds = 0

hunterX = 40
hunterY = 200
hunterRadius = 20
bodyY1 = 179
bodyY2 = 120
hunterLeg = 10
hunterLegX1 = hunterX - 25
hunterLegX2 = hunterX + 25
hunterHandY = 150
leg_direction = 1  # Initialize leg direction

groundY = 10
obstacles = []
last_obstacle_x = 0

jumping = False
jump_start_time = 0
initial_jump_height = 200  # Adjust this value as needed
jump_duration = 2000
Score = 0
CollideScore = 0
color_change_speed = 0.01

bullets = []

birds=[]



def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def ConvertToZoneZero(current_zone, x, y):
    if current_zone == 0:
        return x, y
    elif current_zone == 1:
        return y, x
    elif current_zone == 2:
        return -y, x
    elif current_zone == 3:
        return -x, y
    elif current_zone == 4:
        return -x, -y
    elif current_zone == 5:
        return -y, -x
    elif current_zone == 6:
        return -y, x
    elif current_zone == 7:
        return x, -y


def MidPointLine(zone, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dinit = 2 * dy - dx
    E_pixel = 2 * dy
    NE_pixel = 2 * (dy - dx)
    x = x1
    y = y1
    while x <= x2:
        p1, p2 = ConvertToOriginalZone(zone, x, y)
        drawpoints(p1, p2, 1)
        if dinit > 0:
            dinit = dinit + NE_pixel
            x = x + 1
            y = y + 1
        else:
            dinit = dinit + E_pixel
            x = x + 1


def ConvertToOriginalZone(target_zone, x, y):
    if target_zone == 0:
        return x, y
    if target_zone == 1:
        return y, x
    if target_zone == 2:
        return -y, -x
    if target_zone == 3:
        return -x, y
    if target_zone == 4:
        return -x, -y
    if target_zone == 5:
        return -y, -x
    if target_zone == 6:
        return y, -x
    if target_zone == 7:
        return x, -y


def Line(x1, y1, x2, y2):
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConvertToZoneZero(zone, x1, y1)
    x2, y2 = ConvertToZoneZero(zone, x2, y2)
    MidPointLine(zone, x1, y1, x2, y2)



def draw_circle(xc, yc, x, y):
    glBegin(GL_POINTS)
    glVertex2f(xc + x, yc + y)
    glVertex2f(xc - x, yc + y)
    glVertex2f(xc + x, yc - y)
    glVertex2f(xc - x, yc - y)
    glVertex2f(xc + y, yc + x)
    glVertex2f(xc - y, yc + x)
    glVertex2f(xc + y, yc - x)
    glVertex2f(xc - y, yc - x)
    glEnd()


def midpoint_circle(xc, yc, radius):
    d = 1 - radius
    x = 0
    y = radius

    draw_circle(xc, yc, x, y)
    while x < y:

        if d < 0:
            d += 2 * x + 3
            x += 1
        else:
            d += 2 * (x - y) + 5
            x += 1
            y -= 1
        draw_circle(xc, yc, x, y)


def reset_button():
    glColor3f(0, 0.9765, 0.7804)
    Line(10, 570, 30, 570)
    Line(10, 570, 20, 580)
    Line(10, 570, 20, 560)


def play_button():
    glColor3f(1.0, 0.8431372549019608, 0.0)
    Line(495, 580, 515, 570)
    Line(495, 560, 515, 570)
    Line(495, 580, 495, 560)


def pause_resume_button():
    glColor3f(1.0, 0.8431372549019608, 0.0)
    Line(495, 580, 495, 560)
    Line(505, 580, 505, 560)


def cross_button():
    glColor3f(1, 0, 0)
    Line(990, 580, 970, 560)
    Line(970, 580, 990, 560)


def draw_hunter():
    global hunterX, hunterY, hunterLegX1, hunterLegX2, leg_direction, game_over
    
    if not paused and not game_over:
        leg_range = 25
        hunterLegX1 += leg_direction
        hunterLegX2 -= leg_direction

        if hunterLegX1 >= hunterX + leg_range or hunterLegX2 >= hunterX + leg_range:
            leg_direction *= -1
            
        if hunterLegX2 <= hunterX - leg_range or hunterLegX2 <= hunterX - leg_range:
            leg_direction *= +1

    glColor3f(1.0, 0.5803921568627451, 0.12941176470588237)
    midpoint_circle(hunterX, hunterY, hunterRadius)
    Line(hunterX, bodyY1, hunterX, bodyY2)
    Line(hunterX, bodyY2, hunterLegX1, hunterLeg)
    Line(hunterX, bodyY2, hunterLegX2, hunterLeg)
    Line(hunterX, hunterHandY, hunterX + 30, hunterHandY)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1

    def draw(self):
        glLineWidth(2)  # Set line width to 2
        glColor3f(1.0, 0.0, 0.0)  # Red color for the bullet
        Line(self.x, self.y, self.x + 10, self.y)


    def move(self):
        self.x += self.speed


def draw_bullets():
    for bullet in bullets:
        bullet.draw()


def move_bullets():
    for bullet in bullets:
        bullet.move()
  

def generate_bird(value=None):
    global birds

    if not paused:  # Adjust the interval as needed (1.0 means 1 second)
        bird_x = random.randint(1100, 1200)
        bird_y = random.randint(210, 400)
        bird_r = 5
        birds.append((bird_x, bird_y, bird_r))
        
        new_birds = []
        for b in birds[0:1]:
            b_x, b_y, b_r = b
            b_x -= 1 # Adjust the speed as needed (change 2 to the desired speed)
            if b_x > 0:
                new_birds.append((b_x, b_y, b_r))
        birds = new_birds
        
        glutPostRedisplay()  
        glutTimerFunc(random.randint(1000, 6000), generate_bird, 0)  # Schedule next falling circle after an interval



def draw_bird():
    global birds, bullets, Score, MissedBirds, game_over
    random_color = (random.random(), random.random(), random.random())
    
    for b_index, bird in enumerate(birds):
        bird_x, bird_y, bird_r = bird
        
        glColor3f(*random_color)  # White color for the bird
        midpoint_circle(bird_x, bird_y, bird_r)

        # Set the color of the bird
        glColor3f(*random_color)  # White color for the bird

        # Calculate oscillation offset for wings based on time elapsed
        oscillation = math.sin(time.time() * 5) * 5  # Adjust the multiplier to control the speed


        # Draw the first wing with oscillation
        Line(bird_x + 2, bird_y + bird_r, bird_x + 2 * bird_r, bird_y + bird_r + 8)
        Line(bird_x + 2 * bird_r, bird_y + bird_r + 8, bird_x + 5 * bird_r, bird_y + bird_r + oscillation)

        # Draw the second wing with oscillation
        Line(bird_x - 2, bird_y + bird_r, bird_x - 2 * bird_r, bird_y + bird_r + 8)
        Line(bird_x - 2 * bird_r, bird_y + bird_r + 8, bird_x - 5 * bird_r, bird_y + bird_r + oscillation)

        # Check collision with bullets
        for bullet_index, bullet in enumerate(bullets):
            bullet_x = bullet.x
            bullet_y = bullet.y

            # Calculate the distance between the bullet and the bird's center
            distance = math.sqrt((bird_x - bullet_x) ** 2 + (bird_y - bullet_y) ** 2)

            # Check if the distance is less than the sum of the bird's radius and the bullet's radius
            if distance <= bird_r + 2:  # Adjust the collision detection radius as needed
                # Remove the collided bird and bullet
                del bullets[bullet_index]
                del birds[b_index]
                Score += 1
                print("Hunted Falcon: ", Score)
                break  # Break out of the inner loop to avoid checking other bullets for this bird

        # Check if the bird is missed
        if bird_x <= 10:
            MissedBirds += 1
            if MissedBirds >= 5:
                print("M", MissedBirds)
                game_over = True
                break  # Break out of the loop if the game is over

    
class Obstacle:
    global paused, game_over
    
    def __init__(self, x, width, height, speed):
        self.x = x
        self.y = groundY  # Set y-coordinate to align with the road
        self.width = width
        self.height = height
        self.speed = speed
        self.collided = False  # Initialize collided flag to False

    def draw(self):
        if not paused and not game_over:
            random_color = (random.random(), random.random(), random.random())
            glColor3f(*random_color)
            Line(self.x, self.y + self.height, self.x + self.width, self.y + self.height)
            Line(self.x, self.y + self.height, self.x, self.y)
            Line(self.x + self.width, self.y + self.height, self.x + self.width, self.y)
            Line(self.x, self.y, self.x + self.width, self.y)
        
    def move(self):
        if not paused and not game_over:
            self.x -= self.speed


def draw_obstacles():
    global paused, game_over
    
    if not paused and not game_over:
        for obstacle in obstacles:
            obstacle.draw()


def move_obstacles():
    for obstacle in obstacles:
        obstacle.move()


def generate_obstacle(value):
    global last_obstacle_x  # Use the global variable
    
    if not paused:
        height = random.randint(50, 70)  # Choose randomly between heights of 50 and 100
        speed = 1.5
        dist = random.randint(100, 500)
        new_obstacle_x = last_obstacle_x + dist
        obstacle = Obstacle(new_obstacle_x, 10, height, speed)  
        obstacles.append(obstacle)
        last_obstacle_x = new_obstacle_x  # Update the last obstacle's x-coordinate
        glutPostRedisplay() 
        glutTimerFunc(random.randint(2000, 2500), generate_obstacle, 0)  # Adjust the initial timer interval to at least 2 seconds later
 
     
        

def draw_ground():
    glColor3f(0.5, 0.5, 0.5)
    Line(0, groundY, screenWidth, groundY)  


def lerp(start, end, t):
    return start + (end - start) * t


def timer(value):
    global jumping, hunterY, bodyY1, bodyY2, hunterHandY, hunterLeg, CollideScore, game_over

    if not paused and not game_over:
        move_obstacles()
        move_bullets()  # Move bullets along with other game elements
        glutPostRedisplay()
        
        hunter_leg_bottom = hunterLeg # Collision detection
        hunter_leg_top = hunterLeg + hunterLeg
        
        leg_bounding_box_current = [hunterX - 25, hunterX + 25, hunter_leg_bottom, hunter_leg_top] # Define the bounding box of the hunter's leg
        leg_bounding_box_next = [hunterX - 25 + leg_direction, hunterX + 25 + leg_direction, hunter_leg_bottom, hunter_leg_top]

        for obstacle in obstacles:
            if not obstacle.collided:
                obstacle_left = obstacle.x
                obstacle_right = obstacle.x + obstacle.width
                obstacle_bottom = obstacle.y
                obstacle_top = obstacle.y + obstacle.height

                # Check for collision between the bounding box of the hunter's leg and the obstacle
                if (leg_bounding_box_current[0] < obstacle_right and leg_bounding_box_current[1] > obstacle_left and
                        leg_bounding_box_current[2] < obstacle_top and leg_bounding_box_current[3] > obstacle_bottom) or \
                   (leg_bounding_box_next[0] < obstacle_right and leg_bounding_box_next[1] > obstacle_left and
                        leg_bounding_box_next[2] < obstacle_top and leg_bounding_box_next[3] > obstacle_bottom):
                    CollideScore += 1
                    print("c", CollideScore)
                    obstacle.collided = True
                    if CollideScore >= 3:
                        game_over = True
                    break  # Exit the loop if there's a collision

        if jumping:
            elapsed_time = glutGet(GLUT_ELAPSED_TIME) - jump_start_time
            if elapsed_time >= jump_duration:
                hunterLeg = groundY
                hunterY = hunterLeg + 190
                bodyY1 = hunterY - hunterRadius
                bodyY2 = bodyY1 - 59
                hunterHandY = (hunterY + bodyY2) / 2
                jumping = False
            else:
                jump_progress = elapsed_time / jump_duration
                if jump_progress < 0.6:
                    hunterLeg = lerp(groundY, groundY + initial_jump_height, jump_progress * 2)
                else:
                    jump_progress = (jump_progress - 0.6) * 2
                    hunterLeg = lerp(groundY + initial_jump_height, groundY, jump_progress)
                hunterY = hunterLeg + 190
                bodyY1 = hunterY - hunterRadius
                bodyY2 = bodyY1 - 59
                hunterHandY = (hunterY + bodyY2) / 2

    glutTimerFunc(16, timer, 0)



def lerp_color(start_color, end_color, t):
    return tuple(start + (end - start) * t for start, end in zip(start_color, end_color))


def toggle_day_night():
    
    if not paused and not game_over: 
        global background_color, new_background_color, color_change_speed
        
        if background_color == (0.08235294117647059, 0.20392156862745098, 0.2823529411764706):
            new_background_color = (0.3254901960784314, 0.5098039215686274, 0.6470588235294118) # Day color
        else:
            new_background_color = (0.08235294117647059, 0.20392156862745098, 0.2823529411764706) # Night color

        glutTimerFunc(100, change_background_color, 0)  # Start a timer to gradually change the background color


def change_background_color(value):
    global background_color, new_background_color, color_change_speed
    
    if not paused and not game_over: 
        
        t = min(1.0, color_change_speed) # Calculate the current progress of the color transition       
        background_color = lerp_color(background_color, new_background_color, t) # Interpolate the current background color
        color_change_speed += 0.005 # Increase the interpolation factor for the next tick # Increased to make the transition slower
        
        if t < 1.0: # If the transition is not complete, schedule the next tick
            glutTimerFunc(100, change_background_color, 0) # Increased to 50 milliseconds for a longer duration
        else:
            color_change_speed = 0.005 # Reset the interpolation factor for the next transition
 
            
def update_day_night_cycle(value):
    
    if not paused and not game_over:
        toggle_day_night() # Toggle day and night colors
        glutPostRedisplay() # Redraw the scene with the updated background color
        glutTimerFunc(10000, update_day_night_cycle, 0) # Schedule the next update


# def generate_stars(xc, yc, size):
#     radius = size // 2
#     num_points = 200  # Number of points to approximate the star shape
#     star_points = []
 
#     for i in range(num_points): # Generate points around a circle to approximate the star shape
#         angle = 2.0 * math.pi * i / num_points
#         x = xc + radius * math.cos(angle)
#         y = yc + radius * math.sin(angle)
#         star_points.append((x, y))
   
#     for i in range(num_points // 3):  # Add some additional points to make the star shape more irregular
#         angle = 2.0 * math.pi * random.random()
#         distance = random.uniform(0, radius * 0.4)  # Random distance from the center
#         x = xc + (radius + distance) * math.cos(angle)
#         y = yc + (radius + distance) * math.sin(angle)
#         star_points.append((x, y))

#     glBegin(GL_POINTS)
#     glColor3f(1.0, 1.0, 1.0)  # White color for the star
#     for point in star_points:
#         glVertex2f(point[0], point[1])
#     glEnd()


# def draw_stars():
#     # Draw big stars
#     generate_stars(50, 550, 20)
#     generate_stars(200, 500, 13)
#     generate_stars(400, 460, 9)
#     generate_stars(650, 400, 14)
#     generate_stars(950, 450, 10)
#     generate_stars(750, 550, 23)
#     generate_stars(550, 500, 13)
#     generate_stars(300, 360, 13)
#     generate_stars(150, 400, 6)
#     generate_stars(20, 350, 12)
   
    
#     drawpoints(140, 570, 1)
#     drawpoints(70, 450, 2)
#     drawpoints(320, 550, 1)
#     drawpoints(480, 360, 1)
#     drawpoints(860, 510, 2)
#     drawpoints(830, 360, 2)
    
def initialize():
    glViewport(0, 0, screenWidth, screenHeight)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, screenWidth, 0, screenHeight)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard(key, x, y):
    global hunterY, bodyY1, bodyY2, hunterHandY, hunterLeg, jumping, jump_start_time, game_over
    if key == b' ' and not jumping and not paused and not game_over:  # Allow jumping only when not already jumping
        jumping = True
        jump_start_time = glutGet(GLUT_ELAPSED_TIME)  # Get the current time
        hunterY += initial_jump_height  # Start the jump
        bodyY1 += initial_jump_height
        bodyY2 += initial_jump_height
        hunterHandY += initial_jump_height
        hunterLeg += initial_jump_height
    elif key == b'b' and not paused and not game_over:  # Generate a bullet when "b" key is pressed
        bullet = Bullet(hunterX + 30, hunterHandY)
        bullets.append(bullet)
        move_bullets()
    
        
def mouseListener(button, state, x, y):
    global ResetButton, CrossButton, PlayButton, paused, Score, paused, game_over, screenHeight
    converted_y = screenHeight - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 970 <= x <= 990 and 560 <= converted_y <= 580:
            CrossButton = True
            print("Goodbye!", "Score:", Score)
            paused = True
            glutLeaveMainLoop()
        elif 495 <= x <= 505 and 560 <= converted_y <=580:
            PlayButton = not PlayButton
            paused = not paused
            
        elif 10 <= x <= 30 and 560 <= converted_y <=580:
            ResetButton = True
            # glutLeaveMainLoop()
        glutPostRedisplay()


def drawpoints(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def iterate():
    glViewport(0, 0, screenWidth, screenHeight)
    glOrtho(0.0, screenWidth, 0.0, screenHeight, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)


def reset_game():
    global Score, paused , game_over, CollideScore, leg_direction, MissedBirds, obstacles
    CollideScore = 0
    Score = 0 
    paused = False
    Score = 0
    MissedBirds = 0
    # game_over = False
   
    
def display():
    global paused, ResetButton, game_over
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glClearColor(*background_color, 1.0)  # Set the clear color before clearing the buffer
    glClear(GL_COLOR_BUFFER_BIT)

    draw_hunter()
    draw_obstacles()
    draw_ground()
    #draw_stars()  # Draw stars
    draw_bullets()  # Draw bullets
    generate_bird()
    draw_bird()


    if game_over:
        print("Game Over!", hunter_name ,"scored:", Score)
        obstacles.clear()
        bullets.clear()
        birds.clear()
        paused = True
        game_over = False
        
        
    if ResetButton:
        reset_button()
        reset_game()
        ResetButton = False  
    else:
        reset_button()
        
    if CrossButton:
        cross_button()
        glutLeaveMainLoop()
    else:
        cross_button()
    
    if PlayButton and paused:
        play_button()
    if not paused:
        pause_resume_button()
    
    glutSwapBuffers()  
    

def get_hunter_name():
    global hunter_name
    hunter_name = input("Enter the hunter's name: ").strip()
    
def initialize_game():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(screenWidth, screenHeight)
    glutInitWindowPosition(200, 0)
    get_hunter_name()  # Prompt user for hunter's name
    hunter_title = bytes(f"{hunter_name}'s Hunter Game", 'utf-8')  # Convert title to bytes
    glutCreateWindow(hunter_title)  # Pass bytes title to glutCreateWindow
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouseListener)
    initialize()
    glutTimerFunc(random.randint(500, 2000), generate_obstacle, 0)
    glutTimerFunc(10000, update_day_night_cycle, 0) # Start the day and night cycle
    glutTimerFunc(random.randint(1000, 3000), generate_bird, 0) 
    glutTimerFunc(0, timer, 0)
    glutMainLoop()


if __name__ == "__main__":
    initialize_game()
