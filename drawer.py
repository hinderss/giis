import tkinter as tk
from tkinter import simpledialog, filedialog
import math

import pygame

from colors import LIGHT_GRAY
from game import draw_pixel_figure
import line.algorithms as line
import second_order.algorithms as second_order
import curves.algorithms as curves
from second_order.algorithms.circle import bresenham_circle
from second_order.algorithms.ellipse import bresenham_ellipse
from second_order.algorithms.hyperbola import bresenham_hyperbola
from second_order.algorithms.parabola import bresenham_parabola
from d3d import ObjectViewer
from utils import sort_points_clockwise, hex_color, Arrow


class DrawerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line and Curve Drawer App")

        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Add "Algorithms" menu
        self.algorithm_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Отрезки", menu=self.algorithm_menu)

        self.algorithm_menu.add_command(label="DDA Algorithm", command=self.select_algorithm("DDA"))
        self.algorithm_menu.add_command(label="Bresenham's Algorithm", command=self.select_algorithm("Bresenham"))
        self.algorithm_menu.add_command(label="Wu's Algorithm", command=self.select_algorithm("Wu"))

        # Add "Second Order Curves" menu
        self.curve_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Линии второго порядка", menu=self.curve_menu)

        self.curve_menu.add_command(label="Parabola", command=self.select_algorithm("Parabola"))
        self.curve_menu.add_command(label="Hyperbola", command=self.select_algorithm("Hyperbola"))
        self.curve_menu.add_command(label="Circle", command=self.select_algorithm("Circle"))
        self.curve_menu.add_command(label="Ellipse", command=self.select_algorithm("Ellipse"))

        self.selected_algorithm_label = tk.Label(self.root, text="Selected Mode: DDA", bg="white")

        # Add "Curves" menu
        self.curve_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Кривые", menu=self.curve_menu)

        # Add "3D" menu
        self.D3D_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="3D", menu=self.D3D_menu)
        self.D3D_menu.add_command(label="Запустить 3D пространство", command=self.D3D)

        self.curve_menu.add_command(label="Hermite", command=self.select_algorithm("Hermite"))
        self.curve_menu.add_command(label="Bezier", command=self.select_algorithm("Bezier"))
        self.curve_menu.add_command(label="B-spline", command=self.select_algorithm("B-spline"))

        self.selected_algorithm_label = tk.Label(self.root, text="Selected Mode: DDA", bg="white")
        self.selected_algorithm_label.pack(fill=tk.X)

        self.info_label = tk.Label(root, text="Кликните для задания центра фигуры")
        self.info_label.pack()

        debug_button = tk.Button(root, text="Переключить режим отладки", command=self.toggle_debug_mode)
        debug_button.pack()

        draw_button = tk.Button(root, text="Нарисовать", command=self.draw_curve)
        draw_button.pack()
        root.bind("<Return>", self.draw_curve)

        clear_button = tk.Button(root, text="Очистить", command=self.clear)
        clear_button.pack()

        self.debug_mode = False
        self.algorithm = "DDA"
        self.start_point = None
        self.end_point = None

        self.points = []

        self.canvas.bind("<Button-1>", self.on_left_click)

    @staticmethod
    def open_file():
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("Все файлы", "*.*"), ("Текстовые файлы", "*.txt"), ("Изображения", "*.jpg;*.png")]
        )
        if file_path:
            return file_path

    def D3D(self):
        file = self.open_file()
        # Инициализация Pygame
        pygame.init()

        # Запуск программы
        viewer = ObjectViewer(file)
        viewer.run()

    def clear(self):
        self.canvas.delete("all")

    def clear_debug(self):
        if not self.debug_mode:
            self.canvas.delete("debug")

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            self.info_label.config(text="Режим отладки включен. Кликните для рисования.")
        else:
            self.info_label.config(text="Режим отладки выключен. Кликните для рисования.")

    def select(self, algorithm):
        self.algorithm = algorithm
        self.update_algorithm_label()

    def select_algorithm(self, algorithm):
        return lambda: self.select(algorithm)

    def update_algorithm_label(self):
        self.selected_algorithm_label.config(text=f"Selected Mode: {self.algorithm}")

    def on_left_click(self, event):
        if self.algorithm in second_order.algorithms.keys():
            self.start_point = (event.x, event.y)
            self.get_second_order_parameters()
        elif self.algorithm in curves.algorithms.keys():
            width = 6
            x, y = event.x, event.y
            self.points.append((x, y))

            self.canvas.create_oval(
                x - 0.5 * width, y - 0.5 * width,
                x + 0.5 * width, y + 0.5 * width,
                fill=hex_color(LIGHT_GRAY),
                outline="",
                tags="debug",
            )
            self.get_curve_parameters()
        elif self.start_point is None:
            self.start_point = (event.x, event.y)
        else:
            self.end_point = (event.x, event.y)
            self.draw_line()
            self.start_point = None
            self.end_point = None

    def get_second_order_parameters(self):
        if self.algorithm == "Parabola":
            a = simpledialog.askfloat("Parabola", "Enter coefficient a (y = ax^2):")
            if a is not None:
                self.draw_parabola(a)
        elif self.algorithm == "Circle":
            a = simpledialog.askfloat("Circle", "radius = ")
            if a is not None:
                self.draw_circle(a)
        elif self.algorithm == "Hyperbola":
            a = simpledialog.askfloat("Hyperbola", "Enter coefficient a (x^2/a^2 - y^2/b^2 = 1):")
            b = simpledialog.askfloat("Hyperbola", "Enter coefficient b:")
            if a is not None and b is not None:
                self.draw_hyperbola(a, b)
        elif self.algorithm == "Ellipse":
            a = simpledialog.askfloat("Hyperbola", "Semiaxes1:")
            b = simpledialog.askfloat("Hyperbola", "Semiaxes2:")
            if a is not None and b is not None:
                self.draw_ellipse(a, b)

    def get_curve_parameters(self):
        if self.algorithm == "Hermite":
            if len(self.points) in (2, 4):
                start_idx = 0 if len(self.points) == 2 else 2
                x1, y1 = self.points[start_idx]
                x2, y2 = self.points[start_idx + 1]
                Arrow(self.canvas).create(x1, y1, x2, y2, hex_color(LIGHT_GRAY))

                if len(self.points) == 4:
                    self.draw_curve()
        else:
            if len(self.points) >= 2:
                self.canvas.create_line(*self.points[-2], self.points[-1], fill=hex_color(LIGHT_GRAY), tags="debug")

    def draw_line(self):
        x1, y1 = self.start_point
        x2, y2 = self.end_point

        points = line.algorithms[self.algorithm](x1, y1, x2, y2)
        points = sorted(points, key=lambda point: math.sqrt(point.x ** 2 + point.y ** 2))

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points, "line")

    def draw_points(self, points):
        for x, y, color in points:
            self.canvas.create_line(x, y, x + 1, y + 1, fill=hex_color(color))

    def draw_ellipse(self, rx, ry):
        x0, y0 = self.start_point
        points = bresenham_ellipse(x0, y0, rx, ry)
        points = sort_points_clockwise(points)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points, "ellipse", rx, ry)

    def draw_circle(self, a):
        x0, y0 = self.start_point
        points = bresenham_circle(x0, y0, a)
        # points = sort_points_clockwise(points)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points, "circle", a)

    def draw_parabola(self, a):
        x0, y0 = self.start_point
        points = bresenham_parabola(x0, y0, a, 1, 1, self.width, self.height)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points, "parabola", a)

    def draw_hyperbola(self, a, b):
        x0, y0 = self.start_point
        points = bresenham_hyperbola(x0, y0, a, b, 10)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points, "hyperbola", a, b)

    def draw_curve(self, *args):
        points = curves.algorithms[self.algorithm](self.points)
        self.draw_points(points)
        self.clear_debug()

        debug = {
            "Hermite": self.points,
            "Bezier": self.points,
            "B-spline": self.points,
        }

        if self.debug_mode:
            draw_pixel_figure(points, self.algorithm, *debug[self.algorithm])
        self.points = []
