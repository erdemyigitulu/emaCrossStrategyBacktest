import numpy as np

class BuyPointTrigger:
    def __init__(self, buy_points, signal_type, amount_per_buy):
        self.buy_points = np.array(buy_points)
        self.signal_type = signal_type
        self.amount_per_buy = amount_per_buy

    def get_triggered_points(self, price_array, decision_index):
        relevant_prices = price_array[:decision_index] 
        relevant_prices = relevant_prices[:, np.newaxis] 

        if self.signal_type == "long":
            matches = relevant_prices <= self.buy_points
        else:
            matches = relevant_prices >= self.buy_points
            
        triggered_mask = matches.any(axis=0) 
        triggered_points = self.buy_points[triggered_mask]

        return [(point, self.amount_per_buy) for point in triggered_points]