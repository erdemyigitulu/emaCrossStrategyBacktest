


class ResultFormatter:
    def format(self, result_dict):
        return {
            "decision": result_dict["decision"],
            "shouldClose": result_dict["shouldClose"],
            "exit_timestamp": result_dict["exit_timestamp"],
            "exit_price": result_dict["exit_price"],
            "sell": result_dict["sell"],
            "sell_portion": result_dict["sell_portion"]
        }

    def came_new_signal(self):
        return {
            "decision": "came_new_signal",
            "shouldClose": True,
            "exit_timestamp": None,
            "sell": True,
            "sell_portion": 1
        }