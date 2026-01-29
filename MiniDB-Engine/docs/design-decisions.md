# MiniDB-Engine Design Decisions

## Why These Architectures Were Chosen

---

### Why WAL?

* Guarantees durability
* Enables crash recovery
* Industry standard

### Why Page-Based Storage?

* Predictable IO
* Cache efficiency
* Storage alignment

### Why B+ Tree?

* Fast lookup
* Range queries
* Industry standard indexing

### Why Layered Architecture?

* Fault isolation
* Scalability
* Maintainability

### Why Recovery-First Design?

* Failure is inevitable
* Systems must self-heal

---

# Tradeoffs

| Choice   | Benefit     | Cost               |
| -------- | ----------- | ------------------ |
| WAL      | Durability  | Write overhead     |
| Pages    | Performance | Complexity         |
| B+ Tree  | Fast search | Memory cost        |
| Layering | Stability   | Engineering effort |

---

# Engineering Philosophy

Correctness > Performance
Recovery > Speed
Safety > Throughput
Infrastructure > Features
