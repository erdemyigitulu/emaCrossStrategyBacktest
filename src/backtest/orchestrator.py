from config.config import Config
from backtest.runner import BacktestRunner 

class BacktestOrchestrator:
    def __init__(self, config: Config, runner: BacktestRunner):
        self.config = config
        self.runner = runner

    def run(self):
        for y_index, year in enumerate(self.config.years):
            for m_index, month in enumerate(self.config.months):
                is_first_month = (y_index == 0 and m_index == 0)
                self.runner.run_month(year, month, is_first_month)


    def _get_next_signal_timestamp(self, signal, signals):
        try:
            return signals[index + 1][1]
        except IndexError:
            return float("inf")
        

    