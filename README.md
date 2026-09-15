# Informatics ITS Graph Theory IUP 
## Group 1 Assignment 2

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

*Brovka's:*
- Python 3.x
- No additional libraries are required.

### Instructions

### Samples

## Extras
