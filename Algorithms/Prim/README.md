# Prim's Algorithm — Minimum Spanning Tree (MST) & Fail Cases

## Prerequisites to Run the Code

- **Python**: Python 3.8+ (tested on Python 3.12).
- **Dependencies**: **None** (Pure Python standard library: `argparse`, `random`).

---

## Instructions to Run the Code

### A. Run with Sample Input File
Execute Prim's algorithm on the provided sample input file (`input_sample.txt`):
```bash
python implementation.py --file input_sample.txt --start A
```

### B. Run Complete Automated Benchmark Suite
Runs the baseline MST calculation plus 2 dynamic failure adaptation scenarios:
```bash
python implementation.py --file input_sample.txt --start A --suite
```

### C. Simulate Specific Edge or Node Failures
```bash
# Simulate failure of a specific link (e.g. edge G-F severed):
python implementation.py --file input_sample.txt --start A --fail-edges G-F

# Simulate failure of a specific node (e.g. node C destroyed):
python implementation.py --file input_sample.txt --start A --fail-nodes C

# Simulate concurrent failures:
python implementation.py --file input_sample.txt --start A --fail-nodes C --fail-edges G-F
```

### D. Enter Custom Graph Interactively
```bash
python implementation.py --input
# Enter edges like "A B 7" (one per line). Press Enter on an empty line when finished.
```

### E. Generate and Test Random Connected Graph
```bash
python implementation.py --random 8
```

---

## Result of Sample Run

### Baseline Run Output (Verbatim Terminal Output)
Executed command: `python implementation.py --file input_sample.txt --start A`

```text
================================================================================
LOADED CUSTOM GRAPH FROM FILE (7 Nodes, 12 Edges)
================================================================================
--------------------------------------------------------------------------------------------
Step  Edge        Weight   Status          Reason
--------------------------------------------------------------------------------------------
1     (A, G)      5        [+] ACCEPTED
      -> Minimum-weight edge crossing the cut (tree=['A'] | rest). Frontier considered: (A-B: 7), (A-C: 6), (A-G: 5), (A-F: 10)
2     (A, C)      6        [+] ACCEPTED
      -> Minimum-weight edge crossing the cut (tree=['A', 'G'] | rest). Frontier considered: (A-B: 7), (A-C: 6), (A-F: 10), (G-F: 6)
3     (C, B)      5        [+] ACCEPTED
      -> Minimum-weight edge crossing the cut (tree=['A', 'C', 'G'] | rest). Frontier considered: (A-B: 7), (A-F: 10), (C-B: 5), (C-E: 7), (C-F: 9), (G-F: 6)
4     (G, F)      6        [+] ACCEPTED
      -> Minimum-weight edge crossing the cut (tree=['A', 'B', 'C', 'G'] | rest). Frontier considered: (A-F: 10), (B-D: 7), (B-E: 9), (C-E: 7), (C-F: 9), (G-F: 6)
5     (F, E)      5        [+] ACCEPTED
      -> Minimum-weight edge crossing the cut (tree=['A', 'B', 'C', 'F', 'G'] | rest). Frontier considered: (B-D: 7), (B-E: 9), (C-E: 7), (F-E: 5)
6     (E, D)      5        [+] ACCEPTED
      -> Minimum-weight edge crossing the cut (tree=['A', 'B', 'C', 'E', 'F', 'G'] | rest). Frontier considered: (B-D: 7), (E-D: 5)
--------------------------------------------------------------------------------------------
MST Edges Selected: [A-G (w=5), A-C (w=6), C-B (w=5), G-F (w=6), F-E (w=5), E-D (w=5)]
Total MST Weight: 32
```

**Note on the trace format:** unlike Kruskal's algorithm, Prim's does not need
a per-edge cycle check across the whole edge list. At every step it only
looks at the current **cut** (the edges crossing between the tree so far
and the remaining vertices) and takes the cheapest one — that edge can
never form a cycle, by the Cut Property. This is why the table above has
exactly 6 rows (`V - 1 = 7 - 1 = 6`) instead of listing all 12 edges: each
row already represents an accepted edge, with the full frontier it beat
shown in the reason column for transparency.

### Fail Adaptation

#### Scenario 1: Critical Link Failure (Edge (G, F) severed)
```text
================================================================================
  ADAPTATION REPORT: G-F SEVERED
================================================================================
Failed Nodes : None
Failed Edges : [('G', 'F')]
Active Nodes : 7 (A, B, C, D, E, F, G)

--- Quantitative Impact ---
Baseline MST Cost : 32 (Edges: 6)
Adapted Graph Cost: 33 (Edges: 6)
Cost Difference   : +1

--- Structural Comparison ---
Retained Baseline Edges (5): [A-G: 5, A-C: 6, C-B: 5, D-E: 5, E-F: 5]
Added Replacement Edges (1): [B-D: 7]
Removed / Lost Edges    (1): [G-F: 6]

--- Algorithmic Adaptation Mechanism ---
Status: [SUCCESS] Fully connected Minimum Spanning Tree preserved.
- The cut previously bridged by (G, F) had to be reconnected through a new frontier edge.
- Prim's algorithm re-scanned the frontier and found (B, D) with weight 7 as the new minimum crossing edge.
- Total adapted cost across active nodes is 33.
================================================================================
```

#### Scenario 2: Junction Node Failure (Hub Node C destroyed)
```text
================================================================================
  ADAPTATION REPORT: NODE C DESTROYED
================================================================================
Failed Nodes : ['C']
Failed Edges : None
Active Nodes : 6 (A, B, D, E, F, G)

--- Quantitative Impact ---
Baseline MST Cost : 32 (Edges: 6)
Adapted Graph Cost: 28 (Edges: 5)
Cost Difference   : -4

--- Structural Comparison ---
Retained Baseline Edges (4): [A-G: 5, G-F: 6, F-E: 5, E-D: 5]
Added Replacement Edges (1): [A-B: 7]
Removed / Lost Edges    (2): [A-C: 6, C-B: 5]

--- Algorithmic Adaptation Mechanism ---
Status: [SUCCESS] Fully connected Minimum Spanning Tree preserved.
- All 4 edges incident to 'C' were removed from consideration.
- Prim's algorithm re-scanned the frontier and found (A, B) with weight 7 as the new minimum crossing edge.
- Total adapted cost across active nodes is 28.
================================================================================
```

**Cross-check with Kruskal's results:** both algorithms report identical
adapted costs (33 for the G-F edge failure, 28 for the node-C failure).
This is expected — a minimum spanning tree's *total weight* is the same
no matter which correct MST algorithm produces it, even when the specific
edges chosen along the way differ.

---

## AI Tools Usage Disclosure

In compliance with Institut Teknologi Sepuluh Nopember academic honesty guidelines for group coursework:
- **AI Model / Assistant Used**: Claude
- **Scope of AI Assistance**:
  1. Assisted in writing the frontier/cut-based trace logic for Prim's algorithm.
  2. Formatted step-by-step execution traces and adaptation reports to match the group's Kruskal report style.
- **Verification & Ownership**: All source code, algorithm traces, and mathematical explanations have been reviewed, verified, and tested by the group members.
