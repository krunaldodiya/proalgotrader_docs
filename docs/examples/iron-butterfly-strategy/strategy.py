"""
Iron Butterfly Options Strategy Implementation

This strategy implements an Iron Butterfly options selling strategy
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


class IronButterflyStrategy:
    """Iron Butterfly options selling strategy with hedging."""

    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

        # Strategy parameters
        self.otm_strike_offset = 5  # 5 points OTM for hedging
        self.atm_strike_offset = 0  # ATM for selling
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
        """Initialize the Iron Butterfly strategy."""
        print("🦋 Initializing Iron Butterfly Strategy")
        print(f"   OTM Strike Offset: {self.otm_strike_offset} points")
        print(f"   ATM Strike Offset: {self.atm_strike_offset} points")
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

            # Create Iron Butterfly position
            await self.create_iron_butterfly()

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

    async def create_iron_butterfly(self) -> None:
        """Create an Iron Butterfly options position."""
        try:
            print("🦋 Creating Iron Butterfly Position")

            # Create option symbols
            option_symbols = await self._create_option_symbols()

            # Create order items for Iron Butterfly
            order_items = self._create_order_items(option_symbols)

            # Execute the Iron Butterfly trade
            await self.algorithm.create_multiple_orders(order_items=order_items)

            # Track the trade
            self.trade_count += 1

            print("✅ Iron Butterfly position created successfully!")
            print("=" * 50)

        except Exception as e:
            print(f"❌ Error creating Iron Butterfly: {e}")

    async def _create_option_symbols(self) -> Dict[str, any]:
        """Create all required option symbols for Iron Butterfly."""
        try:
            # OTM Call (Hedge) - Buy
            ce_otm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="CE",
                strike_price_input=self.otm_strike_offset,
            )

            # ATM Call (Sell) - Sell
            ce_atm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="CE",
                strike_price_input=self.atm_strike_offset,
            )

            # ATM Put (Sell) - Sell
            pe_atm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="PE",
                strike_price_input=self.atm_strike_offset,
            )

            # OTM Put (Hedge) - Buy
            pe_otm_symbol = await self.algorithm.add_option(
                symbol_name=SymbolType.Index.NIFTY,
                expiry_input=("Weekly", 0),
                option_type="PE",
                strike_price_input=-self.otm_strike_offset,
            )

            return {
                "ce_otm": ce_otm_symbol,
                "ce_atm": ce_atm_symbol,
                "pe_atm": pe_atm_symbol,
                "pe_otm": pe_otm_symbol,
            }

        except Exception as e:
            print(f"❌ Error creating option symbols: {e}")
            raise

    def _create_order_items(self, option_symbols: Dict[str, any]) -> List[OrderItem]:
        """Create order items for Iron Butterfly strategy."""
        order_items = [
            # Buy OTM Call (Hedge)
            OrderItem(
                broker_symbol=option_symbols["ce_otm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.BUY,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["ce_otm"], self.lot_size
                ),
            ),
            # Sell ATM Call (Income)
            OrderItem(
                broker_symbol=option_symbols["ce_atm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.SELL,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["ce_atm"], self.lot_size
                ),
            ),
            # Sell ATM Put (Income)
            OrderItem(
                broker_symbol=option_symbols["pe_atm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.SELL,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["pe_atm"], self.lot_size
                ),
            ),
            # Buy OTM Put (Hedge)
            OrderItem(
                broker_symbol=option_symbols["pe_otm"],
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                position_type=PositionType.BUY,
                quantities=self.algorithm.lot_to_quantities(
                    option_symbols["pe_otm"], self.lot_size
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

    def get_iron_butterfly_info(self) -> dict:
        """Get Iron Butterfly strategy information."""
        return {
            "strategy_name": "Iron Butterfly",
            "strategy_type": "Neutral Options Selling",
            "otm_strike_offset": self.otm_strike_offset,
            "atm_strike_offset": self.atm_strike_offset,
            "lot_size": self.lot_size,
            "max_loss": self.max_loss,
            "expiry": "Weekly",
            "underlying": "NIFTY",
            "legs": 4,
            "net_position": "Credit",
        }
