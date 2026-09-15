# Boruvka's Algorithm
# Finding Minimum Spanning Tree (MST)

vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

edges = [
    ('A', 'B', 7),
    ('A', 'C', 6),
    ('A', 'G', 5),
    ('A', 'F', 10),
    ('G', 'F', 6),
    ('F', 'C', 9),
    ('F', 'E', 5),
    ('C', 'E', 7),
    ('C', 'B', 5),
    ('E', 'B', 9),
    ('E', 'D', 5),
    ('B', 'D', 7)
]


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
print("Minimum Spanning Tree:")

for u, v, weight in mst:
    print(f"{u} - {v} : {weight}")

print("Total Weight:", total_weight)
