from typing import Dict, List, Any

class PnLManager:
    def __init__(self):
        self.currentPnL = 0
        self.currentValue = 0
        self.currentTimestamp = 0
        self.processPnL = 0
        self.pastPnL = 0

    def vectorizedPnL(self, data_slice, average_price, signal_type):
        prices = data_slice[:, 1]
        if signal_type == "long":
            pnls = ((prices - average_price) / average_price) * 100
        else:
            pnls = ((average_price - prices) / average_price) * 100
        return pnls

    def processResults(self, result_dict: Dict[str, Any]) -> Dict[str, Any]:
        self.pastPnL = 0

        main_info: Dict[str, Any] = result_dict.get("main", {})
        stages: List[Dict[str, Any]] = result_dict.get("stages", [])

        entry = main_info.get("entry_price")
        amount = main_info.get("total_amount")
        signal_type = main_info.get("signal_type")

        for stage in stages:
            is_sell = stage.get("sell")
            current = stage.get("exit_price")
            portion = stage.get("sell_portion")

            if None in (entry, current, amount, portion):
                print(f"[WARNING] Eksik veri var, stage atlandı: {stage}")
                continue
            if is_sell:
                pnl = self._calculate_stage_pnl(
                    entry=entry,
                    current=current,
                    amount=amount,
                    portion=portion,
                    signal_type=signal_type,
                )
                stage["pnl"] = round(pnl, 2)
                self.pastPnL += pnl
                # Satıştan sonra kalan miktarı güncelle
                amount = round(amount * (1 - portion), 4)
        result_dict["main"]["profit_loss"] = round(self.pastPnL, 2)
        return result_dict

    def _calculate_stage_pnl(self, entry, current, amount, portion, signal_type):
        if entry == 0 or amount == 0 or portion == 0:
            return 0

        if signal_type == "short":
            raw_pnl = (entry - current) / entry * amount
        else:
            raw_pnl = (current - entry) / entry * amount

        return raw_pnl * portion