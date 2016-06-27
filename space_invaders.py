"""
Author: Grando Eduardo Alejandro.
Name: Space invaders.
Created: 11-04-2014.
"""
import pygame

import random

class Brick(pygame.sprite.Sprite):
    """ This class represents the bricks """
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([65,20])
        self.image.fill((0,255,0))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullets """
    def __init__(self,direction):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4,10])
        self.image.fill((255,255,255))

        self.rect = self.image.get_rect()
        
        self.direction = direction

    def update(self):
        self.rect.y += self.direction
        

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    speed = 0

    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width,height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.x == 0 and self.speed < 0:
            self.speed = 0
        elif self.rect.x  == 615 and self.speed > 0:
            self.speed = 0

        self.rect.x += self.speed

class Invaders(pygame.sprite.Sprite):
    """ This class represents the space invaders. """
    timer = 0
    flag = True
    limit = ()
    change = 1
    attack = False
    col = 0
    ln = 0
    
    def __init__(self,filename_1,filename_2,score):
        pygame.sprite.Sprite.__init__(self)

        self.score = score

        self.images = []
               
        img = pygame.image.load(filename_1).convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)

        img = pygame.image.load(filename_2).convert()
        img.set_colorkey((0,0,0))
        self.images.append(img)

        self.image = self.images[0]

        self.rect = self.image.get_rect()

       
    def update(self):
        if self.timer == 10:
            self.rect.y += 1            
            self.change_image()
            self.timer = 0
        else:
            self.timer += 1

        if self.rect.x == self.limit[0] or self.rect.x == self.limit[1]:
            self.change *= -1

        self.rect.x += self.change

    def change_image(self):
        """ This will change the image every half a second. """
        if self.flag:
            self.image = self.images[1]
            self.flag = False
        else:
            self.image = self.images[0]
            self.flag = True

    def set_position(self,x,y):
        """ This will set the x and y position of the sprite """
        self.rect.x = x
        self.rect.y = y
        self.limit = (x - 60,x + 45)

    def game_over(self):
        """ This will return True when the game is over. """
        if self.rect.y >= 365:
            return True
        else:
            return False

    def start_attack(self,bullet_list,all_sprites_list):
        """ This will generates the bullets """
        if self.attack:
            if random.randrange(10) == 5:
                bullet = Bullet(10)
                bullet.rect.x = self.rect.x + 16
                bullet.rect.y = self.rect.y + 35
                bullet_list.add(bullet)
                all_sprites_list.add(bullet)

def check(block_list,col,ln):
    done = False

    while not done and ln < 5:
        ln += 1
        for block in block_list:
            if block.col == col and block.ln == ln:
                block.attack = True
                done = True
                

def create_invaders(block_list,all_sprites_list):
    """ This will create the space invaders and added to the lists """

    column = 0
    
    for i in range(60,610,55):
        block = Invaders('invaders_1.png','invaders_2.png',40)
        block.set_position(i,40)
        block.col = column
        block.ln = 5
        block_list.add(block)
        all_sprites_list.add(block)
        column += 1

    column = 0

    for i in range(60,600,54):
        block = Invaders('invaders_3.png','invaders_4.png',20)
        block.set_position(i,90)
        block.col = column
        block.ln = 4
        block_list.add(block)
        all_sprites_list.add(block)
        column += 1

    column = 0

    for i in range(60,600,54):
        block = Invaders('invaders_3.png','invaders_4.png',20)
        block.set_position(i,140)
        block.col = column
        block.ln = 3
        block_list.add(block)
        all_sprites_list.add(block)
        column += 1

    column = 0

    for i in range(60,600,54):
        block = Invaders('invaders_5.png','invaders_6.png',10)
        block.set_position(i,190)
        block.col = column
        block.ln = 2
        block_list.add(block)
        all_sprites_list.add(block)
        column += 1

    column = 0

    for i in range(60,600,54):
        block = Invaders('invaders_5.png','invaders_6.png',10)
        block.set_position(i,240)
        block.attack = True
        block.col = column
        block.ln = 1
        block_list.add(block)
        all_sprites_list.add(block)
        column += 1
    

def main():
    pygame.init()

    # Set the width and height of the screen [width, height]
    
    screen = pygame.display.set_mode([640,480])

    pygame.display.set_caption("Space Invaders")

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Sprite lists
    all_sprites_list = pygame.sprite.Group()
    block_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    brick_list = pygame.sprite.Group()

    # Sprites
    create_invaders(block_list,all_sprites_list)

    player = Player((255,0,0),25,25)
    player.rect.x = 300
    player.rect.y = 455

    all_sprites_list.add(player)

    for i in range(60,660,150):
        brick = Brick(i,400)
        brick_list.add(brick)
        all_sprites_list.add(brick)

    # Keep the score
    score = 0

    # Text
    font = pygame.font.Font("FreeSansBold.ttf",18)

    # Sounds
    laser_sound = pygame.mixer.Sound('laser.ogg')
    music_sound = pygame.mixer.Sound('music.ogg')

    flag = True

    game_over = False

    lives = 3
    
    timer = 0
    
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed = -5
                if event.key == pygame.K_RIGHT:
                    player.speed = 5
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # This will restart the game
                        all_sprites_list.empty()
                        if len(block_list) > 0:
                            block_list.empty()
                        if len(bullet_list) > 0:
                            bullet_list.empty()
                        brick_list.empty()

                        create_invaders(block_list,all_sprites_list)
                        player.rect.x = 300
                        player.rect.y = 455
                        all_sprites_list.add(player)
                        for i in range(60,660,150):
                            brick = Brick(i,400)
                            brick_list.add(brick)
                            all_sprites_list.add(brick)
                        flag = True
                        game_over = False
                        lives = 3
                        timer = 0
                        score = 0
                    else:
                        bullet = Bullet(-10)
                        bullet.rect.x = player.rect.x + 10
                        bullet.rect.y = 445
                        bullet_list.add(bullet)
                        all_sprites_list.add(bullet)

                        laser_sound.play()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.speed = 0
                if event.key == pygame.K_RIGHT:
                    player.speed = 0
                    
        # --- Game logic should go here
        if not game_over:
            for block in block_list:
                if block.game_over():
                    game_over = True

            if lives <= 0:
                game_over = True

            if score == 1000:
                game_over = True

            if flag:
                music_sound.play(-1)
                flag = False

            if done or game_over:
                music_sound.stop()
                
            all_sprites_list.update()

            if timer == 20:
                for block in block_list:
                    block.start_attack(bullet_list,all_sprites_list)
                timer = 0
            else:
                timer += 1
            
            for bullet in bullet_list:
                hit_sprites = pygame.sprite.spritecollide(bullet,block_list,True)
                if len(hit_sprites) > 0:
                    for block in hit_sprites:
                        bullet_list.remove(bullet)
                        all_sprites_list.remove(bullet)
                        if block.attack:
                            check(block_list,block.col,block.ln)
                        score += block.score

                elif bullet.rect.y < -10 or bullet.rect.y > 490:
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)

            text = font.render('Score = ' + str(score),True,(0,255,0))

            for bullet in bullet_list:
                hit_sprites = pygame.sprite.spritecollide(bullet,brick_list,False)
                if len(hit_sprites) > 0:
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)

            for bullet in bullet_list:
                if pygame.sprite.collide_rect(player,bullet):
                    lives -= 1
                    player.rect.x = 300
                    player.rect.y = 455
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)

            text_2 = font.render('Lives = ' + str(lives),True,(0,255,0))

        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill((0,0,0))
        # --- Drawing code should go here
        if not game_over:
            # draw all the sprites
            all_sprites_list.draw(screen)
            screen.blit(text,[5,5])
            screen.blit(text_2,[550,5])
        else:
            if score < 1000:
                text = font.render('Game Over, press <Space> to restart',True,(0,255,0))
                screen.blit(text,[180,230])
            else:
                text = font.render('You Won!, press <Space> to restart',True,(0,255,0))
                screen.blit(text,[180,230])
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 20 frames per second
        clock.tick(20)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

if __name__ == '__main__':
    main()
