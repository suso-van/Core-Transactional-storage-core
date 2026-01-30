# Core-Transactional-Storage-Core

> **Enterprise-grade Transactional Storage Engine & Distributed Systems Platform**
> Research-driven, systems-level project implementing core internals of modern database engines and transactional platforms.

---

## 🚀 Project Overview

**Core-Transactional-Storage-Core** is not a typical application project. It is a **systems engineering platform** that implements the core internals of:

* Transactional storage engines
* Database kernels
* Recovery systems
* Write-ahead logging (WAL)
* Crash recovery (REDO/UNDO)
* Transaction processing
* Indexing engines
* Distributed systems architecture
* Observability and logging infrastructure

This project models real-world architectures used in:

* Banking transaction systems
* Financial trading platforms
* Distributed databases
* Storage engines
* Cloud infrastructure
* Big-tech data platforms

---

## 🎯 Vision

Build a **real systems platform**, not a demo app.

Focus areas:

* Correctness
* Reliability
* Determinism
* Recoverability
* Observability
* Scalability
* Modularity
* System design

This project is designed as a **learning + research + engineering platform** for deep systems knowledge.

---

## 🧠 Engineering Philosophy

> Applications focus on features.
> Systems focus on correctness.

> Products focus on UI.
> Platforms focus on architecture.

This project prioritizes:

* Core correctness over UI
* Engine stability over appearance
* Infrastructure over interfaces
* Architecture over frameworks

---

# 🧱 Architecture

```
User / CLI
   ↓
Control Layer (CLI / Commands)
   ↓
Application Layer
   ↓
Transaction Engine
   ↓
Recovery Engine
   ↓
WAL Engine
   ↓
Storage Engine
   ↓
Disk / Persistence Layer
```

---

# 🧩 Core Components

## 1. Storage Engine

* Page-based storage model
* File manager
* Disk abstraction
* Persistent storage
* Page lifecycle management

## 2. WAL (Write-Ahead Logging)

* JSONL WAL format
* LSN (Log Sequence Number)
* Ordered logging
* Recovery-safe logging
* Replay-safe structure

## 3. Transaction Engine

* Transaction lifecycle
* BEGIN / WRITE / COMMIT / ABORT
* WAL-backed transactions
* Crash-safe semantics

## 4. Recovery Engine

* Crash detection
* REDO engine
* UNDO engine
* Replay engine
* Deterministic recovery

## 5. Index Engine

* Index abstraction
* B+Tree model (design-level)
* Query path foundation

## 6. Logging & Observability

* Structured JSON logging
* Rotating log files
* Trace IDs
* Console logging
* Production-style logging

## 7. CLI (System Control Plane)

* System startup
* Status inspection
* Recovery execution
* WAL inspection
* Transaction execution
* Infra initialization

---

# 📁 Repository Structure

```
Core-Transactional-storage-core/
│
├── MiniDB-Engine/
│   ├── wal/                # WAL engine
│   ├── storage/            # Storage engine
│   ├── txn/                # Transaction engine
│   ├── recovery/           # Recovery engine
│   ├── index/               # Index layer
│   ├── utils/               # Logging & utilities
│   ├── CLI/                 # System CLI
│   ├── core/                # Application core
│   ├── tests/               # pytest test suite
│   ├── main.py              # Engine runtime
│   ├── pyproject.toml       # Packaging
│   └── version.py           # Versioning
│
├── docs/                    # Documentation
├── logs/                    # Runtime logs (ignored in git)
├── data/                    # Storage data (runtime)
└── README.md
```

---

# 🧪 Testing & Verification

The system uses **pytest** for correctness validation.

### Run tests:

```bash
pytest
```

### Coverage:

```bash
pytest --cov=MiniDB-Engine
```

Tests validate:

* WAL correctness
* Transaction correctness
* Recovery correctness
* Storage correctness
* Engine wiring

---

# 🖥 CLI Usage

### Install:

```bash
cd MiniDB-Engine
pip install -e .
```

### Commands:

```bash
minidb init      # initialize system directories
minidb run       # start engine
minidb status    # system status
minidb recover   # run recovery engine
minidb wal       # inspect WAL
minidb txn       # run transaction demo
minidb version   # version info
```

---

# ⚙️ Setup Guide

```bash
# clone repo
git clone <repo-url>
cd Core-Transactional-storage-core

# create env
python3 -m venv venv
source venv/bin/activate

# install engine
cd MiniDB-Engine
pip install -e .

# install dev tools
pip install pytest pytest-cov

# run tests
pytest

# run engine
minidb run
```

---

# 🔐 Reliability Guarantees

* WAL-before-write guarantee
* Recovery-safe commits
* Deterministic replay
* Crash recovery
* Idempotent recovery
* Consistent state rebuild

---

# 🧠 Phase Model

### Phase A – Core Engine

* Storage
* WAL
* Transactions

### Phase B – Recovery

* REDO/UNDO
* Crash detection
* Replay

### Phase C – Stability

* Tests
* Logging
* CLI
* Determinism
* Reliability

### Phase D – Productization (Future)

* APIs
* Query engine
* SQL interface
* UI
* SDK
* Services
* Dashboards

---

# 🎯 Project Classification

This project is:

* ✅ Systems engineering project
* ✅ Infrastructure project
* ✅ Database kernel project
* ✅ Distributed systems project
* ✅ Research-grade platform
* ✅ Core-engine project

Not:

* ❌ CRUD app
* ❌ Demo project
* ❌ UI project
* ❌ API project
* ❌ Framework project

---

# 🏦 Industry Relevance

Aligned with systems used in:

* Banking platforms
* Trading systems
* FinTech infrastructure
* Distributed databases
* Cloud storage engines
* Big-tech infrastructure

---

# 📚 Learning Domains Covered

* Operating Systems
* Database Systems
* Distributed Systems
* Storage Engineering
* Systems Design
* Reliability Engineering
* Software Architecture
* Transaction Processing
* Recovery Algorithms
* Logging Systems

---

# 🧾 License

Educational & Research Use

---

# 🏁 Final Statement

This project represents a **systems-level engineering platform**, not an application.

It demonstrates understanding of:

* Core DB internals
* Transaction processing
* Recovery algorithms
* Storage engines
* WAL systems
* Systems architecture
* Distributed design
* Reliability engineering

> This is infrastructure engineering, not application development.
