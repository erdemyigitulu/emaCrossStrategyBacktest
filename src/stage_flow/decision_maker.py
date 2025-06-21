
import numpy as np
from config.config import Config



class DecisionMaker:
    def __init__(self, config: Config):
        self.config = config

    def get(self, stage, pnl_values, data_slice):
        timestamps = data_slice[:, 0]
        prices = data_slice[:, 1]
        first_pnl = stage["first"]["pnl_value"]
        second_pnl = stage["second"]["pnl_value"]

        mask_first = pnl_values >= first_pnl
        if np.any(mask_first):
            first_idx = np.argmax(mask_first)
        else:
            first_idx = -1

        mask_second = pnl_values <= second_pnl
        if np.any(mask_second):
            second_idx = np.argmax(mask_second)
        else:
            second_idx = -1
        
        candidates = [i for i in [first_idx, second_idx] if i >= 0]
        if not candidates:
            return None

        decision_idx = min(candidates)
        chosen = stage["first"] if decision_idx == first_idx else stage["second"]
        return {
            "decision": chosen["pnl_value"],
            "decision_idx": decision_idx,
            "shouldClose": chosen["shouldClose"],
            "exit_timestamp": timestamps[decision_idx],
            "exit_price": prices[decision_idx],
            "pnl_values": pnl_values[decision_idx + 1:],
            "data_slice": data_slice[decision_idx + 1:],
            "sell": chosen["sell"],
            "sell_portion": chosen["sell_portion"]
        }