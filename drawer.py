import tkinter as tk
from tkinter import simpledialog, filedialog
import math

import pygame

from colors import LIGHT_GRAY
from convex_hull.polygon import Polygon, ConvexHull
from game import draw_pixel_figure
import line.algorithms as line
import second_order.algorithms as second_order
import curves.algorithms as curves
from line.line import Line
from second_order.algorithms.circle import bresenham_circle
from second_order.algorithms.ellipse import bresenham_ellipse
from second_order.algorithms.hyperbola import bresenham_hyperbola
from second_order.algorithms.parabola import bresenham_parabola
from d3d import ObjectViewer
from utils import sort_points_clockwise, hex_color, Arrow


class DrawerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawer App")

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

        self.polygon_points = []
        self.polygons = []
        self.polygon: Polygon | None = None
        self.line = None
        self.polygon_mode = False
        self.line_polygon_intersection_mode = False
        self.point_in_poly_mode = False

        self.poly_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Полигоны", menu=self.poly_menu)
        self.poly_menu.add_command(label="Нарисовать полигон", command=self.toggle_polygon_mode)
        self.poly_menu.add_command(label="Проверить выпуклость", command=self.check_convexity)
        self.poly_menu.add_command(label="Построить полигон", command=self.build_polygon)
        self.poly_menu.add_command(label="Построить выпуклую оболочку методом Jarvis", command=self.build_jarvis)
        self.poly_menu.add_command(label="Построить выпуклую оболочку методом Graham", command=self.build_graham)
        self.poly_menu.add_command(label="Проверить линию", command=self.toggle_line_polygon_intersection)
        self.poly_menu.add_command(label="Проверить точку", command=self.toggle_point_in_poly_mode)
        self.poly_menu.add_command(label="Проверить точку", command=self.toggle_point_in_poly_mode)

        # Add "Polygon Fill Algorithms" menu
        self.fill_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Алгоритмы заполнения", menu=self.fill_menu)

        self.fill_menu.add_command(label="Scanline Fill", command=self.select_fill_algorithm("Scanline"))
        self.fill_menu.add_command(label="Active Edge List", command=self.select_fill_algorithm("ActiveEdge"))
        self.fill_menu.add_command(label="Flood Fill", command=self.select_fill_algorithm("Flood"))
        self.fill_menu.add_command(label="Scanline Flood Fill", command=self.select_fill_algorithm("ScanlineFlood"))

        self.selected_fill_algorithm = None
        # self.selected_fill_algorithm_label = tk.Label(self.root, text="Selected Fill Algorithm: Scanline", bg="white")
        # self.selected_fill_algorithm_label.pack(fill=tk.X)
        print(self.canvas.winfo_width())

    def select_fill_algorithm(self, algorithm):
        return lambda: self.set_fill_algorithm(algorithm)

    def set_fill_algorithm(self, algorithm):
        self.selected_fill_algorithm = algorithm
        if self.selected_fill_algorithm == "Scanline":
            points = self.polygon.scanline_fill()
            self.draw_points(points)
            if self.debug_mode:
                draw_pixel_figure(points, "poly", self.polygon)
        if self.selected_fill_algorithm == "ActiveEdge":
            points = self.polygon.active_edge_fill()
            self.draw_points(points)
            if self.debug_mode:
                draw_pixel_figure(points, "poly", self.polygon)
        self.selected_algorithm_label.config(text=f"Selected Fill Algorithm: {algorithm}")

    def toggle_polygon_mode(self):
        self.polygon_mode = not self.polygon_mode
        if self.polygon_mode:
            self.selected_algorithm_label.config(text="Режим рисования полигона.")
            self.info_label.config(text="Кликните для задания точек.")

    def toggle_point_in_poly_mode(self):
        self.point_in_poly_mode = not self.point_in_poly_mode
        if self.point_in_poly_mode:
            self.selected_algorithm_label.config(text="Пренадлежность точки полигону.")
            self.info_label.config(text="Кликните для задания точки.")

    def toggle_line_polygon_intersection(self):
        self.polygon_mode = False
        self.line_polygon_intersection_mode = True
        self.start_point = None
        self.end_point = None
        self.selected_algorithm_label.config(text="Пересекает ли линия последний полигон.")
        self.info_label.config(text="Нарисуйте линию одним из алгоритмов")

    def check_convexity(self):
        result = self.polygon.is_convex()
        if result:
            self.info_label.config(text="Полигон выпуклый.")
            return
        else:
            self.info_label.config(text="Полигон не выпуклый.")
            return

    def build_polygon(self):
        if len(self.polygon_points) < 3:
            self.info_label.config(text="Полигон должен иметь хотя бы 3 вершины.")
            return

        poly = Polygon(self.polygon_points)
        self.polygons.append(poly)
        self.polygon = poly
        poly.draw(self.canvas)
        self.polygon_points.clear()
        self.start_point = None

    def build_jarvis(self):
        self.build_convex_hull("Jarvis")

    def build_graham(self):
        self.build_convex_hull("Graham")

    def build_convex_hull(self, algorithm):
        if len(self.polygon_points) < 3:
            self.info_label.config(text="Полигон должен иметь хотя бы 3 вершины.")
            return

        poly = ConvexHull(self.polygon_points, algorithm=algorithm)
        self.polygons.append(poly)
        self.polygon = poly
        poly.draw(self.canvas)
        self.polygon_points.clear()
        self.start_point = None

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
        pygame.init()

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
        if self.selected_fill_algorithm == "Flood":
            points = self.polygon.flood_fill(event.x, event.y)
            self.selected_fill_algorithm = None
            self.draw_points(points)
            if self.debug_mode:
                draw_pixel_figure(points, "poly", self.polygon)
        elif self.selected_fill_algorithm == "ScanlineFlood":
            points = self.polygon.scanline_flood_fill(event.x, event.y, self.width, self.height)
            self.selected_fill_algorithm = None
            self.draw_points(points)
            if self.debug_mode:
                draw_pixel_figure(points, "poly", self.polygon)
        elif self.polygon_mode:
            x, y = event.x, event.y
            self.polygon_points.append((x, y))
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")
        elif self.point_in_poly_mode:
            width = 6
            x, y = event.x, event.y

            self.canvas.create_oval(
                x - 0.5 * width, y - 0.5 * width,
                x + 0.5 * width, y + 0.5 * width,
                fill=hex_color(LIGHT_GRAY),
                outline="",
                tags="debug",
            )
            result = self.polygon.point_in_polygon(x, y)
            if result:
                self.info_label.config(text="Точка пренадлежит полигону.")
                return
            else:
                self.info_label.config(text="Точка не пренадлежит полигону.")
                return
        elif self.algorithm in second_order.algorithms.keys():
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
            if self.line_polygon_intersection_mode:
                self.info_label.config(text="Пересекает.") if self.polygon.line_polygon_intersection(*self.line) else self.info_label.config(text="Не пересекает.")
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
        self.line = Line(self.start_point, self.end_point)
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
        if self.polygon_mode:
            self.build_polygon()
            return
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
