from backtest.processor import SignalProcessor
from services.data_converter import DataConverter
from core.signal_service import SignalService

class BacktestRunner:
    def __init__(
        self,
        data_converter: DataConverter,
        signal_service: SignalService,
        signal_processor: SignalProcessor
    ):
        self.data_converter = data_converter
        self.signal_service = signal_service
        self.signal_processor = signal_processor

    def run_month(self, year: int, month: int, is_first_month: bool):
        data1s = self.signal_processor.prepare_data(month, year)

        signals = self.signal_service.extractSignals(
            previousSignal=self.signal_processor.last_signal,
            isFirstMonth=is_first_month,
            carrySignal=self.signal_processor.carry_signal,
            month=month,
            year=year
        )
        for signal in signals:
            self.signal_processor.process(signal, signals, data1s, month, year)