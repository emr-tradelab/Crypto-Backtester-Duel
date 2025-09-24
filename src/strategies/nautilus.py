from __future__ import annotations

from decimal import Decimal

from nautilus_trader.common.enums import LogColor
from nautilus_trader.config import PositiveInt, StrategyConfig
from nautilus_trader.indicators.average.sma import SimpleMovingAverage
from nautilus_trader.model.data import Bar, BarType
from nautilus_trader.model.enums import OrderSide, TimeInForce
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.instruments import Instrument
from nautilus_trader.model.orders import MarketOrder
from nautilus_trader.trading.strategy import Strategy


class SmaCrossConfig(StrategyConfig, frozen=True):
    instrument_id: InstrumentId
    bar_type: BarType
    trade_size: Decimal
    fast_sma_period: PositiveInt = 30
    slow_sma_period: PositiveInt = 100
    request_historical_bars: bool = True
    close_positions_on_stop: bool = True


class SmaCrossNT(Strategy):
    """SMA-crossover LONG-only strategy (simplified)."""

    def __init__(self, config: SmaCrossConfig) -> None:
        if config.fast_sma_period >= config.slow_sma_period:
            raise ValueError("fast_sma_period must be < slow_sma_period")

        super().__init__(config)

        self.instrument: Instrument | None = None
        self.sma_fast = SimpleMovingAverage(config.fast_sma_period)
        self.sma_slow = SimpleMovingAverage(config.slow_sma_period)

    # ──────────────────────────────────────────────────────────────
    # Lifecycle
    # ──────────────────────────────────────────────────────────────
    def on_start(self) -> None:
        self.instrument = self.cache.instrument(self.config.instrument_id)
        if not self.instrument:
            self.log.error(f"Instrument {self.config.instrument_id} not found - stopping")
            self.stop()
            return

        # Indicadores
        self.register_indicator_for_bars(self.config.bar_type, self.sma_fast)
        self.register_indicator_for_bars(self.config.bar_type, self.sma_slow)

        # Datos históricos para que las SMAs arranquen calientes
        if self.config.request_historical_bars:
            self.request_bars(self.config.bar_type)#, lookback_bars=self.config.slow_sma_period)

        # Suscribirse a barras en vivo
        self.subscribe_bars(self.config.bar_type)

    def on_bar(self, bar: Bar) -> None:

        self.log.info(repr(bar), LogColor.CYAN)

        # Check if indicators ready
        if not self.indicators_initialized():
            self.log.info(
                f"Waiting for indicators to warm up [{self.cache.bar_count(self.config.bar_type)}]",
                color=LogColor.BLUE,
            )
            return

        if bar.is_single_price():
            # Implies no market information for this bar
            return

        # Regla de cruce
        fast, slow = self.sma_fast.value, self.sma_slow.value

        # Entry
        if fast >= slow and self.portfolio.is_flat(self.config.instrument_id):
            self._buy_market()
        # Exit
        elif fast < slow and self.portfolio.is_net_long(self.config.instrument_id):
            self.close_all_positions(self.config.instrument_id)

    # ──────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────
    def _buy_market(self) -> None:
        order: MarketOrder = self.order_factory.market(
            instrument_id=self.config.instrument_id,
            order_side=OrderSide.BUY,
            quantity=self.instrument.make_qty(self.config.trade_size),
            time_in_force=TimeInForce.IOC,
        )
        self.submit_order(order)


    # ──────────────────────────────────────────────────────────────
    # Teardown
    # ──────────────────────────────────────────────────────────────
    def on_stop(self) -> None:
        self.cancel_all_orders(self.config.instrument_id)
        if self.config.close_positions_on_stop:
            self.close_all_positions(self.config.instrument_id)
        self.unsubscribe_bars(self.config.bar_type)

    def on_reset(self) -> None:
        self.sma_fast.reset()
        self.sma_slow.reset()
