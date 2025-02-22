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
Целью данной лабораторной работы является изучение методов представления и преобразования трехмерных объектов в графическом редакторе. Необходимо освоить использование матриц для выполнения определенных преобразований, а также разобраться в параметрических кривых, таких как форма Эрмита, Безье и B-сплайн.

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

