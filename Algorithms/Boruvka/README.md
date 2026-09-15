# Boruvka's Algorithm — Minimum Spanning Tree (MST) & Fail Cases

## Prerequisites to Run the Code

- **Python**: Python 3 (tested on Programiz)
- No additional libraries are required
---

## Instructions to Run the Code
1. Open the terminal in the project directory
2. Run the following command:

```bash
python implementation.py
```
3. Enter the vertices when it's prompted
4. Enter the number for the edges
5. Enter each edge using the format:
```text
vertex1 vertex2 weight
```
6. The program will display the Minimum Spanning Tree (MST) and it's total weight

---

## Samples Result
### 1. Successful Run

```text
Minimum Spanning Tree:
A - G : 5
C - B : 5
F - E : 5
E - D : 5
A - C : 6
G - F : 6
Total Weight: 32
```
All vertices are successfully connected and the resulting Minimum Spanning Tree has a total weight of 32.

### 2. Failure Scenario — Edge F-E
```text
Original MST Weight : 32
Failed Edge         : F-E (5)
Adapted MST Weight  : 34
Cost Difference     : +2
```
The adapted Minimum Spanning Tree is:
```text
A - G : 5
B - C : 5
D - E : 5
F - G : 6
A - C : 6
C - E : 7

Total Weight: 34
```
Boruvka's algorithm ignores the failed edge and searches for another cheapest outgoing edge to reconnect the components, so In this case, C-E with weight 7 is selected as the replacement edge

### 3. Failure Scenario — Node C

Node C is assumed to be failed and cannot be traversed. All edges connected to C are therefore removed.
```text
Original MST Weight : 32
Failed Node         : C
Adapted MST Weight  : 28
Cost Difference     : -4
```
The adapted Minimum Spanning Tree for the remaining vertices is:
```text
A - G : 5
D - E : 5
E - F : 5
F - G : 6
A - B : 7

Total Weight: 28
```
Boruvka's algorithm recalculates the cheapest outgoing edges using the remaining graph and successfully connects all remaining vertices.
