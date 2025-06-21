from services.information_service import InformationService
from managers.carry_over_manager import CarryOverManager
from services.data_converter import DataConverter
from trade_engine.core import Engine
from config.config import Config
from typing import Callable

class SignalProcessor:
    def __init__(
        self,
        config : Config,
        data_converter: DataConverter,
        carry_over_manager: CarryOverManager,
        information_service: InformationService,
        engine_factory: Callable[[], Engine],
        
    ):
        self.data_converter = data_converter
        self.carry_over_manager = carry_over_manager
        self.information_service = information_service
        self.engine_factory = engine_factory
        self.config = config

        self.next_signal_timestamp= 0
        self.is_carry_over = False
        self.carry_signal = []
        self.carry_reason = ""
        self.last_signal = []
        self.entry_position = None

    def prepare_data(self, month, year):
        if self.is_carry_over:
            data = self.carry_over_manager.prepareCarryOverData(
                    self.carry_signal, month, year
                )
            self._reset_carry_flags()
        data = self.data_converter.get1sData(month, year)
        return data

    def process(self, signal,  signals, data1s, month, year):
        self._get_signal_datas(signal, signals)
        if self.is_carry_over:
            return
        engine = self.engine_factory()
        result = engine.process(data1s, signal , self.next_signal_timestamp)
        self.information_service.monthlyStats(
            result,
            result["profitLoss"],
            month,
            year
        )

    def _get_signal_datas(self, signal, signals):
        if signal == signals[-1]:
            self.last_signal = signals[-1]
            self.is_carry_over = True
            self.carry_signal = signal
            return
        current_index = next(i for i, s in enumerate(signals) if s["timestamp"] == signal["timestamp"])
        self.next_signal_timestamp = signals[current_index + 1]["timestamp"]
    
    def _reset_carry_flags(self):
        self.is_carry_over = False
        self.carry_signal = []

  



