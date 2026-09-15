import heapq


def prim_mst(vertices, edges, start=None, verbose=True):
    """
    vertices: list of vertex labels, e.g. ['A','B','C','D','E','F','G']
    edges:    list of tuples (u, v, weight) -- undirected
    start:    starting vertex (defaults to the first vertex in the list)
    returns:  (mst_edges, total_cost, steps) where steps is the table data
    """
    if not vertices:
        return [], 0, []

    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))

    if start is None or start not in adj:
        start = vertices[0]

    in_tree = {start}          
    mst_edges = []            
    steps = []                 
    heap = []                  

    for w, nxt in adj[start]:
        heapq.heappush(heap, (w, start, nxt))

    steps.append({
        "step": 0,
        "U": set(),
        "edge": None,
        "weight": None,
        "outside": set(vertices),
    })

    if verbose:
        print(f"Starting Prim's Algorithm from vertex '{start}'\n")

    step_no = 1
    while heap and len(in_tree) < len(vertices):
        w, u, v = heapq.heappop(heap)

      
        if v in in_tree:
            if verbose:
                print(f"  (skipped {u}-{v} = {w}, would create a cycle)")
            continue

        
        in_tree.add(v)
        mst_edges.append((u, v, w))

        steps.append({
            "step": step_no,
            "U": set(in_tree),
            "edge": f"{u}-{v}",
            "weight": w,
            "outside": set(vertices) - in_tree,
        })

        if verbose:
            print(f"Step {step_no}: add edge {u}-{v} (weight {w})"
                  f"  ->  U = {{{', '.join(sorted(in_tree))}}}")

        step_no += 1

        # Queue the newly reachable edges from v
        for w2, nxt in adj[v]:
            if nxt not in in_tree:
                heapq.heappush(heap, (w2, v, nxt))

    total_cost = sum(w for _, _, w in mst_edges)

    if len(in_tree) < len(vertices):
        missing = sorted(set(vertices) - in_tree)
        if verbose:
            print(f"\nWARNING: graph is disconnected. "
                  f"Unreachable vertices: {missing}")
            print("Prim's produced a spanning tree of the reachable "
                  "component only (a minimum spanning FOREST component).")

    return mst_edges, total_cost, steps


def print_step_table(steps, vertices):
    """Prints the step-by-step table in the same style as the sample report."""
    print("\n" + "=" * 68)
    print(f"{'Step':<6}{'U (in tree)':<26}{'Edge(u,v)':<14}{'V - U':<22}")
    print("=" * 68)
    for s in steps:
        u_set = "{" + ", ".join(sorted(s["U"])) + "}" if s["U"] else "{ }"
        out = "{" + ", ".join(sorted(s["outside"])) + "}" if s["outside"] else "{ }"
        edge = f"{s['edge']} = {s['weight']}" if s["edge"] else "-"
        print(f"{s['step']:<6}{u_set:<26}{edge:<14}{out:<22}")
    print("=" * 68)


def simulate_failure(vertices, edges, start='A',
                     failed_edge=None, failed_node=None):
    """
    Task 4: re-run Prim's after a node or an edge becomes untraversable.
    """
    new_vertices = list(vertices)
    new_edges = list(edges)

    if failed_node is not None:
        new_vertices = [v for v in new_vertices if v != failed_node]
        new_edges = [(u, v, w) for (u, v, w) in new_edges
                     if u != failed_node and v != failed_node]
        print(f"--- Simulating failure of NODE '{failed_node}' ---")
        if start == failed_node:
            start = new_vertices[0] if new_vertices else None
            print(f"    (start vertex failed, restarting from '{start}')")

    if failed_edge is not None:
        fu, fv = failed_edge
        new_edges = [(u, v, w) for (u, v, w) in new_edges
                     if {u, v} != {fu, fv}]
        print(f"--- Simulating failure of EDGE '{fu}-{fv}' ---")

    print()
    return prim_mst(new_vertices, new_edges, start=start)


if __name__ == "__main__":
    vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    edges = [
        ('A', 'B', 7),
        ('A', 'C', 6),
        ('A', 'G', 5),
        ('A', 'F', 10),
        ('B', 'C', 5),
        ('B', 'D', 7),
        ('B', 'E', 9),
        ('C', 'E', 7),
        ('C', 'F', 9),
        ('D', 'E', 5),
        ('E', 'F', 5),
        ('F', 'G', 6),
    ]
    

    print("=" * 68)
    print("RUN 1: Normal graph, starting from A")
    print("=" * 68)
    mst, cost, steps = prim_mst(vertices, edges, start='A')
    print_step_table(steps, vertices)
    print(f"\nMST edges : {[(u, v, w) for u, v, w in mst]}")
    print(f"Total cost: {cost}")

    print("\n\n" + "=" * 68)
    print("RUN 2: Edge failure -- A-G cannot be traversed")
    print("=" * 68)
    mst2, cost2, _ = simulate_failure(vertices, edges, start='A',
                                      failed_edge=('A', 'G'))
    print(f"\nMST edges : {mst2}")
    print(f"Total cost: {cost2}  (was {cost}, difference +{cost2 - cost})")

    print("\n\n" + "=" * 68)
    print("RUN 3: Node failure -- C is down")
    print("=" * 68)
    mst3, cost3, _ = simulate_failure(vertices, edges, start='A',
                                      failed_node='C')
    print(f"\nMST edges : {mst3}")
    print(f"Total cost: {cost3}  (spanning 6 vertices instead of 7)")

    print("\n\n" + "=" * 68)
    print("RUN 4: Node failure -- G is down (G is a degree-2 vertex)")
    print("=" * 68)
    mst4, cost4, _ = simulate_failure(vertices, edges, start='A',
                                      failed_node='G')
    print(f"\nMST edges : {mst4}")
    print(f"Total cost: {cost4}")

    print("\n\n" + "=" * 68)
    print("RUN 5: Start vertex does not change the MST cost")
    print("=" * 68)
    for s in vertices:
        m, c, _ = prim_mst(vertices, edges, start=s, verbose=False)
        print(f"  start = {s}: total cost = {c}")
