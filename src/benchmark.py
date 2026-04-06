import os
import time

from hvlcs import parse_instance
from hvlcs import solve


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(ROOT_DIR, "data", "input")
GRAPH_DIR = os.path.join(ROOT_DIR, "graph")
CSV_PATH = os.path.join(GRAPH_DIR, "runtime_results.csv")
SVG_PATH = os.path.join(GRAPH_DIR, "runtime_graph.svg")


def list_runtime_inputs():
    files = []

    for name in os.listdir(INPUT_DIR):
        full_path = os.path.join(INPUT_DIR, name)
        if not os.path.isfile(full_path):
            continue
        if not name.endswith(".in"):
            continue

        stem = name[:-3]
        if stem.isdigit():
            files.append(full_path)

    files.sort(key=get_input_number)
    return files


def get_input_number(path):
    name = os.path.basename(path)
    stem = name[:-3]
    return int(stem)


def median(values):
    sorted_values = list(values)
    sorted_values.sort()
    count = len(sorted_values)
    middle = count // 2

    if count % 2 == 1:
        return sorted_values[middle]

    return (sorted_values[middle - 1] + sorted_values[middle]) / 2.0


def benchmark_file(path):
    instance = parse_instance(path)
    solve(instance)

    complexity = len(instance.a) * len(instance.b)
    if complexity < 1:
        complexity = 1

    repetitions = 1000000 // complexity
    if repetitions < 100:
        repetitions = 100

    samples_ms = []

    for _ in range(5):
        start_time = time.perf_counter()
        for _ in range(repetitions):
            solve(instance)
        elapsed_seconds = time.perf_counter() - start_time
        samples_ms.append((elapsed_seconds * 1000.0) / repetitions)

    result = {}
    result["file"] = os.path.basename(path)
    result["len_a"] = len(instance.a)
    result["len_b"] = len(instance.b)
    result["repetitions"] = repetitions
    result["runtime_ms"] = median(samples_ms)
    return result


def write_csv(results):
    if not os.path.isdir(GRAPH_DIR):
        os.makedirs(GRAPH_DIR)

    with open(CSV_PATH, "w", encoding="utf-8") as outfile:
        outfile.write("file,len_a,len_b,repetitions,runtime_ms\n")
        for result in results:
            line = (
                str(result["file"]) + ","
                + str(result["len_a"]) + ","
                + str(result["len_b"]) + ","
                + str(result["repetitions"]) + ","
                + str(result["runtime_ms"]) + "\n"
            )
            outfile.write(line)


def write_svg(results):
    if not os.path.isdir(GRAPH_DIR):
        os.makedirs(GRAPH_DIR)

    width = 760
    height = 420
    left = 70
    right = 30
    top = 30
    bottom = 60
    plot_width = width - left - right
    plot_height = height - top - bottom

    y_values = []
    for result in results:
        y_values.append(float(result["runtime_ms"]))

    if len(y_values) == 0:
        max_y = 1.0
    else:
        max_y = max(y_values)
        if max_y < 0.001:
            max_y = 0.001

    tick_count = 5
    y_tick_lines = []
    x_labels = []
    circles = []
    point_list = []

    for index, result in enumerate(results):
        if len(results) == 1:
            x = left + plot_width / 2.0
        else:
            x = left + (index * plot_width / float(len(results) - 1))

        y = top + plot_height - (float(result["runtime_ms"]) / max_y) * plot_height
        point_list.append("{0:.2f},{1:.2f}".format(x, y))

        x_labels.append(
            '<text x="{0:.2f}" y="{1}" font-size="11" text-anchor="middle">{2}/{3}</text>'.format(
                x,
                height - 20,
                result["len_a"],
                result["len_b"],
            )
        )

        circles.append(
            '<circle cx="{0:.2f}" cy="{1:.2f}" r="4" fill="#0f766e" />'.format(x, y)
        )

    for tick in range(tick_count + 1):
        value = max_y * tick / float(tick_count)
        y = top + plot_height - (value / max_y) * plot_height
        y_tick_lines.append(
            '<line x1="{0}" y1="{1:.2f}" x2="{2}" y2="{1:.2f}" stroke="#d7dce2" stroke-width="1" />'.format(
                left,
                y,
                width - right,
            )
        )
        y_tick_lines.append(
            '<text x="{0}" y="{1:.2f}" font-size="11" text-anchor="end">{2:.4f}</text>'.format(
                left - 10,
                y + 4,
                value,
            )
        )

    svg_lines = []
    svg_lines.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}" viewBox="0 0 {0} {1}">'.format(
            width,
            height,
        )
    )
    svg_lines.append('<rect width="{0}" height="{1}" fill="#ffffff" />'.format(width, height))
    svg_lines.append(
        '<text x="{0:.2f}" y="18" font-size="18" text-anchor="middle" fill="#111827">HVLCS Runtime on 10 Inputs</text>'.format(
            width / 2.0
        )
    )
    svg_lines.extend(y_tick_lines)
    svg_lines.append(
        '<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" stroke="#111827" stroke-width="2" />'.format(
            left,
            top,
            height - bottom,
        )
    )
    svg_lines.append(
        '<line x1="{0}" y1="{1}" x2="{2}" y2="{1}" stroke="#111827" stroke-width="2" />'.format(
            left,
            height - bottom,
            width - right,
        )
    )
    svg_lines.append(
        '<polyline fill="none" stroke="#0f766e" stroke-width="3" points="{0}" />'.format(
            " ".join(point_list)
        )
    )
    svg_lines.extend(circles)
    svg_lines.extend(x_labels)
    svg_lines.append(
        '<text x="{0:.2f}" y="{1}" font-size="12" text-anchor="middle" fill="#111827">Input lengths |A| / |B|</text>'.format(
            width / 2.0,
            height - 4,
        )
    )
    svg_lines.append(
        '<text x="18" y="{0:.2f}" font-size="12" text-anchor="middle" transform="rotate(-90 18 {0:.2f})" fill="#111827">Median runtime (ms)</text>'.format(
            height / 2.0
        )
    )
    svg_lines.append("</svg>")

    with open(SVG_PATH, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(svg_lines))


def main():
    input_files = list_runtime_inputs()

    results = []
    for path in input_files:
        results.append(benchmark_file(path))

    write_csv(results)
    write_svg(results)

    for result in results:
        print(
            result["file"]
            + ": |A|=" + str(result["len_a"])
            + ", |B|=" + str(result["len_b"])
            + ", median=" + "{0:.4f}".format(float(result["runtime_ms"]))
            + " ms"
        )

    print("Wrote " + CSV_PATH)
    print("Wrote " + SVG_PATH)


if __name__ == "__main__":
    main()

