import dataclasses
from collections import deque


class Binary:
    def __init__(self, binary_list):
        self.value = binary_list

    def __repr__(self):
        return ''.join(map(str, self.value))

    def __ge__(self, other):
        for i in range(len(self.value)):
            if self.value[i] > other.value[i]:
                return True
            elif self.value[i] < other.value[i]:
                return False
        return True

    def __sub__(self, other):
        borrow = 0
        result = []
        for i in range(len(self.value) - 1, -1, -1):
            diff = self.value[i] - other.value[i] - borrow
            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0
            result.insert(0, diff)
        return Binary(result)

    def shift_left(self):
        return Binary(self.value[1:] + [0])

    def append_bit(self, bit):
        return Binary(self.value + [bit])

    def length(self):
        return len(self.value)


class Step:
    def __init__(self, index):
        self.index = index

    def __call__(self, data: "Data"):
        quotient = data.quotient
        remainder = data.remainder
        dividend = data.dividend
        divisor = data.divisor

        remainder = remainder.shift_left()
        remainder.value[-1] = dividend.value[self.index]

        if remainder >= divisor:
            remainder = remainder - divisor
            quotient = quotient.append_bit(1)
        else:
            quotient = quotient.append_bit(0)

        return quotient, remainder


@dataclasses.dataclass
class Data:
    dividend: Binary
    divisor: Binary
    quotient: Binary
    remainder: Binary

    def __init__(self, dividend: Binary, divisor: Binary, quotient: Binary = None, remainder: Binary = None):
        self.dividend: Binary = dividend
        self.divisor: Binary = divisor
        if not quotient:
            self.quotient = Binary([])
        else:
            self.quotient = quotient
        if not remainder:
            self.remainder = Binary([0] * dividend.length())
        else:
            self.remainder = remainder

    def set(self, quotient: Binary, remainder: Binary):
        self.quotient = quotient
        self.remainder = remainder


class Pipeline:
    def __init__(self, steps: list):
        self.steps = steps
        self.pipes = [deque() for _ in range(len(steps) + 1)]
        self.length = 0

        self.stages: list[tuple[deque, Step, deque]] = []
        for i in range(len(steps)):
            input_pipe = self.pipes[i]
            output_pipe = self.pipes[i + 1]
            self.stages.append((input_pipe, steps[i], output_pipe))

    def __call__(self, pairs: list[Data]):
        self.length = len(pairs)
        self.pipes[0].extend(pairs)

        while len(self.pipes[-1]) < self.length:
            for input_pipe, step, output_pipe in reversed(self.stages):
                try:
                    input_data: Data = input_pipe.pop()
                except IndexError:
                    continue
                quotient, remainder = step(input_data)

                input_data.set(quotient, remainder)
                output_pipe.appendleft(input_data)

        return self.pipes[-1]


pipeline = Pipeline([Step(0), Step(1), Step(2), Step(3), Step(4), Step(5)])
input_data = [Data(Binary([1, 0, 1, 0, 1, 1]), Binary([0, 0, 0, 1, 1, 0])), Data(Binary([0, 0, 1, 0, 1, 0]), Binary([0, 0, 0, 1, 1, 0]))]
x = pipeline(input_data)


print(x)
# quotient, remainder = binary_division(Binary([1, 0, 1, 0, 1, 1]), Binary([0, 0, 0, 1, 1, 0]))

quotient_str = ''.join(map(str, quotient.value))
remainder_str = ''.join(map(str, remainder.value))

print(f"Частное: {quotient_str}")
print(f"Остаток: {remainder_str}")
