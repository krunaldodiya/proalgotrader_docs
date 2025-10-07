"""
Swing Trading Strategy - Main Entry Point

This example demonstrates a comprehensive swing trading strategy using
Golden Crossover signals (50-day SMA crossing above 200-day SMA).

Run this file to start the swing trading strategy.
"""

import asyncio
from datetime import timedelta

from proalgotrader_core import start_with_factory
from proalgotrader_core.enums.account_type import AccountType
from proalgotrader_core.algorithm import Algorithm

from strategy import SwingTradingStrategy
from position_manager import SwingPositionManager


class SwingTradingAlgorithm(Algorithm):
    """Main algorithm for swing trading strategy."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Set account type for swing trading (positional)
        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)

        # Set interval to check signals every hour
        self.set_interval(interval=timedelta(hours=1))

        # Initialize strategy and position manager
        self.strategy = SwingTradingStrategy(algorithm=self)
        self.set_position_manager(position_manager_class=SwingPositionManager)

    async def initialize(self) -> None:
        """Initialize the swing trading strategy."""
        await self.strategy.initialize()

    async def next(self) -> None:
        """Main strategy logic - called every interval."""
        await self.strategy.next()


async def main():
    """Main entry point for the swing trading strategy."""
    print("🚀 Starting Swing Trading Strategy")
    print("📊 Using Golden Crossover (50-day vs 200-day SMA)")
    print("⏰ Daily timeframe for swing trading")
    print("=" * 50)

    # Start the strategy
    await start_with_factory(
        algorithm_class=SwingTradingAlgorithm,
        broker_name="angel_one",  # Change to your preferred broker
    )


if __name__ == "__main__":
    asyncio.run(main())
