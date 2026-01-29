# MiniDB-Engine Developer Guide

## Running the System

```bash
pip install -e .
minidb run
```

---

## CLI Commands

```bash
minidb version
minidb status
minidb run
```

---

## Configs

```bash
config/default.yaml
config/dev.yaml
config/prod.yaml
```

---

## Testing

```bash
python3 main.py
```

---

## Extending the System

Add new layers via:

* storage/
* wal/
* txn/
* index/
* query/

---

## Contribution Model

* modular design
* layered structure
* isolated responsibility
