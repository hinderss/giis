import pygame
import numpy as np

# Настройки окна
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class ObjectViewer:
    def __init__(self, file: str, width=800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

        # Загрузка современного шрифта (замените путь на ваш .ttf файл)
        try:
            self.font = pygame.font.Font("Roboto-ExtraBold.ttf", 24)  # Укажите путь к вашему .ttf файлу
        except FileNotFoundError:
            print("Шрифт не найден! Используется системный шрифт.")
            self.font = pygame.font.SysFont("Arial", 24)  # Fallback на системный шрифт

        # Загрузка объекта
        self.vertices, self.edges = self.load_object(file)

        # Загрузка изображения с осями
        try:
            self.axes_image = pygame.image.load("axes.png")  # Укажите путь к вашему изображению
            self.axes_image = pygame.transform.smoothscale(self.axes_image, (50, 50))
        except FileNotFoundError:
            print("Изображение с осями не найдено!")
            self.axes_image = None

        # Параметры объекта
        self.angle_y = 0
        self.angle_z = 0
        self.angle_x = 0
        self.scale_factor_x = 1.0  # Масштаб по оси X
        self.scale_factor_y = 1.0  # Масштаб по оси Y
        self.scale_factor_z = 1.0  # Масштаб по оси Z
        self.scale_factor = 1.0  # Общий масштаб
        self.translation = np.array([0.0, 0.0, 0.0])
        self.distance = 5.0

        # Управление
        self.mode = None  # "rotate" or "translate"
        self.axis = None  # "x", "y", "z"
        self.input_value = ""  # Для хранения введенных чисел
        self.iterative_mode = True  # Флаг для переключения между режимами

    def load_object(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        num_vertices = int(lines[0])
        vertices = [list(map(float, line.split())) + [1] for line in lines[1:num_vertices + 1]]

        num_edges = int(lines[num_vertices + 1])
        edges = [list(map(int, line.split())) for line in lines[num_vertices + 2:num_vertices + 2 + num_edges]]

        return np.array(vertices).T, edges

    def translation_matrix(self, tx, ty, tz):
        return np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ])

    def scale_matrix(self, sx, sy, sz):
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def rotation_matrix_y(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

    def rotation_matrix_z(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

    def rotation_matrix_x(self, angle):
        c, s = np.cos(angle), np.sin(angle)
        return np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def perspective_matrix(self, d):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, -1 / d, 1]
        ])

    def project(self, vertices):
        projected = vertices[:2] / vertices[3]
        return projected.T * 200 + np.array([self.width // 2, self.height // 2])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # Переключение режима
                    self.iterative_mode = not self.iterative_mode
                    self.mode = self.axis = None
                    self.input_value = ""
                elif event.key == pygame.K_KP5:  # Обработка нажатия на цифру 5 (numpad)
                    if self.distance == 5:
                        self.distance = float("inf")  # Бесконечность (отключение перспективы)
                    else:
                        self.distance = 5  # Возврат к перспективе
                if not self.iterative_mode:  # Режим ввода значений
                    if self.mode is None:  # No mode active
                        if event.key == pygame.K_r:
                            self.mode = "rotate"
                        elif event.key == pygame.K_g:
                            self.mode = "translate"
                        elif event.key == pygame.K_s:
                            self.mode = "scale"  # Новый режим для масштабирования
                    elif self.axis is None:  # Mode active but no axis selected
                        if event.key == pygame.K_x:
                            self.axis = "x"
                        elif event.key == pygame.K_y:
                            self.axis = "y"
                        elif event.key == pygame.K_z:
                            self.axis = "z"
                    else:  # Mode and axis selected, capture numbers
                        if event.key == pygame.K_RETURN and self.input_value:
                            value = float(self.input_value)
                            if self.mode == "rotate":
                                if self.axis == "y":
                                    self.angle_y = np.radians(value)
                                elif self.axis == "z":
                                    self.angle_z = np.radians(-value)
                                elif self.axis == "x":
                                    self.angle_x = np.radians(value)
                            elif self.mode == "translate":
                                if self.axis == "y":
                                    self.translation[0] = value
                                elif self.axis == "z":
                                    self.translation[1] = -value
                                elif self.axis == "x":
                                    self.translation[2] = value
                            elif self.mode == "scale":  # Обработка масштабирования
                                if self.axis == "x":
                                    self.scale_factor_x = value
                                elif self.axis == "y":
                                    self.scale_factor_y = value
                                elif self.axis == "z":
                                    self.scale_factor_z = value
                            # Reset mode after applying
                            self.mode = self.axis = None
                            self.input_value = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_value = self.input_value[:-1]
                        elif event.unicode.isdigit() or event.unicode in "-.":
                            self.input_value += event.unicode
        return True

    def update(self):
        if self.iterative_mode:  # Итеративный режим
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.angle_z -= 0.05
            if keys[pygame.K_RIGHT]:
                self.angle_z += 0.05
            if keys[pygame.K_UP]:
                self.angle_y += 0.05
            if keys[pygame.K_DOWN]:
                self.angle_y -= 0.05
            if keys[pygame.K_RCTRL]:
                self.angle_x -= 0.05
            if keys[pygame.K_KP0]:
                self.angle_x += 0.05
            if keys[pygame.K_f]:
                self.scale_factor += 0.05
            if keys[pygame.K_v]:
                self.scale_factor -= 0.05
            if keys[pygame.K_p]:
                self.distance += 0.1
            if keys[pygame.K_o]:
                self.distance -= 0.1
            if keys[pygame.K_d]:
                self.translation[0] += 0.1
            if keys[pygame.K_a]:
                self.translation[0] -= 0.1
            if keys[pygame.K_LCTRL]:
                self.translation[1] += 0.1
            if keys[pygame.K_LSHIFT]:
                self.translation[1] -= 0.1
            if keys[pygame.K_w]:
                self.translation[2] -= 0.1
            if keys[pygame.K_s]:
                self.translation[2] += 0.1

    def render(self):
        self.screen.fill(WHITE)

        # Общая матрица трансформации
        transform = (
                self.perspective_matrix(self.distance) @
                self.translation_matrix(*self.translation) @
                self.rotation_matrix_y(self.angle_y) @
                self.rotation_matrix_z(self.angle_z) @
                self.rotation_matrix_x(self.angle_x) @
                self.scale_matrix(self.scale_factor_x, self.scale_factor_y, self.scale_factor_z) @
                self.scale_matrix(self.scale_factor, self.scale_factor, self.scale_factor)
        )

        transformed_vertices = transform @ self.vertices
        projected_vertices = self.project(transformed_vertices)

        # Отрисовка объекта
        for edge in self.edges:
            i, j = edge
            pygame.draw.line(self.screen, BLACK, projected_vertices[i], projected_vertices[j], 1)

        # Отображение текущего режима и ввода в правом верхнем углу
        if not self.iterative_mode:
            text = f"{self.mode} {self.axis} {self.input_value}" if self.mode and self.axis else f"{self.mode} {self.input_value}" if self.mode else ""
            text_surface = self.font.render(text, True, BLACK)
            self.screen.blit(text_surface, (self.width - text_surface.get_width() - 10, 10))

        # Отображение изображения с осями в левом нижнем углу
        if self.axes_image:
            self.screen.blit(self.axes_image, (10, self.height - self.axes_image.get_height() - 10))

        pygame.display.flip()
        self.clock.tick(30)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
        pygame.quit()

# # Инициализация Pygame
# pygame.init()
#
# # Запуск программы
# viewer = ObjectViewer(WIDTH, HEIGHT)
# viewer.run()