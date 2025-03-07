# /main.py
from services.backtest_service import BacktestService


def main():
    backtest_service = BacktestService()
    backtest_service.startBacktest()


if __name__ == "__main__":
    main()

