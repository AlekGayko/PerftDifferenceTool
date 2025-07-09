# PerftDifferenceTool

**PerftDifferenceTool** is a Python utility designed to compare the perft (performance test) results between your UCI-compatible chess engine and [Stockfish](https://stockfishchess.org/). It helps you identify and debug discrepancies in move generation down to the exact position where the engines diverge.

## What It Does

Given a FEN position and a search depth, the tool:

- Runs a perft search using Stockfish and your chess engine.
- Compares the total number of generated positions.
- If a mismatch is found, identifies specific moves with differing counts.
- Recursively investigates the largest discrepancy by stepping deeper into the move tree and reducing depth until:
  - A depth of 1 is reached, or
  - The number of legal moves becomes inconsistent (suggesting an illegal or missing move).

This process pinpoints the root cause of incorrect move generation—ideal for debugging engines at scale where billions of positions are involved.

---

## Setup

### 1. Clone and Build Stockfish

Use the provided script to download and compile Stockfish into the `Stockfish/` directory:

```bash
chmod +x scripts/setup_stockfish.sh
./scripts/setup_stockfish.sh
```

### 2. Install Python Dependencies

Install required libraries using pip:

```bash
pip install -r requirements.txt
```

---

## Running the Tool

Once Stockfish and your engine are ready, run:

```bash
python3 main.py [ENGINE_PATH] [FEN] [DEPTH] [-v]
```

### Arguments

| Argument      | Description                                                         |
| ------------- | ------------------------------------------------------------------- |
| `ENGINE_PATH` | Path to your UCI-compatible chess engine executable                 |
| `FEN`         | FEN string describing the board position                            |
| `DEPTH`       | Depth for perft search (positive non-zero integer)                  |
| `-v`          | *(Optional)* Enables verbose output for detailed difference tracing |

---

## Example

```bash
python3 main.py ./SandalBot "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" 5 -v
```

---

## Directory Structure

```
PerftDifferenceTool/
├── main.py
├── requirements.txt
├── scripts/
│   └── setup_stockfish.sh
├── Stockfish/  <-- Cloned Stockfish engine
├── your_engine  <-- Your UCI-compatible chess engine binary
```

---

## License

This project is licensed under the MIT License.

