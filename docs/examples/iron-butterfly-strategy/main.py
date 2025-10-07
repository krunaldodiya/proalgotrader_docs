"""
Iron Butterfly Options Strategy - Main Entry Point

This example demonstrates an Iron Butterfly options selling strategy
with hedging for income generation and risk management.

Run this file to start the Iron Butterfly strategy.
"""

import asyncio
from datetime import timedelta

from proalgotrader_core import start_with_factory
from proalgotrader_core.enums.account_type import AccountType
from proalgotrader_core.algorithm import Algorithm

from strategy import IronButterflyStrategy
from position_manager import IronButterflyPositionManager


class IronButterflyAlgorithm(Algorithm):
    """Main algorithm for Iron Butterfly options strategy."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Set account type for options trading (positional)
        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)

        # Set interval to check every second for quick execution
        self.set_interval(interval=timedelta(seconds=1))

        # Initialize strategy and position manager
        self.strategy = IronButterflyStrategy(algorithm=self)
        self.set_position_manager(position_manager_class=IronButterflyPositionManager)

    async def initialize(self) -> None:
        """Initialize the Iron Butterfly strategy."""
        await self.strategy.initialize()

    async def next(self) -> None:
        """Main strategy logic - called every interval."""
        await self.strategy.next()


async def main():
    """Main entry point for the Iron Butterfly strategy."""
    print("🦋 Starting Iron Butterfly Options Strategy")
    print("📊 Strategy: Neutral options selling with hedging")
    print("💰 Income Generation: Premium collection")
    print("🛡️ Risk Management: Limited maximum loss")
    print("⏰ Timeframe: Weekly options")
    print("=" * 50)

    # Start the strategy
    await start_with_factory(
        algorithm_class=IronButterflyAlgorithm,
        broker_name="angel_one",  # Change to your preferred broker
    )


if __name__ == "__main__":
    asyncio.run(main())
