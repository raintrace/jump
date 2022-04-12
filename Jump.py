import pygame
import sys
import random



class Bird(object):
    """define a bird"""

    def __init__(self):
        """Define initialization method"""
        self.birdRect = pygame.Rect(65, 50, 50, 50)  # Bird rectangle
        # Define the list of 3 states of birds
        self.birdStatus = [pygame.image.load("assets/1.png"),
                           pygame.image.load("assets/2.png"),
                           pygame.image.load("assets/dead.png")]
        self.status = 0      # Default flight status
        self.birdX = 120     # The x-axis coordinate of the bird is the speed of flying to the right
        self.birdY = 350     # The y-axis coordinate of the bird, i.e. the flying height up and down
        self.jump = False    # By default, the bird will land automatically
        self.jumpSpeed = 10  # Jump height
        self.gravity = 5     # gravity
        self.dead = False    # The default bird life state is alive

    def birdUpdate(self):
        if self.jump:
            # Bird jump
            self.jumpSpeed -= 1           # The speed decreases and the rise is slower and slower
            self.birdY -= self.jumpSpeed  # The bird's Y-axis coordinate decreases and the bird rises
        else:
            # Bird falling
            self.gravity += 0.2           # Gravity increases and decreases faster and faster
            self.birdY += self.gravity    # The bird's Y-axis coordinates increase and the bird descends
        self.birdRect[1] = self.birdY     # Change Y-axis position


class Pipeline(object):
    """Define a pipe class"""

    def __init__(self):
        """Define initialization method"""
        self.wallx = 400  # X-axis coordinate of the pipe
        self.pineUp = pygame.image.load("assets/top.png")
        self.pineDown = pygame.image.load("assets/bottom.png")

    def updatePipeline(self):
        """"Pipeline moving method"""
        self.wallx -= 5  # The x-axis coordinate of the pipe decreases, that is, the pipe moves to the left

        if self.wallx < -80:
            global score
            score += 1
            self.wallx = 400


def createMap():
    """Define how to create a map"""
    screen.fill((255, 255, 255))     # fill color
    screen.blit(background, (0, 0))  # Fill in background

    # Show pipe
    screen.blit(Pipeline.pineUp, (Pipeline.wallx, -300))   # Coordinate position of upper pipe
    screen.blit(Pipeline.pineDown, (Pipeline.wallx, 500))  # Lower pipe coordinate position
    Pipeline.updatePipeline()  # Pipe movement

    # Show birds
    if Bird.dead:              # Pipe collision status
        Bird.status = 2

    screen.blit(Bird.birdStatus[Bird.status], (Bird.birdX, Bird.birdY))              # Set the coordinates of the bird
    Bird.birdUpdate()          # Bird movement

    # 显示分数
    screen.blit(font.render('Score:' + str(score), -1, (255, 255, 255)), (100, 50))  # Set color and coordinate position
    pygame.display.update()    # update display



def checkDead():
    # Rectangular position of upper pipe
    upRect = pygame.Rect(Pipeline.wallx, -300,
                         Pipeline.pineUp.get_width() - 10,
                         Pipeline.pineUp.get_height())

    # Rectangular position of the lower tube
    downRect = pygame.Rect(Pipeline.wallx, 500,
                           Pipeline.pineDown.get_width() - 10,
                           Pipeline.pineDown.get_height())
    # Check whether the bird collides with the upper and lower pipes
    if upRect.colliderect(Bird.birdRect) or downRect.colliderect(Bird.birdRect):
        Bird.dead = True
    # Detect whether the bird flies out of the upper and lower boundaries
    if not 0 < Bird.birdRect[1] < height:
        Bird.dead = True
        return True
    else:
        return False


def getResutl():
    final_text1 = "Game Over"
    final_text2 = "final score :  " + str(score)
    ft1_font = pygame.font.SysFont("Arial", 70)
    ft1_surf = font.render(final_text1, 1, (242, 3, 36))
    ft2_font = pygame.font.SysFont("Arial", 50)
    ft2_surf = font.render(final_text2, 1, (253, 177, 6))
    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])
    screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])
    pygame.display.flip()               # Update the entire surface object to be displayed to the screen


if __name__ == '__main__':
    """main program"""
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 50)
    size = width, height = 400, 650
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    Pipeline = Pipeline()
    Bird = Bird()
    file = "music.mp3"
    pygame.mixer.init()
    track = pygame.mixer.music.load(file)
    pygame.mixer.music.play()


    score = 0
    while True:
        clock.tick(60)                       # Execute 60 times per second
        # 轮询事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not Bird.dead:
                Bird.jump = True
                Bird.gravity = 5
                Bird.jumpSpeed = 10
            if event.type == pygame.MOUSEBUTTONDOWN:
                Bird.status = 1
            else:
                Bird.status = 0


        background = pygame.image.load("assets/background.png")
        if checkDead():
            getResutl()
        else:
            createMap()

    pygame.quit()
python3: input("please input any key to exit!")