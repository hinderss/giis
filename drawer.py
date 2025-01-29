import tkinter as tk
from tkinter import simpledialog
import math

from game import draw_pixel_figure
import line.algorithms as line
import second_order.algorithms as second_order
from second_order.algorithms.circle import bresenham_circle
from second_order.algorithms.ellipse import bresenham_ellipse
from second_order.algorithms.hyperbola import bresenham_hyperbola
from second_order.algorithms.parabola import bresenham_parabola
from utils import sort_points_clockwise


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
        self.selected_algorithm_label.pack(fill=tk.X)

        self.debug_mode = False

        self.info_label = tk.Label(root, text="Кликните для задания центра фигуры")
        self.info_label.pack()

        debug_button = tk.Button(root, text="Переключить режим отладки", command=self.toggle_debug_mode)
        debug_button.pack()

        self.algorithm = "DDA"
        self.start_point = None
        self.end_point = None

        self.canvas.bind("<Button-1>", self.on_left_click)

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
            self.get_curve_parameters()
        elif self.start_point is None:
            self.start_point = (event.x, event.y)
        else:
            self.end_point = (event.x, event.y)
            self.draw_line()
            self.start_point = None
            self.end_point = None

    def get_curve_parameters(self):
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

    def draw_line(self):
        x1, y1 = self.start_point
        x2, y2 = self.end_point

        points = line.algorithms[self.algorithm](x1, y1, x2, y2)
        points = sorted(points, key=lambda point: math.sqrt(point.x ** 2 + point.y ** 2))

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points)

    def draw_points(self, points):
        for x, y, color in points:
            r, g, b = color
            if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                raise ValueError("Цветовые значения должны быть в диапазоне от 0 до 255")
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(x, y, x + 1, y + 1, fill=hex_color)

    def draw_ellipse(self, rx, ry):
        x0, y0 = self.start_point
        points = bresenham_ellipse(x0, y0, rx, ry)
        points = sort_points_clockwise(points)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points)

    def draw_circle(self, a):
        x0, y0 = self.start_point
        points = bresenham_circle(x0, y0, a)
        points = sort_points_clockwise(points)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points)

    def draw_parabola(self, a):
        x0, y0 = self.start_point
        points = bresenham_parabola(x0, y0, a, 1, 1, self.width, self.height)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points)

    def draw_hyperbola(self, a, b):
        x0, y0 = self.start_point
        points = bresenham_hyperbola(x0, y0, a, b, self.width)

        self.draw_points(points)
        if self.debug_mode:
            draw_pixel_figure(points)
