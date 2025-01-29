# Лабораторная работа №1
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

Конечно! Вот обновленный раздел с добавлением скриншотов программы:

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

---

Не забудьте заменить `path_to_screenshotX` на реальные пути к файлам скриншотов в вашем проекте.

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
