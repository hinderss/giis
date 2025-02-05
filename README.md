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

### Листинг кода:

#### Рисование окружности:
```python
def bresenham_circle(x0, y0, radius):
    x, y = 0, radius
    d = 3 - 2 * radius
    points = []

    def plot_circle_points(cx, cy, x, y, d=None):
        points.extend([
            Point(cx + x, cy + y, debug={"x": cx + x, "y": cy + y, "d": f"{d} < 0"}), Point(cx - x, cy + y, debug={"x": cx - x, "y": cy + y, "d": f"{d} < 0"}),
            Point(cx + x, cy - y, debug={"x": cx + x, "y": cy - y, "d": f"{d} < 0"}), Point(cx - x, cy - y, debug={"x": cx - x, "y": cy - y, "d": f"{d} < 0"}),
            Point(cx + y, cy + x, debug={"x": cx + y, "y": cy + x, "d": f"{d} < 0"}), Point(cx - y, cy + x, debug={"x": cx - y, "y": cy + x, "d": f"{d} < 0"}),
            Point(cx + y, cy - x, debug={"x": cx + y, "y": cy - x, "d": f"{d} < 0"}), Point(cx - y, cy - x, debug={"x": cx - y, "y": cy - x, "d": f"{d} < 0"}),
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
            Point(cx + x, cy + y, debug={"x": cx + x, "y": cy + y, "d2": f"{d} {string}"}), Point(cx - x, cy + y, debug={"x": cx - x, "y": cy + y, "d2": f"{d} {string}"}),
            Point(cx + x, cy - y, debug={"x": cx + x, "y": cy - y, "d2": f"{d} {string}"}), Point(cx - x, cy - y, debug={"x": cx - x, "y": cy - y, "d2": f"{d} {string}"})
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
        points.append(Point(x + x0, y + y0, debug={"x": x + x0, "y": y + y0, "d_pre": f"{d_pre:.3f} < 0", "d_post": f"{d_post:.3f} >= 0"}))
        points.append(Point(-x + x0, y + y0, debug={"x": x + x0, "y": y + y0, "d_pre": f"{d_pre:.3f} < 0", "d_post": f"{d_post:.3f} >= 0"}))

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

        points.append(Point(x0 - x, y0 - y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))
        points.append(Point(x0 + x, y0 + y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))
        points.append(Point(x0 + x, y0 - y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))
        points.append(Point(x0 - x, y0 + y, debug={"x": x0-x, "y": y0-y, "F1": f1, "F2": f2}))

        x = x + 1 if f1 else x
        y = y + 1 if f2 else y

        d = d + b * (2 * x + 1) if f1 else d
        d = d - a * (2 * y - 1) if f2 else d

    return points
```

### Выводы:  
В ходе лабораторной работы студенты изучат основные алгоритмы построения кривых второго порядка, проанализируют их эффективность и особенности, а также реализуют графический редактор с возможностью визуализации процесса построения.  


</details>