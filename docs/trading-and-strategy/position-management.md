# Position Management

Position management in ProAlgoTrader allows you to implement sophisticated risk management and position handling strategies. The framework supports two types of position managers:

- **Single Position Manager** (`PositionManagerProtocol`) - Manages all positions globally
- **Multiple Position Manager** (`MultiplePositionManagerProtocol`) - Manages each position individually

## Position Manager Types

### Single Position Manager

A single position manager handles all positions in your strategy with a global perspective. This is useful when you want to implement portfolio-level risk management.

**Key Characteristics:**

- One instance manages all positions
- Global view of all positions
- Ideal for portfolio-level risk management
- Created once when the algorithm starts

### Multiple Position Manager

A multiple position manager creates a separate instance for each individual position. This allows for position-specific management logic.

**Key Characteristics:**

- One instance per position
- Position-specific management logic
- Ideal for individual position strategies
- Created dynamically when positions are opened

## Setting Up Position Managers

### Basic Setup

```python
# project/strategy.py
from proalgotrader_core.algorithm import Algorithm
from project.position_manager import PositionManager

class Strategy(Algorithm):
    async def initialize(self) -> None:
        # Set up single position manager
        self.set_position_manager(position_manager_class=PositionManager)

        # Your strategy initialization code here
        pass

    async def next(self) -> None:
        # Your strategy logic here
        pass
```

### Position Manager Implementation

#### Single Position Manager Example

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
        self.max_positions = 5

    async def initialize(self) -> None:
        """Initialize the position manager."""
        # Set exit time 30 minutes after strategy starts
        self.exit_time = datetime.now().replace(microsecond=0) + timedelta(minutes=30)
        print("Position manager initialized")


    async def next(self) -> None:
        """Called on every algorithm iteration."""
        # Time-based exit strategy
        if self.exit_time and self.exit_time <= self.algorithm.current_datetime:
            print("Time-based exit: Closing all positions")
            await self.algorithm.exit_all_positions()
            return

        # Portfolio-level risk management
        if self.algorithm.unrealized_pnl.profit >= 2000:
            print("Profit target reached: Closing all positions")
            await self.algorithm.exit_all_positions()
        elif self.algorithm.unrealized_pnl.loss >= 1000:
            print("Stop loss triggered: Closing all positions")
            await self.algorithm.exit_all_positions()

        # Position limit management
        if len(self.algorithm.positions) >= self.max_positions:
            print(f"Maximum positions ({self.max_positions}) reached")
```

#### Multiple Position Manager Example

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
        self.max_hold_time = timedelta(minutes=15)

    async def initialize(self) -> None:
        """Initialize the position manager for this specific position."""
        self.entry_time = datetime.now()
        print(f"Position manager initialized for {self.position.broker_symbol.symbol_name}")


    async def next(self) -> None:
        """Called on every algorithm iteration for this position."""
        # Position-specific time-based exit
        if self.entry_time and datetime.now() - self.entry_time >= self.max_hold_time:
            print(f"Time limit reached for {self.position.broker_symbol.symbol_name}")
            await self.position.exit()
            return

        # Position-specific profit/loss management
        if self.position.pnl.profit >= 500:
            print(f"Position profit target reached: {self.position.broker_symbol.symbol_name}")
            await self.position.exit()
        elif self.position.pnl.loss >= 250:
            print(f"Position stop loss triggered: {self.position.broker_symbol.symbol_name}")
            await self.position.exit()
```

## Position Manager Lifecycle

### Single Position Manager

1. **Initialization**: Created once when `set_position_manager()` is called
2. **Management Logic**: `next()` is called on every algorithm iteration for position management
3. **Execution**: `next()` is called on every algorithm iteration
4. **Scope**: Manages all positions globally

### Multiple Position Manager

1. **Initialization**: Created for each individual position when the position is opened
2. **Management Logic**: `next()` is called on every algorithm iteration for this specific position
3. **Execution**: `next()` is called on every algorithm iteration for each position
4. **Scope**: Manages individual positions independently

## Key Methods

### PositionManagerProtocol Methods

- `__init__(algorithm: AlgorithmProtocol)` - Initialize with algorithm reference
- `async initialize()` - Called once during setup
- `async next()` - Called on every algorithm iteration

### MultiplePositionManagerProtocol Methods

- `__init__(algorithm: AlgorithmProtocol, position: PositionProtocol)` - Initialize with algorithm and specific position
- `async initialize()` - Called once during setup for this position
- `async next()` - Called on every algorithm iteration for this position

## Best Practices

### Single Position Manager Use Cases

- Portfolio-level risk management
- Global position limits
- Market-wide exit strategies
- Overall P&L management

### Multiple Position Manager Use Cases

- Position-specific strategies
- Individual position risk management
- Position-specific time limits
- Custom exit logic per position

### General Guidelines

1. **Choose the Right Type**: Use single for global management, multiple for position-specific logic
2. **Implement All Methods**: Always implement all required methods, even if empty
3. **Handle Errors**: Add proper error handling in your position management logic
4. **Use Risk-Reward**: Leverage the built-in risk-reward system for stop-loss and targets
5. **Monitor Performance**: Log important events for debugging and monitoring

## Separation of Concerns

Position managers focus on position management logic, while position events and risk-reward management are handled in the strategy:

- **Position Managers**: Handle position lifecycle, portfolio management, and position-specific logic
- **Strategy**: Handles position events (`on_position_open`, `on_position_closed`), risk-reward setting, signal generation, and trading decisions

### Position Event Methods in Strategy

The Algorithm class provides two position event methods that you can override in your strategy:

- `async on_position_open(position: PositionProtocol)` - Called when a position is opened
- `async on_position_closed(position: PositionProtocol)` - Called when a position is closed

These methods have default empty implementations, so you only need to override them if you want to handle position events.

## Example: Complete Strategy with Position Management

```python
# project/strategy.py
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.protocols.position import PositionProtocol
from project.position_manager import PositionManager

class Strategy(Algorithm):
    async def initialize(self) -> None:
        # Set up position manager
        self.set_position_manager(position_manager_class=PositionManager)

        # Add your symbols and indicators
        await self.add_chart("NIFTY", "1m")
        await self.add_chart("BANKNIFTY", "1m")

    async def on_position_open(self, position: PositionProtocol) -> None:
        """Called when a position is opened - override this method in your strategy."""
        print(f"Position opened: {position.broker_symbol.symbol_name} | Qty: {position.net_quantities}")

        # Set risk-reward in the strategy (not in position manager)
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

    async def next(self) -> None:
        # Your trading logic here
        # Position management is handled automatically by the position manager
        pass
```

This comprehensive position management system gives you the flexibility to implement both global and position-specific management strategies, while keeping risk-reward management in the strategy layer for better separation of concerns.
