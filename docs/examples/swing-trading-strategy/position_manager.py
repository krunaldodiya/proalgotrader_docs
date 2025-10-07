"""
Position Manager for Swing Trading Strategy

This module handles position management for swing trades including
stop loss, take profit, and position tracking.
"""

from typing import Dict, Optional

from proalgotrader_core.protocols.position_manager import PositionManagerProtocol
from proalgotrader_core.algorithm import Algorithm


class SwingPositionManager(PositionManagerProtocol):
    """Position manager for swing trading strategy."""

    def __init__(self, *, algorithm: "Algorithm") -> None:
        self.algorithm = algorithm

        # Position tracking
        self.positions: Dict[str, dict] = {}
        self.trade_history: list = []

        # Risk management parameters
        self.max_positions = 5  # Maximum concurrent positions
        self.position_size_pct = 0.1  # 10% of capital per position
        self.stop_loss_pct = 0.08  # 8% stop loss
        self.take_profit_pct = 0.20  # 20% take profit

        # Performance tracking
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0

    async def initialize(self) -> None:
        """Initialize the position manager."""
        print("📊 Initializing Swing Position Manager")
        print(f"   Max positions: {self.max_positions}")
        print(f"   Position size: {self.position_size_pct * 100}%")
        print(f"   Stop loss: {self.stop_loss_pct * 100}%")
        print(f"   Take profit: {self.take_profit_pct * 100}%")
        print("=" * 50)

    async def next(self) -> None:
        """Main position management logic."""
        # Check existing positions for exit conditions
        await self._check_exit_conditions()

        # Update position tracking
        await self._update_positions()

    async def can_open_position(self, symbol: str) -> bool:
        """Check if we can open a new position."""
        # Check if we already have a position in this symbol
        if symbol in self.positions:
            return False

        # Check if we've reached maximum positions
        if len(self.positions) >= self.max_positions:
            return False

        return True

    async def open_position(
        self,
        symbol: str,
        side: str,
        quantity: int,
        entry_price: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
    ) -> bool:
        """Open a new position."""
        try:
            if not await self.can_open_position(symbol):
                return False

            # Calculate stop loss and take profit if not provided
            if stop_loss is None:
                stop_loss = (
                    entry_price * (1 - self.stop_loss_pct)
                    if side == "BUY"
                    else entry_price * (1 + self.stop_loss_pct)
                )

            if take_profit is None:
                take_profit = (
                    entry_price * (1 + self.take_profit_pct)
                    if side == "BUY"
                    else entry_price * (1 - self.take_profit_pct)
                )

            # Create position record
            position = {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "entry_price": entry_price,
                "entry_time": self.algorithm.current_datetime,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "current_price": entry_price,
                "unrealized_pnl": 0.0,
                "status": "OPEN",
            }

            self.positions[symbol] = position
            self.total_trades += 1

            print(f"📈 OPENED POSITION: {symbol}")
            print(f"   Side: {side}")
            print(f"   Quantity: {quantity}")
            print(f"   Entry Price: ₹{entry_price:.2f}")
            print(f"   Stop Loss: ₹{stop_loss:.2f}")
            print(f"   Take Profit: ₹{take_profit:.2f}")
            print("=" * 50)

            return True

        except Exception as e:
            print(f"❌ Error opening position for {symbol}: {e}")
            return False

    async def close_position(
        self, symbol: str, exit_price: float, reason: str = "Manual"
    ) -> bool:
        """Close an existing position."""
        try:
            if symbol not in self.positions:
                return False

            position = self.positions[symbol]

            # Calculate realized P&L
            if position["side"] == "BUY":
                realized_pnl = (exit_price - position["entry_price"]) * position[
                    "quantity"
                ]
            else:
                realized_pnl = (position["entry_price"] - exit_price) * position[
                    "quantity"
                ]

            # Update performance tracking
            self.total_pnl += realized_pnl
            if realized_pnl > 0:
                self.winning_trades += 1
            else:
                self.losing_trades += 1

            # Record trade history
            trade_record = {
                "symbol": symbol,
                "side": position["side"],
                "quantity": position["quantity"],
                "entry_price": position["entry_price"],
                "exit_price": exit_price,
                "entry_time": position["entry_time"],
                "exit_time": self.algorithm.current_datetime,
                "holding_period": self.algorithm.current_datetime
                - position["entry_time"],
                "realized_pnl": realized_pnl,
                "exit_reason": reason,
            }

            self.trade_history.append(trade_record)

            print(f"📉 CLOSED POSITION: {symbol}")
            print(f"   Exit Price: ₹{exit_price:.2f}")
            print(f"   Realized P&L: ₹{realized_pnl:.2f}")
            print(f"   Reason: {reason}")
            print(f"   Holding Period: {trade_record['holding_period']}")
            print("=" * 50)

            # Remove position
            del self.positions[symbol]

            return True

        except Exception as e:
            print(f"❌ Error closing position for {symbol}: {e}")
            return False

    async def _check_exit_conditions(self) -> None:
        """Check all positions for exit conditions."""
        for symbol, position in list(self.positions.items()):
            try:
                # Get current price (simplified - in real implementation, get from market data)
                current_price = await self._get_current_price(symbol)

                if current_price is None:
                    continue

                # Update position with current price
                position["current_price"] = current_price

                # Calculate unrealized P&L
                if position["side"] == "BUY":
                    position["unrealized_pnl"] = (
                        current_price - position["entry_price"]
                    ) * position["quantity"]
                else:
                    position["unrealized_pnl"] = (
                        position["entry_price"] - current_price
                    ) * position["quantity"]

                # Check stop loss
                if self._is_stop_loss_hit(position, current_price):
                    await self.close_position(symbol, current_price, "Stop Loss")
                    continue

                # Check take profit
                if self._is_take_profit_hit(position, current_price):
                    await self.close_position(symbol, current_price, "Take Profit")
                    continue

            except Exception as e:
                print(f"❌ Error checking exit conditions for {symbol}: {e}")

    def _is_stop_loss_hit(self, position: dict, current_price: float) -> bool:
        """Check if stop loss is hit."""
        if position["side"] == "BUY":
            return current_price <= position["stop_loss"]
        else:
            return current_price >= position["stop_loss"]

    def _is_take_profit_hit(self, position: dict, current_price: float) -> bool:
        """Check if take profit is hit."""
        if position["side"] == "BUY":
            return current_price >= position["take_profit"]
        else:
            return current_price <= position["take_profit"]

    async def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol (simplified implementation)."""
        # In real implementation, get from market data or broker
        # For now, return a placeholder
        return 1000.0  # Placeholder price

    async def _update_positions(self) -> None:
        """Update position tracking and statistics."""
        # This method can be used to update position statistics
        # or perform other maintenance tasks
        pass

    def get_performance_stats(self) -> dict:
        """Get performance statistics."""
        total_trades = self.winning_trades + self.losing_trades
        win_rate = (self.winning_trades / total_trades * 100) if total_trades > 0 else 0

        return {
            "total_trades": total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": win_rate,
            "total_pnl": self.total_pnl,
            "active_positions": len(self.positions),
            "average_trade_pnl": (
                self.total_pnl / total_trades if total_trades > 0 else 0
            ),
        }

    def get_position_summary(self) -> dict:
        """Get current position summary."""
        return {
            "active_positions": len(self.positions),
            "positions": list(self.positions.keys()),
            "total_unrealized_pnl": sum(
                pos["unrealized_pnl"] for pos in self.positions.values()
            ),
        }
