from services.information_service import InformationService
from managers.carry_over_manager import CarryOverManager
from services.data_converter import DataConverter
from core.engine import Engine
from typing import Callable

class SignalProcessor:
    def __init__(
        self,
        data_converter: DataConverter,
        carry_over_manager: CarryOverManager,
        information_service: InformationService,
        engine_factory: Callable[[], Engine]
    ):
        self.data_converter = data_converter
        self.carry_over_manager = carry_over_manager
        self.information_service = information_service
        self.engine_factory = engine_factory

        self.is_carry_over = False
        self.carry_signal = []
        self.carry_reason = ""
        self.last_signal = []

    def prepare_data(self, month, year):
        if self.is_carry_over:
            if self.carry_reason == "late_entry":
                return self.data_converter.get1sData(month, year)
            elif self.carry_reason == "unclosed_trade":
                return self.carry_over_manager.prepareCarryOverData(
                    self.carry_signal, month, year
                )
        return self.data_converter.get1sData(month, year)

    def process(self, signal,  signals, data1s, month, year):
        next_ts = self._get_next_signal_timestamp(signal, signals)
        engine = self.engine_factory()
        engine.pushSignalData(signal, data1s, next_ts)
        self.last_signal = signals[-1]

        if engine.isCarryOver:
            self.is_carry_over = True
            self.carry_signal = engine.carrySignal
            self.carry_reason = engine.carryReason
            return

        result = engine.process(data1s, next_ts)

        self.information_service.monthlyStats(
            result,
            result["profitLoss"],
            month,
            year
        )
        self._reset_carry_flags()

    def _reset_carry_flags(self):
        self.is_carry_over = False
        self.carry_signal = []
        self.carry_reason = ""

    def _get_next_signal_timestamp(self, signal, signals):
        try:
            index = next(i for i, s in enumerate(signals) if s["timestamp"] == signal["timestamp"])
            return signals[index + 1]["timestamp"]
        except (IndexError, StopIteration):
            return float("inf")
    

    