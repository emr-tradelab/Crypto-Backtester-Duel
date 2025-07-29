# src/strategies/nautilus.py

from decimal import Decimal
from nautilus_trader.config import StrategyConfig
from nautilus_trader.model import InstrumentId, BarType
from nautilus_trader.trading.strategy import Strategy
from nautilus_trader.indicators.average.sma import SimpleMovingAverage
from nautilus_trader.model.enums import OrderSide, TriggerType


class SmaCrossConfig(StrategyConfig):
    """
    Configuration for an SMA crossover strategy in NautilusTrader.
    """
    trade_size: Decimal
    order_id_tag: str
    instrument_id: InstrumentId
    bar_type: BarType
    fast_sma_period: int = 30
    slow_sma_period: int = 100


class SmaCrossNT(Strategy):
    """
    NautilusTrader SMA crossover strategy:
    - Go long when fast SMA crosses above slow SMA.
    - Sell when fast SMA crosses below slow SMA.
    """
    def __init__(self, config: SmaCrossConfig) -> None:
        super().__init__(config)
        # Initialize indicators
        self.fast_sma = SimpleMovingAverage(self.config.fast_sma_period)
        self.slow_sma = SimpleMovingAverage(self.config.slow_sma_period)
        # Variables to hold previous values for crossover detection
        self._prev_fast: float | None = None
        self._prev_slow: float | None = None

    def on_start(self) -> None:
        # Load instrument
        self.instrument = self.cache.instrument(self.config.instrument_id)
        if self.instrument is None:
            self.log.error(f"Instrument {self.config.instrument_id} not found")
            self.stop()
            return
        # Register indicators to receive bar updates
        self.register_indicator_for_bars(self.config.bar_type, self.fast_sma)
        self.register_indicator_for_bars(self.config.bar_type, self.slow_sma)
        # Request historical bars to hydrate indicators
        self.request_bars(self.config.bar_type)
        # Subscribe to live bars and quote ticks
        self.subscribe_bars(self.config.bar_type)
        self.subscribe_quote_ticks(self.config.instrument_id)

    def on_bar(self, bar) -> None:
        # Current SMA values
        curr_fast = self.fast_sma.value  # Assumes SimpleMovingAverage.value holds latest SMA
        curr_slow = self.slow_sma.value
        # Detect crossover, if previous values exist
        if self._prev_fast is not None and self._prev_slow is not None:
            # Bullish crossover
            if self._prev_fast <= self._prev_slow and curr_fast > curr_slow:
                order = self.order_factory.market(
                    instrument_id=self.config.instrument_id,
                    order_side=OrderSide.BUY,
                    quantity=self.instrument.make_qty(self.config.trade_size),
                    emulation_trigger=TriggerType.LAST_PRICE,
                )
                self.submit_order(order)
            # Bearish crossover
            elif self._prev_fast >= self._prev_slow and curr_fast < curr_slow:
                order = self.order_factory.market(
                    instrument_id=self.config.instrument_id,
                    order_side=OrderSide.SELL,
                    quantity=self.instrument.make_qty(self.config.trade_size),
                    emulation_trigger=TriggerType.LAST_PRICE,
                )
                self.submit_order(order)
        # Update previous values
        self._prev_fast = curr_fast
        self._prev_slow = curr_slow
