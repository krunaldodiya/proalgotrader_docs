"""
Iron Condor Options Strategy Implementation

This strategy implements an Iron Condor options selling strategy
with hedging for income generation and risk management.
"""

from typing import Dict, List

from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.order_item import OrderItem
from proalgotrader_core.enums.market_type import MarketType
from proalgotrader_core.enums.order_type import OrderType
from proalgotrader_core.enums.position_type import PositionType
from proalgotrader_core.enums.product_type import ProductType
from proalgotrader_core.enums.symbol_type import SymbolType
from proalgotrader_core.protocols.position import PositionProtocol


class IronCondorStrategy:
    """Iron Condor options selling strategy with hedging."""

    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

        # Strategy parameters
        self.inner_strike_offset = 10  # 10 points OTM for selling
        self.outer_strike_offset = 20  # 20 points OTM for hedging
        self.lot_size = 1  # 1 lot per trade
        self.max_loss = 500  # ₹500 maximum loss per trade

        # Track positions and performance
        self.positions: Dict[str, dict] = {}
        self.trade_count = 0
        self.win_count = 0
        self.total_pnl = 0.0

        # Option symbols cache
        self.option_symbols: Dict[str, any] = {}

    async def initialize(self) -> None:
        """Initialize the Iron Condor strategy."""
        print("🦅 Initializing Iron Condor Strategy")
        print(f"   Inner Strike Offset: {self.inner_strike_offset} points")
        print(f"   Outer Strike Offset: {self.outer_strike_offset} points")
        print(f"   Lot Size: {self.lot_size}")
        print(f"   Max Loss: ₹{self.max_loss}")
        print("   Expiry: Weekly options")
        print("=" * 50)

    async def next(self) -> None:
        """Main strategy logic - check for trading opportunities."""
        try:
            # Check if we should trade
            if not self.should_trade():
                return

            # Create Iron Condor position
            await self.create_iron_condor()

        except Exception as e:
            print(f"❌ Error in strategy execution: {e}")

    def should_trade(self) -> bool:
        """Check if we should enter a new trade."""
        # No pending orders
        if len(self.algorithm.pending_orders) > 0:
            return False

        # No existing positions
        if len(self.algorithm.positions) > 0:
            return False

        # Within loss limits
        if self.algorithm.net_pnl.loss >= self.max_loss:
            print(f"🛑 Maximum loss reached: ₹{self.algorithm.net_pnl.loss}")
            return False

        return True

    async def create_iron_condor(self) -> None:
        """Create an Iron Condor options position."""
        try:
            print("🦅 Creating Iron Condor Position")

            # Create option symbols
            option_symbols = await self._create_option_symbols()

            # Create order items for Iron Condor
            order_items = self._create_order_items(option_symbols)

            # Execute the Iron Condor trade
            await self.algorithm.create_multiple_orders(order_items=order_items)

            # Track the trade
            self.trade_count += 1

            print("✅ Iron Condor position created successfully!")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error creating Iron Condor: {e}")

    async def _create_option_symbols(self) -> Dict[str, any]:
        """Create all required option symbols for Iron Condor."""
        try:
            # Far OTM Call (Hedge) - Buy
            ce_far_otm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="CE",
                strike_price_input=self.outer_strike_offset,
            )

            # OTM Call (Sell) - Sell
            ce_otm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="CE",
                strike_price_input=self.inner_strike_offset,
            )

            # OTM Put (Sell) - Sell
            pe_otm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="PE",
                strike_price_input=-self.inner_strike_offset,
            )

            # Far OTM Put (Hedge) - Buy
            pe_far_otm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="PE",
                strike_price_input=-self.outer_strike_offset,
            )

            return {
                "ce_far_otm": ce_far_otm_symbol,
                "ce_otm": ce_otm_symbol,
                "pe_otm": pe_otm_symbol,
                "pe_far_otm": pe_far_otm_symbol,
            }

        except Exception as e:
            print(f"❌ Error creating option symbols: {e}")
            raise

    def _create_order_items(self, option_symbols: Dict[str, any]) -> List[OrderItem]:
        """Create order items for Iron Condor strategy."""
        order_items = [
            # Buy Far OTM Call (Hedge)
            OrderItem(
                broker_symbol=option_symbols["ce_far_otm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.BUY,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["ce_far_otm"], self.lot_size
                ),
            ),
            # Sell OTM Call (Income)
            OrderItem(
                broker_symbol=option_symbols["ce_otm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.SELL,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["ce_otm"], self.lot_size
                ),
            ),
            # Sell OTM Put (Income)
            OrderItem(
                broker_symbol=option_symbols["pe_otm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.SELL,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["pe_otm"], self.lot_size
                ),
            ),
            # Buy Far OTM Put (Hedge)
            OrderItem(
                broker_symbol=option_symbols["pe_far_otm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.BUY,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["pe_far_otm"], self.lot_size
                ),
            ),
        ]

        return order_items

    async def on_position_open(self, position: PositionProtocol) -> None:
        """Handle position opening."""
        print(f"📈 POSITION OPENED: {position.symbol}")
        print(f"   Side: {position.position_type}")
        print(f"   Quantity: {position.quantity}")
        print(f"   Entry Price: ₹{position.entry_price}")
        print("=" * 50)

    async def on_position_closed(self, position: PositionProtocol) -> None:
        """Handle position closing."""
        pnl = position.pnl

        if pnl > 0:
            self.win_count += 1

        self.total_pnl += pnl

        print(f"📉 POSITION CLOSED: {position.symbol}")
        print(f"   Side: {position.position_type}")
        print(f"   Exit Price: ₹{position.exit_price}")
        print(f"   P&L: ₹{pnl:.2f}")
        print(f"   Total P&L: ₹{self.total_pnl:.2f}")
        print("=" * 50)

    def get_strategy_stats(self) -> dict:
        """Get strategy performance statistics."""
        total_trades = self.trade_count
        win_rate = (self.win_count / total_trades * 100) if total_trades > 0 else 0

        return {
            "total_trades": total_trades,
            "win_count": self.win_count,
            "win_rate": win_rate,
            "total_pnl": self.total_pnl,
            "average_pnl": self.total_pnl / total_trades if total_trades > 0 else 0,
            "max_loss": self.max_loss,
            "current_loss": self.algorithm.net_pnl.loss,
        }

    def get_iron_condor_info(self) -> dict:
        """Get Iron Condor strategy information."""
        return {
            "strategy_name": "Iron Condor",
            "strategy_type": "Neutral Options Selling",
            "inner_strike_offset": self.inner_strike_offset,
            "outer_strike_offset": self.outer_strike_offset,
            "lot_size": self.lot_size,
            "max_loss": self.max_loss,
            "expiry": "Weekly",
            "underlying": "NIFTY",
            "legs": 4,
            "net_position": "Credit",
            "profit_zone_width": self.outer_strike_offset - self.inner_strike_offset,
        }
