import pygame, os, time, random, json
from math import *
from pseudo import *
pygame.init()


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "Assets")


# functions to create our resources
def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pygame.mixer.Sound(fullname)

    return sound


if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")


class Arrow(pygame.sprite.Sprite):
    def __init__(self,state = 1 , speed = 1) -> None:
        super().__init__()
        self.image, self.rect = load_image(arrow_images[state], -1)
        self.image = pygame.transform.scale(self.image,(100,100))
        self.rect = self.image.get_rect()
        self.position = (state-1)*110 + 10
        self.rect.x = self.position
        self.speed = speed
        self.rect.y = FPS*10*self.speed - 30*self.speed + offset*self.speed
        if state != 0:
            self.image = pygame.transform.rotate(self.image, (ceil(-0.67*state**3 +4.5*state**2 - 7.85*state + 5))*90)#I really don't want to explain this
        else:
            print('uh oh')
            print((ceil(-0.67*((state%4)+1)**3 +4.5*((state%4)+1)**2 - 7.85*((state%4)+1) + 5)))
    def update(self):
        global score, combo
        self.rect.y += -1 * self.speed
        if self.rect.y < -120:
            self.kill()
            combo = 0
            score -= 30
            

class Player(pygame.sprite.Sprite):
    def __init__(self,state) -> None:
        super().__init__()
        self.image, self.rect = load_image('arrow.png',-1)
        self.rect.y = 30
        self.rect.x =(state-1)*110 + 10
        self.state = state
        if self.state != 0:
            self.image = pygame.transform.rotate(self.image, (ceil(-0.67*self.state**3 +4.5*self.state**2 - 7.85*self.state + 5))*90)#I really don't want to explain this
        else:
            print('uh oh')
            print((ceil(-0.67*((self.state%4)+1)**3 +4.5*((self.state%4)+1)**2 - 7.85*((self.state%4)+1) + 5)))
        self.scaled_image = pygame.transform.scale(self.image,(90,90))
    def press(self):
        global score, combo, highest_combo
        self.image = self.scaled_image
        self.rect = self.scaled_image.get_rect()
        self.rect.y = 30 + 15/2
        self.rect.x =(self.state-1)*110 + 10 +15/2
        collide = pygame.sprite.spritecollide(self,arrow_group,False,None)
        if len(collide) > 0:
            margin = abs(30- collide[0].rect.y)
            print((103- collide[0].rect.y))
            if margin < 20:
                score += 2*(103-margin)
                combo += 1
                if combo > highest_combo:
                    highest_combo = score
                collide[0].kill()
            elif margin < 80:
                score += 120 - margin
                combo = 0
                collide[0].kill()
        #for arrow in collide:
        #    margin = abs(30- arrow.rect.y)
        #    if margin < 20:    
        #        score += 2*(120-margin)
        #        combo += 1
        #        if combo > highest_combo:
        #            highest_combo = score
        #        arrow.kill()
        #    elif margin < 80:
        #        score += 120 - margin
        #        combo = 0
        #        arrow.kill()
    def unpress(self):
        self.image, self.rect = load_image('arrow.png',-1)
        self.rect.y = 30
        self.rect.x =(self.state-1)*110 + 10
        if self.state != 0:
            self.image = pygame.transform.rotate(self.image, (ceil(-0.67*self.state**3 +4.5*self.state**2 - 7.85*self.state + 5))*90)#I really don't want to explain this
        else:
            print('uh oh')
            print((ceil(-0.67*((self.state%4)+1)**3 +4.5*((self.state%4)+1)**2 - 7.85*((self.state%4)+1) + 5)))
        self.scaled_image = pygame.transform.scale(self.image,(90,90))
        pass




##### Colours #####
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
BLUE = (0,   0, 255)

#SCREEN INITIALISATION

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("")
pygame.mouse.set_visible(True)
######             #######
def draw_text(text, size, x, y,Method = 'topleft'):
    font = pygame.font.Font(os.path.join(data_dir,'8-BIT WONDER.TTF'),size)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    if Method == 'center':
        text_rect.center = (x,y)
    else:
        text_rect.topleft = (x,y)
    screen.blit(text_surface,text_rect)
    
def main_menu():
    global state, song_number
    menu_font = pygame.font.Font(os.path.join(data_dir,'8-BIT WONDER.TTF'), 30)
    clock = pygame.time.Clock()
    run = True
    pressed_up,pressed_down,pressed_enter,pressed_esc, pressed_left, pressed_right = [False]*6
    current_screen = 0
    state = 'menu'
    cursor_postion = 0
    song_number = 0
    cursor_position_list = [[400,450,500],[]]
    left, left_rect = load_image('menuleft.png',-1,1)
    right, left_rect = load_image('menuleft.png',-1,1)
    right = pygame.transform.rotate(right, 180)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run ,state, = False, 'quit'
                break
        screen.fill(BLACK)
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            if pressed_up == False:
                pressed_up = True
                #print('left')
                cursor_postion = (cursor_postion-1)%3
        else:
            if pressed_up == True:
                pressed_up = False
        if keystate[pygame.K_DOWN]:
            if pressed_down == False:
                pressed_down = True
                cursor_postion = (cursor_postion+1)%3
        else:
            if pressed_down == True:
                pressed_down = False
        if keystate[pygame.K_ESCAPE]:
            if pressed_esc == False:
                pressed_esc = True
                if state == 'menu':
                    state = 'quit'
                    break
                else:
                    state = 'menu'
                    current_screen = 0
                    cursor_postion = previous_cursor
        else:
            if pressed_esc == True:
                pressed_esc = False
        if keystate[pygame.K_RETURN]:
            if pressed_enter == False:
                pressed_enter = True
                if state == 'menu':
                    if cursor_postion == 0:
                        current_screen = 1
                        state = 'level'
                        previous_cursor = cursor_postion
                        cursor_postion = 0
                    elif cursor_postion == 1:
                        current_screen = 2
                        state = 'how'
                        previous_cursor = cursor_postion
                        cursor_postion = 0
                    elif cursor_postion == 2:
                        current_screen = 3
                        state = 'credits'
                        previous_cursor = cursor_postion
                        cursor_postion = 0
                elif state == 'level':
                    state = 'start'
                    break
        else:
            if pressed_enter == True:
                pressed_enter = False
        if keystate[pygame.K_RIGHT]:
            if pressed_right == False:
                pressed_right = True
                song_number = (song_number+1)%6
        else:
            if pressed_right == True:
                pressed_right = False
        if keystate[pygame.K_LEFT]:
            if pressed_left == False:
                pressed_left = True
                song_number = (song_number-1)%6
        else:
            if pressed_left == True:
                pressed_left = False
        if state == 'menu':
            draw_text('Arrow', 50, SCREEN_WIDTH/2, 100,'center')
            draw_text('Apocalypse', 40, SCREEN_WIDTH/2, 150,'center')
            draw_text('Song Select', 30,100, 400,'topleft')
            draw_text('How to Play', 30,100, 450,'topleft')
            draw_text('Credits', 30,100, 500,'topleft')
            draw_text('*', 30,55, [400,450,500][cursor_postion])
        elif state == 'level':
            draw_text('Level', 50, SCREEN_WIDTH/2, 100,'center')
            draw_text('Selection', 40, SCREEN_WIDTH/2, 150,'center')
            with open(os.path.join(data_dir, 'songs.json'), "r") as read_file:
                data = json.load(read_file)
            if type(data) != list:
                song_data = [item for item in data['songs']]  
            else:
                song_data = data
            song_name_list, highscore_list = [],[]
            for i in song_data:
                song_name_list.append(i['name'])
                highscore_list.append(i['highscore'])
            #workinghere
            draw_text(str(song_name_list[song_number]), 40, SCREEN_WIDTH/2, 250,'center')
            
            draw_text('highscore', 50, SCREEN_WIDTH/2, 450,'center')
            draw_text(str(highscore_list[song_number]), 50, SCREEN_WIDTH/2, 500,'center')
            
            screen.blit(left,(-40,SCREEN_WIDTH/2))
            screen.blit(right,(350,SCREEN_WIDTH/2))
            
        elif state == 'how':
            draw_text('How to play', 40, SCREEN_WIDTH/2, 100,'center')
            draw_text('Press the corresponding ', 15,20, 450+100,'topleft')
            draw_text('arrow when an arrow is  ', 15,20, 470+100,'topleft')
            draw_text('on top of it ', 15,20, 490+100,'topleft')
        elif state == 'credits':
            draw_text('Credits', 50, SCREEN_WIDTH/2, 100,'center')
            draw_text('Made by Me', 30,SCREEN_WIDTH/2, 250,'center')

        
        pygame.display.flip()
    pass
state = 'menu'
def playing(song_number):
    global score, state
    if state =='quit':
        return
    screen = pygame.display.set_mode(size)
    with open(os.path.join(data_dir, 'songs.json'), "r") as read_file:
        data = json.load(read_file)
    if type(data) != list:
        song_data = [item for item in data['songs']]  
    else:
        song_data = data
    current_song_data = song_data[int(song_number)]
    song_name, song_file,mpb,beats,seed,speed_single,speed_double,offset,highscore = list(current_song_data.values())
    print('Now playing '+ song_name)
    run = True
    counter = 0
    start_time = time.time()
    current_beat = 0
    score = 0
    combo = 0
    highest_combo = 0
    player_list = []
    pressed_left,pressed_up,pressed_down,pressed_right = False,False,False,False
    seed = pseudo(seed)
    current_song = load_sound(song_file)
    arrow_images = [0,'b.png','d.png','c.png','e.png']
    arrow_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    current_song.play()
    for i in range(1,5):
        player = Player(i)
        player_group.add(player)
        player_list.append(player)
    score_font = pygame.font.Font(os.path.join(data_dir,'Rowdies-Regular.ttf'), 30)
    globals().update(locals())
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                #print('click')
                pass
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                if pressed_left == False:
                    pressed_left = True
                    #print('left')
                    player_list[0].press()
            else:
                if pressed_left == True:
                    pressed_left = False
                    player_list[0].unpress()

            if keystate[pygame.K_DOWN]:
                if pressed_down == False:
                    pressed_down = True
                    #print('down')
                    player_list[1].press()
            else:
                if pressed_down == True:
                    pressed_down = False
                    player_list[1].unpress()
            if keystate[pygame.K_UP]:
                if pressed_up == False:
                    pressed_up = True
                    #print('up')
                    player_list[2].press()
            else:
                if pressed_up == True:
                    pressed_up = False
                    player_list[2].unpress()
            if keystate[pygame.K_RIGHT]:
                if pressed_right == False:
                    pressed_right = True
                    #print('right')
                    player_list[3].press()
            else:
                if pressed_right == True:
                    pressed_right = False
                    player_list[3].unpress()
        # Game logic here\
        current_time = (time.time()- start_time)*1000
        if counter < beats:
            if current_time > (int(current_beat) + int(mpb)):
                counter += 1
                current_beat = int(counter)*int(mpb)#, trying this for uneven bpms
                arrow_state = (seed[counter-1]) % 28
                if 0 < arrow_state <= 24:
                    arrow = Arrow((arrow_state%4)+1,speed_single)
                    arrow_group.add(arrow)
                elif arrow_state == 25:
                    arrow_group.add(Arrow(1,speed_double))
                    arrow_group.add(Arrow(2,speed_double))
                elif arrow_state == 26:
                    arrow_group.add(Arrow(2,speed_double))
                    arrow_group.add(Arrow(3,speed_double))
                elif arrow_state == 27:
                    arrow_group.add(Arrow(3,speed_double))
                    arrow_group.add(Arrow(4,speed_double))
                elif arrow_state != 0:
                    print(arrow_state)
        else:
            if len((arrow_group.sprites())) == 0:
                print('highest combo ' + str(highest_combo))
                print('score" ' + str(score))
                if score > int(highscore):
                    print('You beat the high score!')
                    highscore = int(score)
                    with open(os.path.join('Assets\songs.json'), "r") as read_file:
                        data = json.load(read_file)
                    if type(data) != list:
                        song_data = [item for item in data['songs']]  
                    else:
                        song_data = data
                    song_data[0]['highscore'] = highscore
                    with open('Assets\songs.json', 'w') as f: 
                        json.dump(song_data, f)
                screen.fill(BLACK)
                draw_text(f'score:{score}', 40, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                draw_text(f'highscore:{highscore}', 40, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
                screen.blit(text,textpos)
                pygame.display.flip()
                time.sleep(2)
                run = False

        arrow_group.update()
        ####    DRAWING    ######
        screen.fill(BLACK)
        arrow_group.draw(screen)
        player_group.draw(screen)
        text = score_font.render(f'Score: {score}',True,WHITE)
        textpos = text.get_rect(x=20,y=SCREEN_HEIGHT-50)
        screen.blit(text,textpos)
        pygame.display.flip()
    current_song.stop()
while state != 'quit':
    main_menu()
    playing(song_number)
#song_number = int(input('Song number 0-4: '))
song_number = random.randint(0,6)
playing(song_number)
pygame.quit()