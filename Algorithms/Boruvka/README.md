# Boruvka's Algorithm — Minimum Spanning Tree (MST) & Fail Cases

## Prerequisites to Run the Code

- **Python**: Python 3 (tested on Programiz).
- **Dependencies**: **None** (Pure Python standard library).

---

## Instructions to Run the Code

### A. Run the Program

Execute Boruvka's algorithm using:

```bash
python implementation.py
```

### B. Enter the Graph
1. Enter the vertices separated by spaces:
```text
A B C D E F G
```
2. Enter the number of edges.
3. Enter each edge using the format:
```text
vertex1 vertex2 weight
```
For example:
```text
A B 7
A C 6
A G 5
```
The program will calculate and display the Minimum Spanning Tree (MST) and its total weight.

### C. Simulate Failure Cases

After the original MST is displayed, enter one of the following failure types:
```text
edge
node
none
```
For an edge failure, enter the two vertices of the failed edge:
```text
F E
```
For a node failure, enter the failed node:
```text
C
```
The program will recalculate the MST using the remaining graph.

## Result of Sample Run
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
After edge F-E fails, the edge is removed from the graph. Boruvka's algorithm recalculates the cheapest outgoing edges and selects another available edge to reconnect the components.

In this case, C-E with weight 7 is selected as the replacement edge.

The adapted MST has a total weight of 34, which is 2 more than the original MST.

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
After node C fails, the node and all edges connected to it are removed from the graph. Boruvka's algorithm then recalculates the cheapest outgoing edges using the remaining graph.

The algorithm successfully connects all remaining vertices, resulting in an adapted MST with a total weight of 28.

## AI Tools Usage Disclosure
In compliance with Institut Teknologi Sepuluh Nopember academic honesty guidelines for group coursework:

- **AI Model / Assistant Used**: ChatGPT
- **Scope of AI Assistance**:
1. Assisted in understanding Boruvka's algorithm and its implementation.
2. Assisted in reviewing the implementation and failure simulation.
3. Assisted in preparing sample test cases and README documentation.
- **Verification & Ownership**: All source code, test results, and explanations have been reviewed, verified, and tested by the group members.
