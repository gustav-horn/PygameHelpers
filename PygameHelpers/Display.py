from typing import Callable
import pygame


class Display():
    '''
    A wrapper class that holds a collection of screens to display
    '''

    def __init__(self, screens: list[Callable[[pygame.event.Event], bool]]):
        self.screens = screens

    def __call__(self, event: pygame.event.Event):
        for screen in self.screens:
            screen(event)

    def add_screen(self, screen: Callable[[pygame.event.Event], bool]):
        self.screens.append(screen)

    def remove_screen(self, screen: Callable[[pygame.event.Event], bool]):
        if screen in self.screens:
            self.screens.remove(screen)