"""
Position Manager for Iron Butterfly Options Strategy

This module handles position management for Iron Butterfly options trades
including risk management, P&L tracking, and position monitoring.
"""

from typing import Dict, List, Optional

from proalgotrader_core.protocols.position_manager import PositionManagerProtocol
from proalgotrader_core.algorithm import Algorithm


class IronButterflyPositionManager(PositionManagerProtocol):
    """Position manager for Iron Butterfly options strategy."""

    def __init__(self, *, algorithm: "Algorithm") -> None:
        self.algorithm = algorithm

        # Position tracking
        self.positions: Dict[str, dict] = {}
        self.trade_history: List[dict] = []

        # Risk management parameters
        self.max_loss = 500  # ₹500 maximum loss per trade
        self.position_size = 1  # 1 lot per trade
        self.max_positions = 1  # Only one Iron Butterfly at a time

        # Performance tracking
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
        self.max_drawdown = 0.0

        # Iron Butterfly specific tracking
        self.iron_butterfly_trades = 0
        self.premium_collected = 0.0
        self.premium_paid = 0.0
        self.net_premium = 0.0

    async def initialize(self) -> None:
        """Initialize the Iron Butterfly position manager."""
        print("🦋 Initializing Iron Butterfly Position Manager")
        print(f"   Max Loss: ₹{self.max_loss}")
        print(f"   Position Size: {self.position_size} lot")
        print(f"   Max Positions: {self.max_positions}")
        print("   Strategy: Iron Butterfly Options")
        print("=" * 50)

    async def next(self) -> None:
        """Main position management logic."""
        # Monitor existing positions
        await self._monitor_positions()

        # Update performance metrics
        await self._update_performance_metrics()

    async def can_open_position(self, symbol: str) -> bool:
        """Check if we can open a new position."""
        # Check if we already have positions (Iron Butterfly is one trade)
        if len(self.algorithm.positions) > 0:
            return False

        # Check if we've reached maximum loss
        if self.algorithm.net_pnl.loss >= self.max_loss:
            return False

        return True

    async def open_position(
        self,
        symbol: str,
        side: str,
        quantity: int,
        entry_price: float,
        option_type: str = None,
        strike_price: float = None,
        expiry: str = None,
    ) -> bool:
        """Open a new position (for individual legs)."""
        try:
            if not await self.can_open_position(symbol):
                return False

            # Create position record
            position = {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "entry_price": entry_price,
                "entry_time": self.algorithm.current_datetime,
                "option_type": option_type,
                "strike_price": strike_price,
                "expiry": expiry,
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
            print(f"   Option Type: {option_type}")
            print(f"   Strike Price: {strike_price}")
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
                "option_type": position.get("option_type"),
                "strike_price": position.get("strike_price"),
                "expiry": position.get("expiry"),
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

    async def _monitor_positions(self) -> None:
        """Monitor existing positions for risk management."""
        try:
            # Check if we need to close positions due to loss limits
            if self.algorithm.net_pnl.loss >= self.max_loss:
                print(f"🛑 Maximum loss reached: ₹{self.algorithm.net_pnl.loss}")
                print("   Consider closing positions to limit further losses")
                return

            # Monitor individual option positions
            for symbol, position in list(self.positions.items()):
                try:
                    # Update current price (simplified - in real implementation, get from market data)
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

                except Exception as e:
                    print(f"❌ Error monitoring position {symbol}: {e}")

        except Exception as e:
            print(f"❌ Error in position monitoring: {e}")

    async def _get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol (simplified implementation)."""
        # In real implementation, get from market data or broker
        # For now, return a placeholder
        return 100.0  # Placeholder price

    async def _update_performance_metrics(self) -> None:
        """Update performance metrics and statistics."""
        try:
            # Calculate current drawdown
            current_loss = self.algorithm.net_pnl.loss
            if current_loss > self.max_drawdown:
                self.max_drawdown = current_loss

            # Update Iron Butterfly specific metrics
            self.iron_butterfly_trades = len(
                [t for t in self.trade_history if t.get("option_type")]
            )

        except Exception as e:
            print(f"❌ Error updating performance metrics: {e}")

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
            "average_pnl": self.total_pnl / total_trades if total_trades > 0 else 0,
            "max_drawdown": self.max_drawdown,
            "current_loss": self.algorithm.net_pnl.loss,
            "iron_butterfly_trades": self.iron_butterfly_trades,
            "premium_collected": self.premium_collected,
            "premium_paid": self.premium_paid,
            "net_premium": self.net_premium,
        }

    def get_position_summary(self) -> dict:
        """Get current position summary."""
        return {
            "active_positions": len(self.positions),
            "positions": list(self.positions.keys()),
            "total_unrealized_pnl": sum(
                pos["unrealized_pnl"] for pos in self.positions.values()
            ),
            "current_net_pnl": self.algorithm.net_pnl.total,
            "current_loss": self.algorithm.net_pnl.loss,
            "max_loss_limit": self.max_loss,
        }

    def get_iron_butterfly_summary(self) -> dict:
        """Get Iron Butterfly specific summary."""
        return {
            "strategy_name": "Iron Butterfly",
            "strategy_type": "Neutral Options Selling",
            "total_iron_butterfly_trades": self.iron_butterfly_trades,
            "premium_collected": self.premium_collected,
            "premium_paid": self.premium_paid,
            "net_premium": self.net_premium,
            "max_loss_per_trade": self.max_loss,
            "current_positions": len(self.positions),
            "risk_status": (
                "LOW" if self.algorithm.net_pnl.loss < self.max_loss * 0.5 else "HIGH"
            ),
        }
