from config.config import Config
from services.data_converter import DataConverter
from services.information_service import InformationService
from services.result_logger import ResultLogger
from services.buy_points_generator import BuyPointsGenerator
from services.trade_aggregator import TradeAggregator
from services.signal_service import SignalService
from services.result_logger import ResultLogger
from managers.carry_over_manager import CarryOverManager
from managers.pnl_manager import PnLManager
from managers.result_builder import ResultBuilder
from stage_flow.stage_controller import StageController
from stage_flow.decision_maker import DecisionMaker
from stage_flow.result_formatter import ResultFormatter
from stage_flow.buy_point_trigger import BuyPointTrigger
from trade_engine.core import Engine
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
        self.base_indicator = BaseIndicator(config=self.config)
        self._setup_services()
        self._setup_managers()
        self._setup_stage_flow()
        self.engine_factory = self._build_engine_factory()

    def _setup_services (self):
        self.data_converter = DataConverter(path_provider=self.path_provider)

        self.buy_point_generator = BuyPointsGenerator(config=self.config)
        
        self.result_logger = ResultLogger(path_provider=self.path_provider)

        self.information_service = InformationService(result_logger=self.result_logger)

        self.trade_aggregator = TradeAggregator()

        self.signal_service = SignalService(
            config=self.config,
            path_provider=self.path_provider,
            base_indicator=self.base_indicator
        )

    def _setup_managers (self):
        self.carry_over_manager = CarryOverManager(
            data_converter=self.data_converter
        )

        self.pnl_manager = PnLManager()

        self.result_builder = ResultBuilder(
            config=self.config,
            pnl_manager=self.pnl_manager,
            trade_aggregator=self.trade_aggregator
        )

    def _setup_stage_flow (self):

        self.decision_maker = DecisionMaker(config=self.config)

        self.result_formatter = ResultFormatter()

        self.stage_controller = StageController(config=self.config,
            result_formatter=self.result_formatter,
            decision_maker=self.decision_maker
        )

    def _build_engine_factory(self) -> Callable[[], Engine]:
        return lambda: Engine(
            config=self.config,
            trade_aggregator=self.trade_aggregator,
            buy_point_generator=self.buy_point_generator,
            pnl_manager=self.pnl_manager,
            stage_controller=self.stage_controller,
            result_builder=self.result_builder,
        )

    def build_backtest(self) -> BacktestOrchestrator:
        processor = SignalProcessor(
            config=self.config,
            data_converter=self.data_converter,
            carry_over_manager=self.carry_over_manager,
            information_service=self.information_service,
            engine_factory=self.engine_factory
        )

        runner = BacktestRunner(
            signal_service=self.signal_service,
            signal_processor=processor
        )

        return BacktestOrchestrator(
            config=self.config,
            runner=runner
        )
    