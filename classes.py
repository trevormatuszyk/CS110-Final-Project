import math
import pygame

block_width = 23
block_height = 15


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
magenta = (255, 0, 255)

class Ball(pygame.sprite.Sprite):

    def __init__(self, player):

        self.y = 180
        self.speed = 10 #starting speed (in pixels per second)
        self.direction = 200 #in degrees
        self.player = player
        self.width = 10
        self.height = 10

                # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        if (player == 1):
            self.x = 0
        else:
            self.x = self.screenwidth/2

        self.rect.x = self.x
        self.rect.y = self.y

    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if(self.player == 1):

            if self.x <= 0:
                self.direction = (360 - self.direction) % 360
                self.x = 1
        else:

            if(self.x <= self.screenwidth/2):
                self.direction = (360 - self.direction) % 360
                self.x = 1 + self.screenwidth/2


        # Do we bounce of the right side of the screen?
        if(self.player == 1):

            if(self.x > self.screenwidth/2 - self.width):
                self.direction = (360 - self.direction) % 360
                self.x = self.screenwidth/2 - self.width - 1

        else:
            if(self.x > self.screenwidth - self.width):
                self.direction = (360 - self.direction) % 360
                self.x = self.screenwidth - self.width - 1

        # fall off the bottom of the screen?
        if(self.y > 600):
            return True
        else:
            return False

class Block(pygame.sprite.Sprite):

    def __init__(self, player, color, x, y):

        super().__init__()

        self.image = pygame.Surface([block_width, block_height])

        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

class Paddle(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        if (player == 1):
            self.speed = 10
        else:
            self.speed = 10

        if(player == 1):

            self.rect.x = self.screenwidth/4 - self.width
            self.rect.y = self.screenheight - self.height

        elif(player == 2):

            self.rect.x = self.screenwidth*3/4 - self.width
            self.rect.y = self.screenheight - self.height

    def update(self):
        # Make sure we don't push the player paddle
        # off the right side of the screen
        if(player == 1):
            if self.rect.x > self.screenwidth/2 - self.width:
                self.rect.x = self.screenwidth/2 - self.width

        else:
            if self.rect.x > self.screenwidth - self.width:
                self.rect.x = self.screenwidth - self.width

        #make sure we don't push the paddle off the left side of the screen
        if(player == 1):
            if(self.rect.x < 0):
                self.rect.x = 0

        else:
            if(self.rect.x < self.screenwidth/2):
                self.rect.x = self.screenwidth/2

    def move(self, dir):
        #move player left
        if (dir == "left"):
            if(self.player == 1):
                if(self.rect.x - self.speed >= 0):
                    self.rect.x -= self.speed
                else:
                    self.rect.x = 0
            else:
                if(self.rect.x - self.speed >= self.screenwidth/2):
                    self.rect.x -= self.speed
                else:
                    self.rect.x = self.screenwidth/2

        if (dir == "right"):
            if (self.player == 1):
                if(self.rect.x + self.speed <= self.screenwidth/2 - self.width):
                    self.rect.x += self.speed
                else:
                    self.rect.x = self.screenwidth/2 - self.width

            else:
                if(self.rect.x + self.speed <= self.screenwidth - self.width):
                    self.rect.x += self.speed
                else:
                    self.rect.x = self.screenwidth - self.width
        #move the player left or right

class Game:

    def __init__(self):

        #initialize pygame
        pygame.init()

        #setup screen
        screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('Steven A Moore')
        font = pygame.font.Font(None, 36)
        background = pygame.Surface(screen.get_size())
        screenheight = pygame.display.get_surface().get_height()
        screenwidth = pygame.display.get_surface().get_width()

        #define sprite groups
        blocks1 = pygame.sprite.Group()
        blocks2 = pygame.sprite.Group()
        balls = pygame.sprite.Group()
        players = pygame.sprite.Group()
        allsprites = pygame.sprite.Group()

        #add in players
        player1 = Paddle(1)
        allsprites.add(player1)
        players.add(player1)

        player2 = Paddle(2)
        allsprites.add(player2)
        players.add(player2)

        #create balls
        ball1 = Ball(1)
        allsprites.add(ball1)
        balls.add(ball1)

        ball2 = Ball(2)
        allsprites.add(ball2)
        balls.add(ball2)

        #create blocks
        # The top of the block (y position)
        top = 80

        # Number of blocks to create
        blockcount = 16

        for row in [red, blue, green, yellow, magenta]:
            for column in range(0, blockcount):
                # Create a block (color,x,y)
                block = Block(1, row, column * (block_width + 2) + 1, top)
                blocks1.add(block)
                allsprites.add(block)
                block = Block(2, row, screenwidth/2 +  column * (block_width + 2) + 1, top)
                blocks2.add(block)
                allsprites.add(block)
            #move next row down
            top += block_height + 2

        #create clock to limit speed
        clock = pygame.time.Clock()

        # Is the game over?
        game_over = False

        # Exit the program?
        exit_program = False

        while (exit_program == False):

            #set fps to 30
            clock.tick(30)

            #clear screen
            screen.fill(black)

            # Process the events in the game
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    exit_program = True
                elif(event.type == pygame.KEYDOWN):
                    if(event.key == ord("a")):
                        player1.move("left")
                    if(event.key == ord("d")):
                        player1.move("right")
                    if(event.key == ord("j")):
                        player2.move("left")
                    if(event.key == ord("l")):
                        player2.move("right")

            #update ball if game is not over
            if (game_over == False):
                ball1.update()
                ball2.update()

            if game_over:
                text = font.render("Game Over", True, white)
                textpos = text.get_rect(centerx=background.get_width()/2)
                textpos.top = 300
                screen.blit(text, textpos)

            if (pygame.sprite.spritecollide(ball1, players, 0)):

                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff = (player1.rect.x + player1.width/2) - (ball1.rect.x+ball1.width/2)

                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball1.rect.y = screen.get_height() - player1.rect.height - ball1.rect.height - 1
                ball1.bounce(diff)

            if (pygame.sprite.spritecollide(ball2, players, 0)):
                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff = (player2.rect.x + player2.width/2) - (ball2.rect.x+ball2.width/2)

                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball2.rect.y = screen.get_height() - player2.rect.height - ball2.rect.height - 1
                ball2.bounce(diff)

            deadblocks1 = pygame.sprite.spritecollide(ball1, blocks1, True)
            deadblocks2 = pygame.sprite.spritecollide(ball2, blocks2, True)

            if len(deadblocks1) > 0:
                ball1.bounce(0)

            if len(deadblocks2) > 0:
                ball2.bounce(0)

            # Game ends if all the blocks are gone
            if (len(blocks1) == 0 or len(blocks2) == 0):
                game_over = True

            allsprites.draw(screen)

            pygame.display.flip()

        pygame.quit()


def main():
    game = Game()

main()
