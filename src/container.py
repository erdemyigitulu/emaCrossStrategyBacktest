from config.config import Config
from services.data_converter import DataConverter
from services.information_service import InformationService
from services.write_csv_data import WriteCsvData
from services.entry_points_generator import EntryPointGenerator
from core.signal_service import SignalService
from managers.carry_over_manager import CarryOverManager
from managers.position_manager import PositionManager
from managers.pnl_manager import PnLManager
from managers.result_builder import ResultBuilder
from managers.stage_controller import StageController
from core.engine import Engine
from data_paths.path_provider import PathProvider
from indicators.base_indicator import BaseIndicator
from backtest.orchestrator import BacktestOrchestrator
from backtest.runner import BacktestRunner
from backtest.processor import SignalProcessor
from typing import Callable

class Container:
    def __init__(self):
        self.config = Config()
        self.path_provider = PathProvider()
        self._setup_services()
        self._setup_managers()
        self._setup_core()

    def _setup_services (self):
        self.data_converter = DataConverter(
            path_provider=self.path_provider
        )

        self.entry_point_generator = EntryPointGenerator(
            config=self.config)
        
        self.write_csv_data = WriteCsvData(
            path_provider=self.path_provider
        )

        self.information_service = InformationService(
            write_csv_data=self.write_csv_data
        )

    def _setup_managers (self):
        self.carry_over_manager = CarryOverManager(
            data_converter=self.data_converter
        )

        self.position_manager = PositionManager(
            config=self.config,
            entry_point_generator=self.entry_point_generator
        )

        self.result_builder = ResultBuilder(
            config=self.config
        )

        self.stage_controller = StageController(
            config=self.config
        )
        
        self.pnl_manager = PnLManager()

    def _setup_core (self):
        self.base_indicator = BaseIndicator(
            config=self.config
        )        
        self.signal_service = self._build_signal_service()

        self.engine_factory = self._build_engine_factory()

    def _build_engine_factory(self) -> Callable[[], Engine]:
        return lambda: Engine(
            config=self.config,
            stage_controller=self.stage_controller,
            position_manager=self.position_manager,
            result_builder=self.result_builder,
            pnl_manager=self.pnl_manager
        )

    def _build_signal_service(self) -> SignalService:
        return SignalService(
            config=self.config,
            data_processor=self.data_converter,
            path_provider=self.path_provider,
            base_indicator=self.base_indicator
        )

    def build_backtest(self) -> BacktestOrchestrator:
        processor = SignalProcessor(
            data_converter=self.data_converter,
            carry_over_manager=self.carry_over_manager,
            information_service=self.information_service,
            engine_factory=self.engine_factory
        )

        runner = BacktestRunner(
            data_converter=self.data_converter,
            signal_service=self.signal_service,
            signal_processor=processor
        )

        return BacktestOrchestrator(
            config=self.config,
            runner=runner
        )
    
