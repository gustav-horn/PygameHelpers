
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional
import pygame


class Position(Enum):
    '''Sequence of values for positional locations'''
    none = "none"
    top = "top"
    centre = "centre"
    bottom = "bottom"
    bottom_left = "bottom left"
    bottom_right = "bottom right"

@dataclass
class Coords:
    x: float|None
    y: float|None

    def __getitem__(self, index: int) -> float|None:
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise IndexError
            
    def __setitem__(self, index: int, value: float) -> None:
        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case _:
                raise IndexError
            
    def __repr__(self) -> str:
        return str((self.x,self.y))


class Alignment:

    def __init__(self, position: Position = Position.none, offsets: tuple[float, float] = (0,0), overwrites: tuple[Optional[float], Optional[float]] = (None, None)):
        self.position = position
        self.offsets = Coords(offsets[0], offsets[1])
        self.overwrites = Coords(overwrites[0], overwrites[1])

    def get_coords(self, object, screen) -> tuple[float, float]:
        match self.position:
            case Position.none:
                x, y = 0.0, 0.0
            case Position.top:
                x = self.centre_position(object, screen)[0]
                y = 0
            case Position.centre:
                x, y = self.centre_position(object, screen)
            case Position.bottom:
                x = self.centre_position(object, screen)[0]
                y = self.bottom_y(object, screen)
            case Position.bottom_left:
                x = 0
                y = self.bottom_y(object, screen)
            case Position.bottom_right:
                x = self.right_x(object, screen)
                y = self.bottom_y(object, screen)

        x = x + self.offsets.x if self.offsets.x is not None else 0
        y = y + self.offsets.y if self.offsets.y is not None else 0

        if self.overwrites.x is not None:
            x = self.overwrites.x

        if self.overwrites.y is not None:
            y = self.overwrites.y

        return (x, y)
    
    def centre_position(self, object: pygame.Surface, screen: pygame.Surface) -> tuple[float, float]: 
        x = (screen.get_width() - object.get_width()) / 2
        y = (screen.get_height() - object.get_height()) / 2
        return (x, y)
    
    def bottom_y(self, object: pygame.Surface, screen: pygame.Surface) -> float:
        y = screen.get_height() - object.get_height()
        return y
    
    def right_x(self, object, screen) -> float:
        x = screen.get_width() - object.get_width()
        return x
    
    def get_offsets(self):
        return self.offsets
    
    def set_offsets(self, values: Coords):
        self.offsets = values

    def get_overwrites(self):
        return self.overwrites
    
    def set_overwrites(self, values: Coords):
        self.overwrites = values