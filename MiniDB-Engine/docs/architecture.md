# MiniDB-Engine Architecture

## System Architecture Specification

This document defines the **formal architecture** of MiniDB-Engine as an enterprise-grade transactional storage platform.

MiniDB-Engine follows a **layered kernel architecture** inspired by real-world database and storage engines used in banking systems and big-tech infrastructure.

---

# Architectural Style

**Model:** Layered Architecture + Kernel Design

Principles:

* separation of concerns
* fault isolation
* recovery-first design
* durability-first design
* correctness-first engineering
* deterministic execution

---

# High-Level Architecture

```
Client / CLI
   │
   ▼
Query Engine
   │
   ▼
Transaction Engine
   │
   ▼
Index Engine
   │
   ▼
Storage Engine
   │
   ▼
WAL Engine + Recovery
   │
   ▼
Disk Storage
```

---

# Layer Responsibilities

## 1. Query Engine

**Role:** Execution abstraction layer

Responsibilities:

* query planning
* query execution
* API normalization
* transaction binding

This layer provides controlled system access.

---

## 2. Transaction Engine

**Role:** Consistency and atomicity layer

Responsibilities:

* transaction lifecycle
* atomic commit
* rollback
* write-set management
* consistency enforcement
* isolation foundations

---

## 3. Index Engine

**Role:** Performance and access layer

Responsibilities:

* B+ Tree indexing
* key-based lookup
* range scanning
* index durability
* index recovery

---

## 4. Storage Engine

**Role:** Persistence layer

Responsibilities:

* page management
* metadata headers
* checksums
* corruption detection
* disk IO
* page allocation

---

## 5. WAL Engine

**Role:** Durability and recovery layer

Responsibilities:

* write-ahead logging
* redo logging
* undo logging
* commit markers
* checkpoints
* crash recovery

---

## 6. Observability Layer

**Role:** System visibility layer

Responsibilities:

* metrics
* logging
* diagnostics
* health checks
* audit trails

---

# Data Flow Architecture

```
Client Request
   ↓
Query Plan
   ↓
Transaction Context
   ↓
Index Lookup
   ↓
Page Access
   ↓
WAL Append
   ↓
Disk Write
```

---

# Write Path

```
Client → Query Engine → Transaction Engine
        → WAL Engine (log first)
        → Storage Engine (write page)
        → Disk
```

Guarantee: **No data is written to disk without WAL**

---

# Read Path

```
Client → Query Engine → Transaction Engine
        → Index Engine → Storage Engine
        → Disk → Page Deserialize
```

---

# Recovery Flow

```
System Start
   ↓
WAL Scan
   ↓
Identify Committed TX
   ↓
REDO committed writes
   ↓
UNDO incomplete writes
   ↓
Restore consistent state
```

---

# Failure Model

The system assumes failures by default:

* power loss
* partial writes
* crashes
* corrupted pages
* torn pages
* interrupted commits

Recovery is mandatory, not optional.

---

# Consistency Model

* atomicity via WAL
* consistency via transaction engine
* durability via WAL + fsync
* isolation foundation via transaction layer

---

# Security Model (Foundational)

* audit logs
* trace IDs
* transaction IDs
* controlled entrypoints
* config isolation

---

# Architectural Constraints

* correctness > performance
* safety > throughput
* recovery > speed
* determinism > concurrency

---

# Industry Alignment

This architecture mirrors:

* PostgreSQL kernel model
* InnoDB engine design
* Oracle DB internals
* Core banking ledgers
* Trading systems
* Payment processing engines

---

# System Classification

**Category:** Infrastructure System
**Type:** Transactional Storage Kernel
**Domain:** Systems Engineering
**Level:** Enterprise / Research

---

# Evolution Readiness

The architecture supports future upgrades:

* distributed WAL
* sharded storage
* replication
* leader-follower model
* consensus
* distributed transactions
* cluster recovery

---

# Summary

MiniDB-Engine is architected as a **kernel-grade transactional platform**, not an application system.

It is designed for:

* reliability
* correctness
* recovery
* durability
* observability
* enterprise evolution
