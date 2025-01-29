import pygame

from colors import RED
from point import Point


def recalculate_points(points):
    min_x = min(p.x for p in points)
    min_y = min(p.y for p in points)

    return [Point(p.x - min_x, p.y - min_y, p.color, p.debug) for p in points]


def draw_line(surface, x1, y1, x2, y2, color=RED, thickness=1):
    pygame.draw.line(surface, color, (x1, y1), (x2, y2), thickness)


def calculate_pixel_size(points, screen_width, screen_height):
    max_x = max(p.x for p in points)
    max_y = max(p.y for p in points)
    pixel_width = screen_width // (max_x + 1)
    pixel_height = screen_height // (max_y + 1)
    return min(pixel_width, pixel_height)


def draw_pixel_figure(points: list[Point], screen_width=800, screen_height=600):
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

        draw_line(screen, points[0].x * pixel_size + 0.5*pixel_size, points[0].y * pixel_size + 0.5*pixel_size, points[-1].x * pixel_size + 0.5*pixel_size, points[-1].y * pixel_size + 0.5*pixel_size)

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