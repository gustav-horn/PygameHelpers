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
        self.key_responses: list[Callable[[pygame.event.Event], bool]] = []
        self.FPS = pygame.time.Clock()

    def update(self, update: bool = True):
        '''Gameloop function. Used for statically updating the game display. 
        Same dependencies as run(). 
        Parameters:
            - update: bool that determines whether the function should update the screen itself. Leave False if you don't need the screen to change immediately to prevent flicker
        '''
        [background() for background in self.backgrounds]
        [display() for display in self.static_displays] 
        if update: pygame.display.flip()

    def run(self):
        '''Gamemainloop. Exits upon the submission of an input string to the game window, in which case it returns the string, or upon the closing of the game which results in an error and the termination of the program.
        Uses:
         - backgrounds: Parameter that provides a list of backgrounds that will be activated.
         - static_displays: Parameter that provides a list of callables that will be called in mainloop. Used for adding Callables that display objects that will NOT respond to user input
         - key_responses: Parameter that specifies a list of callables that will be executed when a pygame event occurs. All callables must return a boolean which determines if the run() function will continue or end, passing control back to the programmer. It is the RESPONSIBILITY of each callable to filter the events.
        '''
        ans: str = ''

        while True:
            self.update(update=False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit() #kills program

                for action in self.key_responses:
                    if action(event) == False:
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

    def add_key_response(self, response: Callable[[pygame.event.Event], bool]):
        self.key_responses.append(response)
    def remove_key_response(self, response: Callable[[pygame.event.Event], bool]):
        if response in self.key_responses:
            self.key_responses.remove(response)
