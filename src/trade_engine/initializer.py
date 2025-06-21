from typing import TYPE_CHECKING
from pandas import DataFrame

if TYPE_CHECKING:
    from trade_engine.core import Engine

def initialize_signal(engine: "Engine", signal, data1s: DataFrame):

    engine.signal = signal
    engine.start_timestamp = signal["timestamp"]
    engine.signalType = signal["Type"]
    engine.startIndex = next((i for i, data in enumerate(data1s) if int(data[0]) >= int(signal["timestamp"])), None)
    engine.entry_price = data1s[engine.startIndex][1]
    engine.entry_position = (engine.entry_price, engine.config.totalEntryAmount)
    entry_points = engine.buy_point_generator.getBuyPoints(engine.entry_position, signal)
    engine.trade_aggregator.buyPoints = entry_points
    engine.total_amount, engine.avarage_price=  engine.trade_aggregator.calculateAverageAndTotal(engine.purchased_points)