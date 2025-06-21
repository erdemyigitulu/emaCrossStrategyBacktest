
from config.config import Config
from services.trade_aggregator import TradeAggregator
from managers.pnl_manager import PnLManager   
from typing import List, Dict, Any

class ResultBuilder:
    def __init__(self, config: Config , trade_aggregator: TradeAggregator , pnl_manager: PnLManager):
        self.config = config
        self.trade_aggregator = trade_aggregator
        self.pnl_manager = pnl_manager

    def buildResult(self, stage_results,signal, purchased_points):
        last_stage = stage_results[-1]
        exit_process_timestamp = last_stage["exit_timestamp"]
        exit_price = last_stage["exit_price"]
        close_reason = last_stage["decision"]
        total_amount, average_price = self.trade_aggregator.calculateAverageAndTotal(purchased_points)

        result = {
            "main": {
                "signal": signal,
                "signal_type": signal["Type"],
                "average_price": average_price,
                "total_amount": total_amount,
                "exit_price": exit_price,
                "exit_timestamp": exit_process_timestamp,
                "close_reason": close_reason,
                "purchased_points": purchased_points,
            },
            "stages": stage_results,
        }

        self.pnl_manager.processResults(result)

        main: Dict[str, Any] = result.get("main", {})
        stages: List[Dict[str, Any]] = result.get("stages", [])

        signal = main.get("signal")
        average_price = main.get("average_price")
        total_amount = main.get("total_amount")
        current_value = main.get("exit_price")
        current_timestamp = main.get("exit_timestamp")
        profit_loss = main.get("profit_loss", 0)
        close_reason = main.get("close_reason", "")

        net_profit_loss = profit_loss - (average_price * 0.04 / 100)
        purchased_points_str = "".join([f"({x[0]}, {x[1]})" for x in purchased_points])

        result = {
            "signalTimestamp": signal["timestamp"],
            "signalType": signal["Type"],
            "entryPrice": average_price,
            "exitPrice": current_value,
            "exitTimestamp": current_timestamp,
            "purchasedPoints": purchased_points_str,
            "averagePrice": average_price,
            "profitLoss": round(net_profit_loss, 2),
            "exitReason": close_reason,
            "totalAmount": total_amount,
            "stages": stages,
        }


        input(result)
        return result