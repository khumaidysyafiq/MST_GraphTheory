# Kruskal's Algorithm — Minimum Spanning Tree (MST) & Fail Cases

## Prerequisites to Run the Code

- **Python**: Python 3.8+ (tested on Python 3.14).
- **Dependencies**: **None** (Pure Python standard library: `dataclasses`, `typing`, `argparse`, `math`, `random`, `re`).

---

## Instructions to Run the Code

### A. Run with Sample Input File
Execute Kruskal's algorithm on the provided sample input file (`input_sample.txt`):
```bash
python implementation.py --file input_sample.txt
```

### B. Run Complete Automated Benchmark Suite
Runs the baseline MST calculation plus 2 dynamic failure adaptation scenarios:
```bash
python implementation.py --suite
```

### C. Simulate Specific Edge or Node Failures
```bash
# Simulate failure of a specific link (e.g. edge G-F severed):
python implementation.py --fail-edges G-F

# Simulate failure of a specific node (e.g. node C destroyed):
python implementation.py --fail-nodes C

# Simulate concurrent failures:
python implementation.py --fail-nodes C --fail-edges G-F
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
Executed command: `python implementation.py --file input_sample.txt`

```text
================================================================================
       LOADED CUSTOM GRAPH FROM FILE (7 Nodes, 12 Edges)
================================================================================
------------------------------------------------------------------------------------------
Step  | Edge       | Weight  | Status           | Reason
------------------------------------------------------------------------------------------
1     | (A, G)     | 5.0     | [+] ACCEPTED     | Roots differ (A != G). Merged sets without cycle.
2     | (B, C)     | 5.0     | [+] ACCEPTED     | Roots differ (B != C). Merged sets without cycle.
3     | (E, D)     | 5.0     | [+] ACCEPTED     | Roots differ (E != D). Merged sets without cycle.
4     | (F, E)     | 5.0     | [+] ACCEPTED     | Roots differ (F != E). Merged sets without cycle.
5     | (A, C)     | 6.0     | [+] ACCEPTED     | Roots differ (A != B). Merged sets without cycle.
6     | (G, F)     | 6.0     | [+] ACCEPTED     | Roots differ (A != E). Merged sets without cycle.
7     | (A, B)     | 7.0     | [x] CYCLE        | Both endpoints already in root 'A'. Adding would form cycle.
8     | (B, D)     | 7.0     | [x] CYCLE        | Both endpoints already in root 'A'. Adding would form cycle.
9     | (C, E)     | 7.0     | [x] CYCLE        | Both endpoints already in root 'A'. Adding would form cycle.
10    | (B, E)     | 9.0     | [x] CYCLE        | Both endpoints already in root 'A'. Adding would form cycle.
11    | (C, F)     | 9.0     | [x] CYCLE        | Both endpoints already in root 'A'. Adding would form cycle.
12    | (A, F)     | 10.0    | [x] CYCLE        | Both endpoints already in root 'A'. Adding would form cycle.
------------------------------------------------------------------------------------------
MST Edges Selected: [(A-G, w=5), (B-C, w=5), (E-D, w=5), (F-E, w=5), (A-C, w=6), (G-F, w=6)]
Total MST Weight: 32.0
```

### Fail Adaptation

#### Scenario 1: Critical Link Failure (Edge $(G, F)$ severed)
```text
================================================================================
  ADAPTATION REPORT: EDGE FAILURE (G-F SEVERED)
================================================================================
Failed Nodes : None
Failed Edges : (G,F)
Active Nodes : 7 (A, B, C, D, E, F, G)

--- Quantitative Impact ---
Baseline MST Cost : 32.0 (Edges: 6)
Adapted Graph Cost: 33.0 (Edges: 6)
Cost Difference   : +1.0

--- Structural Comparison ---
Retained Baseline Edges (5): [(A-G: 5), (B-C: 5), (E-D: 5), (F-E: 5), (A-C: 6)]
Added Replacement Edges (1): [(B-D: 7)]
Removed / Lost Edges    (1): [(G-F: 6)]

--- Algorithmic Adaptation Mechanism ---
Status: [SUCCESS] Fully Connected Minimum Spanning Tree preserved.
- When link (G, F) failed, the cut between {A, B, C, G} and {D, E, F} was severed.
- Kruskal dynamically scanned the remaining candidate edges in non-decreasing weight order.
- The next available minimum-weight crossing edge was (B, D) with weight 7.0.
- The algorithm bridged the components into a new valid MST with total weight 33.0.
================================================================================
```

#### Scenario 2: Junction Node Failure (Hub Node $C$ destroyed)
```text
================================================================================
  ADAPTATION REPORT: NODE FAILURE (NODE C DESTROYED)
================================================================================
Failed Nodes : ['C']
Failed Edges : None
Active Nodes : 6 (A, B, D, E, F, G)

--- Quantitative Impact ---
Baseline MST Cost : 32.0 (Edges: 6)
Adapted Graph Cost: 28.0 (Edges: 5)
Cost Difference   : -4.0

--- Structural Comparison ---
Retained Baseline Edges (4): [(A-G: 5), (E-D: 5), (F-E: 5), (G-F: 6)]
Added Replacement Edges (1): [(A-B: 7)]
Removed / Lost Edges    (2): [(B-C: 5), (A-C: 6)]

--- Algorithmic Adaptation Mechanism ---
Status: [SUCCESS] Fully Connected Minimum Spanning Tree preserved.
- All 4 edges incident to C ((A,C), (B,C), (C,E), (C,F)) were removed.
- Remaining 6 vertices required 5 spanning links.
- Kruskal dynamically selected (A, B: 7.0) to connect {A, G, F, E, D} to {B}.
- Total adapted cost across active nodes is 28.0.
================================================================================
```

---

## AI Tools Usage Disclosure

In compliance with Institut Teknologi Sepuluh Nopember academic honesty guidelines for group coursework:
- **AI Model / Assistant Used**: Gemini
- **Scope of AI Assistance**:
  1. Assisted in structuring the Disjoint Set Union (DSU) heuristics (path compression and union by rank).
  2. Formatted step-by-step execution traces and ASCII adaptation reports.
- **Verification & Ownership**: All source code, algorithm traces, and mathematical explanations have been reviewed, verified, and tested by the group members.
