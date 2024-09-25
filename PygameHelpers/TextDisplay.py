

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
        @dataclass
        class Talker:
            message: str
            alignment: Alignment
            screen: pygame.Surface
            font: pygame.font.Font
            colour: tuple

            def talk(self) -> None:
                line = self.font.render(self.message, True, self.colour)
                start_position = self.alignment.get_coords(line, self.screen)
                self.screen.blit(line,start_position)
        return Talker(message, alignment, self.screen, font, colour).talk


    def displayMultipleLines(self, message: list[str], alignment: Alignment, new_font: Optional[pygame.font.Font] = None, new_colour: Optional[tuple] = None) -> Callable[[], None]:
        '''Returns function that displays multiple lines of text cascading down a window. Use if displayLine() is going off the screen'''
        font: pygame.font.Font = optionalUnpack(new_font, self.font)
        colour: tuple = optionalUnpack(new_colour, self.colour)
        @dataclass
        class Talker:
            message: list[str]
            alignment: Alignment
            screen: pygame.Surface
            font: pygame.font.Font
            colour: tuple

            def talk(self) -> None:
                line_no = 0
                diff = int(self.screen.get_width() * 0.8/self.font.size('a')[0]) #number of characters that can fit on 80% of the screen's width
                height = self.font.get_height()
                interim: pygame.Surface = pygame.Surface((float(diff), reduce(lambda curr, new: curr + len(range(0, len(new), diff)), self.message, 0)*height))
                for item in self.message:
                    strings = [item[start:start+diff] for start in range(0, len(item), diff)]
                    for segment in strings:
                        line = self.font.render(segment, True, self.colour)
                        interim.blit(line,(0, height*line_no))
                        line_no+=1
                start_position = self.alignment.get_coords(interim, self.screen)
                self.screen.blit(interim, start_position)
        return Talker(message, alignment, self.screen, font, colour).talk
                

    def request_prompt(self, message: str, alignment: Alignment, new_font: Optional[pygame.font.Font] = None, new_colour: Optional[tuple] = None) -> Callable[[str], None]:
        '''Returns callable that displays one line with option to add more chrs onto end'''
        font: pygame.font.Font = optionalUnpack(new_font, self.font)
        colour: tuple = optionalUnpack(new_colour, self.colour)
        @dataclass
        class Talker:
            message: str
            alignment: Alignment
            screen: pygame.Surface
            font: pygame.font.Font
            colour: tuple

            def talk(self, add: str) -> None:
                line = self.font.render(self.message + add, True, self.colour)
                start_position = self.alignment.get_coords(line, self.screen)
                self.screen.blit(line,start_position)
        return Talker(message, alignment, self.screen, font, colour).talk
    

    def image_display(self, image: pygame.Surface, alignment: Alignment, scale: tuple) -> Callable[[], None]:
        '''Returns callable that displays image at specified position with the specified size'''
        @dataclass
        class Painter:
            image: pygame.Surface
            alignment: Alignment
            screen: pygame.Surface  
            scale: tuple
          
            def paint(self):
                start_position = self.alignment.get_coords(self.image, self.screen)
                self.screen.blit(pygame.transform.scale(image, scale), start_position)
        return Painter(image, alignment, self.screen, scale).paint