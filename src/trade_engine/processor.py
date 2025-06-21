
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from trade_engine.core import Engine

def run_process(engine: "Engine", data1s, signal, next_signal_timestamp):
    start_ts = signal["timestamp"] + 900_000
    end_ts = next_signal_timestamp + 900_000
    mask = (data1s[:, 0] >= start_ts) & (data1s[:, 0] < end_ts)
    data_slice = data1s[mask]
    pnls = engine.pnl_manager.vectorizedPnL(
        data_slice=data_slice,
        average_price=engine.avarage_price,
        signal_type=engine.signalType
    )


    return data_slice, pnls