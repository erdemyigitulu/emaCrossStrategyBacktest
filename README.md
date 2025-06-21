# EMA Cross Strategy Backtest

This project provides a backtesting framework for evaluating an Exponential Moving Average (EMA) cross trading strategy on historical BTCUSDT data.

## Project Structure

- `src/main.py` – Entry point that builds the dependency container and starts the backtest.
- `src/container.py` – Wires together services, managers and the trading engine.
- `src/config/config.py` – Holds configuration values such as EMA periods, trading stages and data paths.
- `src/backtest/` – Orchestrates running the backtest month by month.
- `src/services/` – Utility classes for loading data, generating buy points, logging results and more.
- `src/trade_engine/` – Core trading engine that processes signals and manages trade stages.

Input CSV files should be placed under `backTestDatas/datas/BTC/` in the structure expected by `PathProvider`. Results are written to `backTestDatas/results` as JSON files.

## Installation

Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

## Running

After placing the required data files, start the backtest with:

```bash
python src/main.py
```

The program will iterate over the years and months defined in `config.py`, process trading signals and save the statistics for each month.
