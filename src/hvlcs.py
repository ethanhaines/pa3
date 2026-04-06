import sys


class HVLCSInstance:
    def __init__(self, alphabet_values, first_string, second_string):
        self.alphabet_values = alphabet_values
        self.a = first_string
        self.b = second_string


def parse_instance(filename):
    with open(filename, "r", encoding="utf-8") as infile:
        lines = infile.read().splitlines()

    alphabet_size = int(lines[0])

    alphabet_values = {}
    index = 1

    for _ in range(alphabet_size):
        parts = lines[index].split()
        symbol = parts[0]
        alphabet_values[symbol] = int(parts[1])
        index += 1

    first_string = lines[index]
    second_string = lines[index + 1]

    return HVLCSInstance(alphabet_values, first_string, second_string)


def build_value_table(instance):
    first_string = instance.a
    second_string = instance.b
    alphabet_values = instance.alphabet_values

    rows = len(first_string) + 1
    cols = len(second_string) + 1
    table = []

    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(0)
        table.append(row)

    for i in range(1, rows):
        for j in range(1, cols):
            best_value = table[i - 1][j]

            if table[i][j - 1] > best_value:
                best_value = table[i][j - 1]

            if first_string[i - 1] == second_string[j - 1]:
                match_value = table[i - 1][j - 1] + alphabet_values[first_string[i - 1]]
                if match_value > best_value:
                    best_value = match_value

            table[i][j] = best_value

    return table


def reconstruct_subsequence(instance, table):
    first_string = instance.a
    second_string = instance.b
    alphabet_values = instance.alphabet_values
    i = len(first_string)
    j = len(second_string)
    chosen = []

    while i > 0 and j > 0:
        if table[i][j] == table[i - 1][j]:
            i -= 1
        elif table[i][j] == table[i][j - 1]:
            j -= 1
        else:
            same_character = first_string[i - 1] == second_string[j - 1]
            right_value = table[i - 1][j - 1] + alphabet_values[first_string[i - 1]]

            if same_character and table[i][j] == right_value:
                chosen.append(first_string[i - 1])
                i -= 1
                j -= 1

    chosen.reverse()
    return "".join(chosen)


def solve(instance):
    table = build_value_table(instance)
    best_value = table[len(instance.a)][len(instance.b)]
    subsequence = reconstruct_subsequence(instance, table)
    return best_value, subsequence


def main():
    filename = sys.argv[1]
    instance = parse_instance(filename)
    best_value, subsequence = solve(instance)

    print(best_value)
    print(subsequence)


if __name__ == "__main__":
    main()

