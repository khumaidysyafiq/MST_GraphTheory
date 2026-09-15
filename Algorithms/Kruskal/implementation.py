#!/usr/bin/env python3
"""
kruskal_mst.py
==============
Senior-grade implementation of Kruskal's Algorithm for Minimum Spanning Tree (MST),
featuring Disjoint Set Union (DSU / Union-Find) with path compression and union by rank.

Includes dynamic failure simulation:
- Simulates edge failures (blocked roads, severed links)
- Simulates node failures (destroyed junctions, downed vertices)
- Automatically adapts to find new MST or Minimum Spanning Forest (MSF)
- Generates detailed step-by-step execution traces and adaptation comparative reports.

Graph modeled from MIT Urban Operations Research (Larson & Odoni, Figure 6.11).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set, Optional
import argparse


@dataclass(frozen=True)
class Edge:
    u: str
    v: str
    weight: float

    def __repr__(self) -> str:
        return f"({self.u} - {self.v}, w={self.weight})"

    def connects(self, node: str) -> bool:
        return self.u == node or self.v == node

    def normalized(self) -> Tuple[str, str, float]:
        """Returns tuple with lexicographically ordered endpoints."""
        u_sorted, v_sorted = sorted([self.u, self.v])
        return (u_sorted, v_sorted, self.weight)

    def matches(self, u: str, v: str) -> bool:
        return (self.u == u and self.v == v) or (self.u == v and self.v == u)


class DisjointSetUnion:
    """
    Disjoint Set Union (Union-Find) with:
    - Path compression in find()
    - Union by rank in union()
    Amortized time complexity: O(alpha(V)) per operation, effectively O(1).
    """

    def __init__(self, elements: List[str]):
        self.parent: Dict[str, str] = {x: x for x in elements}
        self.rank: Dict[str, int] = {x: 0 for x in elements}

    def find(self, x: str) -> str:
        """Finds representative root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:
        """
        Unites sets containing x and y using rank heuristic.
        Returns True if merged, False if already in the same set (cycle detected).
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        return True

    def get_components(self) -> Dict[str, List[str]]:
        """Returns map from root -> list of elements in that component."""
        comps: Dict[str, List[str]] = {}
        for elem in self.parent:
            root = self.find(elem)
            comps.setdefault(root, []).append(elem)
        for comp in comps.values():
            comp.sort()
        return comps


@dataclass
class StepRecord:
    step_num: int
    edge: Edge
    u_root: str
    v_root: str
    status: str  # 'ACCEPTED', 'REJECTED_CYCLE', 'SKIPPED_FAILED'
    reason: str
    components_snapshot: Dict[str, List[str]]
    current_tree_weight: float


@dataclass
class KruskalResult:
    mst_edges: List[Edge]
    total_weight: float
    steps: List[StepRecord]
    components: Dict[str, List[str]]
    is_connected: bool
    active_nodes: List[str]
    failed_nodes: List[str]
    failed_edges: List[Edge]


def get_default_graph() -> Tuple[List[str], List[Edge]]:
    """
    Default graph from ITS Graph Theory / MIT Urban Operations Research (Fig 6.11).
    Nodes: A, B, C, D, E, F, G
    Total Edges: 12
    """
    nodes = ["A", "B", "C", "D", "E", "F", "G"]
    raw_edges = [
        ("A", "B", 7),
        ("A", "C", 6),
        ("A", "G", 5),
        ("A", "F", 10),
        ("G", "F", 6),
        ("B", "C", 5),
        ("B", "D", 7),
        ("B", "E", 9),
        ("C", "E", 7),
        ("C", "F", 9),
        ("F", "E", 5),
        ("E", "D", 5),
    ]
    edges = [Edge(u, v, float(w)) for u, v, w in raw_edges]
    return nodes, edges


def run_kruskal(
    nodes: List[str],
    edges: List[Edge],
    failed_nodes: Optional[Set[str]] = None,
    failed_edges: Optional[List[Tuple[str, str]]] = None,
) -> KruskalResult:
    failed_nodes_set = set(failed_nodes) if failed_nodes else set()
    failed_edge_pairs = set()
    if failed_edges:
        for u, v in failed_edges:
            failed_edge_pairs.add((min(u, v), max(u, v)))

    active_nodes = [n for n in sorted(nodes) if n not in failed_nodes_set]
    dsu = DisjointSetUnion(active_nodes)

    # Sort all edges primarily by weight, tie-break by node names for deterministic trace
    sorted_edges = sorted(
        edges, key=lambda e: (e.weight, min(e.u, e.v), max(e.u, e.v))
    )

    mst_edges: List[Edge] = []
    steps: List[StepRecord] = []
    current_weight = 0.0
    step_counter = 1

    for edge in sorted_edges:
        edge_pair = (min(edge.u, edge.v), max(edge.u, edge.v))

        # Check if edge touches a failed node
        if edge.u in failed_nodes_set or edge.v in failed_nodes_set:
            steps.append(
                StepRecord(
                    step_num=step_counter,
                    edge=edge,
                    u_root="N/A",
                    v_root="N/A",
                    status="SKIPPED_FAILED",
                    reason=f"Incident to failed node ({edge.u if edge.u in failed_nodes_set else edge.v})",
                    components_snapshot=dsu.get_components(),
                    current_tree_weight=current_weight,
                )
            )
            step_counter += 1
            continue

        # Check if edge is explicitly failed
        if edge_pair in failed_edge_pairs:
            steps.append(
                StepRecord(
                    step_num=step_counter,
                    edge=edge,
                    u_root=dsu.find(edge.u),
                    v_root=dsu.find(edge.v),
                    status="SKIPPED_FAILED",
                    reason="Edge is damaged / blocked (failed link)",
                    components_snapshot=dsu.get_components(),
                    current_tree_weight=current_weight,
                )
            )
            step_counter += 1
            continue

        # Valid candidate: examine union-find roots
        u_root = dsu.find(edge.u)
        v_root = dsu.find(edge.v)

        if u_root != v_root:
            dsu.union(edge.u, edge.v)
            mst_edges.append(edge)
            current_weight += edge.weight
            steps.append(
                StepRecord(
                    step_num=step_counter,
                    edge=edge,
                    u_root=u_root,
                    v_root=v_root,
                    status="ACCEPTED",
                    reason=f"Roots differ ({u_root} != {v_root}). Merged sets without cycle.",
                    components_snapshot=dsu.get_components(),
                    current_tree_weight=current_weight,
                )
            )
        else:
            steps.append(
                StepRecord(
                    step_num=step_counter,
                    edge=edge,
                    u_root=u_root,
                    v_root=v_root,
                    status="REJECTED_CYCLE",
                    reason=f"Both endpoints already in root '{u_root}'. Adding would form cycle.",
                    components_snapshot=dsu.get_components(),
                    current_tree_weight=current_weight,
                )
            )

        step_counter += 1

    final_components = dsu.get_components()
    is_connected = len(final_components) <= 1 and len(active_nodes) > 0

    failed_edges_obj = [
        e
        for e in edges
        if (min(e.u, e.v), max(e.u, e.v)) in failed_edge_pairs
    ]

    return KruskalResult(
        mst_edges=mst_edges,
        total_weight=current_weight,
        steps=steps,
        components=final_components,
        is_connected=is_connected,
        active_nodes=active_nodes,
        failed_nodes=sorted(list(failed_nodes_set)),
        failed_edges=failed_edges_obj,
    )


def print_step_table(steps: List[StepRecord]):
    header = f"{'Step':<5} | {'Edge':<10} | {'Weight':<7} | {'Status':<16} | {'Reason'}"
    divider = "-" * 90
    print(divider)
    print(header)
    print(divider)
    for s in steps:
        edge_str = f"({s.edge.u}, {s.edge.v})"
        status_tag = s.status
        if s.status == "ACCEPTED":
            status_tag = "[+] ACCEPTED"
        elif s.status == "REJECTED_CYCLE":
            status_tag = "[x] CYCLE"
        elif s.status == "SKIPPED_FAILED":
            status_tag = "[-] FAILED"
        print(
            f"{s.step_num:<5} | {edge_str:<10} | {s.edge.weight:<7.1f} | {status_tag:<16} | {s.reason}"
        )
    print(divider)


def print_adaptation_report(
    baseline: KruskalResult, adapted: KruskalResult, scenario_title: str
):
    print("\n" + "=" * 80)
    print(f"  ADAPTATION REPORT: {scenario_title.upper()}")
    print("=" * 80)

    print(f"Failed Nodes : {adapted.failed_nodes if adapted.failed_nodes else 'None'}")
    failed_edges_str = (
        ", ".join(f"({e.u},{e.v})" for e in adapted.failed_edges)
        if adapted.failed_edges
        else "None"
    )
    print(f"Failed Edges : {failed_edges_str}")
    print(f"Active Nodes : {len(adapted.active_nodes)} ({', '.join(adapted.active_nodes)})")

    print("\n--- Quantitative Impact ---")
    print(f"Baseline MST Cost : {baseline.total_weight:.1f} (Edges: {len(baseline.mst_edges)})")
    print(f"Adapted Graph Cost: {adapted.total_weight:.1f} (Edges: {len(adapted.mst_edges)})")
    cost_delta = adapted.total_weight - baseline.total_weight
    delta_sign = "+" if cost_delta > 0 else ""
    print(f"Cost Difference   : {delta_sign}{cost_delta:.1f}")

    print("\n--- Structural Comparison ---")
    base_set = {e.normalized() for e in baseline.mst_edges}
    adapt_set = {e.normalized() for e in adapted.mst_edges}

    retained = [e for e in adapted.mst_edges if e.normalized() in base_set]
    new_edges = [e for e in adapted.mst_edges if e.normalized() not in base_set]
    lost_edges = [e for e in baseline.mst_edges if e.normalized() not in adapt_set]

    retained_str = ", ".join(f"({e.u}-{e.v}: {e.weight:.0f})" for e in retained)
    new_edges_str = ", ".join(f"({e.u}-{e.v}: {e.weight:.0f})" for e in new_edges)
    lost_edges_str = ", ".join(f"({e.u}-{e.v}: {e.weight:.0f})" for e in lost_edges)

    print(f"Retained Baseline Edges ({len(retained)}): [{retained_str}]")
    print(f"Added Replacement Edges ({len(new_edges)}): [{new_edges_str}]")
    print(f"Removed / Lost Edges    ({len(lost_edges)}): [{lost_edges_str}]")

    print("\n--- Algorithmic Adaptation Mechanism ---")
    if adapted.is_connected:
        print("Status: [SUCCESS] Fully Connected Minimum Spanning Tree preserved.")
        print("- Kruskal dynamically scanned the remaining candidate edges in non-decreasing weight order.")
        print("- Subgraphs severed by the failure were bridged by the next minimum-weight crossing edge")
        print("  satisfying the Cut Property without generating cycles.")
    else:
        print("Status: [PARTITIONED] Graph split into a Minimum Spanning Forest (MSF).")
        print(f"- Disconnected into {len(adapted.components)} independent components:")
        for root, comp in adapted.components.items():
            print(f"  * Component rooted at {root}: {comp}")
        print("- The failure eliminated critical articulation points or bridges without alternative bypasses.")
        print("- Kruskal gracefully assembled independent minimum spanning trees for every reachable component.")
    print("=" * 80 + "\n")


def run_full_suite():
    nodes, edges = get_default_graph()

    print("=" * 80)
    print("           KRUSKAL'S ALGORITHM MST & DYNAMIC FAILURE SIMULATION")
    print("=" * 80)
    print(f"Input Graph: {len(nodes)} Vertices {nodes}, {len(edges)} Edges")

    # 1. Baseline Run
    print("\n[SCENARIO 1] BASELINE MST COMPUTATION (Zero Failures)")
    baseline = run_kruskal(nodes, edges)
    print_step_table(baseline.steps)
    mst_edges_str = ", ".join(f"({e.u}-{e.v}, w={e.weight:.0f})" for e in baseline.mst_edges)
    print(f"MST Edges Selected: [{mst_edges_str}]")
    print(f"Total MST Weight: {baseline.total_weight:.1f}")

    # 2. Edge Failure Simulation
    print("\n[SCENARIO 2] SIMULATION: Critical MST Edge Failure (G - F fails)")
    sim_edge = run_kruskal(nodes, edges, failed_edges=[("G", "F")])
    print_step_table(sim_edge.steps)
    print_adaptation_report(baseline, sim_edge, "Edge Failure (G-F severed)")

    # 3. Node Failure Simulation
    print("\n[SCENARIO 3] SIMULATION: Hub Node Failure (Node C fails)")
    sim_node = run_kruskal(nodes, edges, failed_nodes={"C"})
    print_step_table(sim_node.steps)
    print_adaptation_report(baseline, sim_node, "Node Failure (Node C destroyed)")


def generate_random_graph(
    num_nodes: int = 7,
    extra_edges: int = 4,
    min_weight: int = 1,
    max_weight: int = 20,
    seed: Optional[int] = None,
) -> Tuple[List[str], Dict[str, Dict[str, int]], List[Edge]]:
    """
    Generates a connected random graph:
    1. Generates num_nodes labels ('A', 'B', ...) and positions.
    2. Constructs a random spanning tree (ensures graph is 100% connected).
    3. Adds extra_edges random links without multigraph duplicates.
    4. Returns (nodes, positions_dict, edges).
    """
    import random
    import math

    if seed is not None:
        random.seed(seed)

    num_nodes = max(3, min(26, num_nodes))
    labels = [chr(65 + i) for i in range(num_nodes)]

    cx, cy = 410, 290
    rx, ry = 280, 200
    positions = {}
    for i, label in enumerate(labels):
        angle = (2 * math.pi * i) / num_nodes + random.uniform(-0.15, 0.15)
        r_jitter = random.uniform(0.75, 1.05)
        x = int(cx + rx * r_jitter * math.cos(angle))
        y = int(cy + ry * r_jitter * math.sin(angle))
        x = max(70, min(750, x))
        y = max(60, min(520, y))
        positions[label] = {"x": x, "y": y}

    shuffled = list(labels)
    random.shuffle(shuffled)
    edges_set = set()
    edges: List[Edge] = []

    for i in range(1, num_nodes):
        u = shuffled[i]
        v = random.choice(shuffled[:i])
        edge_key = (min(u, v), max(u, v))
        edges_set.add(edge_key)
        w = float(random.randint(min_weight, max_weight))
        edges.append(Edge(edge_key[0], edge_key[1], w))

    all_possible = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            pair = (labels[i], labels[j])
            if pair not in edges_set:
                all_possible.append(pair)
    random.shuffle(all_possible)
    for pair in all_possible[:extra_edges]:
        edges_set.add(pair)
        w = float(random.randint(min_weight, max_weight))
        edges.append(Edge(pair[0], pair[1], w))

    return labels, positions, edges


def parse_graph_input(
    text: str,
) -> Tuple[List[str], Dict[str, Dict[str, int]], List[Edge]]:
    """
    Parses edge list from user input text.
    Handles multiple formats per line:
      'A B 7'
      'A, B, 7'
      'A - B: 7'
      'A-B 7'
    Ignores empty lines and comments starting with # or //.
    Computes smooth 2D layout coordinates for visualization.
    """
    import re
    import math

    nodes_set = set()
    edges: List[Edge] = []
    lines = text.strip().splitlines()

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        parts = re.split(r"[,:\s\-]+", line)
        parts = [p for p in parts if p]
        if len(parts) < 3:
            raise ValueError(
                f"Line {line_num}: invalid syntax '{line}'. Expected: 'node1 node2 weight'"
            )
        u, v = parts[0].strip().upper(), parts[1].strip().upper()
        try:
            w = float(parts[2])
        except ValueError:
            raise ValueError(
                f"Line {line_num}: invalid weight '{parts[2]}'. Must be a number."
            )
        nodes_set.add(u)
        nodes_set.add(v)
        edges.append(Edge(u, v, w))

    if not nodes_set:
        raise ValueError("Input contained no valid edges.")

    nodes = sorted(list(nodes_set))
    num_nodes = len(nodes)
    cx, cy = 410, 290
    rx, ry = 280, 200
    positions = {}
    for i, label in enumerate(nodes):
        angle = (2 * math.pi * i) / num_nodes if num_nodes > 1 else 0
        x = int(cx + rx * math.cos(angle))
        y = int(cy + ry * math.sin(angle))
        x = max(70, min(750, x))
        y = max(60, min(520, y))
        positions[label] = {"x": x, "y": y}

    return nodes, positions, edges


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kruskal MST and Failure Simulation Engine")
    parser.add_argument("--suite", action="store_true", help="Run complete benchmark & simulation suite")
    parser.add_argument("--random", type=int, nargs="?", const=7, help="Generate random connected graph with N nodes (default: 7)")
    parser.add_argument("--file", "-f", type=str, help="Load custom graph from edge list text file")
    parser.add_argument("--input", "-i", action="store_true", help="Enter custom edge list interactively from terminal")
    parser.add_argument("--fail-nodes", nargs="*", help="Node labels to simulate failure for (e.g. C G)")
    parser.add_argument("--fail-edges", nargs="*", help="Edge pairs to simulate failure for (e.g. G-F B-C)")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            nodes, pos, edges = parse_graph_input(f.read())
        print("=" * 80)
        print(f"       LOADED CUSTOM GRAPH FROM FILE ({len(nodes)} Nodes, {len(edges)} Edges)")
        print("=" * 80)
        baseline = run_kruskal(nodes, edges)
        print_step_table(baseline.steps)
        mst_edges_str = ", ".join(f"({e.u}-{e.v}, w={e.weight:.0f})" for e in baseline.mst_edges)
        print(f"MST Edges Selected: [{mst_edges_str}]")
        print(f"Total MST Weight: {baseline.total_weight:.1f}")

        failed_nodes = set(args.fail_nodes) if args.fail_nodes else set()
        failed_edges = []
        if args.fail_edges:
            for ep in args.fail_edges:
                parts = ep.replace(",", "-").split("-")
                if len(parts) == 2:
                    failed_edges.append((parts[0].strip().upper(), parts[1].strip().upper()))
        if failed_nodes or failed_edges:
            adapted = run_kruskal(nodes, edges, failed_nodes=failed_nodes, failed_edges=failed_edges)
            print_step_table(adapted.steps)
            print_adaptation_report(baseline, adapted, "Custom Graph Failure Adaptation")

    elif args.input:
        print("Enter custom graph edges (e.g. 'A B 7', blank line to finish):")
        lines = []
        while True:
            try:
                line = input()
                if not line.strip():
                    break
                lines.append(line)
            except EOFError:
                break
        nodes, pos, edges = parse_graph_input("\n".join(lines))
        print("=" * 80)
        print(f"       CUSTOM GRAPH PARSED ({len(nodes)} Nodes, {len(edges)} Edges)")
        print("=" * 80)
        baseline = run_kruskal(nodes, edges)
        print_step_table(baseline.steps)
        mst_edges_str = ", ".join(f"({e.u}-{e.v}, w={e.weight:.0f})" for e in baseline.mst_edges)
        print(f"MST Edges Selected: [{mst_edges_str}]")
        print(f"Total MST Weight: {baseline.total_weight:.1f}")

        failed_nodes = set(args.fail_nodes) if args.fail_nodes else set()
        failed_edges = []
        if args.fail_edges:
            for ep in args.fail_edges:
                parts = ep.replace(",", "-").split("-")
                if len(parts) == 2:
                    failed_edges.append((parts[0].strip().upper(), parts[1].strip().upper()))
        if failed_nodes or failed_edges:
            adapted = run_kruskal(nodes, edges, failed_nodes=failed_nodes, failed_edges=failed_edges)
            print_step_table(adapted.steps)
            print_adaptation_report(baseline, adapted, "Custom Graph Failure Adaptation")

    elif args.random is not None:
        nodes, pos, edges = generate_random_graph(num_nodes=args.random)
        print("=" * 80)
        print(f"       GENERATED RANDOM CONNECTED GRAPH ({len(nodes)} Nodes, {len(edges)} Edges)")
        print("=" * 80)
        baseline = run_kruskal(nodes, edges)
        print_step_table(baseline.steps)
        mst_edges_str = ", ".join(f"({e.u}-{e.v}, w={e.weight:.0f})" for e in baseline.mst_edges)
        print(f"MST Edges Selected: [{mst_edges_str}]")
        print(f"Total MST Weight: {baseline.total_weight:.1f}")

        failed_nodes = set(args.fail_nodes) if args.fail_nodes else set()
        failed_edges = []
        if args.fail_edges:
            for ep in args.fail_edges:
                parts = ep.replace(",", "-").split("-")
                if len(parts) == 2:
                    failed_edges.append((parts[0].strip().upper(), parts[1].strip().upper()))

        if failed_nodes or failed_edges:
            adapted = run_kruskal(nodes, edges, failed_nodes=failed_nodes, failed_edges=failed_edges)
            print_step_table(adapted.steps)
            print_adaptation_report(baseline, adapted, "Random Graph Failure Adaptation")
    elif args.suite or (not args.fail_nodes and not args.fail_edges):
        run_full_suite()
    else:
        nodes, edges = get_default_graph()
        failed_nodes = set(args.fail_nodes) if args.fail_nodes else set()
        failed_edges = []
        if args.fail_edges:
            for ep in args.fail_edges:
                parts = ep.replace(",", "-").split("-")
                if len(parts) == 2:
                    failed_edges.append((parts[0].strip().upper(), parts[1].strip().upper()))

        baseline = run_kruskal(nodes, edges)
        adapted = run_kruskal(nodes, edges, failed_nodes=failed_nodes, failed_edges=failed_edges)

        print_step_table(adapted.steps)
        print_adaptation_report(baseline, adapted, "Custom Failure Simulation")

