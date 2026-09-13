import os
import time
from pathlib import Path


BLUE_BG = "\x1b[44m"
WHITE_BG = "\x1b[47m"
RED_BG = "\x1b[41m"
RESET = "\x1b[0m"


def build_flag(width=30, height=6):
    if width < 3 or height < 1:
        raise ValueError("Размер флага должен быть положительным")
    blue_width = width // 3
    white_width = width // 3
    red_width = width - blue_width - white_width
    row = (
        BLUE_BG
        + " " * blue_width
        + WHITE_BG
        + " " * white_width
        + RED_BG
        + " " * red_width
        + RESET
    )
    return [row for _ in range(height)]


def build_pattern(repeats=5):
    if repeats < 1:
        raise ValueError("Число повторов должно быть положительным")
    motifs = ("██  ██", "  ██  ", "██  ██")
    return ["  ".join([motif] * repeats) for motif in motifs]


def build_plot(rows=9, x_start=1, x_end=9):
    if rows < 9:
        raise ValueError("Высота графика должна быть не менее 9 строк")
    if x_start < 0 or x_end < x_start:
        raise ValueError("Диапазон x должен быть в первом квадранте")
    xs = list(range(x_start, x_end + 1))
    values = [x**2 for x in xs]
    maximum = max(values) if values else 0
    grid = [[" " for _ in xs] for _ in range(rows)]
    for column, value in enumerate(values):
        if maximum == 0:
            row = 0
        else:
            row = round((maximum - value) / maximum * (rows - 1))
        grid[row][column] = "●"
    return [" ".join(line) for line in grid]


def format_plot(rows=9, x_start=1, x_end=9):
    plot = build_plot(rows, x_start, x_end)
    maximum = x_end**2
    lines = []
    for index, line in enumerate(plot):
        value = maximum - index * maximum / (rows - 1)
        lines.append(f"{value:6.1f} | {line}")
    width = 2 * (x_end - x_start + 1)
    lines.append("       +" + "-" * width)
    labels = " ".join(str(x) for x in range(x_start, x_end + 1))
    lines.append("         " + labels)
    return lines


def read_sequence(path="sequence.txt"):
    values = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            values.append(float(line))
    return values


def calculate_sign_statistics(numbers):
    negative_count = sum(number < 0 for number in numbers)
    positive_count = sum(number > 0 for number in numbers)
    zero_count = sum(number == 0 for number in numbers)
    classified = negative_count + positive_count
    if classified == 0:
        negative_percent = 0.0
        positive_percent = 0.0
    else:
        negative_percent = negative_count / classified * 100
        positive_percent = positive_count / classified * 100
    return {
        "negative_count": negative_count,
        "positive_count": positive_count,
        "zero_count": zero_count,
        "negative_percent": negative_percent,
        "positive_percent": positive_percent,
    }


def format_diagram(numbers):
    stats = calculate_sign_statistics(numbers)
    negative_bar = "#" * round(stats["negative_percent"] / 2)
    positive_bar = "#" * round(stats["positive_percent"] / 2)
    negative_text = (
        f"Меньше 0: {stats['negative_count']:3d} "
        f"({stats['negative_percent']:5.1f}%) {negative_bar}"
    )
    positive_text = (
        f"Больше 0: {stats['positive_count']:3d} "
        f"({stats['positive_percent']:5.1f}%) {positive_bar}"
    )
    return [
        negative_text,
        positive_text,
        f"Равны 0 : {stats['zero_count']:3d}",
    ]


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def play_animation(delay=0.5):
    frames = (
        "   o   \n  /|\\  \n  / \\  ",
        "   o   \n --|-- \n  / \\  ",
        "   o   \n  |\\   \n  / \\  ",
    )
    for frame in frames:
        clear_console()
        print(frame)
        time.sleep(delay)


def main(sequence_path="sequence.txt"):
    if os.name == "nt":
        os.system("")
    print("Флаг Франции:")
    print(*build_flag(), sep="\n")
    print("\nУзор a:")
    print(*build_pattern(), sep="\n")
    print("\nГрафик функции y = x²:")
    print(*format_plot(), sep="\n")
    print("\nДиаграмма количества чисел меньше и больше 0:")
    print(*format_diagram(read_sequence(sequence_path)), sep="\n")


if __name__ == "__main__":
    main()
