from config.config import Config
from stage_flow.buy_point_trigger import BuyPointTrigger
from stage_flow.decision_maker import DecisionMaker
from stage_flow.result_formatter import ResultFormatter


class StageController:
    def __init__(self, config: Config, result_formatter: ResultFormatter, decision_maker: DecisionMaker):
        self.config = config
        self.result_formatter = result_formatter
        self.decision_maker = decision_maker
        self.closeEngine = False 

    def run(self, pnl_values, data_slice, buy_points, signal):
        self.closeEngine = False 
        self.pnl_values = pnl_values
        self.data_slice = data_slice
        triggered_results = []

        for idx, stage in enumerate(self.config.STAGE_FLOW):
            result = self.decision_maker.get(stage, self.pnl_values, self.data_slice)
            if result is None:
                formatted = self.result_formatter.came_new_signal()
                triggered_results.append(formatted)
                self.closeEngine = True
                break
            purchased_points = self._find_purchased_points(buy_points, idx, self.data_slice, result, signal)
            formatted = self.result_formatter.format(result)
            triggered_results.append(formatted)
            if result["shouldClose"]:
                self.closeEngine = True
                break
            self.pnl_values = result["pnl_values"]
            self.data_slice = result["data_slice"]

        return triggered_results , purchased_points
    
    def _find_purchased_points(self, buy_points, idx, data_slice, result,signal):
        if idx == 0:
                buy_trigger = BuyPointTrigger(
                    buy_points=buy_points,
                    signal_type=signal["Type"],
                    amount_per_buy=self.config.seperatedMoneyAmount
                )
                purchased_points = buy_trigger.get_triggered_points(
                    price_array=data_slice[:, 1],
                    decision_index=result["decision_idx"]
                )
        else:
            purchased_points = []
        
        return purchased_points
