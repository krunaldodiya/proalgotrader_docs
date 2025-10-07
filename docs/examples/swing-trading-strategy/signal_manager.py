"""
Signal Manager for Swing Trading Strategy

This module implements the Golden Crossover signal detection using
50-day and 200-day Simple Moving Averages on daily candles.
"""

from datetime import timedelta

from proalgotrader_core.enums.candle_type import CandleType
from proalgotrader_core.protocols.signal_manager import SignalManagerProtocol
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.indicators import SMA


class SignalManager(SignalManagerProtocol):
    """Signal manager for Golden Crossover detection."""

    def __init__(self, *, algorithm: "Algorithm", symbol_name: str) -> None:
        self.algorithm = algorithm
        self.symbol_name = symbol_name

    async def initialize(self) -> None:
        """Initialize the signal manager with chart and indicators."""
        self.broker_symbol = await self.algorithm.add_equity(
            symbol_name=self.symbol_name
        )

        # Use daily candles for proper moving average calculation
        self.chart = await self.algorithm.add_chart(
            broker_symbol=self.broker_symbol,
            timeframe=timedelta(days=1),
            candle_type=CandleType.REGULAR,
        )

        # Add 50-day and 200-day SMA indicators for golden crossover
        self.sma_50 = await self.chart.add_indicator(
            key="sma_50", indicator=SMA(period=50)
        )
        self.sma_200 = await self.chart.add_indicator(
            key="sma_200", indicator=SMA(period=200)
        )

    async def next(self) -> None:
        """Check for Golden Crossover and Death Cross signals."""
        try:
            # Get current and previous SMA values
            current_sma_50 = await self.sma_50.get_data(0, "sma_50_close")
            current_sma_200 = await self.sma_200.get_data(0, "sma_200_close")

            # Get previous SMA values for crossover detection
            prev_sma_50 = await self.sma_50.get_data(-1, "sma_50_close")
            prev_sma_200 = await self.sma_200.get_data(-1, "sma_200_close")

            # Check for golden crossover: 50-day SMA crosses above 200-day SMA
            golden_crossover = (
                current_sma_50 > current_sma_200 and prev_sma_50 <= prev_sma_200
            )

            # Check for death cross: 50-day SMA crosses below 200-day SMA
            death_cross = (
                current_sma_50 < current_sma_200 and prev_sma_50 >= prev_sma_200
            )

            # Signal detection and logging
            if golden_crossover:
                print(
                    f"🟢 GOLDEN CROSSOVER DETECTED for {self.broker_symbol.symbol_name}"
                )
                print(f"   Current SMA 50: {current_sma_50:.2f}")
                print(f"   Current SMA 200: {current_sma_200:.2f}")
                print(f"   Previous SMA 50: {prev_sma_50:.2f}")
                print(f"   Previous SMA 200: {prev_sma_200:.2f}")
                print("   📈 BULLISH SIGNAL - Consider BUY")
                print("=" * 50)

            elif death_cross:
                print(f"🔴 DEATH CROSS DETECTED for {self.broker_symbol.symbol_name}")
                print(f"   Current SMA 50: {current_sma_50:.2f}")
                print(f"   Current SMA 200: {current_sma_200:.2f}")
                print(f"   Previous SMA 50: {prev_sma_50:.2f}")
                print(f"   Previous SMA 200: {prev_sma_200:.2f}")
                print("   📉 BEARISH SIGNAL - Consider SELL")
                print("=" * 50)

        except Exception as e:
            print(f"⚠️ Error in signal detection for {self.symbol_name}: {e}")
            # Continue execution - don't let signal errors stop the strategy
