"""
Swing Trading Strategy Implementation

This strategy implements a comprehensive swing trading system using
Golden Crossover signals for long-term trend following.
"""

from typing import Dict

from proalgotrader_core.algorithm import Algorithm

from signal_manager import SignalManager


class SwingTradingStrategy:
    """Swing trading strategy using Golden Crossover signals."""

    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

        # Swing trading symbols (large-cap, liquid stocks)
        self.symbols = [
            "RELIANCE-EQ",
            "TCS-EQ",
            "HDFCBANK-EQ",
            "INFY-EQ",
            "BHARTIARTL-EQ",
            "ICICIBANK-EQ",
            "KOTAKBANK-EQ",
            "LT-EQ",
            "HINDUNILVR-EQ",
            "ITC-EQ",
        ]

        # Signal managers for each symbol
        self.signal_managers: Dict[str, SignalManager] = {}

        # Strategy parameters
        self.position_size = 0.1  # 10% of capital per trade
        self.stop_loss_pct = 0.08  # 8% stop loss
        self.take_profit_pct = 0.20  # 20% take profit

        # Track positions
        self.positions: Dict[str, dict] = {}
        self.trade_count = 0
        self.win_count = 0

    async def initialize(self) -> None:
        """Initialize the swing trading strategy."""
        print("📈 Initializing Swing Trading Strategy")
        print(f"🎯 Trading {len(self.symbols)} symbols")
        print(f"💰 Position size: {self.position_size * 100}% per trade")
        print(f"🛡️ Stop loss: {self.stop_loss_pct * 100}%")
        print(f"🎯 Take profit: {self.take_profit_pct * 100}%")
        print("=" * 50)

        # Initialize signal managers for each symbol
        for symbol in self.symbols:
            print(f"🔧 Setting up signal manager for {symbol}")
            self.signal_managers[symbol] = SignalManager(
                algorithm=self.algorithm, symbol_name=symbol
            )
            await self.signal_managers[symbol].initialize()

        print("✅ Swing trading strategy initialized successfully!")
        print("=" * 50)

    async def next(self) -> None:
        """Main strategy logic - check for signals and manage positions."""
        for symbol, signal_manager in self.signal_managers.items():
            try:
                # Check for signals
                await signal_manager.next()

                # Get current signal status
                signal_status = await self._get_signal_status(signal_manager)

                # Manage positions based on signals
                await self._manage_position(symbol, signal_status)

            except Exception as e:
                print(f"❌ Error processing {symbol}: {e}")
                continue

    async def _get_signal_status(self, signal_manager: SignalManager) -> dict:
        """Get current signal status for a symbol."""
        try:
            # Get current SMA values
            current_sma_50 = await signal_manager.sma_50.get_data(0, "sma_50_close")
            current_sma_200 = await signal_manager.sma_200.get_data(0, "sma_200_close")

            # Get previous SMA values for crossover detection
            prev_sma_50 = await signal_manager.sma_50.get_data(-1, "sma_50_close")
            prev_sma_200 = await signal_manager.sma_200.get_data(-1, "sma_200_close")

            # Check for golden crossover (buy signal)
            golden_crossover = (
                current_sma_50 > current_sma_200 and prev_sma_50 <= prev_sma_200
            )

            # Check for death cross (sell signal)
            death_cross = (
                current_sma_50 < current_sma_200 and prev_sma_50 >= prev_sma_200
            )

            return {
                "golden_crossover": golden_crossover,
                "death_cross": death_cross,
                "current_sma_50": current_sma_50,
                "current_sma_200": current_sma_200,
                "prev_sma_50": prev_sma_50,
                "prev_sma_200": prev_sma_200,
            }

        except Exception as e:
            print(f"⚠️ Error getting signal status: {e}")
            return {
                "golden_crossover": False,
                "death_cross": False,
                "current_sma_50": None,
                "current_sma_200": None,
                "prev_sma_50": None,
                "prev_sma_200": None,
            }

    async def _manage_position(self, symbol: str, signal_status: dict) -> None:
        """Manage positions based on signal status."""
        try:
            # Check if we have an existing position
            has_position = symbol in self.positions

            # Golden Crossover - Buy Signal
            if signal_status["golden_crossover"] and not has_position:
                await self._enter_long_position(symbol, signal_status)

            # Death Cross - Sell Signal
            elif signal_status["death_cross"] and has_position:
                await self._exit_position(symbol, "Death Cross Signal")

            # Check stop loss and take profit for existing positions
            elif has_position:
                await self._check_exit_conditions(symbol, signal_status)

        except Exception as e:
            print(f"❌ Error managing position for {symbol}: {e}")

    async def _enter_long_position(self, symbol: str, signal_status: dict) -> None:
        """Enter a long position on golden crossover."""
        try:
            # Calculate position size
            available_capital = await self.algorithm.get_available_capital()
            position_value = available_capital * self.position_size

            # Get current price (simplified - in real implementation, get from broker)
            current_price = 1000  # Placeholder - get actual price

            quantity = int(position_value / current_price)

            if quantity > 0:
                # Enter long position
                await self.algorithm.buy(
                    symbol=symbol, quantity=quantity, order_type="MARKET"
                )

                # Track position
                self.positions[symbol] = {
                    "entry_price": current_price,
                    "quantity": quantity,
                    "entry_time": self.algorithm.current_datetime,
                    "stop_loss": current_price * (1 - self.stop_loss_pct),
                    "take_profit": current_price * (1 + self.take_profit_pct),
                }

                self.trade_count += 1

                print(f"🟢 BUY SIGNAL: {symbol}")
                print(f"   Entry Price: ₹{current_price}")
                print(f"   Quantity: {quantity}")
                print(f"   Stop Loss: ₹{self.positions[symbol]['stop_loss']:.2f}")
                print(f"   Take Profit: ₹{self.positions[symbol]['take_profit']:.2f}")
                print(f"   SMA 50: {signal_status['current_sma_50']:.2f}")
                print(f"   SMA 200: {signal_status['current_sma_200']:.2f}")
                print("=" * 50)

        except Exception as e:
            print(f"❌ Error entering position for {symbol}: {e}")

    async def _exit_position(self, symbol: str, reason: str) -> None:
        """Exit an existing position."""
        try:
            if symbol in self.positions:
                position = self.positions[symbol]

                # Sell the position
                await self.algorithm.sell(
                    symbol=symbol, quantity=position["quantity"], order_type="MARKET"
                )

                # Calculate P&L (simplified)
                current_price = 1000  # Placeholder - get actual price
                pnl = (current_price - position["entry_price"]) * position["quantity"]

                if pnl > 0:
                    self.win_count += 1

                print(f"🔴 SELL SIGNAL: {symbol}")
                print(f"   Exit Price: ₹{current_price}")
                print(f"   P&L: ₹{pnl:.2f}")
                print(f"   Reason: {reason}")
                print("=" * 50)

                # Remove position
                del self.positions[symbol]

        except Exception as e:
            print(f"❌ Error exiting position for {symbol}: {e}")

    async def _check_exit_conditions(self, symbol: str, signal_status: dict) -> None:
        """Check stop loss and take profit conditions."""
        try:
            if symbol in self.positions:
                position = self.positions[symbol]
                current_price = 1000  # Placeholder - get actual price

                # Check stop loss
                if current_price <= position["stop_loss"]:
                    await self._exit_position(symbol, "Stop Loss Hit")

                # Check take profit
                elif current_price >= position["take_profit"]:
                    await self._exit_position(symbol, "Take Profit Hit")

        except Exception as e:
            print(f"❌ Error checking exit conditions for {symbol}: {e}")

    def get_strategy_stats(self) -> dict:
        """Get strategy performance statistics."""
        total_trades = self.trade_count
        win_rate = (self.win_count / total_trades * 100) if total_trades > 0 else 0

        return {
            "total_trades": total_trades,
            "win_count": self.win_count,
            "win_rate": win_rate,
            "active_positions": len(self.positions),
            "symbols_trading": len(self.symbols),
        }
