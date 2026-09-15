# Boruvka's Algorithm
# Finding Minimum Spanning Tree (MST)

# Input vertices
vertices = input("Enter vertices (separated by spaces): ").split()

# Input edges
edges = []

edge_count = int(input("Enter number of edges: "))

print("Enter each edge in the format: vertex1 vertex2 weight")

for i in range(edge_count):
    u, v, weight = input(f"Edge {i + 1}: ").split()
    edges.append((u, v, int(weight)))


# Disjoint Set
parent = {v: v for v in vertices}


def find(v):
    if parent[v] != v:
        parent[v] = find(parent[v])
    return parent[v]


def union(a, b):
    root_a = find(a)
    root_b = find(b)

    if root_a == root_b:
        return False

    parent[root_b] = root_a
    return True


# Boruvka Algorithm
mst = []
total_weight = 0

while len(mst) < len(vertices) - 1:

    # Menyimpan edge termurah
    # untuk setiap component
    cheapest = {}

    for u, v, weight in edges:

        root_u = find(u)
        root_v = find(v)

        # Edge harus menghubungkan
        # dua component yang berbeda
        if root_u == root_v:
            continue

        if root_u not in cheapest or weight < cheapest[root_u][2]:
            cheapest[root_u] = (u, v, weight)

        if root_v not in cheapest or weight < cheapest[root_v][2]:
            cheapest[root_v] = (u, v, weight)

    # Gabungkan component
    for u, v, weight in cheapest.values():

        if union(u, v):
            mst.append((u, v, weight))
            total_weight += weight


# Output
print("\nMinimum Spanning Tree:")

for u, v, weight in mst:
    print(f"{u} - {v} : {weight}")

print("Total Weight:", total_weight)

for u, v, weight in mst:
    print(f"{u} - {v} : {weight}")

print("Total Weight:", total_weight)
