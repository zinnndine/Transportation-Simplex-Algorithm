
---

# Transportation Simplex Algorithm

Implementation of the Transportation Simplex Algorithm for solving transportation problems in linear programming.

---

## Problem Statement

The transportation problem is a special case of linear programming where goods must be transported from multiple sources to multiple destinations at minimum cost, subject to supply and demand constraints.

This project implements the **Transportation Simplex Algorithm**, exploiting the problem’s structure for efficient solution.

---

## Initial Feasible Solution Methods

The initial basic feasible solution is generated using one of the following classical methods:

- **North-West Corner (NWC) Method**
  - Simple and fast
  - Does not consider transportation costs
  - Used as a baseline feasible solution

- **Least Cost Method**
  - Greedy approach selecting the minimum cost cell
  - Typically produces a better starting solution than NWC
  
The selected initial solution is then refined using the **Transportation Simplex Algorithm**.


## Implementation Details

- Language: **Python**
- No external optimization libraries


---

## How to Run (linux)

```bash
cd scripts
python3 script.py
