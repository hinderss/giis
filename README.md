# Лабораторная работа №1
<details>
  <summary>Раскрыть описание лабораторной работы</summary>

## Алгоритмы построения отрезков

### Цель работы:
Целью данной лабораторной работы является разработка элементарного графического редактора, который реализует алгоритмы построения отрезков. В частности, будут использованы три известных алгоритма: Цифровой дифференциальный анализатор (ЦДА), целочисленный алгоритм Брезенхема и алгоритм Ву. Программа должна позволять выбирать метод генерации отрезков через панель инструментов, а также отображать отладочную информацию о процессе построения отрезка.

### Задание:
Разработать элементарный графический редактор, реализующий построение отрезков с помощью алгоритма ЦДА, целочисленного алгоритма Брезенхема и алгоритма Ву. Вызов способа генерации отрезка задается из пункта меню и доступно через панель инструментов «Отрезки». В редакторе кроме режима генерации отрезков в пользовательском окне должен быть предусмотрен отладочный режим, где отображается пошаговое решение на дискретной сетке.


### Основные теоретические сведения:

1. **Алгоритм ЦДА (DDA - Digital Differential Analyzer):**
   Этот алгоритм представляет собой метод, основанный на непрерывном увеличении значений координат точек, через которые проходит отрезок. Основная идея заключается в вычислении приращений по осям X и Y, и поочередном отрисовывании точек, пока не будет достигнута конечная точка.

2. **Алгоритм Брезенхема (Bresenham's Algorithm):**
   Это целочисленный алгоритм, который позволяет точно и быстро вычислять координаты точек, лежащих на отрезке. Он использует решение задачи, минимизируя ошибки округления, что позволяет существенно повысить производительность. Отличается от алгоритма ЦДА тем, что не использует деления, что делает его более быстрым.

3. **Алгоритм Ву (Wu's Algorithm):**
   Алгоритм Ву использует концепцию сглаживания отрезков для более качественного отображения линий на экране, управляя интенсивностью каждого пикселя на основе его положения относительно отрезка. Этот алгоритм применяет антиподиальные вычисления и используется для получения более плавных и эстетичных линий, с возможностью регулирования прозрачности.

---

## Скриншоты программы

### Основное окно программы:
Это окно является основным интерфейсом редактора. Оно содержит рабочую область, где можно создавать отрезки, а также меню для выбора алгоритма и инструментов.

![Screenshot from 2025-01-29 17-46-29](https://github.com/user-attachments/assets/e31cbd6d-1e60-466a-b38c-077cfbad2bce)

### Экран выбора метода рисования отрезков:
На этом экране пользователь выбирает один из доступных методов рисования отрезков, таких как алгоритм ЦДА, Брезенхема или Ву.

![Screenshot from 2025-01-29 17-46-16](https://github.com/user-attachments/assets/7fe20259-a784-4745-86d6-c81a916e70fc)

### Окно отладочного режима:
В этом режиме отображается пошаговое решение на дискретной сетке, что позволяет пользователю проследить процесс построения отрезка на каждом шаге.

![Screenshot from 2025-01-29 17-51-38](https://github.com/user-attachments/assets/68f0b993-706f-4c95-af1d-65916ccfb4a5)


### Листинг кода:

#### Метод DDA (Цифровой дифференциальный анализатор):
```python
def dda_algorithm(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps

    x, y = x1, y1
    for step in range(steps + 1):
        points.append(Point(round(x), round(y), debug=debug_info))
        x += x_increment
        y += y_increment

    return points
```

#### Метод Bresenham (Алгоритм Брезенхема):
```python
def bresenham_algorithm(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append(Point(x1, y1, debug=debug_info))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return points
```

#### Метод Wu (Алгоритм Ву):
```python
import math

def wu_algorithm(x1, y1, x2, y2) -> list[Point]:
    points = []

    def plot(x, y, intensity, debug=None):
        intensity = max(0, min(1, intensity))
        r = g = b = int(255 * (1 - intensity))
        points.append(Point(x, y, (r, g, b), debug=debug))

    def fpart(x):
        return x - math.floor(x)

    def rfpart(x):
        return 1 - fpart(x)

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    gradient = dy / dx if dx != 0 else 1

    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend
    ypxl1 = math.floor(yend)

    if steep:
        plot(ypxl1, xpxl1, rfpart(yend) * xgap, debug_info)
        plot(ypxl1 + 1, xpxl1, fpart(yend) * xgap, debug_info)
    else:
        plot(xpxl1, ypxl1, rfpart(yend) * xgap, debug_info)
        plot(xpxl1, ypxl1 + 1, fpart(yend) * xgap, debug_info)

    intery = yend + gradient

    # Вторая точка
    xend = round(x2)
    yend = y2 + gradient * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend
    ypxl2 = math.floor(yend)

    if steep:
        plot(ypxl2, xpxl2, rfpart(yend) * xgap, debug_info)
        plot(ypxl2 + 1, xpxl2, fpart(yend) * xgap, debug_info)
    else:
        plot(xpxl2, ypxl2, rfpart(yend) * xgap, debug_info)
        plot(xpxl2, ypxl2 + 1, fpart(yend) * xgap, debug_info)

    if steep:
        for x in range(xpxl1 + 1, xpxl2):
            plot(math.floor(intery), x, rfpart(intery), debug_info)
            plot(math.floor(intery) + 1, x, fpart(intery), debug_info)
            intery += gradient
    else:
        for x in range(xpxl1 + 1, xpxl2):
            plot(x, math.floor(intery), rfpart(intery), debug_info)
            plot(x, math.floor(intery) + 1, fpart(intery), debug_info)
            intery += gradient

    return points
```

### Класс Point:

```python
class Point:
    def __init__(self, x, y, color: Iterable[int] = BLACK, debug: dict | None = None):
        self.x = x
        self.y = y
        self.color = tuple(color)
        self.debug: dict | None = debug

    def __iter__(self):
        return iter((self.x, self.y, self.color))

    def __str__(self):
        return f"({self.x}, {self.y})"
```

### Вывод:
В результате работы над лабораторной работой был разработан графический редактор, который позволяет строить отрезки с использованием различных алгоритмов (ЦДА, Брезенхем, Ву). Алгоритмы обеспечивают точное отображение отрезков на экране и позволяют эффективно рисовать линии с различными характеристиками. Отладочный режим программы помогает наблюдать за шагами алгоритмов и предоставляет подробную информацию о процессе генерации отрезков.


Вот дополненный текст с исправленными ошибками и добавленными недостающими частями:  

</details>

# Лабораторная работа №2  
<details>  
  <summary>Раскрыть описание лабораторной работы</summary>  

## Алгоритмы построения линий второго порядка  

### Цель работы:  
Изучить алгоритмы построения линий второго порядка, такие как окружность, эллипс, гипербола и парабола. Реализовать их программно с использованием алгоритма Брезенхема и исследовать особенности их дискретизации.  

### Задание:  
Разработать элементарный графический редактор, реализующий построение линий второго порядка: окружности, эллипса, гиперболы и параболы.  

Функциональные требования:  
- Выбор типа кривой должен осуществляться через меню и панель инструментов «Линии второго порядка».  
- Реализация генерации линий второго порядка в пользовательском окне.  
- Возможность переключения в отладочный режим, в котором отображается пошаговое построение на дискретной сетке.  
- Возможность изменения параметров кривых (например, радиус окружности, оси эллипса и т. д.).  

### Основные теоретические сведения:  

1. **Алгоритм Брезенхема для рисования окружности:**  
   Метод Брезенхема позволяет рисовать окружность, используя целочисленные вычисления. Алгоритм основан на симметрии окружности, что позволяет эффективно заполнять все октанты, используя минимальное количество вычислений.  

2. **Алгоритм Брезенхема для рисования эллипса:**  
   Расширение алгоритма Брезенхема для эллипсов основано на разделении построения на две части:  
   - Область, где преобладает изменение координаты \(x\).  
   - Область, где преобладает изменение координаты \(y\).  
   Это позволяет минимизировать ошибки округления и улучшить точность отображения эллиптической формы.  

3. **Алгоритм Брезенхема для рисования параболы:**  
   Построение параболы основано на использовании пошагового прироста координат с минимальным накоплением ошибок. Основной принцип заключается в том, что прирост \(y\) меняется линейно, а прирост \(x\) — квадратично.  

4. **Алгоритм Брезенхема для рисования гиперболы:**  
   Алгоритм Брезенхема для гипербол строится аналогично эллипсу, но с учетом разницы знаков в уравнении гиперболы. Он позволяет строить дискретное приближение гиперболических ветвей с высокой точностью.  

## Скриншоты программы

![image](https://github.com/user-attachments/assets/88b243f5-d94a-4530-b94b-b1091bd22bd9)

### Листинг кода:

#### Рисование окружности:
```python
def bresenham_circle(x0, y0, radius):
    x, y = 0, radius
    d = 3 - 2 * radius
    points = []

    def plot_circle_points(cx, cy, x, y, d=None):
        points.extend([
            Point(cx + x, cy + y, debug_info), Point(cx - x, cy + y, debug_info),
            Point(cx + x, cy - y, debug_info), Point(cx - x, cy - y, debug_info),
            Point(cx + y, cy + x, debug_info), Point(cx - y, cy + x, debug_info),
            Point(cx + y, cy - x, debug_info), Point(cx - y, cy - x, debug_info),
        ])

    plot_circle_points(x0, y0, x, y, d)

    while x < y:
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
        plot_circle_points(x0, y0, x, y, d)

    return points
```

#### Рисование эллипса:
```python
def bresenham_ellipse(x0, y0, rx, ry):
    points = []

    def plot_ellipse_points(cx, cy, x, y, d=None, string=None):
        points.extend([
            Point(cx + x, cy + y, debug_info), Point(cx - x, cy + y, debug_info),
            Point(cx + x, cy - y, debug_info), Point(cx - x, cy - y, debug_info)
        ])

    x, y = 0, ry
    rx2, ry2 = rx ** 2, ry ** 2
    tworx2, twory2 = 2 * rx2, 2 * ry2
    px, py = 0, tworx2 * y

    # Region 1
    d1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    while px < py:
        plot_ellipse_points(x0, y0, x, y, d1, "< 0")
        x += 1
        px += twory2
        if d1 < 0:
            d1 += ry2 + px
        else:
            y -= 1
            py -= tworx2
            d1 += ry2 + px - py

    # Region 2
    d2 = (ry2 * (x + 0.5) ** 2) + (rx2 * (y - 1) ** 2) - (rx2 * ry2)
    while y >= 0:
        plot_ellipse_points(x0, y0, x, y, d2, "> 0")
        y -= 1
        py -= tworx2
        if d2 > 0:
            d2 += rx2 - py
        else:
            x += 1
            px += twory2
            d2 += rx2 - py + px

    return points
```

#### Рисование параболы:
```python
def bresenham_parabola(x0, y0, a, b, c, x_limit, y_limit):
    points = []

    div = 0.5 / a
    x, y = 0, 0
    d_pre = 0.5 - a
    d_post = 1 - a * math.ceil(div) - 0.25 * a

    while x + x0 <= x_limit and y + y0 <= y_limit:
        points.append(Point(x + x0, y + y0, debug_info))
        points.append(Point(-x + x0, y + y0, debug_info))

        if x < div:
            tmp = -2 * a * x - 3 * a
            x += 1
            if d_pre < 0:
                y += 1
                d_pre += tmp + 1
            else:
                d_pre += tmp
        else:
            tmp = -2 * a * x - 2 * a + 1
            y += 1
            if d_post >= 0:
                x += 1
                d_post += tmp
            else:
                d_post += 1

    return points
```

#### Рисование гиперболы:
```python
def bresenham_hyperbola(x0, y0, a, b, x_limit):
    points = []
    x = abs(a)
    y = 0
    a **= 2
    b **= 2
    d = b * (2 * x + 1) - a
    bx = x

    while x - bx <= x_limit:
        f1 = (d <= 0) or (2 * d - b * (2 * x + 1) <= 0)
        f2 = (d <= 0) or (2 * d - a * (2 * y + 1) > 0)

        points.append(Point(x0 - x, y0 - y, debug_info))
        points.append(Point(x0 + x, y0 + y, debug_info))
        points.append(Point(x0 + x, y0 - y, debug_info))
        points.append(Point(x0 - x, y0 + y, debug_info))

        x = x + 1 if f1 else x
        y = y + 1 if f2 else y

        d = d + b * (2 * x + 1) if f1 else d
        d = d - a * (2 * y - 1) if f2 else d

    return points
```

### Выводы:  
В ходе лабораторной работы студенты изучат основные алгоритмы построения кривых второго порядка, проанализируют их эффективность и особенности, а также реализуют графический редактор с возможностью визуализации процесса построения.  

</details>

# Лабораторная работа №3
<details>  
  <summary>Раскрыть описание лабораторной работы</summary>  

## Алгоритмы построения линий второго порядка

### Цель работы
Разработать элементарный графический редактор, реализующий построение параметрических кривых, используя форму Эрмита, форму Безье и B-сплайн.

### Задание
Создать графический редактор с возможностью выбора метода построения кривых через меню и панель инструментов "Кривые". Обеспечить режим корректировки опорных точек и состыковки сегментов. Включить в программу базовые функции матричных вычислений.

### Основные теоретические сведения
- **Кривая Эрмита** – метод построения кривых, использующий начальные и конечные точки, а также касательные в этих точках.
- **Кривая Безье** – параметрическая кривая, определяемая опорными точками, с использованием полиномиальных функций.
- **B-сплайн** – гибкий метод построения кривых, который позволяет более плавно контролировать форму кривой за счет весовых коэффициентов.

## Скриншоты программы
![image](https://github.com/user-attachments/assets/a733a317-94b2-49ec-b096-87aa0ffdb5b6)


## Листинг кода

#### Рисование методом Эрмита:
```python
def hermite_curve(points: tuple) -> list[Point]:
    p1, vend1, p4, vend4 = points

    r1 = (vend1[0] - p1[0], vend1[1] - p1[1])
    r4 = (vend4[0] - p4[0], vend4[1] - p4[1])

    P1 = np.array(p1)
    P4 = np.array(p4)
    R1 = np.array(r1)
    R4 = np.array(r4)

    hermite_matrix = np.array([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ])

    parameter_matrix = np.array([P1, P4, R1, R4])

    coefficients = np.dot(hermite_matrix, parameter_matrix)

    curve_points = []
    for t in np.linspace(0, 1, 1000):
        T = np.array([t**3, t**2, t, 1])
        x, y = np.dot(T, coefficients)
        point = Point(round(x), round(y))
        if point not in curve_points:
            matrix_dict = {
                "t3": f"{t ** 3:.3f}",
                "t2": f"{t ** 2:.3f}",
                "t1": f"{t:.3f}",
                "1": "1",
                "": "*",
            }
            max_len = max(len(str(int(coefficients[i, 0]))) for i in range(coefficients.shape[0]))
            for i in range(coefficients.shape[0]):
                matrix_dict[str(int(coefficients[i, 0])).zfill(max_len)] = str(int(coefficients[i, 1])).zfill(max_len)
            point.debug = matrix_dict
            curve_points.append(point)

    return curve_points
```

#### Рисование методом Безье:
```python
def bezier_curve(control_points: list[tuple[int, int]], num_points: int = 1000) -> list[Point]:
    n = len(control_points) - 1
    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x, y = 0, 0
        for j, point in enumerate(control_points):
            point_x, point_y = point
            binom = 1
            for k in range(1, j + 1):
                binom *= (n - k + 1) / k
            x += binom * (1 - t)**(n - j) * t**j * point_x
            y += binom * (1 - t)**(n - j) * t**j * point_y
        p = Point(round(x), round(y))
        if p not in points:
            p.debug = {
                "t": f"{t:.3f}",
                "x": f"{p.x:.3f}",
                "y": f"{p.y:.3f}",
            }
            points.append(p)
    return points
```

#### Рисование методом B-сплайнов:
```python
def b_spline(control_points: list[tuple[int, int]], degree: int = 3, num_points: int = 1000) -> list[Point]:
    n = len(control_points) - 1
    m = n + degree + 1

    knots = [0] * (degree + 1) + list(range(1, m - 2 * degree)) + [m - 2 * degree] * (degree + 1)

    def basis_function(i, k, t):
        if k == 0:
            return 1 if knots[i] <= t < knots[i + 1] else 0
        c1 = (t - knots[i]) / (knots[i + k] - knots[i]) * basis_function(i, k - 1, t) if knots[i + k] != knots[i] else 0
        c2 = (knots[i + k + 1] - t) / (knots[i + k + 1] - knots[i + 1]) * basis_function(i + 1, k - 1, t) if knots[i + k + 1] != knots[i + 1] else 0
        return c1 + c2

    points = []
    for i in range(num_points):
        t = knots[degree] + (knots[-degree - 1] - knots[degree]) * i / (num_points - 1)
        x, y = 0, 0
        for j in range(n + 1):
            b = basis_function(j, degree, t)
            point_x, point_y = control_points[j]
            x += point_x * b
            y += point_y * b
        p = Point(round(x), round(y))
        if p not in points and p != Point(0, 0):
            p.debug = {
                "t": f"{t:.3f}",
                "x": f"{p.x:.3f}",
                "y": f"{p.y:.3f}",
            }
            points.append(p)

    return points[1:]
```

## Выводы
Разработанный графический редактор успешно реализует построение параметрических кривых Эрмита, Безье и B-сплайнов. Добавлена возможность корректировки опорных точек и состыковки сегментов. Реализованы базовые функции матричных вычислений для работы с кривыми.



</details>

# Лабораторная работа №4
<details>  
  <summary>Раскрыть описание лабораторной работы</summary>  

## Алгоритм
Разработка базового графического редактора с возможностью выполнения различных геометрических преобразований на трехмерных объектах с использованием матричных операций.

## Цель работы
Целью данной лабораторной работы является изучение методов представления и преобразования трехмерных объектов в графическом редакторе. 

## Задание
Разработать графическую программу, выполняющую следующие геометрические преобразования над трехмерным объектом: перемещение, поворот, скалирование, отображение, перспектива. В программе должно быть предусмотрено считывание координат 3D объекта из текстового файла, обработка клавиатуры и выполнение геометрических преобразований в зависимости от нажатых клавиш. Все преобразования следует производить с использованием матричного аппарата и представления координат в однородных координатах.

## Основные теоретические сведения
- Однородные координаты — это система координат, которая позволяет выполнять преобразования, такие как перемещение, поворот и масштабирование, с использованием матриц.
- Матрицы преобразования — это инструменты, используемые для осуществления различных геометрических изменений объектов в пространстве.

## Скриншоты программы
![image](https://github.com/user-attachments/assets/e4c384c0-d05a-4d33-a2a1-39856e36ffa2)


## Листинг кода

### Матрицы преобразования
```python
#перемещение
def translation_matrix(self, tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

#изменение размера
def scale_matrix(self, sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

#поворот по y
def rotation_matrix_y(self, angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])

#поворот по z
def rotation_matrix_z(self, angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])

#поворот по x
def rotation_matrix_x(self, angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

#изменение перспективы
def perspective_matrix(self, d):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, -1 / d, 1]
    ])
```


## Выводы
В процессе выполнения лабораторной работы были изучены основные методы графической визуализации и трансформации трехмерных объектов. Практическая реализация графического редактора на основе матричных преобразований предоставила ценные навыки в области компьютерной графики и геометрии. Основное внимание было уделено использованию однородных координат и их преобразованию, что является ключевым для работы с трехмерной графикой.

</details>

# Лабораторная работа №5

<details>  
  <summary>Раскрыть описание лабораторной работы</summary>  

## Цель работы
Целью данной лабораторной работы является разработка элементарного графического редактора, который позволяет выполнять геометрические преобразования на полигонах, проверять их на выпуклость, находить внутренние нормали, строить выпуклые оболочки различными методами, а также определять точки пересечения отрезков и принадлежность точек полигонам.

## Задание
Разработать элементарный графический редактор, реализующий построение полигонов. Реализованная программа должна уметь проверять полигон на выпуклость, находить его внутренние нормали. Программа должна выполнять построение выпуклых оболочек методом обхода Грэхема и методом Джарвиса. Выбор метода задается из пункта меню и должен быть доступен через панель инструментов «Построение полигонов». Графический редактор должен позволять рисовать линии первого порядка (лабораторная работа №1) и определять точки пересечения отрезка со стороной полигона, также программа должна определять принадлежность введенной точки полигону.

## Основные теоретические сведения
Для проверки полигона на выпуклость используется алгоритм, основанный на определении направления поворота для каждой тройки последовательных вершин полигона. Если все тройки вершин имеют одинаковое направление поворота, то полигон является выпуклым.

Для построения выпуклых оболочек используются два метода:
- **Метод обхода Грэхема**: алгоритм, который строит выпуклую оболочку, обходя точки в порядке увеличения угла относительно начальной точки.
- **Метод Джарвиса**: алгоритм, который строит выпуклую оболочку, последовательно находя точки с наименьшим углом относительно предыдущей точки.

Для определения принадлежности точки полигону используется алгоритм, основанный на подсчете количества пересечений луча, исходящего из точки, с границами полигона. Если количество пересечений нечетное, то точка находится внутри полигона.

## Скриншоты программы
![image](https://github.com/user-attachments/assets/bdd5485a-01be-4527-8466-db0117f3eed9)


## Листинг кода

### Проверка принадлежности точки полигону
```python
def point_in_polygon(self, x, y):
    inside = False
    for point1, point2 in self:
        x1, y1, _ = point1
        x2, y2, _ = point2
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if y1 == y2 or x <= xinters:
                        inside = not inside
    return inside
```

### Определение пересечения отрезка с полигоном
```python
def line_polygon_intersection(self, line_start: Point, line_end: Point):
    intersections = []
    for point1, point2 in self:
        intersection = line_intersection(line_start, line_end, point1, point2)
        if intersection:
            intersections.append(intersection)
    return intersections
```

### Проверка полигона на выпуклость
```python
def is_convex(self) -> bool:
    if len(self.points) < 3:
        raise Exception("Полигон должен иметь хотя бы 3 вершины.")

    n = len(self.points)
    if n == 3:
        return True

    sign = 0
    for i in range(n):
        a = self.points[i]
        b = self.points[(i + 1) % n]
        c = self.points[(i + 2) % n]
        cp = cross_product(a, b, c)
        if cp == 0:
            continue
        if sign == 0:
            sign = 1 if cp > 0 else -1
        elif (cp > 0 and sign == -1) or (cp < 0 and sign == 1):
            return False
    return True
```

### Построение выпуклой оболочки методом Джарвиса
```python
def jarvis_convex_hull(points: list[(int, int)]) -> list[Point]:
    n = len(points)
    if n < 3:
        return points

    hull = []
    l = min(range(n), key=lambda i: points[i][0])
    p = l
    while True:
        hull.append(Point(*points[p]))
        q = (p + 1) % n
        for i in range(n):
            if i == p:
                continue
            val = (points[i][1] - points[p][1]) * (points[q][0] - points[p][0]) - (points[q][1] - points[p][1]) * (points[i][0] - points[p][0])
            if val < 0:
                q = i
        p = q
        if p == l:
            break
    return hull
```

### Построение выпуклой оболочки методом Грэхема
```python
def graham_convex_hull(points: list[(int, int)]):
    points = sorted([Point(*point) for point in points], key=lambda point: (point.x, point.y))
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(Point(*p))
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(Point(*p))
    return lower[:-1] + upper[:-1]
```

## Выводы
В ходе выполнения лабораторной работы был разработан элементарный графический редактор, который позволяет выполнять различные геометрические преобразования на полигонах. Программа успешно проверяет полигоны на выпуклость, находит внутренние нормали, строит выпуклые оболочки методами Грэхема и Джарвиса, а также определяет точки пересечения отрезков и принадлежность точек полигонам. Реализованные алгоритмы работают корректно и позволяют эффективно решать поставленные задачи.

</details>

# Лабораторная работа №6

<details>  
  <summary>Раскрыть описание лабораторной работы</summary>

## Цель работы
Целью данной лабораторной работы является разработка элементарного графического редактора, который позволяет выполнять построение полигонов и их заполнение с использованием различных алгоритмов растровой развертки и заполнения с затравкой. Программа должна поддерживать режим отладки для визуализации пошагового выполнения алгоритмов.

## Задание
Разработать элементарный графический редактор, реализующий построение полигонов и их заполнение, используя:
1. **Алгоритм растровой развертки с упорядоченным списком ребер**.
2. **Алгоритм растровой развертки с использованием списка активных ребер**.
3. **Простой алгоритм заполнения с затравкой**.
4. **Построчный алгоритм заполнения с затравкой**.

Выбор алгоритма должен задаваться из пункта меню и быть доступен через панель инструментов «Алгоритмы заполнения полигонов». В редакторе должен быть предусмотрен режим отладки, где отображается пошаговое решение.

## Основные теоретические сведения
### Алгоритмы заполнения полигонов
1. **Алгоритм растровой развертки с упорядоченным списком ребер**:
   - Ребра полигона сортируются по координате Y.
   - Для каждой строки растра определяются пересечения с ребрами и заполняются пиксели между точками пересечения.

2. **Алгоритм растровой развертки с использованием списка активных ребер**:
   - Поддерживается список активных ребер (AEL), которые пересекают текущую строку растра.
   - Для каждой строки растра обновляется AEL, и заполняются пиксели между точками пересечения.

3. **Простой алгоритм заполнения с затравкой**:
   - Начиная с заданной точки (затравки), заполняются все соседние пиксели, пока не встретится граница полигона.

4. **Построчный алгоритм заполнения с затравкой**:
   - Заполнение происходит построчно, начиная с затравки. Для каждой строки определяются границы заполнения, что позволяет уменьшить количество рекурсивных вызовов.

### Режим отладки
Режим отладки позволяет визуализировать пошаговое выполнение алгоритмов, что помогает понять их работу и выявить возможные ошибки.

## Скриншоты программы
![image](https://github.com/user-attachments/assets/b5ef5245-6331-4c95-85fa-e2e5e793d1d7)


## Листинг кода

### Алгоритм растровой развертки с упорядоченным списком ребер
```python
def scanline_fill(self, fill_color=BLUE):
    min_y = min(point.y for point in self.points)
    max_y = max(point.y for point in self.points)
    filled_points = []

    for y in range(min_y, max_y + 1):
        intersections = []
        for point1, point2 in zip(self.points, self.points[1:] + [self.points[0]]):  # Обход по ребрам
            x1, y1 = point1.x, point1.y
            x2, y2 = point2.x, point2.y

            if y1 == y2:
                continue

            if min(y1, y2) <= y < max(y1, y2):
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersections.append(x)

        intersections.sort()

        for i in range(0, len(intersections) - 1, 2):
            x_start = round(intersections[i])
            x_end = round(intersections[i + 1])

            for x in range(x_start, x_end + 1):
                filled_points.append(Point(x, y, color=fill_color))

    return filled_points
```

### Алгоритм растровой развертки с использованием списка активных ребер
```python
def active_edge_fill(self, fill_color=RED):
    min_y = min(point.y for point in self.points)
    max_y = max(point.y for point in self.points)
    filled_points = []

    edges = []
    for point1, point2 in self:
        if point1.y != point2.y:
            edges.append((point1, point2))

    edges.sort(key=lambda edge: min(edge[0].y, edge[1].y))

    ael = []
    current_y = min_y

    while current_y <= max_y:
        for edge in edges:
            if min(edge[0].y, edge[1].y) == current_y:
                ael.append(edge)

        ael = [edge for edge in ael if max(edge[0].y, edge[1].y) > current_y]

        ael.sort(key=lambda edge: edge[0].x + (current_y - edge[0].y) * (edge[1].x - edge[0].x) / (edge[1].y - edge[0].y))

        for i in range(0, len(ael), 2):
            x_start = int(ael[i][0].x + (current_y - ael[i][0].y) * (ael[i][1].x - ael[i][0].x) / (ael[i][1].y - ael[i][0].y))
            x_end = int(ael[i + 1][0].x + (current_y - ael[i + 1][0].y) * (ael[i + 1][1].x - ael[i + 1][0].x) / (ael[i + 1][1].y - ael[i + 1][0].y))
            for x in range(x_start, x_end + 1):
                debug_info = {
                    "current_y": current_y,
                    "x_start": x_start,
                    "x_end": x_end,
                }
                filled_points.append(Point(x, current_y, debug=debug_info, color=fill_color))

        current_y += 1

    return filled_points
```

### Простой алгоритм заполнения с затравкой
```python
def flood_fill(self, start_x, start_y, fill_color=GREEN):
    filled_points = []
    filled = set()
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack.pop()
        if (x, y) not in filled and self.point_in_polygon(x, y):
            debug_info = {
                "in_poly?": self.point_in_polygon(x, y),
                "x": x,
                "y": y,
            }
            filled_points.append(Point(x, y, color=GREEN, debug=debug_info))
            filled.add((x, y))
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

    return filled_points
```

### Построчный алгоритм заполнения с затравкой
```python
def scanline_flood_fill(self, start_x, start_y, width, height, fill_color=YELLOW):
    filled_points = []
    filled = set()
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack.pop()
        if (x, y) not in filled and self.point_in_polygon(x, y):
            left = x
            while left >= 0 and (left, y) not in filled and self.point_in_polygon(left, y):
                debug_info = {
                    "x=left": left,
                    "y": y,
                }
                filled_points.append(Point(left, y, color=fill_color, debug=debug_info))
                filled.add((left, y))
                left -= 1
            right = x + 1
            while right < width and (right, y) not in filled and self.point_in_polygon(right, y):
                debug_info = {
                    "x=right": right,
                    "y": y,
                }
                filled_points.append(Point(right, y, color=fill_color, debug=debug_info))
                filled.add((right, y))
                right += 1
            for i in range(left + 1, right):
                if y + 1 < height and (i, y + 1) not in filled and self.point_in_polygon(i, y + 1):
                    stack.append((i, y + 1))
                if y - 1 >= 0 and (i, y - 1) not in filled and self.point_in_polygon(i, y - 1):
                    stack.append((i, y - 1))

    return filled_points
```

## Выводы
В ходе выполнения лабораторной работы был разработан элементарный графический редактор, который позволяет выполнять построение полигонов и их заполнение с использованием различных алгоритмов растровой развертки и заполнения с затравкой. Программа поддерживает режим отладки, что позволяет визуализировать пошаговое выполнение алгоритмов. Реализованные алгоритмы работают корректно и позволяют эффективно решать поставленные задачи.

</details>


# Лабораторная работа №7

<details>  
  <summary>Раскрыть описание лабораторной работы</summary>

## Цель работы
Целью данной лабораторной работы является разработка графической программы, которая выполняет триангуляцию Делоне и строит диаграмму Вороного по заданному набору точек. Это позволит изучить основы вычислительной геометрии и применение этих методов в практических задачах.

## Задание
Разработать графическую программу, выполняющую триангуляцию Делоне и построение диаграммы Вороного по заданному набору точек.

## Основные теоретические сведения
### Триангуляция Делоне
Триангуляция Делоне — это разбиение множества точек на плоскости на треугольники таким образом, что ни одна точка не попадает внутрь описанной окружности любого треугольника. Это обеспечивает максимальную равномерность треугольников и минимизирует "острые" углы.

### Диаграмма Вороного
Диаграмма Вороного — это разбиение плоскости на области (ячейки), где каждая ячейка соответствует одной точке из заданного множества. Все точки внутри ячейки ближе к соответствующей точке, чем к любой другой точке из множества.

## Скриншоты программы

## Листинг кода

### Алгоритм
```python
    def build_voronoi(self):
        points = np.array([[x / self.width, y / self.height] for x, y in self.voronoi_points])

        triang = tri.Triangulation(points[:, 0], points[:, 1])
        circumcenters = np.zeros((len(triang.triangles), 2))
        for i, t in enumerate(triang.triangles):
            pts = points[t]
            A = np.column_stack((pts, np.ones(3)))
            b = np.sum(pts ** 2, axis=1)
            circumcenters[i] = np.linalg.solve(A, b)[:2] / 2

        voronoi_edges = []
        infinite_edges = []

        window = (0, 0, 1, 1)

        for i, t in enumerate(triang.triangles):
            for j in range(3):
                neighbor = triang.neighbors[i][j]
                if neighbor != -1:
                    c1, c2 = circumcenters[i], circumcenters[neighbor]
                    voronoi_edges.append((c1, c2))
                else:
                    p1, p2 = points[t[j]], points[t[(j + 1) % 3]]
                    midpoint = (p1 + p2) / 2
                    direction = midpoint - circumcenters[i]
                    alt_direction = direction * -1
                    direction /= np.linalg.norm(direction)
                    alt_direction /= np.linalg.norm(alt_direction)
                    far_point = circumcenters[i] + direction * 2  # Extend outward
                    alt_far_point = circumcenters[i] + alt_direction * 2  # Extend outward
                    correct_edge = choose_correct_infinite_edge(
                        [(circumcenters[i], far_point), (circumcenters[i], alt_far_point)], circumcenters[i], window)
                    (x1, y1), (x2, y2) = correct_edge
                    if (0 < x1 < 1) and (0 < y1 < 1):
                        infinite_edges.append(correct_edge)
        self.clear()
        for c1, c2 in voronoi_edges:
            self.canvas.create_line(c1[0] * self.width, c1[1] * self.height,
                                    c2[0] * self.width, c2[1] * self.height,
                                    fill="blue", width=2)

        for c1, c2 in infinite_edges:
            self.canvas.create_line(c1[0] * self.width, c1[1] * self.height,
                                    c2[0] * self.width, c2[1] * self.height,
                                    fill="blue", width=2, dash=(4, 2))

        for x, y in points:
            self.canvas.create_oval(x * self.width - 3, y * self.height - 3,
                                    x * self.width + 3, y * self.height + 3,
                                    fill="red", outline="red")

        self.voronoi_points.clear()
```

## Выводы
В ходе выполнения лабораторной работы была разработана программа, которая успешно выполняет триангуляцию Делоне и строит диаграмму Вороного для заданного набора точек. Это позволило на практике изучить и применить методы вычислительной геометрии, что является важным навыком для решения задач, связанных с анализом и визуализацией данных.

</details>
