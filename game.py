import math

import pygame

from colors import RED
from point import Point


WIDTH = 800
HEIGHT = 600

def recalculate_points(points):
    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)

    return [Point(p.x - min_x, p.y - min_y, p.color, p.debug) for p in points]


def draw_line(surface, x1, y1, x2, y2, color=RED, thickness=1):
    pygame.draw.line(surface, color, (x1, y1), (x2, y2), thickness)


def draw_parabola(surface, x0, y0, a, color=RED, thickness=1, width=800, height=600):
    for x in range(width):
        y = a * (x - x0)**2 + y0
        if 0 <= y < height:
            pygame.draw.circle(surface, color, (x, int(y)), thickness)


def draw_hyperbola(surface, x0, y0, a, b, color=RED, thickness=1, width=800, height=600):
    for x in range(width):
        # Проверяем, что выражение под корнем неотрицательное
        under_root = (x - x0)**2 / a**2 - 1
        if under_root >= 0:  # Только если подкоренное выражение >= 0
            y1 = y0 + b * math.sqrt(under_root)
            y2 = y0 - b * math.sqrt(under_root)
            if 0 <= y1 < height:
                pygame.draw.circle(surface, color, (x, int(y1)), thickness)
            if 0 <= y2 < height:
                pygame.draw.circle(surface, color, (x, int(y2)), thickness)


def draw_ellipse(surface, x0, y0, rx, ry, color=RED, thickness=1):
    for angle in range(0, 360):
        x = x0 + rx * math.cos(math.radians(angle))
        y = y0 + ry * math.sin(math.radians(angle))
        pygame.draw.circle(surface, color, (int(x), int(y)), thickness)


def draw_circle(surface, x0, y0, radius, color=RED, thickness=1):
    pygame.draw.circle(surface, color, (x0, y0), radius, thickness)


def calculate_pixel_size(points, screen_width, screen_height):
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    pixel_width = screen_width // (max_x + 1)
    pixel_height = screen_height // (max_y + 1)
    return min(pixel_width, pixel_height)


def draw_pixel_figure(points: list[Point], figure="line", *args):
    screen_width = WIDTH
    screen_height = HEIGHT

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))




    pygame.display.set_caption("Рисование пиксельной фигуры")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)  # Шрифт для вывода текста

    points = recalculate_points(points)

    current_point_index = 0

    pixel_switch_delay = 100  # Задержка в миллисекундах
    last_switch_time = pygame.time.get_ticks()

    while True:
        screen.fill((255, 255, 255))  # Очистка экрана (белый фон)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_SPACE]:
            if current_time - last_switch_time > pixel_switch_delay:
                if current_point_index < len(points):
                    current_point_index += 1
                    last_switch_time = current_time

        if points:
            pixel_size = calculate_pixel_size(points, screen_width, screen_height)
        else:
            pixel_size = 1  # На случай пустого списка точек

        if not pixel_size:
            pixel_size = 1

        for x in range(0, screen_width, int(pixel_size)):
            pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, screen_height))
        for y in range(0, screen_height, int(pixel_size)):
            pygame.draw.line(screen, (200, 200, 200), (0, y), (screen_width, y))


        for i in range(current_point_index):
            x, y, color = points[i]
            pygame.draw.rect(screen, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

        if current_point_index > 0:
            current_point = points[current_point_index - 1]
            if hasattr(current_point, 'debug') and isinstance(current_point.debug, dict):
                debug_info = current_point.debug
                rows = len(debug_info)

                text_area_width = 200  # Ширина области текста
                text_area_height = 20*(rows+1)  # Высота области текста

                text_y_offset = screen_height - text_area_height + 10  # Начальная позиция по Y (отступ от нижнего края)
                for key, value in debug_info.items():
                    text = f"{key}: {value}"
                    text_surface = font.render(text, True, (0, 0, 0))  # Черный цвет текста
                    screen.blit(text_surface, (screen_width - text_area_width + 10, text_y_offset))  # Правый нижний угол
                    text_y_offset += 20  # Смещение для следующей строки

        mean_x = sum([point.x * pixel_size for point in points]) // len(points)
        mean_y = sum([point.y * pixel_size for point in points]) // len(points)

        sample = {
            "line": lambda: draw_line(screen, points[0].x * pixel_size + 0.5*pixel_size, points[0].y * pixel_size + 0.5*pixel_size, points[-1].x * pixel_size + 0.5*pixel_size, points[-1].y * pixel_size + 0.5*pixel_size),
            "circle": lambda r: draw_circle(screen, mean_x + 0.5*pixel_size, mean_y + 0.5*pixel_size, r * pixel_size),
            "ellipse": lambda rx, ry: draw_ellipse(screen, mean_x + 0.5*pixel_size, mean_y + 0.5*pixel_size, rx * pixel_size, ry * pixel_size),
            "parabola": lambda a: draw_parabola(screen, mean_x + 0.5*pixel_size, min(p.y for p in points) + 0.5*pixel_size, a / pixel_size),
            "hyperbola": lambda a, b: draw_hyperbola(screen, mean_x + 0.5*pixel_size, mean_y + 0.5*pixel_size, a * pixel_size, b * pixel_size),
        }
        sample[figure](*args)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    points = [
        Point(0, 0, (255, 0, 0), debug={"ID": 1, "Status": "Active"}),
        Point(1, 0, (0, 255, 0), debug={"ID": 2, "Status": "Inactive"}),
        Point(2, 0, (0, 0, 255), debug={"ID": 3, "Status": "Active"}),
        Point(0, 1, (255, 255, 0), debug={"ID": 4, "Status": "Pending"}),
        Point(1, 1, (0, 255, 255), debug={"ID": 5, "Status": "Active"}),
        Point(2, 15, (255, 0, 255), debug={"ID": 6, "Status": "Inactive"}),
        Point(3, 100, (128, 128, 128), debug={"ID": 7, "Status": "Pending"}),
    ]
    draw_pixel_figure(points)