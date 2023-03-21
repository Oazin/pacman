#-------------------------------------------------------------------------------
# Name:        Pac-Man
# Purpose:     Recreate the Pacman video game in Python
#
# Author:      Oazin
#
# Created:     03/09/2021
# Copyright:   (c) Oazin 2021
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#                                   Pac-Man
#-------------------------------------------------------------------------------


import pygame
import sys
import Liste_coordonnee
from random import randint


# Screen dimension
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 530

class Player(pygame.sprite.Sprite):
    # Class PacMan


    def __init__(self):
        """Constructor method of the PacMan class which initializes all the useful information"""
        super().__init__()

        self.life = 2
        self.score = 0
        self.ghost_est = 0
        self.image = pygame.image.load('assets/Pacman_sprites/Pacman_fill.png').convert_alpha()

        # Image open mouth
        self.img_r = pygame.image.load('assets/Pacman_sprites/Pacman_right.png').convert_alpha()
        self.img_l = pygame.image.load('assets/Pacman_sprites/Pacman_left.png').convert_alpha()
        self.img_u = pygame.image.load('assets/Pacman_sprites/Pacman_up.png').convert_alpha()
        self.img_d = pygame.image.load('assets/Pacman_sprites/Pacman_down.png').convert_alpha()

        # Image fill for PacMan animation
        self.animation = False
        self.cpt = 0
        self.img_fill_r = pygame.image.load('assets/Pacman_sprites/Pacman_fill_r.png').convert_alpha()
        self.img_fill_l = pygame.image.load('assets/Pacman_sprites/Pacman_fill_l.png').convert_alpha()
        self.img_fill_u = pygame.image.load('assets/Pacman_sprites/Pacman_fill_u.png').convert_alpha()
        self.img_fill_d = pygame.image.load('assets/Pacman_sprites/Pacman_fill_d.png').convert_alpha()

        self.invincible = 0

        # Rect for movement
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 226, 383
        self.change_x, self.change_y = 0, 0

    def update(self):
        """Update method that changes all necessary modifications"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.invincible != 0:
            self.invincible -= 1

        self.function_animation()
        if self.change_x > 0:
            if self.animation is True:
                self.image = self.img_r
            else:
                self.image = self.img_fill_r
        if self.change_x < 0:
            if self.animation is True:
                self.image = self.img_l
            else:
                self.image = self.img_fill_l
        if self.change_y > 0:
            if self.animation is True:
                self.image = self.img_d
            else:
                self.image = self.img_fill_d
        if self.change_y < 0:
            if self.animation is True:
                self.image = self.img_u
            else:
                self.image = self.img_fill_u


    def move_right(self):
        """Method that changes the values to go right"""
        self.change_x = 2
        self.change_y = 0

    def move_left(self):
        """Method that changes the values to go left"""
        self.change_x = -2
        self.change_y = 0

    def move_up(self):
        """Method that changes the values to go up"""
        self.change_y = -2
        self.change_x = 0

    def move_down(self):
        """Method that changes the values to go down"""
        self.change_y = 2
        self.change_x = 0

    def function_animation(self):
        """Pacman animation method which uses a nand (not and) to choose the annimation"""
        self.cpt += 1
        if self.cpt == 20:
            self.animation = not (self.animation and True)
            self.cpt = 0



class Wall(pygame.sprite.Sprite):

    def __init__(self, a, b, l, h):
        """Constructor method of the Wall class which initializes all walls to their coordinate"""
        super().__init__()

        self.image = pygame.Surface((l,h))
        self.image.fill((120,120,120))
        self.rect = self.image.get_rect()
        self.rect.x = a
        self.rect.y = b



class Power_Pellet(pygame.sprite.Sprite):

    def __init__(self, a, b):
        """Constructor method of the Power Pellet class which initializes all walls to their coordinate"""
        super().__init__()

        self.image = pygame.image.load('assets\Point_sprites\Power_pellet.png')
        self.rect = self.image.get_rect()
        self.rect.x = a
        self.rect.y = b
        self.point = 50

class Pac_Dot(pygame.sprite.Sprite):

    def __init__(self, a, b):
        """Constructor method of the Pac Dot class which initializes all walls to their coordinate"""
        super().__init__()

        self.image = pygame.image.load('assets\Point_sprites\Pac_dot.png')
        self.rect = self.image.get_rect()
        self.rect.x = a
        self.rect.y = b
        self.point = 10


class Ghosts(pygame.sprite.Sprite):

    def __init__(self,a, b, id):
        super().__init__()

        self.velocity = 2
        self.id = id

        # Initialize the image of the ghost according to its id
        dest = "assets\Ghost_sprites\{}\{}_{}.png"
        if self.id == 0:
            name = "Blinky"
            self.image = pygame.image.load(dest.format(name, name, "r_1")).convert_alpha()
        elif self.id == 1:
            name = "Pinky"
            self.image = pygame.image.load(dest.format(name, name, "r_1")).convert_alpha()
        elif self.id == 2:
            name = "Inky"
            self.image = pygame.image.load(dest.format(name, name, "r_1")).convert_alpha()
        elif self.id == 3:
            name = "Clyde"
            self.image = pygame.image.load(dest.format(name, name, "r_1")).convert_alpha()

        # Different image of the ghost to make the animation
        self.r_1 = pygame.image.load(dest.format(name, name, "r_1")).convert_alpha()
        self.r_2 = pygame.image.load(dest.format(name, name, "r_2")).convert_alpha()
        self.l_1 = pygame.image.load(dest.format(name, name, "l_1")).convert_alpha()
        self.l_2 = pygame.image.load(dest.format(name, name, "l_2")).convert_alpha()
        self.u_1 = pygame.image.load(dest.format(name, name, "u_1")).convert_alpha()
        self.u_2 = pygame.image.load(dest.format(name, name, "u_2")).convert_alpha()
        self.d_1 = pygame.image.load(dest.format(name, name, "d_1")).convert_alpha()
        self.d_2 = pygame.image.load(dest.format(name, name, "d_2")).convert_alpha()

        #Afraid ghost images
        self.afraid_b_1 = pygame.image.load("assets\Ghost_sprites\Afraid_ghost\Afraid_b_1.png").convert_alpha()
        self.afraid_b_2 = pygame.image.load("assets\Ghost_sprites\Afraid_ghost\Afraid_b_2.png").convert_alpha()
        self.afraid_w_1 = pygame.image.load("assets\Ghost_sprites\Afraid_ghost\Afraid_w_1.png").convert_alpha()
        self.afraid_w_2 = pygame.image.load("assets\Ghost_sprites\Afraid_ghost\Afraid_w_2.png").convert_alpha()
        self.afraid = 0

        #varibles for animations
        self.animation = False
        self.animation_2 = False
        self.cpt = 0

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = a, b

        self.change_x, self.change_y = 2, 0


    def update(self):
        """Update method that changes all necessary modifications"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        self.function_animation()
        # If Pacman eat Power pellet
        if self.afraid != 0:
            self.velocity = 1
            self.afraid -= 1
            if self.animation is True:
                self.image = self.afraid_b_1
            else:
                self.image = self.afraid_w_2

        # If not
        else:
            self.velocity = 2
            if self.change_x > 0:
                if self.animation is True:
                    self.image = self.r_1
                else:
                    self.image = self.r_2
            if self.change_x < 0:
                if self.animation is True:
                    self.image = self.l_1
                else:
                    self.image = self.l_2
            if self.change_y > 0:
                if self.animation is True:
                    self.image = self.d_1
                else:
                    self.image = self.d_2
            if self.change_y < 0:
                if self.animation is True:
                    self.image = self.u_1
                else:
                    self.image = self.u_2

    def move_right(self):
        """Method that changes the values to go right"""
        self.change_x = self.velocity
        self.change_y = 0

    def move_left(self):
        """Method that changes the values to go left"""
        self.change_x = -self.velocity
        self.change_y = 0

    def move_up(self):
        """Method that changes the values to go up"""
        self.change_y = -self.velocity
        self.change_x = 0

    def move_down(self):
        """Method that changes the values to go down"""
        self.change_y = self.velocity
        self.change_x = 0

    def function_animation(self):
        """Ghosts animation method which uses a nand (not and) to choose the annimation"""
        self.cpt += 1
        if self.cpt == 10:
            self.animation = not (self.animation and True)
            self.cpt = 0

def end_game():
    pass


def terminate():
    pygame.quit()
    sys.exit()


def main():

    # Screen initialization
    pygame.init()
    pygame.display.set_caption("Pac-man")
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)) # pygame.FULLSCREEN pygame.RESIZABLE
    background = pygame.image.load('assets/background.png')

    # Pacman initialization
    active_sprite = pygame.sprite.Group()
    player = Player()
    active_sprite.add(player)

    # Ghost initializations
    ghost_list = pygame.sprite.Group()
    for i in range(4):
        ghost = Ghosts(Liste_coordonnee.ghost_spawns[i][0],Liste_coordonnee.ghost_spawns[i][1],i)
        active_sprite.add(ghost)
        ghost_list.add(ghost)


    # Wall initializations
    wall_sprite_list = pygame.sprite.Group()
    for elmt in Liste_coordonnee.mur:
        wall=Wall(elmt[0], elmt[1], elmt[2], elmt[3])
        wall_sprite_list.add(wall)

    # Power pellet and Pac-Dot initializations
    point_sprite_list = pygame.sprite.Group()
    for elmt in Liste_coordonnee.pellet:
       power_pellet = Power_Pellet(elmt[0], elmt[1])
       point_sprite_list.add(power_pellet)

    for elmt in Liste_coordonnee.pac_dot:
       pacdot = Pac_Dot(elmt[0], elmt[1])
       point_sprite_list.add(pacdot)

    # Front and score image initialization
    myfont = pygame.font.SysFont("monospace", 16)
    score_image = pygame.image.load("assets\Score_image.png")


    while True:

        # Movements-------------------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.move_up()
                elif event.key == pygame.K_s:
                    player.move_down()
                elif event.key == pygame.K_d:
                    player.move_right()
                elif event.key == pygame.K_a:
                    player.move_left()
        #-----------------------------------------------------------------------

        clock = pygame.time.Clock()


        # Updating--------------------------------------------------------------
        active_sprite.update()
        score_display = myfont.render(str(player.score), True, (255,255,0))
        #-----------------------------------------------------------------------



        # Collision management--------------------------------------------------
        wall_hit_list = pygame.sprite.spritecollide(player, wall_sprite_list , False, False)
        for hit in wall_hit_list:
            if player.change_x > 0:
                player.rect.x -= 4
            if player.change_x < 0:
                player.rect.x += 4
            if player.change_y > 0:
                player.rect.y -= 4
            if player.change_y < 0:
                player.rect.y += 4
            player.change_y, player.change_x = 0, 0


        ghost_hit = pygame.sprite.groupcollide(active_sprite, wall_sprite_list , False, False)
        for hit in ghost_hit:
            if hit.change_x > 0:
                hit.rect.x -= 4
            if hit.change_x < 0:
                hit.rect.x += 4
            if hit.change_y > 0:
                hit.rect.y -= 4
            if hit.change_y < 0:
                hit.rect.y += 4
            hit.change_y, hit.change_x = 0, 0

            mv = randint(0,100)
            if mv < 25 :
                hit.move_right()
            if mv >= 25 and mv < 50:
                hit.move_up()
            if mv >= 50 and mv < 75:
                hit.move_down()
            if mv >= 75:
                hit.move_left()

        for ghost in ghost_list:
            for inter in Liste_coordonnee.intersection:
                if ghost.rect.x == inter[0] and ghost.rect.y == inter[1]:
                    ghost.change_y, ghost.change_x = 0, 0
                    mv = randint(0,100)
                    if mv < 25 :
                        ghost.move_right()
                    if mv >= 25 and mv < 50:
                        ghost.move_up()
                    if mv >= 50 and mv < 75:
                        ghost.move_down()
                    if mv >= 75:
                        ghost.move_left()


        # Management of collision between pacman and points, as well as management of pacman invincibility and ghost vulnerability
        point_hit_list = pygame.sprite.spritecollide(player, point_sprite_list , True)
        for hit in point_hit_list:
            point_sprite_list.remove(hit)
            player.score += hit.point
            if hit.point == 50:
                player.invincible = 400
                for sprite in active_sprite:
                    sprite.afraid = 400

        if player.invincible != 0: # When Pamcan is invincible
            hit_P2G = pygame.sprite.spritecollide(player, ghost_list, True, False)
            for hit in hit_P2G:
                id_g = hit.id
                player.score += 200
                active_sprite.add(Ghosts(Liste_coordonnee.ghost_spawns[id_g][0],Liste_coordonnee.ghost_spawns[id_g][1],id_g))
                ghost_list.add(Ghosts(Liste_coordonnee.ghost_spawns[id_g][0],Liste_coordonnee.ghost_spawns[id_g][1],id_g))

        else:   # When Pamcan is vulnerable
            hit_P2G = pygame.sprite.spritecollide(player, ghost_list, False)
            for hit in hit_P2G:
                player.life -= 1
                print(player.life)


        #-----------------------------------------------------------------------


        # Active sprites' teleportation-----------------------------------------
        for sprite in active_sprite:
            if sprite.rect.x == 476:
                sprite.rect.x = 1
            if sprite.rect.x == 0:
                sprite.rect.x = 475
        #-----------------------------------------------------------------------


        # Display---------------------------------------------------------------
        screen.fill((0,0,0))
        wall_sprite_list.draw(screen)
        screen.blit(background,(0,0))
        point_sprite_list.draw(screen)
        active_sprite.draw(screen)
        screen.blit(score_image, (510, 35))
        screen.blit(score_display, (510, 50))
        #-----------------------------------------------------------------------


        clock.tick(60)
        pygame.display.update()


if "__name__" == main():
    main()
