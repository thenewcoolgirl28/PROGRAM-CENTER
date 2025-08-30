# A FLASHCARD APP.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# IMPORTS
import pygame as pg
import sys, Fonts

pg.init()

# CONSTANTS
WIDTH,HEIGHT = 800,600

# COLORS
RED = 255,0,0
BLUE = 0,0,255
GREEN = 0,255,0
PINK = 255,0,255
BLACK = 0,0,0
WHITE = 255,255,255


running = True
answer = False
button_up = False
button_here = False
edit_mode = False
edited = False


# FONTS
FONT_NAMES = ["LucySaid.ttf", "AnandaBlack.ttf", "RandomWednesday.ttf"]

Audio = pg.mixer.music.load("Sonder.mp3")

papaflik = "dry-leaves-rustling.mp3"
pg.mixer.music.play(-1)

# DISPLAY
q = 0
screen = pg.display.set_mode((WIDTH, HEIGHT))
Edit_button = pg.image.load("icons\\Button4.png").convert()
pg.display.set_caption('Flashcardiom')

shortcuts =[pg.K_TAB, pg.K_INSERT, pg.K_ESCAPE, pg.K_PAGEUP, pg.K_PAGEDOWN, pg.K_NUMLOCK, pg.K_HOME, pg.K_LSHIFT, pg.K_RSHIFT, pg.K_LALT, pg.K_RALT]
clock = pg.time.Clock()



color = WHITE
rquest = open('Questions.txt', 'r+')
rans = open('Answers.txt', 'r+')



user_text = ''

class Text():
    def __init__(s, surface, x, y, size, txt):
        s.size = size


        #s.txt = txt

        s.update(txt)



        if x == 'middle':
            s.rect.x = (surface.get_width() // 2) - (s.txtw // 2)
        if y == 'middle':
            s.rect.y = (surface.get_height() // 2) - (s.txth // 2)
        else:
            s.rect.x = x
            s.rect.y = y


    def line_splitter(s):
        if isinstace(s.text.split(), list):
            line = s.text.split('\n')


    def update(s, txt):
        s.txt = txt
        s.font = pg.font.Font(f'Fonts\\{FONT_NAMES[2]}', s.size)
        if isinstance(s.txt, list) is False:
            s.txtsurf = s.font.render(s.txt, False, BLACK)
        else:
            s.txtsurf = s.font.render(s.txt[q], False, BLACK)
        s.rect = s.txtsurf.get_rect()
        s.txtw = s.rect.width
        s.txth = s.txtsurf.get_height()


class Spritesheet():
    def __init__(s, surface):
        s.sheet = pg.image.load(surface).convert()

    def get_sprite(s, x, y, width, height, colorkey=None):
        sprite = pg.Surface([width, height])
        sprite.blit(s.sheet, (0,0), (x, y,width, height))
        sprite.set_colorkey(colorkey)
        return sprite


class Mode():
    def __init__(s):
        s.questions = rquest.read().split('(/)')
        s.answers = rans.read().split('(/)')

        s.file = s.questions
        s._edit_mode = edit_mode
        s._answer_mode = answer
        s._user_text = user_text
        s._file = s.file

    @property
    def edit_mode(s):
        return s._edit_mode

    @edit_mode.setter
    def edit_mode(s, value):
        s._edit_mode = value

    @property
    def answer_mode(s):
        return s._answer_mode

    @answer_mode.setter
    def answer_mode(s, value):
        s._answer_mode = value

    @property
    def file(s):
        return s._file

    @file.setter
    def file(s, value):
        s._file = value

    @property
    def user_text(s):
        return s._user_text

    @user_text.setter
    def user_text(s, value):
        s._user_text = value
mode = Mode()
if mode.answer_mode is True:
#    mode.file = answers
    mode.user_text = mode.file[q]

class Button():
    def __init__(s, surface, directions=None):
        s.plate = Spritesheet("icons\\Button4.png").get_sprite(0, 0, 359, 131, WHITE)
        s.image = s.plate
        s.rect = s.image.get_rect()
        pg.sprite.Sprite.__init__(s)

        if directions is not None:
            x = directions[0]
            y = directions[1]
            if x == 'middle':
                s.rect.x = (surface.get_width() // 2) - 359//2
            if y == 'middle':
                s.rect.y = (surface.get_height() // 2) - (s.image.get_height() // 2)


    def button_click(s,pos, pressed):
        if s.rect.collidepoint(pos):
            s.image = Spritesheet("icons\\Button4.png").get_sprite(364, 0, 359, 131, WHITE)
            if pressed:
                mode.edit_mode = True
                return True
            return False
        else:
            s.image = Spritesheet("icons\\Button4.png").get_sprite(0, 0, 359, 131, WHITE)
        return False
button = Button(screen)
button.rect.x, button.rect.y = WIDTH,HEIGHT
def filey():

    for idx in mode.file[q]: # repeat times
        if mode.answer_mode is False:
            rquest.seek(idx)
            rquest.write(mode.user_text)
            rquest.flush()

        if mode.answer_mode is True:

            rans.seek(idx)
            rans.write(mode.user_text)
            rans.flush()


    text = mode.file[q]
    txt = Text(screen, 'middle', 'middle', 30, text)
    return txt

def draw():

    if mode._edit_mode is True:

        txt = filey()
    else:

        txt = Text(screen, 'middle', 'middle', 30, mode.file)
    counter = Text(screen, 770, 0, 30, f'{q+1}')
    screen.fill(color)
    button.button_click(mouse_pos, pg.mouse.get_pressed()[0])
    screen.blit(txt.txtsurf, txt.rect)
    screen.blit(counter.txtsurf, counter.rect)
    screen.blit(button.image, button.rect, (0, 0, 359, 130))

while running:
    mouse_pos = pg.mouse.get_pos()
    #filey(WHITE, user_text, file)
    if mode.answer_mode is True:
        color = BLUE
        mode.file = mode.answers

    if not mode.answer_mode:
        color = WHITE
        mode.file = mode.questions
    print(mode.user_text)
    print(mode.file[q])
    #print(button.rect.y, '', button.rect.x)
    draw()
    if (button.rect.x > (WIDTH-359)):
        button.rect.x -= 1.5

    if (button.rect.y > (HEIGHT-Edit_button.get_height()-30)) and button_up is True:
        button.rect.y -= 1

    if (button.rect.x != (WIDTH-359)) and (button.rect.y != (HEIGHT-Edit_button.get_height()-30)) and button_here is True:
        button.rect.x = (WIDTH-359)
        button.rect.y = (HEIGHT-Edit_button.get_height()-30)

    if button.rect.x <= (WIDTH-359) and button.rect.y <= (HEIGHT-Edit_button.get_height()-30):
        button_here = True
        button_up = False

    if q < -3:
        q = -3
        #mode.user_text.join(mode.file[q],mode.user_text)
    elif q > 3:
        q = 3
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEMOTION:

            if button_up is False and button_here is False:
                button_up = True
        if mode.answer_mode is True and q >= len(mode.answers):
            q = len(mode.answers) - 1

        if event.type == pg.KEYDOWN:
            if mode.edit_mode is True:
                edited = True
            key = pg.key.get_pressed()
            if mode.edit_mode is True:
                pass
            if key[pg.K_BACKSPACE] or (event.unicode in shortcuts):
                mode.user_text = mode.user_text[:-1]
            else:
                if len(mode.user_text) < len(mode.file[q][:-1]):
                    mode.user_text += event.unicode


            if key[pg.K_TAB]:
                mode.answer_mode = not mode.answer_mode
                #pg.mixer.Sound(papaflik).play(0)
            if key[pg.K_ESCAPE]:
                mode.edit_mode = False
                mode.user_text = ''
            if key[pg.K_RIGHT]:
                if mode.answer_mode is False:
                   if q < len(mode.questions) -1 and q >= -len(mode.questions):
                        q += 1
                if mode.answer_mode is True and isinstance(mode.answers, list):
                    if q < len(mode.answers) - 1 and q >= -len(mode.answers):
                        q += 1
                mode.user_text = ''
            if key[pg.K_LEFT]:
                if mode.answer_mode is False:
                    if q > -len(mode.questions) +1 and q <= len(mode.questions) - 1:
                        q -= 1
                if mode.answer_mode is True and isinstance(mode.answers, list):
                    if q > -len(mode.answers) and q <= len(mode.answers) - 1:
                        q -= 1
                mode.user_text = ''

            elif key[pg.K_SPACE]:
                if mode.edit_mode is False:
                    mode.user_text = ''
                    mode.answer_mode = not mode.answer_mode
                    pg.mixer.Sound(papaflik).play(0)
    pg.display.flip()
    clock.tick(60)
pg.quit()
sys.exit()