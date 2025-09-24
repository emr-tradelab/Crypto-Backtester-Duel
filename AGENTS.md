# AGENTS.md

## Project Purpose

This project compares two Python backtesting frameworks:  
- **backtesting.py**  
- **nautilustrader**

Goal: run identical strategies on both, compare results, and analyze performance.  
Expectation: nautilustrader should run faster while yielding equivalent results. If results diverge, document and justify why.  

Data source: BTC price data from Binance API.  
Current state: exploratory Jupyter notebooks for backtesting, data download is already modular.
Target: modular code pipeline, callable via `main.py`, that runs the full workflow:  
1. Download data  
2. Run backtests on both frameworks  
3. Compare results  

---

## Setup & Environment

- Install dependencies with [uv](https://github.com/astral-sh/uv):  
```bash
  uv sync
```

- Activate environment:
```bash
source .venv/bin/activate
```

- If needed, download BTC data with:
```bash
python main.py --download
```

---

## Development Workflow

### Pre-commit checks
- Run Ruff before committing:  
```bash
ruff check .
ruff format .
````

---

## Git / PR Workflow

* Branch naming:

  * `feature/<short-description>`
  * `bugfix/<short-description>`

* Before pushing code:

  * `ruff check .`
  * `ruff format .`

* PR requirements:

  * Clean lint, format, and type checks
  * Description explaining purpose of changes
  * Minimal diff, no unnecessary changes

---

## Notes for Agents

* Ensure deterministic results: fix random seeds where applicable.
* Use UTC consistently for all timestamps.
* Document runtime differences between frameworks along with result differences.