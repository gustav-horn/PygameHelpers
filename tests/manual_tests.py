import pygame

from PygameHelpers.TextDisplay import TextDisplay
from PygameHelpers.Alignment import Alignment, Position


def setup() -> tuple[pygame.Surface, TextDisplay]: 
    pygame.init()
    pygame.font.init()
    curr_device = pygame.display.Info()
    width = curr_device.current_w * 0.9
    height = curr_device.current_h * 0.9
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Testing")

    background_color = (255, 255, 255)
    text_colour = (0,0,138)
    font = pygame.font.SysFont("comicsansms", int(width*0.04)) 
    FPS = pygame.time.Clock()

    talker = TextDisplay(screen, font, text_colour)

    return screen, talker


def main(screen: pygame.Surface, talker: TextDisplay) -> None:
    talker.image_display(pygame.image.load("tests/teacher.jpg"), Alignment(Position.bottom), (100, 100))()
    pygame.display.flip()


if __name__ == '__main__':
    main(*setup())