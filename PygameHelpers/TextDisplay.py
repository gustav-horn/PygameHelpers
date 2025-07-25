

from dataclasses import dataclass
from typing import Callable, Optional, TypeVar
from functools import reduce
from .Alignment import Alignment
import pygame

type coordsOrAlignment = tuple[float, float] | Callable[[pygame.Surface, pygame.Surface], tuple[float, float]]

T = TypeVar("T")
def optionalUnpack(value: Optional[T], default: T) -> T:
    if value is None:
        return default
    else:
        return value

class TextDisplay:
    '''A collection of helper functions for displaying messages in pygame'''

    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, colour: tuple):
        self.screen = screen
        self.font = font
        self.colour = colour


    def displayLine(self, message: str, alignment: Alignment, new_font: Optional[pygame.font.Font] = None, new_colour: Optional[tuple] = None) -> Callable[[], None]:
        '''Returns callable that displays single line of text on screen'''
        font: pygame.font.Font = optionalUnpack(new_font, self.font)
        colour: tuple = optionalUnpack(new_colour, self.colour)
        def talk() -> None:
            line = font.render(message, True, colour)
            start_position = alignment.get_coords(line, self.screen)
            self.screen.blit(line,start_position)
        return talk


    def displayMultipleLines(self, message: list[str], alignment: Alignment, new_font: Optional[pygame.font.Font] = None, new_colour: Optional[tuple] = None) -> Callable[[], None]:
        '''Returns function that displays multiple lines of text cascading down a window. Use if displayLine() is going off the screen'''
        font: pygame.font.Font = optionalUnpack(new_font, self.font)
        colour: tuple = optionalUnpack(new_colour, self.colour)
        def talk() -> None:
            line_no = 0
            diff = int(self.screen.get_width() * 0.8/font.size('a')[0]) #number of characters that can fit on 80% of the screen's width
            height = font.get_height()
            interim: pygame.Surface = pygame.Surface((
                min(diff, sum([len(i) for i in message], 0))*self.font.size('a')[0]*0.8, #width required (width of window or width taken up by the text, whichever is smaller)
                reduce(lambda curr, new: curr + len(range(0, len(new), diff)), message, 0)*height #height required (number of lines in message * height)
                ))
            start_position = alignment.get_coords(interim, self.screen)
            for item in message:
                strings = [item[start:start+diff] for start in range(0, len(item), diff)]
                for segment in strings:
                    line = font.render(segment, True, colour)
                    self.screen.blit(line,(start_position[0], start_position[1] + height*line_no))
                    line_no+=1
        return talk
                

    def request_prompt(self, message: str, alignment: Alignment, new_font: Optional[pygame.font.Font] = None, new_colour: Optional[tuple] = None) -> Callable[[str], None]:
        '''Returns callable that displays one line with option to add more chrs onto end'''
        font: pygame.font.Font = optionalUnpack(new_font, self.font)
        colour: tuple = optionalUnpack(new_colour, self.colour)
        def talk(add: str) -> None:
            line = font.render(message + add, True, colour)
            start_position = alignment.get_coords(line, self.screen)
            self.screen.blit(line, start_position)
        return talk
    

    def image_display(self, image: pygame.Surface, alignment: Alignment, scale: tuple) -> Callable[[], None]:
        '''Returns callable that displays image at specified position with the specified size'''

        def paint(image):
            image = pygame.transform.scale(image, scale)
            start_position = alignment.get_coords(image, self.screen)
            self.screen.blit(image, start_position)
        return lambda : paint(image)