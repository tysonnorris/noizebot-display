import pygame as pg
import sys
import io
from spotify import Spotify
from threading import Timer
import requests

pg.init()

class Control:
    def __init__(self):
        self.done = False
        self.fps = 5
        self.screen = pg.display.set_mode((320,240))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    def flip_state(self):
        self.state.done = False
        previous,self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.state.get_event(event)
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps)/1000.0
            self.event_loop()
            self.update(delta_time)
            pg.display.update()

class MenuManager:
    def __init__(self):
        self.selected_index = 0
        self.last_option = None
        self.selected_color = (255,255,0)
        self.deselected_color = (255,255,255)

    def draw_menu(self, screen):
        '''handle drawing of the menu options'''
        for i,opt in enumerate(self.rendered["des"]):
            centery = self.from_bottom+i*self.spacer
            opt[1].center = (self.screen_rect.centerx, centery)
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                screen.blit(opt[0],opt[1])

    # def update_menu(self):
        # self.mouse_hover_sound()
        # self.change_selected_option()

    def get_event_menu(self, event):
        if event.type == pg.KEYDOWN:
            '''select new index'''
            print("check for offscreen")
            if event.key in [pg.K_UP, pg.K_w]:
                self.change_selected_option(-1)
            elif event.key in [pg.K_DOWN, pg.K_s]:
                self.change_selected_option(1)

            elif event.key == pg.K_RETURN:
                self.select_option(self.selected_index)
        self.mouse_menu_click(event)

    def mouse_hover_sound(self):
        '''play sound when selected option changes'''
        for i,opt in enumerate(self.rendered["des"]):
            if opt[1].collidepoint(pg.mouse.get_pos()):
                if self.last_option != opt:
                    self.last_option = opt
    def mouse_menu_click(self, event):
        '''select menu option '''
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i,opt in enumerate(self.rendered["des"]):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
                    self.select_option(i)
                    break
    def pre_render_options(self):
        '''setup render menu options based on selected or deselected'''
        font_deselect = pg.font.SysFont("arial", 50)
        font_selected = pg.font.SysFont("arial", 70)

        rendered_msg = {"des":[],"sel":[]}
        for option in self.options:
            d_rend = font_deselect.render(option, 1, self.deselected_color)
            d_rect = d_rend.get_rect()
            s_rend = font_selected.render(option, 1, self.selected_color)
            s_rect = s_rend.get_rect()
            rendered_msg["des"].append((d_rend,d_rect))
            rendered_msg["sel"].append((s_rend,s_rect))
        self.rendered = rendered_msg

    def select_option(self, i):
        '''select menu option via keys or mouse'''
        if i == len(self.next_list):
            self.quit = True
        else:
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0

    def change_selected_option(self, op=0):
        '''change highlighted menu option'''
        # for i,opt in enumerate(self.rendered["des"]):
        #     if opt[1].collidepoint(pg.mouse.get_pos()):
        #         self.selected_index = i
        if op:
            self.selected_index += op
            max_ind = len(self.rendered['des'])-1
            if self.selected_index < 0:
                self.selected_index = max_ind
            elif self.selected_index > max_ind:
                self.selected_index = 0

class States(Control):
    def __init__(self, closeOnTimer=True):
        Control.__init__(self)
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None
        self.timer = None
        self.closeOnTimer = closeOnTimer
    def startup(self):
        if self.closeOnTimer:
            self.reset()

    def spotifycontrols(self):
        self.done = True

    def reset(self):
        #timer to jump back to spotify
        if self.timer != None:
            self.timer.cancel()
        self.timer = Timer(5, self.spotifycontrols)
        self.timer.start()

class SpotifyControls(States):
    def __init__(self, s):
        States.__init__(self, False)
        self.next = 'spotifycontrols'
        self.from_bottom = 20
        self.spacer = 75
        self.selected_color = (0,0,0)
        self.playing = False
        self.spotify = s
        self.art = None
        self.updateDisplay = True
    def cleanup(self):
        print('cleaning up SpotifyControls state stuff')
    def startup(self):
        super().startup()
        print('starting SpotifyControls state stuff')
        self.updateDisplay = True
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN or event.key == pg.K_UP:
                self.next = "volume"
                self.done = True
            elif event.key == pg.K_SPACE:
                self.togglePlay()
                self.updateDisplay = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            self.next = "options"
            self.done = True
        elif event.type == pg.QUIT:
            self.quit = True
    def togglePlay(self):
        self.spotify.togglePlay()
        self.updateDisplay = True
    def update(self, screen, dt):
        if spotify.art != self.art:
            print("changing art to ", spotify.art)
            self.art = spotify.art
            self.updateDisplay = True

        self.draw(screen)
    def draw(self, screen):
        if self.updateDisplay:
            self.updateDisplay = False #stop updating
            screen.fill((0,0,255))
            if self.art != None:
                image_url = self.art
                image_req = requests.get(image_url)
                # create a file object (stream)
                image_file = io.BytesIO(image_req.content)
                image = pg.image.load(image_file)
                screen.blit(image, (0, 0))
            font_selected = pg.font.SysFont("arial", 70)
            msg = "Playing" if self.spotify.playing else "Paused"
            s_rend = font_selected.render(msg, 1, self.selected_color)
            s_rect = s_rend.get_rect()
            screen.blit(s_rend, s_rect)

class Volume(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'spotifycontrols'
        self.from_bottom = 20
        self.spacer = 75
        self.selected_color = (0,0,0)
        self.volume = 50
    def cleanup(self):
        print('cleaning up Volume state stuff')
    def startup(self):
        super().startup()
        print('starting Volume state stuff')


    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.reset()
            if event.key == pg.K_DOWN:
                if self.volume >= 5:
                    self.volume -= 5
            if event.key == pg.K_UP:
                if self.volume <= 95:
                    self.volume += 5

    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))
        font_selected = pg.font.SysFont("arial", 70)
        s_rend = font_selected.render("Volume is "+str(self.volume), 1, self.selected_color)
        s_rect = s_rend.get_rect()
        screen.blit(s_rend, s_rect)


class Menu(States, MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = 'spotifycontrols'
        self.options = ['Play', 'Options', 'Quit']
        self.next_list = ['game', 'options']
        self.pre_render_options()
        self.from_bottom = 20
        self.spacer = 75
    def cleanup(self):
        print('cleaning up Main Menu state stuff')
    def startup(self):
        super().startup()
        print('starting Main Menu state stuff')
    def get_event(self, event):
        self.reset()
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)
    def update(self, screen, dt):
        # self.update_menu()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
        self.draw_menu(screen)

class Options(States, MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)

    def cleanup(self):
        print('cleaning up Options state stuff')
    def startup(self):
        print('starting Options state stuff')
        self.next = 'spotifycontrols'
        self.options = ['Playlist', 'Sound/EQ', 'Display', 'System']
        self.next_list = ['playlists', 'options', 'display', 'system']
        self.from_bottom = 20
        self.spacer = 75
        self.deselected_color = (150,150,150)
        self.selected_color = (0,0,0)
        self.pre_render_options()
        self.done = False
        super().startup()
    def get_event(self, event):
        self.reset()
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)
    def update(self, screen, dt):
        # self.update_menu()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
        self.draw_menu(screen)

class Display(States, MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)

    def cleanup(self):
        print('cleaning up Display state stuff')
    def startup(self):
        print('starting Display state stuff')
        self.next = 'spotifycontrols'
        self.options = ['Show Artwork', 'Enable LEDs', 'Enable Second Display']
        self.next_list = ['spotifycontrols', 'spotifycontrols', 'spotifycontrols']
        self.from_bottom = 20
        self.spacer = 75
        self.deselected_color = (150,150,150)
        self.selected_color = (0,0,0)
        self.pre_render_options()
        self.done = False
        super().startup()
    def get_event(self, event):
        self.reset()
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)
    def update(self, screen, dt):
        # self.update_menu()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
        self.draw_menu(screen)

class System(States, MenuManager):
    def __init__(self):
        States.__init__(self)
        MenuManager.__init__(self)

    def cleanup(self):
        print('cleaning up System state stuff')
    def startup(self):
        print('starting System state stuff')
        self.next = 'spotifycontrols'
        self.options = ['Spotify User', 'Restart', 'Reset']
        self.next_list = ['spotifycontrols', 'spotifycontrols', 'spotifycontrols']
        self.from_bottom = 20
        self.spacer = 75
        self.deselected_color = (150,150,150)
        self.selected_color = (0,0,0)
        self.pre_render_options()
        self.done = False
        super().startup()
    def get_event(self, event):
        self.reset()
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)
    def update(self, screen, dt):
        # self.update_menu()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
        self.draw_menu(screen)


class Playlists(States, MenuManager):
    def __init__(self, s):
        States.__init__(self)
        MenuManager.__init__(self)
        self.next = 'spotifycontrols'
        self.spotify = s
    def cleanup(self):
        print('cleaning up Playlists state stuff')
    def startup(self):
        print('starting Playlists state stuff')
        #self.options = ['Playlist1', 'Playlist2', 'Playlist3']
        self.playlists = self.spotify.getPlaylists()
        #convert to array of strings
        self.options = []
        for p in self.playlists:
            self.options.append(p['name'])

        self.next_list = ['spotifycontrols'] * len(self.playlists)
        #self.next_list = ['spotifycontrols', 'spotifycontrols', 'spotifycontrols']
        self.from_bottom = 20
        self.spacer = 75
        self.deselected_color = (150,150,150)
        self.selected_color = (0,0,0)
        self.pre_render_options()
        self.done = False
        super().startup()
    def get_event(self, event):
        self.reset()
        if event.type == pg.QUIT:
            self.quit = True
        self.get_event_menu(event)
    def update(self, screen, dt):
        # self.update_menu()
        self.draw(screen)
    def draw(self, screen):
        screen.fill((255,0,0))
        self.draw_menu(screen)
    def select_option(self, i):
        print("selected playlist", self.options[i])
        self.next = self.next_list[i]
        self.done = True
        self.selected_index = 0

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'menu'
    def cleanup(self):
        print('cleaning up Game state stuff')
    def startup(self):
        print('starting Game state stuff')
        super().startup()
    def get_event(self, event):
        self.reset()
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN:
            self.done = True
    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,255))

app = Control()
spotify = Spotify()
state_dict = {
    'spotifycontrols': SpotifyControls(spotify),
    'playlists': Playlists(spotify),
    'volume': Volume(),
    'display': Display(),
    'system': System(),
    'menu': Menu(),
    'game': Game(),
    'options':Options()
}
app.setup_states(state_dict, 'spotifycontrols')
app.main_game_loop()
pg.quit()
sys.exit()