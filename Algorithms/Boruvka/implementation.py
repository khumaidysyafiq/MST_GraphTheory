# Boruvka's Algorithm
# Finding Minimum Spanning Tree (MST)


# Boruvka Algorithm
def boruvka(vertices, edges):

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

    mst = []
    total_weight = 0

    while len(mst) < len(vertices) - 1:

        cheapest = {}

        for u, v, weight in edges:

            root_u = find(u)
            root_v = find(v)

            if root_u == root_v:
                continue

            if root_u not in cheapest or weight < cheapest[root_u][2]:
                cheapest[root_u] = (u, v, weight)

            if root_v not in cheapest or weight < cheapest[root_v][2]:
                cheapest[root_v] = (u, v, weight)

        if not cheapest:
            break

        for u, v, weight in cheapest.values():

            if union(u, v):
                mst.append((u, v, weight))
                total_weight += weight

    return mst, total_weight


# Input vertices
vertices = input("Enter vertices (separated by spaces): ").split()

# Input edges
edges = []

edge_count = int(input("Enter number of edges: "))

print("Enter each edge in the format: vertex1 vertex2 weight")

for i in range(edge_count):
    u, v, weight = input(f"Edge {i + 1}: ").split()
    edges.append((u, v, int(weight)))


# -------------------------
# Successful Run
# -------------------------

mst, total_weight = boruvka(vertices, edges)

print("\nMinimum Spanning Tree:")
for u, v, weight in mst:
    print(f"{u} - {v} : {weight}")

print("Total Weight:", total_weight)


# -------------------------
# Failure Simulation
# -------------------------

failure = input(
    "\nEnter failure type (edge/node/none): "
).lower()


# Edge Failure
if failure == "edge":

    failed_u, failed_v = input(
        "Enter failed edge (e.g. F E): "
    ).split()

    failed_edges = [
        edge for edge in edges
        if not (
            (edge[0] == failed_u and edge[1] == failed_v)
            or
            (edge[0] == failed_v and edge[1] == failed_u)
        )
    ]

    new_mst, new_weight = boruvka(vertices, failed_edges)

    print("\nMST After Edge Failure:")
    for u, v, weight in new_mst:
        print(f"{u} - {v} : {weight}")

    if len(new_mst) == len(vertices) - 1:
        print("Total Weight:", new_weight)
    else:
        print("A spanning tree cannot be formed.")


# Node Failure
elif failure == "node":

    failed_node = input("Enter failed node: ")

    remaining_vertices = [
        v for v in vertices
        if v != failed_node
    ]

    remaining_edges = [
        edge for edge in edges
        if edge[0] != failed_node
        and edge[1] != failed_node
    ]

    new_mst, new_weight = boruvka(
        remaining_vertices,
        remaining_edges
    )

    print("\nMST After Node Failure:")
    for u, v, weight in new_mst:
        print(f"{u} - {v} : {weight}")

    if len(new_mst) == len(remaining_vertices) - 1:
        print("Total Weight:", new_weight)
    else:
        print("A spanning tree cannot be formed.")


elif failure == "none":

    print("\nNo failure simulation performed.")
