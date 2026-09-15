# Informatics ITS Graph Theory IUP 
## Group 1 Assignment 2

<div align=center>

|    NRP     |           Nama              |
| :--------: |       :------------:        |
| 5025251012 | Khumaidy Syafiq El Maududy  |
| 5025251015 | Renato Kiran Arisandi       |
| 5025251016 | Keven John Gondowardojo     |
| 5025251010 | Agile Octa Agrakha Handrian |

</div>

## Algorithm Explanation

### Prim's Algorithm 

Prim’s algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a connected, weighted, undirected graph. It works by starting from any vertex and repeatedly adding the minimum-weight edge that connects a vertex already in the MST to a vertex outside it.

__Steps__

1. Start with any vertex.

2. Select the smallest edge connecting the MST to an unvisited vertex.

3. Add that edge and vertex to the MST.

4. Repeat until all vertices are included.

### Kruskal's Algorithm 

Kruskal’s algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a connected, weighted, undirected graph. It works by selecting edges in increasing order of their weights, while making sure that no cycle is formed.

__Steps__

1. Sort all edges by their weight in ascending order.

2. Select the smallest edge.

3. Add it to the MST if it does not create a cycle.

4. Continue until the MST contains V − 1 edges.

### Boruvska's Algorithm

Boruvka’s algorithm is a greedy algorithm used to find the Minimum Spanning Tree (MST) of a connected, weighted, undirected graph. It works by finding the cheapest outgoing edge for each component and merging the components together.

__Steps__

1. Initially, treat every vertex as a separate component.

2. For each component, find its minimum-weight outgoing edge.

3. Add these edges to the MST and merge the connected components.

4. Repeat until only one component remains.

## Code

### Prerequisites

**Boruvka's:**
- Python 3.x
- No additional libraries that is required...

### Instructions

**Boruvka's:**
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

### Samples
**Boruvka's:**

**Input:**
```text
Vertices: A B C D E F G
Number of edges: 12

A B 7
A C 6
A G 5
A F 10
G F 6
F C 9
F E 5
C E 7
C B 5
E B 9
E D 5
B D 7
```
**Input:**
```text
Minimum Spanning Tree:
A - G : 5
B - C : 5
D - E : 5
E - F : 5
F - G : 6
A - C : 6

Total Weight: 32
```

## Extras
 
### PDF Report: https://docs.google.com/document/d/1dUxCAeh-EWFMoCXYLiiq1xA0WyRx0lT65QbrU_OLGAQ/edit?usp=sharing

### AI Prompts

``` explain the algorithms of Prim, Kruskal, Boruvka ```
``` i want a pyhton code for the boruvska in mst, where i can put input and errors ```
``` what are the edge cases such that traversing the graph fails ```
``` given my current code make the visualizations for the kruskal mst, allow exporting as image step by step and also gif ```
``` visualize the graph treversal in gif ```
