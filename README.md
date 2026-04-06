# Programming Assignment 3: Highest Value Longest Common Sequence

## Student Information
- Student: Ethan Haines
- UFID: 35007385


## Run Instructions
Run the solver on the provided example:

```powershell
python src\hvlcs.py data\input\example.in
```

Expected output:

```text
9
cb
```

Run the runtime experiment and regenerate the graph:

```powershell
python src\benchmark.py
```

## Assumptions
- Each alphabet line contains one character and one nonnegative integer value.
- Strings `A` and `B` contain only characters listed in the alphabet table.
- If multiple optimal subsequences exist, any one of them is acceptable.
- If the maximum value is 0, the subsequence output may be empty.

## Question 1: Empirical Comparison
I used the 10 input files in `data/input/1.in` through `data/input/10.in`. Each file contains strings of length at least 25. The benchmark script solves each file repeatedly, computes the median per-run time in milliseconds, writes the raw results to `graph/runtime_results.csv`, and generates the graph in `graph/runtime_graph.svg`.

### Runtime Results

| File | A length | B length | Median runtime (ms) |
| --- | ---: | ---: | ---: |
| 1.in | 25 | 29 | 0.1229 |
| 2.in | 30 | 34 | 0.2136 |
| 3.in | 35 | 39 | 0.3026 |
| 4.in | 40 | 44 | 0.3855 |
| 5.in | 45 | 49 | 0.3743 |
| 6.in | 50 | 54 | 0.5566 |
| 7.in | 55 | 59 | 0.7017 |
| 8.in | 60 | 64 | 0.7384 |
| 9.in | 65 | 69 | 1.0243 |
| 10.in | 70 | 74 | 1.0104 |

The curve increases as the string lengths increase, which matches the dynamic programming table size of `(m + 1)(n + 1)`.

## Question 2: Recurrence Equation
Let `OPT(i, j)` be the maximum total value of a common subsequence between the prefixes `A[1..i]` and `B[1..j]`.

Base cases:

- `OPT(i, 0) = 0` for all `i >= 0`
- `OPT(0, j) = 0` for all `j >= 0`

Recurrence:

- If `A[i] = B[j]`, then
  - `OPT(i, j) = max(OPT(i - 1, j), OPT(i, j - 1), OPT(i - 1, j - 1) + value(A[i]))`
- Otherwise
  - `OPT(i, j) = max(OPT(i - 1, j), OPT(i, j - 1))`

Correctness explanation:
Any optimal common subsequence for prefixes `A[1..i]` and `B[1..j]` falls into one of two structural cases. Either it does not use at least one of the last characters, which gives the subproblems `OPT(i - 1, j)` or `OPT(i, j - 1)`, or it uses both last characters together. The second case is only legal when `A[i] = B[j]`, and then the remaining prefix problem is `OPT(i - 1, j - 1)` plus the value of the matched character. Since every optimal solution must fall into one of these cases and the remainder of each case must itself be optimal, taking the maximum gives the correct recurrence.

## Question 3: Pseudocode and Big-Oh

```text
HVLCS(A, B, value):
    let m = length(A)
    let n = length(B)
    create table DP[0..m][0..n], initialized to 0

    for i = 1 to m:
        for j = 1 to n:
            DP[i][j] = max(DP[i - 1][j], DP[i][j - 1])
            if A[i] == B[j]:
                DP[i][j] = max(DP[i][j], DP[i - 1][j - 1] + value(A[i]))

    return DP[m][n]
```

The table has `(m + 1)(n + 1)` entries, and each entry is filled in constant time, so the runtime is `O(mn)`. The table also uses `O(mn)` space. Reconstructing one optimal subsequence takes `O(m + n)` time by tracing backward through the table.
