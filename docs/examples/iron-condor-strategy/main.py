"""
Iron Condor Options Strategy - Main Entry Point

This example demonstrates an Iron Condor options selling strategy
with hedging for income generation and risk management.

Run this file to start the Iron Condor strategy.
"""

import asyncio
from datetime import timedelta

from proalgotrader_core import start_with_factory
from proalgotrader_core.enums.account_type import AccountType
from proalgotrader_core.algorithm import Algorithm

from strategy import IronCondorStrategy
from position_manager import IronCondorPositionManager


class IronCondorAlgorithm(Algorithm):
    """Main algorithm for Iron Condor options strategy."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Set account type for options trading (positional)
        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)

        # Set interval to check every second for quick execution
        self.set_interval(interval=timedelta(seconds=1))

        # Initialize strategy and position manager
        self.strategy = IronCondorStrategy(algorithm=self)
        self.set_position_manager(position_manager_class=IronCondorPositionManager)

    async def initialize(self) -> None:
        """Initialize the Iron Condor strategy."""
        await self.strategy.initialize()

    async def next(self) -> None:
        """Main strategy logic - called every interval."""
        await self.strategy.next()


async def main():
    """Main entry point for the Iron Condor strategy."""
    print("🦅 Starting Iron Condor Options Strategy")
    print("📊 Strategy: Neutral options selling with wider profit zone")
    print("💰 Income Generation: Premium collection")
    print("🛡️ Risk Management: Limited maximum loss")
    print("⏰ Timeframe: Weekly options")
    print("=" * 50)

    # Start the strategy
    await start_with_factory(
        algorithm_class=IronCondorAlgorithm,
        broker_name="angel_one",  # Change to your preferred broker
    )


if __name__ == "__main__":
    asyncio.run(main())
