
from .initializer import initialize_signal
from .processor import run_process
from stage_flow.stage_controller import StageController
from services.trade_aggregator import TradeAggregator
from managers.pnl_manager import PnLManager
from managers.result_builder import ResultBuilder
from services.buy_points_generator import BuyPointsGenerator
from config.config import Config

class Engine:
    def __init__(
        self,
        config: Config,
        trade_aggregator : TradeAggregator,
        buy_point_generator: BuyPointsGenerator,
        pnl_manager: PnLManager,
        stage_controller: StageController,
        result_builder: ResultBuilder,

    ):
        self.config = config
        self.trade_aggregator = trade_aggregator
        self.buy_point_generator = buy_point_generator
        self.pnl_manager = pnl_manager
        self.stage_controller = stage_controller
        self.result_builder = result_builder
        self.reset_state()

    def reset_state(self):
        self.closeEngine = False
        self.signal = None
        self.signalType = None
        self.result = None
        self.startIndex = None
        self.triggeredReasons = []
        self.entry_position = ()
        self.entry_price = 0
        self.total_amount = 0
        self.start_timestamp = 0
        self.avarage_price = 0
        self.purchased_points = []

    def process(self, data1s, signal, next_signal_timestamp):
        initialize_signal(self, signal, data1s)
        data_slice, pnls = run_process(self, data1s, signal, next_signal_timestamp)
        input(pnls)
        input(data_slice)
        self.stage_results, self.purchased_points = self.stage_controller.run(pnls, data_slice, self.entry_position,signal)

        if self.stage_controller.closeEngine:
            self.log_exit()
            return self.result

    def log_exit(self):
        self.result = self.result_builder.buildResult(self.stage_results ,self.signal, self.purchased_points)



    
    

    
