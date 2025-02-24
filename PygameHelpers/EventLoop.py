import sys
from typing import Any, Callable
import pygame


class EventLoop:
    '''The principal event loop of the program. This is the home of everything that is executed during runtime'''
    def __init__(self, dimensions: tuple[float, float], name: str, background_colour: tuple[int, int, int] = (0, 0, 0)):
        pygame.init()
        pygame.font.init()
        self.curr_device = pygame.display.Info()
        self.width = self.curr_device.current_w * dimensions[0]
        self.height = self.curr_device.current_h * dimensions[1]
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(name)

        self.background_colour = background_colour
        self.backgrounds = [lambda : self.screen.fill(self.background_colour)]
        self.static_displays: list[Callable[[], None]] = []
        self.key_responses: dict[pygame.event.Event, Callable[[str], bool]] = {}
        self.FPS = pygame.time.Clock()

    def update(self, static_displays: list[Callable[[], None]] = [lambda : None], update: bool = True):
        '''Gameloop function. Used for statically updating the game display. 
        Same parameters as run()'''
        [background() for background in self.backgrounds]
        [display() for display in static_displays] 
        if update: pygame.display.flip()

    def run(self):
        '''Gamemainloop. Exits upon the submission of an input string to the game window, in which case it returns the string, or upon the closing of the game which results in an error and the termination of the program.
        Parameters:
         - static_displays: Optional parameter that provides a list of callables that will be called in mainloop. Used for adding Callables that display objects that will NOT respond to user input
         - editable_text_displays: Optional parameter that provides a list of callables that will be called in mainloop with the text the user has placed in (before submitting it) as input. Used to add Callables to add objects that will respond to user input, i.e. text input fields
         - key_responses: Optional parameter that specifies a dictionary of pygame constants and callables that will be executed when the corresponding key is pressed 
        '''
        ans: str = ''

        while True:
            self.update(static_displays=self.static_displays, update=False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit() #kills program
                 #i.e. if we get input

                action = self.key_responses.get(event)
                if action is not None: 
                    if action(event.key) == False:
                        return

            pygame.display.flip()
            self.FPS.tick(60)

    def add_background(self, background: Callable[[], Any]):
        self.backgrounds.append(background)
    def remove_background(self, background: Callable[[], Any]):
        if background in self.backgrounds:
            self.backgrounds.remove(background)

    def add_static_display(self, display: Callable[[], None]):
        self.static_displays.append(display)
    def remove_static_display(self, display: Callable[[], None]):
        if display in self.static_displays:
            self.static_displays.remove(display)
