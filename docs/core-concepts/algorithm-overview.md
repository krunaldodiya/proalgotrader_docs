# Algorithm Overview

The `Algorithm` class is the main interface for algorithmic trading in ProAlgoTrader Core. It provides a clean API for managing trading strategies, market data, and order execution.

## Quick Start

```python
# main.py
from project.strategy import Strategy

from proalgotrader_core.start import run_strategy


if __name__ == "__main__":
    run_strategy(strategy=Strategy)
```

## Project Structure

When you create a new trading project, you'll have this minimal structure:

```
your-trading-project/
├── main.py                    # Entry point (already included)
├── project/
│   ├── strategy.py            # Your trading strategy
│   └── position_manager.py    # Position management logic
├── requirements.txt           # Dependencies (includes proalgotrader_core)
├── .env.example              # Environment template
└── .env                      # Your environment variables (created from .env.example)
```

The `proalgotrader_core` framework is installed as a library via pip, so you don't need to manage the framework code directly.

## Core Concepts

The Algorithm class provides:

- 📊 **Market Data Management**: Add charts and subscribe to real-time data
- 💼 **Order Execution**: Place buy/sell orders with simple methods
- 📈 **Position Management**: Track positions and P&L
- ⏰ **Time Management**: Check market hours and set intervals
- 🎯 **Strategy Integration**: Connect your trading strategies

## Public API Reference

### Properties

#### Market Data Properties

```python
# Current market time
algorithm.current_datetime  # datetime
algorithm.current_date      # date
algorithm.current_time      # time
```

#### Position & Order Properties

```python
# Get all orders
algorithm.orders           # List[Order]

# Get all positions
algorithm.positions        # List[Position]

# Get only open positions
algorithm.positions   # List[Position]

# Get P&L information
algorithm.unrealized_pnl   # PnlCalculatorProtocol - Current open positions P&L
algorithm.net_pnl          # PnlCalculatorProtocol - All positions (closed + open) P&L
algorithm.pnl              # PnlCalculatorProtocol - Alias for unrealized_pnl

# Access P&L values
algorithm.unrealized_pnl.pnl     # float - Unrealized P&L
algorithm.unrealized_pnl.profit  # float - Unrealized profit
algorithm.unrealized_pnl.loss    # float - Unrealized loss
algorithm.net_pnl.pnl            # float - Net P&L (realized + unrealized)
```

### Market Data Methods

#### Add Charts

```python
# Add equity chart
chart = await algorithm.add_chart(
    broker_symbol=equity_symbol,
    timeframe=timedelta(minutes=5),
    candle_type=CandleType.REGULAR
)

# Add chart with custom parameters
chart = await algorithm.add_chart(
    broker_symbol=equity_symbol,
    timeframe=timedelta(minutes=1),
    candle_type=CandleType.HEIKEN_ASHI
)
```

#### Data Access

Charts expose two main ways to access data:

**Data Property** - Get full DataFrame:

```python
# Get full DataFrame with all available data
chart_data = chart.data
print(chart_data)

# Access specific columns
close_prices = chart.data.select("close")
print(close_prices)
```

**Get Data Method** - Get specific values:

```python
# Get current candle close price (row 0 = most recent)
current_close = await chart.get_data(0, "close")
print(f"Current close: {current_close}")

# Get previous candle high price (row 1 = previous candle)
previous_high = await chart.get_data(1, "high")
print(f"Previous high: {previous_high}")

# Get current candle data as Series
current_candle = await chart.get_data(0)
print(current_candle)
```

**Available Columns:**

- `current_candle`, `current_timestamp`, `current_datetime`, `symbol`
- `open`, `high`, `low`, `close`, `volume`

**Debugging Data Structure:**

```python
# Print DataFrame structure
print(chart.data)
print(chart.data.columns)
print(chart.data.dtypes)
```

#### Add Symbols

```python
# Add equity symbol
equity = await algorithm.add_equity(symbol_name=SymbolType.Stock.RELIANCE)

# Add future symbol
future = await algorithm.add_future(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Monthly", 0)  # (period, number)
)

# Add option symbol
option = await algorithm.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),  # 0 = current week, 1 = next week
    strike_price_input=0,         # 0 = ATM, 1 = OTM, -1 = ITM
    option_type="CE"              # "CE" or "PE"
)
```

### Trading Methods

#### Place Orders

```python
# Buy equity
await algorithm.buy(
    broker_symbol=equity_symbol,
    market_type=MarketType.Cash,
    product_type=ProductType.CNC,
    order_type=OrderType.MARKET_ORDER,
    quantities=100
)

# Sell equity
await algorithm.sell(
    broker_symbol=equity_symbol,
    market_type=MarketType.Cash,
    product_type=ProductType.CNC,
    order_type=OrderType.MARKET_ORDER,
    quantities=100
)

# Buy derivatives (futures/options)
await algorithm.buy(
    broker_symbol=option_symbol,
    market_type=MarketType.Derivative,
    product_type=ProductType.NRML,
    order_type=OrderType.MARKET_ORDER,
    quantities=50
)

# Exit all positions
await algorithm.exit_all_positions()
```

### Configuration Methods

#### Time Management

```python
# Set algorithm interval
algorithm.set_interval(timedelta(seconds=1))

# Check if current time is between two times
is_trading_time = algorithm.between_time(
    first=time(9, 15),   # 9:15 AM
    second=time(15, 30)  # 3:30 PM
)
```

#### Account & Risk Management

```python
# Set account type (determines trading behavior)
algorithm.set_account_type(account_type=AccountType.CASH_POSITIONAL)     # Default: Long-term equity
algorithm.set_account_type(account_type=AccountType.CASH_INTRADAY)       # Intraday equity trading
algorithm.set_account_type(account_type=AccountType.DERIVATIVE_INTRADAY) # Intraday options/futures
algorithm.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL) # Multi-day options/futures

# Set position manager
algorithm.set_position_manager(position_manager_class=MyPositionManager)
```

## Algorithm Lifecycle

Understanding the algorithm lifecycle is crucial for building effective trading strategies. The ProAlgoTrader Core framework calls different methods at specific times during execution.

### Method Execution Order

```python
class LifecycleExample(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        # 1. FIRST: Constructor called when class is instantiated
        super().__init__(*args, **kwargs)
        print("Constructor called - setting up basic configuration")

        # Configure strategy settings here
        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)
        self.set_position_manager(position_manager=PositionManager)

        # Set iteration interval (default is 1 second)
        self.set_interval(interval=timedelta(seconds=1))  # High-frequency
        # self.set_interval(interval=timedelta(minutes=5))   # Medium-frequency
        # self.set_interval(interval=timedelta(hours=1))     # Swing trading

    async def initialize(self) -> None:
        # 2. SECOND: Called ONCE after market opens and system is ready
        print("Initialize called - setting up symbols, charts, and indicators")

        # Add symbols, charts, and indicators here
        self.symbol = await self.add_equity(symbol_name=SymbolType.Index.NIFTY)
        self.chart = await self.add_chart(broker_symbol=self.symbol, timeframe=timedelta(minutes=5))

        # This is where you prepare everything for trading

    async def next(self) -> None:
        # 3. REPEATEDLY: Called every interval (default: every 1 second)
        print(f"Next called at {self.current_time}")

        # Your trading logic goes here
        # This runs continuously during market hours
```

### Method Purposes

| Method         | When Called         | Purpose                           | Frequency      |
| -------------- | ------------------- | --------------------------------- | -------------- |
| `__init__()`   | Class instantiation | Basic configuration, settings     | Once           |
| `initialize()` | After market opens  | Setup symbols, charts, indicators | Once           |
| `next()`       | During market hours | Trading logic execution           | Every interval |

### Timing Control with `set_interval()`

The `next()` method frequency can be customized based on your trading strategy:

```python
class TimingExamples(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # High-frequency trading: Every second (default)
        self.set_interval(interval=timedelta(seconds=1))

        # Medium-frequency: Every 5 minutes
        # self.set_interval(interval=timedelta(minutes=5))

        # Swing trading: Every hour
        # self.set_interval(interval=timedelta(hours=1))

        # Daily signals: Every 6 hours (check 2-3 times per day)
        # self.set_interval(interval=timedelta(hours=6))

    async def initialize(self) -> None:
        # Called once regardless of interval setting
        pass

    async def next(self) -> None:
        # Called at the frequency set by set_interval()
        # For swing trading with 1-hour interval, this runs once per hour
        # For scalping with 1-second interval, this runs every second
        pass
```

### Real-World Strategy Examples

#### Scalping Strategy (High Frequency)

```python
class ScalpingStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Need quick reactions to price movements
        self.set_interval(interval=timedelta(seconds=1))

    async def next(self) -> None:
        # Executes every second - good for quick entry/exit decisions
        pass
```

#### Swing Trading Strategy (Low Frequency)

```python
class SwingTradingStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Signals generated hourly, no need for second-by-second checks
        self.set_interval(interval=timedelta(hours=1))

    async def next(self) -> None:
        # Executes every hour - perfect for swing trading signals
        # Saves computational resources by not running unnecessarily
        pass
```

#### Position Monitoring Strategy

```python
class PositionMonitoringStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Check positions every 5 minutes for risk management
        self.set_interval(interval=timedelta(minutes=5))

    async def next(self) -> None:
        # Monitor existing positions, apply stop-loss/take-profit
        # Runs every 5 minutes - balances responsiveness with efficiency
        pass
```

### Performance Considerations

⚡ **Optimization Tip**: Match your interval to your strategy's signal frequency:

- **1 second**: Scalping, tick-based strategies
- **1-5 minutes**: Intraday momentum strategies
- **15-30 minutes**: Short-term mean reversion
- **1-4 hours**: Swing trading, daily signals
- **Daily**: Position-only strategies, long-term signals

```python
# ❌ INEFFICIENT: Hourly signals with second-by-second checking
class InefficientStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_interval(interval=timedelta(seconds=1))  # Too frequent!

    async def next(self) -> None:
        # Only checks signals once per hour, but runs 3600 times per hour
        if self.current_time.minute == 0 and self.current_time.second == 0:
            self.check_hourly_signals()

# ✅ EFFICIENT: Match interval to signal frequency
class EfficientStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.set_interval(interval=timedelta(hours=1))  # Perfect match!

    async def next(self) -> None:
        # Runs exactly when needed - once per hour
        self.check_hourly_signals()
```

## AccountType Configuration

The `AccountType` is an **optional but recommended** configuration for strategy validation. When set, it ensures order parameters match your intended trading style, preventing common mistakes.

**Key Benefits:**

- ✅ **Optional**: Strategies work without AccountType (maximum flexibility)
- ⚙️ **Strict Validation**: When set, validates all order parameters
- 🔒 **Error Prevention**: Catches parameter mismatches before orders
- 📋 **Documentation**: Makes your strategy intent clear

### Account Type Overview

The `AccountType` enum combines `MarketType` and `ProductType` to define your trading behavior:

```python
from proalgotrader_core.enums.account_type import AccountType

# Available Account Types:
AccountType.CASH_POSITIONAL      # Default: Long-term equity trading
AccountType.CASH_INTRADAY        # Intraday equity trading
AccountType.DERIVATIVE_INTRADAY  # Intraday options/futures trading
AccountType.DERIVATIVE_POSITIONAL # Multi-day options/futures trading
```

### Account Type Selection Guide

#### 🏦 **CASH_POSITIONAL** (Default)

```python
self.set_account_type(account_type=AccountType.CASH_POSITIONAL)
```

**Best For:**

- ✅ Long-term investment strategies
- ✅ Swing trading in equity
- ✅ Buy and hold strategies
- ✅ Multi-day stock positions

**Characteristics:**

- **Market**: Cash/Equity only
- **Duration**: Multi-day (no auto square-off)
- **Settlement**: Delivery-based (T+2)

#### ⚡ **CASH_INTRADAY**

```python
self.set_account_type(account_type=AccountType.CASH_INTRADAY)
```

**Best For:**

- ✅ Intraday equity trading
- ✅ Same-day buy and sell in stocks
- ✅ Day trading strategies

**Characteristics:**

- **Market**: Cash/Equity only
- **Duration**: Same day only (auto square-off at 3:20 PM)
- **Leverage**: Higher leverage available

#### 📈 **DERIVATIVE_INTRADAY**

```python
self.set_account_type(account_type=AccountType.DERIVATIVE_INTRADAY)
```

**Best For:**

- ✅ Intraday options trading
- ✅ Same-day futures trading
- ✅ Options buying strategies

**Characteristics:**

- **Market**: Derivatives (options, futures)
- **Duration**: Same day only (auto square-off at 3:20 PM)
- **Leverage**: High leverage for derivatives

#### 🎯 **DERIVATIVE_POSITIONAL**

```python
self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)
```

**Best For:**

- ✅ Multi-day options strategies
- ✅ Options selling strategies
- ✅ Futures swing trading

**Characteristics:**

- **Market**: Derivatives (options, futures)
- **Duration**: Multi-day (hold until expiry)
- **Flexibility**: Can hold positions across multiple days

### Important: Validation Only When AccountType is Set

**Order validation only happens when you set an AccountType.** Without AccountType, you have complete flexibility:

```python
# ✅ NO AccountType = No validation (maximum flexibility)
class FlexibleStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # No account_type set - any combination allowed

    async def next(self) -> None:
        # Can mix any market_type and product_type freely
        await self.buy(
            broker_symbol=stock_symbol,
            market_type=MarketType.Cash,
            product_type=ProductType.MIS,  # ✅ Any combo works
            order_type=OrderType.MARKET_ORDER,
            quantities=100
        )
```

### Strict Validation When AccountType is Set

When you **do** set an AccountType, your order parameters **must match**:

```python
# ✅ CORRECT: Parameters match DERIVATIVE_POSITIONAL
self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)

await self.buy(
    broker_symbol=option_symbol,
    market_type=MarketType.Derivative,  # ✅ Matches
    product_type=ProductType.NRML,      # ✅ Matches
    order_type=OrderType.MARKET_ORDER,
    quantities=50
)

# ❌ WRONG: Parameters don't match CASH_POSITIONAL
self.set_account_type(account_type=AccountType.CASH_POSITIONAL)

await self.buy(
    broker_symbol=option_symbol,        # ❌ Options not allowed
    market_type=MarketType.Derivative,  # ❌ Should be Cash
    product_type=ProductType.MIS,       # ❌ Should be CNC
    order_type=OrderType.MARKET_ORDER,
    quantities=50
)
```

### Parameter Matching Reference

| Account Type            | market_type             | product_type       | Allowed Symbols    |
| ----------------------- | ----------------------- | ------------------ | ------------------ |
| `CASH_POSITIONAL`       | `MarketType.Cash`       | `ProductType.CNC`  | Equity/Stocks only |
| `CASH_INTRADAY`         | `MarketType.Cash`       | `ProductType.MIS`  | Equity/Stocks only |
| `DERIVATIVE_POSITIONAL` | `MarketType.Derivative` | `ProductType.NRML` | Options, Futures   |
| `DERIVATIVE_INTRADAY`   | `MarketType.Derivative` | `ProductType.MIS`  | Options, Futures   |

## Strategy Integration

### Basic Strategy Example

```python
# project/strategy.py
from datetime import timedelta

from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.enums.account_type import AccountType
from project.position_manager import PositionManager


class Strategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Set account type based on your strategy needs:
        # CASH_POSITIONAL (default) - Long-term equity trading
        # CASH_INTRADAY - Same-day equity trading
        # DERIVATIVE_INTRADAY - Same-day options/futures
        # DERIVATIVE_POSITIONAL - Multi-day options/futures
        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)

        self.set_position_manager(position_manager=PositionManager)

        self.set_interval(interval=timedelta(seconds=1))

    async def initialize(self) -> None:
        # Add symbols and charts here
        pass

    async def next(self) -> None:
        # Implement your trading logic here
        pass
```

### Position Event Methods in Strategy

The Algorithm class provides position event methods that you can override in your strategy:

```python
# project/strategy.py
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.protocols.position import PositionProtocol

class Strategy(Algorithm):
    async def on_position_open(self, position: PositionProtocol) -> None:
        """Called when a position is opened - override this method in your strategy."""
        print(f"Position opened: {position.broker_symbol.symbol_name} | Qty: {position.net_quantities}")

        # Set risk-reward for the position
        from proalgotrader_core.risk_reward import RiskReward, Stoploss, Target
        from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

        await self.create_risk_reward(
            position=position,
            stoploss=Stoploss(value=2.0),  # 2% stop loss
            target=Target(value=4.0),      # 4% target
            unit=RiskRewardUnit.PERCENTAGE,
        )

    async def on_position_closed(self, position: PositionProtocol) -> None:
        """Called when a position is closed - override this method in your strategy."""
        print(f"Position closed: {position.broker_symbol.symbol_name} | P&L: {position.pnl.profit}")
```

**Note**: These methods have default empty implementations in the Algorithm class, so you only need to override them if you want to handle position events.

### Position Manager Examples

ProAlgoTrader supports two types of position managers:

#### Single Position Manager (Global Management)

```python
# project/position_manager.py
from datetime import datetime, timedelta
from proalgotrader_core.protocols.algorithm import AlgorithmProtocol
from proalgotrader_core.protocols.position import PositionProtocol
from proalgotrader_core.protocols.position_manager import PositionManagerProtocol


class PositionManager(PositionManagerProtocol):
    def __init__(self, algorithm: AlgorithmProtocol) -> None:
        self.algorithm = algorithm
        self.exit_time = None

    async def initialize(self) -> None:
        # Set exit time 5 minutes after strategy starts
        self.exit_time = datetime.now().replace(microsecond=0) + timedelta(minutes=5)


    async def next(self) -> None:
        # Time-based exit strategy
        if self.exit_time and self.exit_time <= self.algorithm.current_datetime:
            print("Time-based exit: Closing all positions")
            await self.algorithm.exit_all_positions()

        # Portfolio-level risk management
        if self.algorithm.unrealized_pnl.profit >= 1000:
            print("Profit target reached: Closing all positions")
            await self.algorithm.exit_all_positions()
        elif self.algorithm.unrealized_pnl.loss >= 500:
            print("Stop loss triggered: Closing all positions")
            await self.algorithm.exit_all_positions()
```

#### Multiple Position Manager (Per-Position Management)

```python
# project/position_manager.py
from datetime import datetime, timedelta
from proalgotrader_core.protocols.algorithm import AlgorithmProtocol
from proalgotrader_core.protocols.position import PositionProtocol
from proalgotrader_core.protocols.multiple_position_manager import MultiplePositionManagerProtocol


class MultiplePositionManager(MultiplePositionManagerProtocol):
    def __init__(self, algorithm: AlgorithmProtocol, position: PositionProtocol) -> None:
        self.algorithm = algorithm
        self.position = position
        self.entry_time = None

    async def initialize(self) -> None:
        self.entry_time = datetime.now()

    async def on_position_open(self, position: PositionProtocol) -> None:
        print(f"Position opened: {position.broker_symbol.symbol_name}")

    async def on_position_closed(self, position: PositionProtocol) -> None:
        print(f"Position closed: {position.broker_symbol.symbol_name}")

    async def next(self) -> None:
        # Position-specific time-based exit
        if self.entry_time and datetime.now() - self.entry_time >= timedelta(minutes=10):
            print(f"Time limit reached for {self.position.broker_symbol.symbol_name}")
            await self.position.exit()
```

#### Setting Up Position Managers

```python
# project/strategy.py
class Strategy(Algorithm):
    async def initialize(self) -> None:
        # For single position manager (global management)
        self.set_position_manager(position_manager_class=PositionManager)

        # For multiple position manager (per-position management)
        # self.set_position_manager(position_manager_class=MultiplePositionManager)
```

### Advanced Strategy Example

```python
# project/strategy.py
from datetime import time, timedelta
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.enums.account_type import AccountType
from proalgotrader_core.enums.candle_type import CandleType
from proalgotrader_core.enums.market_type import MarketType
from proalgotrader_core.enums.order_type import OrderType
from proalgotrader_core.enums.product_type import ProductType
from proalgotrader_core.enums.symbol_type import SymbolType
from proalgotrader_core.indicators import Indicators
from project.position_manager import PositionManager


class AdvancedStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Set account type for derivatives trading
        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)

        # Set position manager
        self.set_position_manager(position_manager=PositionManager)

        # Set strategy interval
        self.set_interval(interval=timedelta(seconds=5))

    async def initialize(self) -> None:
        # Add multiple symbols using correct string format
        self.nifty = await self.add_equity(symbol_name=SymbolType.Index.NIFTY)
        self.banknifty = await self.add_equity(symbol_name=SymbolType.Index.BANKNIFTY)

        # Add options for trading
        self.nifty_ce = await self.add_option(
            symbol_name=SymbolType.Index.NIFTY,
            expiry_input=("Weekly", 0),  # Current week
            strike_price_input=0,         # ATM
            option_type="CE"
        )

        # Add charts with different timeframes
        self.nifty_5min = await self.add_chart(
            broker_symbol=self.nifty,
            timeframe=timedelta(minutes=5),
            candle_type=CandleType.REGULAR
        )

        self.banknifty_1min = await self.add_chart(
            broker_symbol=self.banknifty,
            timeframe=timedelta(minutes=1),
            candle_type=CandleType.HEIKEN_ASHI
        )

        # Add indicators to charts
        # IMPORTANT: Create indicator instance first
        self.rsi = Indicators.Momentum.RSI_TV(timeperiod=14)
        # MUST register with chart - this initializes the indicator with historical data
        await self.nifty_5min.add_indicator(self.rsi)

        # Same pattern for all indicators
        self.sma = Indicators.Overlap.SMA_TV(timeperiod=20)
        await self.nifty_5min.add_indicator(self.sma)

    async def next(self) -> None:
        # Check trading hours
        if not self.between_time(time(9, 15), time(15, 30)):
            return

        # Get P&L using correct property names
        unrealized_pnl = self.unrealized_pnl.pnl
        net_pnl = self.net_pnl.pnl

        # Risk management
        if unrealized_pnl < -5000:  # Stop if unrealized loss > 5000
            await self.exit_all_positions()
            return

        # Daily loss limit
        if net_pnl < -10000:  # Stop if daily loss > 10000
            await self.exit_all_positions()
            return

        # Get indicator values
        current_rsi = await self.rsi.get_data(row_number=0, column_name="rsi")
        current_sma = await self.sma.get_data(row_number=0, column_name="sma")
        current_price = self.nifty.ltp

        # Trading logic with indicators
        if self.should_buy(current_rsi, current_sma, current_price):
            await self.buy(
                broker_symbol=self.nifty_ce,
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                quantities=50
            )

    def should_buy(self, rsi: float, sma: float, current_price: float) -> bool:
        """Custom method to determine buy signal using indicators"""
        # RSI oversold and price above SMA
        return (
            rsi < 30 and  # RSI oversold
            current_price > sma and  # Price above SMA
            len(self.positions) == 0  # No open positions
        )
```

## Best Practices

### 1. Error Handling

```python
from logzero import logger
from proalgotrader_core.algorithm import Algorithm

class RobustStrategy(Algorithm):
    async def next(self) -> None:
        try:
            # Your trading logic
            await self.place_trades()
        except Exception as e:
            # Log error and continue
            logger.error(f"Strategy error: {e}")
            # Optionally exit positions
            await self.exit_all_positions()

    async def place_trades(self):
        """Custom method to place trades"""
        # Your trading strategy implementation
        pass
```

### 2. Risk Management

```python
from proalgotrader_core.algorithm import Algorithm

class RiskManagedStrategy(Algorithm):
    async def next(self) -> None:
        # Check daily loss limit
        if self.net_pnl.pnl < -10000:
            logger.warning("Daily loss limit reached")
            await self.exit_all_positions()
            return

        # Check position limits
        if len(self.positions) >= 5:
            return  # Don't open new positions

        # Check unrealized loss limit
        if self.unrealized_pnl.loss >= 5000:
            logger.warning("Unrealized loss limit reached")
            await self.exit_all_positions()
            return
```

### 3. Performance Optimization

```python
from datetime import datetime, timedelta
from proalgotrader_core.algorithm import Algorithm

class OptimizedStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.last_signal_time = None
        self.signal_cooldown = timedelta(minutes=5)

    async def next(self) -> None:
        # Avoid excessive signals
        current_time = self.current_datetime
        if self.is_in_cooldown(current_time):
            return

        # Your trading logic here
        if await self.should_trade():
            await self.place_trades()
            self.set_cooldown(current_time)

    def is_in_cooldown(self, current_time: datetime) -> bool:
        """Check if we're in cooldown period"""
        if self.last_signal_time is None:
            return False
        return current_time - self.last_signal_time < self.signal_cooldown

    def set_cooldown(self, current_time: datetime) -> None:
        """Set cooldown for current signal"""
        self.last_signal_time = current_time

    async def should_trade(self) -> bool:
        """Custom method to determine if we should trade"""
        # Implement your trading conditions
        return len(self.positions) == 0

    async def place_trades(self):
        """Custom method to place trades"""
        # Implement your trading logic
        pass
```

## AccountType Strategy Examples

### Long-term Equity Investment

```python
class LongTermEquityStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Default CASH_POSITIONAL is perfect for long-term equity
        # No need to set explicitly - it's the default
        self.set_interval(interval=timedelta(hours=1))  # Check hourly

    async def initialize(self) -> None:
        # Can only trade equity/stocks with CASH_POSITIONAL
        self.reliance = await self.add_equity(symbol_name=SymbolType.Stock.RELIANCE)
        self.tcs = await self.add_equity(symbol_name=SymbolType.Stock.TCS)

    async def next(self) -> None:
        # Buy and hold strategy - positions held for weeks/months
        if self.should_buy_and_hold():
            await self.buy(
                broker_symbol=self.reliance,
                market_type=MarketType.Cash,      # ✅ Matches CASH_POSITIONAL
                product_type=ProductType.CNC,    # ✅ Matches CASH_POSITIONAL
                order_type=OrderType.MARKET_ORDER,
                quantities=100
            )

    def should_buy_and_hold(self) -> bool:
        """Custom logic for long-term investment signals"""
        return False  # Implement your logic
```

### Intraday Equity Trading

```python
class IntradayEquityStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Set for intraday equity trading
        self.set_account_type(account_type=AccountType.CASH_INTRADAY)
        self.set_interval(interval=timedelta(minutes=1))  # Active monitoring

    async def initialize(self) -> None:
        self.nifty_stocks = [
            await self.add_equity(symbol_name=SymbolType.Stock.RELIANCE),
            await self.add_equity(symbol_name=SymbolType.Stock.TCS),
            await self.add_equity(symbol_name=SymbolType.Stock.INFY)
        ]

    async def next(self) -> None:
        # All positions automatically squared off by 3:20 PM
        for stock in self.nifty_stocks:
            if self.should_buy_intraday(stock):
                await self.buy(
                    broker_symbol=stock,
                    market_type=MarketType.Cash,   # ✅ Matches CASH_INTRADAY
                    product_type=ProductType.MIS, # ✅ Matches CASH_INTRADAY
                    order_type=OrderType.MARKET_ORDER,
                    quantities=100
                )

    def should_buy_intraday(self, stock) -> bool:
        """Custom logic for intraday signals"""
        return False  # Implement your logic
```

### Intraday Options Strategy

```python
class IntradayOptionsStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Set for intraday options trading
        self.set_account_type(account_type=AccountType.DERIVATIVE_INTRADAY)
        self.set_interval(interval=timedelta(seconds=30))  # High frequency

    async def initialize(self) -> None:
        # Can trade options with DERIVATIVE account types
        self.nifty_ce = await self.add_option(
            symbol_name=SymbolType.Index.NIFTY,
            expiry_input=("Weekly", 0),
            strike_price_input=0,  # ATM
            option_type="CE"
        )

    async def next(self) -> None:
        # Quick options buying/selling - auto squared off by 3:20 PM
        if self.should_buy_options():
            await self.buy(
                broker_symbol=self.nifty_ce,
                market_type=MarketType.Derivative,  # ✅ Matches DERIVATIVE_INTRADAY
                product_type=ProductType.MIS,       # ✅ Matches DERIVATIVE_INTRADAY
                order_type=OrderType.MARKET_ORDER,
                quantities=50  # NIFTY lot size
            )

    def should_buy_options(self) -> bool:
        """Custom logic for options signals"""
        return False  # Implement your logic
```

### Options Selling Strategy

```python
class OptionsSellingStrategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Set for positional options trading
        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)
        self.set_interval(interval=timedelta(minutes=15))  # Monitor regularly

    async def initialize(self) -> None:
        # Set up options for selling strategies
        self.nifty_ce_otm = await self.add_option(
            symbol_name=SymbolType.Index.NIFTY,
            expiry_input=("Weekly", 0),
            strike_price_input=2,  # 2 strikes OTM
            option_type="CE"
        )
        self.nifty_pe_otm = await self.add_option(
            symbol_name=SymbolType.Index.NIFTY,
            expiry_input=("Weekly", 0),
            strike_price_input=-2,  # 2 strikes OTM
            option_type="PE"
        )

    async def next(self) -> None:
        # Can hold short options positions for multiple days
        if self.should_sell_straddle():
            # Sell CE
            await self.sell(
                broker_symbol=self.nifty_ce_otm,
                market_type=MarketType.Derivative,   # ✅ Matches DERIVATIVE_POSITIONAL
                product_type=ProductType.NRML,       # ✅ Matches DERIVATIVE_POSITIONAL
                order_type=OrderType.MARKET_ORDER,
                quantities=50
            )
            # Sell PE
            await self.sell(
                broker_symbol=self.nifty_pe_otm,
                market_type=MarketType.Derivative,   # ✅ Matches DERIVATIVE_POSITIONAL
                product_type=ProductType.NRML,       # ✅ Matches DERIVATIVE_POSITIONAL
                order_type=OrderType.MARKET_ORDER,
                quantities=50
            )

    def should_sell_straddle(self) -> bool:
        """Custom logic for options selling signals"""
        return False  # Implement your logic
```

## Common Patterns

### Multi-Timeframe Analysis

```python
from datetime import timedelta
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.enums.symbol_type import SymbolType
from proalgotrader_core.enums.market_type import MarketType
from proalgotrader_core.enums.order_type import OrderType
from proalgotrader_core.enums.product_type import ProductType
from proalgotrader_core.indicators import Indicators

class MultiTimeframeStrategy(Algorithm):
    async def initialize(self) -> None:
        self.symbol = await self.add_equity(symbol_name=SymbolType.Index.NIFTY)

        # Multiple timeframes
        self.chart_1min = await self.add_chart(
            broker_symbol=self.symbol,
            timeframe=timedelta(minutes=1)
        )
        self.chart_5min = await self.add_chart(
            broker_symbol=self.symbol,
            timeframe=timedelta(minutes=5)
        )
        self.chart_15min = await self.add_chart(
            broker_symbol=self.symbol,
            timeframe=timedelta(minutes=15)
        )

        # Add indicators to different timeframes
        self.sma_1min = Indicators.Overlap.SMA_TV(timeperiod=20)
        await self.chart_1min.add_indicator(self.sma_1min)

        self.sma_5min = Indicators.Overlap.SMA_TV(timeperiod=20)
        await self.chart_5min.add_indicator(self.sma_5min)

        self.sma_15min = Indicators.Overlap.SMA_TV(timeperiod=20)
        await self.chart_15min.add_indicator(self.sma_15min)

    async def next(self) -> None:
        # Analyze multiple timeframes using indicators
        trend_1min = await self.get_trend(self.sma_1min)
        trend_5min = await self.get_trend(self.sma_5min)
        trend_15min = await self.get_trend(self.sma_15min)

        # Only trade when all timeframes align
        if trend_1min == "UP" and trend_5min == "UP" and trend_15min == "UP":
            if len(self.positions) == 0:  # No existing positions
                await self.buy(
                    broker_symbol=self.symbol,
                    market_type=MarketType.Cash,
                    product_type=ProductType.CNC,
                    order_type=OrderType.MARKET_ORDER,
                    quantities=100
                )

    async def get_trend(self, sma_indicator) -> str:
        """Determine trend direction based on SMA"""
        try:
            current_sma = await sma_indicator.get_data(row_number=0, column_name="sma")
            current_price = self.symbol.ltp

            return "UP" if current_price > current_sma else "DOWN"
        except:
            return "NEUTRAL"
```

### Options Trading

```python
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.enums.symbol_type import SymbolType
from proalgotrader_core.enums.market_type import MarketType
from proalgotrader_core.enums.order_type import OrderType
from proalgotrader_core.enums.product_type import ProductType
from proalgotrader_core.indicators import Indicators

class OptionsStrategy(Algorithm):
    async def initialize(self) -> None:
        # Add underlying
        self.nifty = await self.add_equity(symbol_name=SymbolType.Index.NIFTY)

        # Add options
        self.ce_option = await self.add_option(
            symbol_name=SymbolType.Index.NIFTY,
            expiry_input=("Weekly", 0),  # 0 = current week, 1 = next week
            strike_price_input=0,         # 0 = ATM, 1 = OTM, -1 = ITM
            option_type="CE"
        )
        self.pe_option = await self.add_option(
            symbol_name=SymbolType.Index.NIFTY,
            expiry_input=("Weekly", 0),  # 0 = current week, 1 = next week
            strike_price_input=0,         # 0 = ATM, 1 = OTM, -1 = ITM
            option_type="PE"
        )

        # Add chart and indicators for underlying
        self.nifty_chart = await self.add_chart(
            broker_symbol=self.nifty,
            timeframe=timedelta(minutes=5)
        )

        self.rsi = Indicators.Momentum.RSI_TV(timeperiod=14)
        await self.nifty_chart.add_indicator(self.rsi)

    async def next(self) -> None:
        # Options trading logic with indicators
        if await self.should_buy_call():
            await self.buy(
                broker_symbol=self.ce_option,
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                quantities=50  # Options lot size (NIFTY lot size is 50)
            )
        elif await self.should_buy_put():
            await self.buy(
                broker_symbol=self.pe_option,
                market_type=MarketType.Derivative,
                product_type=ProductType.NRML,
                order_type=OrderType.MARKET_ORDER,
                quantities=50
            )

    async def should_buy_call(self) -> bool:
        """Determine call option buy signal using RSI"""
        try:
            if len(self.positions) > 0:
                return False  # Already have positions

            rsi_value = await self.rsi.get_data(row_number=0, column_name="rsi")
            return rsi_value < 30  # Oversold, expect upward move
        except:
            return False

    async def should_buy_put(self) -> bool:
        """Determine put option buy signal using RSI"""
        try:
            if len(self.positions) > 0:
                return False  # Already have positions

            rsi_value = await self.rsi.get_data(row_number=0, column_name="rsi")
            return rsi_value > 70  # Overbought, expect downward move
        except:
            return False
```

### Using Indicators

Indicators in ProAlgoTrader Core follow a **two-step process**:

1. **Create**: Create the indicator instance with desired parameters
2. **Register**: Add the indicator to a chart to initialize it with data

⚠️ **Important**: Until an indicator is registered with `chart.add_indicator()`, it has no data and cannot be used for analysis.

```python
from datetime import timedelta
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.enums.symbol_type import SymbolType
from proalgotrader_core.enums.candle_type import CandleType
from proalgotrader_core.enums.market_type import MarketType
from proalgotrader_core.enums.order_type import OrderType
from proalgotrader_core.enums.product_type import ProductType
from proalgotrader_core.indicators import Indicators

class IndicatorStrategy(Algorithm):
    async def initialize(self) -> None:
        # Add symbol and chart
        self.symbol = await self.add_equity(symbol_name=SymbolType.Stock.RELIANCE)
        self.chart = await self.add_chart(
            broker_symbol=self.symbol,
            timeframe=timedelta(minutes=5),
            candle_type=CandleType.REGULAR
        )

        # STEP 1: Create indicator instances (not usable yet)
        self.rsi = Indicators.Momentum.RSI_TV(timeperiod=14)
        self.macd = Indicators.Momentum.MACD_TV(fastperiod=12, slowperiod=26, signalperiod=9)
        self.sma = Indicators.Overlap.SMA_TV(timeperiod=20)
        self.ema = Indicators.Overlap.EMA_TV(timeperiod=20)
        self.bbands = Indicators.Overlap.BBANDS_TV(timeperiod=20, nbdevup=2, nbdevdn=2)
        self.atr = Indicators.Volatility.ATR_TV(timeperiod=14)

        # STEP 2: Register indicators with chart (now they become usable)
        # This initializes them with historical data and enables tick-by-tick updates
        await self.chart.add_indicator(self.rsi)
        await self.chart.add_indicator(self.macd)
        await self.chart.add_indicator(self.sma)
        await self.chart.add_indicator(self.ema)
        await self.chart.add_indicator(self.bbands)
        await self.chart.add_indicator(self.atr)

        # Alternative: You can also do both steps in one line
        # self.supertrend = await self.chart.add_indicator(
        #     Indicators.Trend.Supertrend(period=10, multiplier=3.0)
        # )

    async def next(self) -> None:
        try:
            # Get current indicator values
            rsi_value = await self.rsi.get_data(row_number=0, column_name="rsi")
            macd_line = await self.macd.get_data(row_number=0, column_name="macd")
            macd_signal = await self.macd.get_data(row_number=0, column_name="macdsignal")
            sma_value = await self.sma.get_data(row_number=0, column_name="sma")
            ema_value = await self.ema.get_data(row_number=0, column_name="ema")
            bb_upper = await self.bbands.get_data(row_number=0, column_name="upperband")
            bb_lower = await self.bbands.get_data(row_number=0, column_name="lowerband")
            atr_value = await self.atr.get_data(row_number=0, column_name="atr")

            current_price = self.symbol.ltp

            # Trading logic using multiple indicators
            bullish_signal = (
                rsi_value < 30 and  # RSI oversold
                macd_line > macd_signal and  # MACD bullish crossover
                current_price > ema_value and  # Price above EMA
                current_price <= bb_lower  # Price at lower Bollinger Band
            )

            if bullish_signal and len(self.positions) == 0:
                await self.buy(
                    broker_symbol=self.symbol,
                    market_type=MarketType.Cash,
                    product_type=ProductType.CNC,
                    order_type=OrderType.MARKET_ORDER,
                    quantities=100
                )

        except Exception as e:
            # Handle indicator data not available yet
            pass
```

### Custom Indicator Usage

```python
from datetime import timedelta
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.enums.symbol_type import SymbolType
from proalgotrader_core.enums.market_type import MarketType
from proalgotrader_core.enums.order_type import OrderType
from proalgotrader_core.enums.product_type import ProductType
from proalgotrader_core.indicators import CustomIndicator
import polars_talib as pta
import polars as pl

class MyCustomRSI(CustomIndicator):
    def __init__(self, timeperiod: int = 14):
        super().__init__()
        self.timeperiod = timeperiod

    def build(self) -> pl.Expr:
        return pta.rsi(pl.col("close"), timeperiod=self.timeperiod).alias("custom_rsi")

    def window_size(self) -> int:
        return self.timeperiod

class CustomIndicatorStrategy(Algorithm):
    async def initialize(self) -> None:
        self.symbol = await self.add_equity(symbol_name=SymbolType.Stock.TCS)
        self.chart = await self.add_chart(
            broker_symbol=self.symbol,
            timeframe=timedelta(minutes=5)
        )

        # STEP 1: Create custom indicator instance
        self.custom_rsi = MyCustomRSI(timeperiod=21)

        # STEP 2: Register with chart (critical for initialization)
        await self.chart.add_indicator(self.custom_rsi)

    async def next(self) -> None:
        try:
            rsi_value = await self.custom_rsi.get_data(row_number=0, column_name="custom_rsi")

            if rsi_value < 25 and len(self.positions) == 0:
                await self.buy(
                    broker_symbol=self.symbol,
                    market_type=MarketType.Cash,
                    product_type=ProductType.CNC,
                    order_type=OrderType.MARKET_ORDER,
                    quantities=50
                )
        except:
            pass
```

## Indicator Lifecycle and Best Practices

### Understanding Indicator Registration

The indicator system works in two distinct phases:

```python
# ❌ WRONG: This indicator is created but NOT usable
self.rsi = Indicators.Momentum.RSI_TV(timeperiod=14)
# At this point, self.rsi has no data and calling get_data() will fail

# ✅ CORRECT: Register the indicator to make it usable
await self.chart.add_indicator(self.rsi)
# Now self.rsi is initialized with historical data and will update on every tick
```

### What happens during `add_indicator()`?

1. **Historical Data Initialization**: The indicator processes all existing chart data
2. **Data Structure Setup**: Internal data storage is configured
3. **Tick Updates Enabled**: The indicator will now update with each new price tick
4. **Return Value**: `add_indicator()` returns the same indicator instance

### Indicator Data Access

Indicators expose the same data access methods as charts:

**Data Property** - Get full DataFrame:

```python
# Get full indicator DataFrame
indicator_data = self.rsi.data
print(indicator_data)

# Access specific indicator columns
rsi_values = self.rsi.data.select("rsi")
print(rsi_values)
```

**Get Data Method** - Get specific values:

```python
# Get current RSI value (row 0 = most recent)
current_rsi = await self.rsi.get_data(0, "rsi")
print(f"Current RSI: {current_rsi}")

# Get previous RSI value (row 1 = previous value)
previous_rsi = await self.rsi.get_data(1, "rsi")
print(f"Previous RSI: {previous_rsi}")

# Get current indicator data as Series
current_data = await self.rsi.get_data(0)
print(current_data)
```

**Common Usage Patterns:**

```python
async def analyze_rsi(self):
    # Get RSI values
    current_rsi = await self.rsi.get_data(0, "rsi")
    previous_rsi = await self.rsi.get_data(1, "rsi")

    # Check for RSI signals
    if current_rsi > 70 and previous_rsi <= 70:
        print("RSI crossed above 70 - Overbought signal")
    elif current_rsi < 30 and previous_rsi >= 30:
        print("RSI crossed below 30 - Oversold signal")
```

### Common Patterns

```python
class IndicatorLifecycleExample(Algorithm):
    async def initialize(self) -> None:
        self.chart = await self.add_chart(
            broker_symbol=await self.add_equity(symbol_name=SymbolType.Stock.TCS),
            timeframe=timedelta(minutes=5)
        )

        # Pattern 1: Two-step approach (recommended for multiple indicators)
        self.rsi = Indicators.Momentum.RSI_TV(timeperiod=14)
        self.sma = Indicators.Overlap.SMA_TV(timeperiod=20)

        await self.chart.add_indicator(self.rsi)
        await self.chart.add_indicator(self.sma)

        # Pattern 2: One-line approach (good for single indicators)
        self.macd = await self.chart.add_indicator(
            Indicators.Momentum.MACD_TV(fastperiod=12, slowperiod=26, signalperiod=9)
        )

    async def next(self) -> None:
        # All indicators are now ready to use
        rsi_val = await self.rsi.get_data(row_number=0, column_name="rsi")
        sma_val = await self.sma.get_data(row_number=0, column_name="sma")
        macd_val = await self.macd.get_data(row_number=0, column_name="macd")
```

### Common Mistakes to Avoid

```python
# ❌ DON'T: Try to use indicator before registration
class BadExample(Algorithm):
    async def initialize(self) -> None:
        self.rsi = Indicators.Momentum.RSI_TV(timeperiod=14)
        # This will fail - indicator has no data yet!
        rsi_value = await self.rsi.get_data(row_number=0, column_name="rsi")

# ✅ DO: Always register first, then use
class GoodExample(Algorithm):
    async def initialize(self) -> None:
        self.chart = await self.add_chart(...)
        self.rsi = Indicators.Momentum.RSI_TV(timeperiod=14)
        await self.chart.add_indicator(self.rsi)

        # Now it's safe to use in next() method

    async def next(self) -> None:
        rsi_value = await self.rsi.get_data(row_number=0, column_name="rsi")
```

## Troubleshooting

### Common Issues

1. **Algorithm not starting**

   - Check broker credentials in environment variables
   - Verify market hours
   - Check network connectivity

2. **Orders not executing**

   - Verify symbol is tradeable (`broker_symbol.can_trade`)
   - Check account type and position type compatibility
   - Ensure quantities match lot size

3. **Charts not updating**

   - Verify symbol is added correctly
   - Check timeframe settings
   - Ensure market data subscription is active

4. **Indicators not working**

   - Ensure `await chart.add_indicator(indicator)` was called
   - Check if indicator has sufficient historical data
   - Verify correct column names when calling `get_data()`
   - Use try-except blocks in `next()` for indicator data access

5. **Strategy running too frequently/slowly**

   - Check `self.set_interval()` setting in `__init__()`
   - Match interval to your strategy's signal frequency
   - For swing trading, use `timedelta(hours=1)` instead of default `timedelta(seconds=1)`
   - Monitor CPU usage - very short intervals may impact performance

6. **Logic not executing**
   - Ensure trading logic is in `next()` method, not `__init__()` or `initialize()`
   - Check if market hours validation is blocking execution
   - Verify `next()` method is async: `async def next(self) -> None:`

### Debug Information

```python
# Check current state
print(f"Current time: {algorithm.current_time}")
print(f"Open positions: {len(algorithm.positions)}")
print(f"Unrealized P&L: {algorithm.unrealized_pnl.pnl}")
print(f"Net P&L: {algorithm.net_pnl.pnl}")

# Check symbol status
print(f"Symbol tradeable: {equity_symbol.can_trade}")
print(f"Current LTP: {equity_symbol.ltp}")

# Check position details
for position in algorithm.positions:
    print(f"Position: {position.symbol_name} | Qty: {position.quantity} | P&L: {position.pnl}")

# Check order status
for order in algorithm.orders:
    print(f"Order: {order.symbol_name} | Status: {order.status} | Qty: {order.quantity}")
```

## Quick Reference

### Algorithm Lifecycle Cheat Sheet

```python
class MyStrategy(Algorithm):
    def __init__(self, *args, **kwargs):
        # 🔧 SETUP: Called once during class instantiation
        super().__init__(*args, **kwargs)
        self.set_account_type(...)        # ✅ Do this here
        self.set_position_manager(...)    # ✅ Do this here
        self.set_interval(...)            # ✅ Do this here

    async def initialize(self):
        # 🏗️ PREPARATION: Called once after market opens
        self.symbol = await self.add_equity(...)     # ✅ Do this here
        self.chart = await self.add_chart(...)       # ✅ Do this here
        self.rsi = await self.chart.add_indicator(...) # ✅ Do this here

    async def next(self):
        # 🔄 EXECUTION: Called repeatedly at set interval
        # ✅ Trading logic goes here
        # ✅ Position monitoring goes here
        # ✅ Risk management goes here
```

### Interval Guidelines

| Strategy Type    | Recommended Interval     | Use Case             |
| ---------------- | ------------------------ | -------------------- |
| Scalping         | `timedelta(seconds=1-5)` | Quick entries/exits  |
| Day Trading      | `timedelta(minutes=1-5)` | Intraday momentum    |
| Swing Trading    | `timedelta(hours=1-4)`   | Daily/weekly signals |
| Position Trading | `timedelta(hours=6-24)`  | Long-term holds      |

### Common Mistakes

❌ **Don't put trading logic in `__init__()` or `initialize()`**

```python
def __init__(self):
    # ❌ WRONG: This runs before market opens
    if some_condition:
        self.buy(...)  # This will fail!
```

✅ **Do put trading logic in `next()`**

```python
async def next(self):
    # ✅ CORRECT: This runs during market hours
    if some_condition:
        await self.buy(...)
```

## Next Steps

- **Indicators**: Learn about [Built-in Indicators](../indicators/built-in-indicators.md)
- **Custom Indicators**: Create [Custom Indicators](../indicators/custom-indicators-guide.md)
- **Broker Integration**: Understand [Broker Setup](../brokers/)
- **Examples**: See [Strategy Examples](../examples/)

---

**Need help?** Check our [API Reference](../api-reference/) or [Contact Support](../support/contact.md).
