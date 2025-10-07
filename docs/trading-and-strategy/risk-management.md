# Risk Management

## Automatic Risk Reward Management

ProAlgoTrader provides built-in risk management through multiple methods that automatically set stop-loss and target orders when positions are opened.

### Quick Start with Risk Management

```python
class MyStrategy(Algorithm):
    async def on_position_open(self, position):
        # Set risk-reward using create_risk_reward method
        from proalgotrader_core.risk_reward import Stoploss, Target
        from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

        # For equity trading with percentages
        await self.create_risk_reward(
            position=position,
            stoploss=Stoploss(value=2.0),  # 2% stop loss
            target=Target(value=4.0),      # 4% target
            unit=RiskRewardUnit.PERCENTAGE,
        )

        # Or for derivatives with points
        await self.create_risk_reward(
            position=position,
            stoploss=Stoploss(value=50),   # 50 points stop loss
            target=Target(value=100),      # 100 points target
            unit=RiskRewardUnit.POINTS,
        )
```

### Advanced Usage with create_risk_reward Method

```python
from proalgotrader_core.risk_reward import Stoploss, Target
from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

class MyStrategy(Algorithm):
    async def on_position_open(self, position):
        # Advanced configuration with create_risk_reward method
        await self.create_risk_reward(
            position=position,
            stoploss=Stoploss(value=50),  # 50 points stop-loss
            target=Target(value=100),     # 100 points target
            unit=RiskRewardUnit.POINTS
        )
```

### Risk Reward Methods

#### Percentage-based Risk Management (Recommended for Equity)

```python
from proalgotrader_core.risk_reward import RiskReward, Stoploss, Target
from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

# Simple percentage-based risk management
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=2.0),  # 2% stop loss
    target=Target(value=4.0),      # 4% target
    unit=RiskRewardUnit.PERCENTAGE,
)

# With trailing stop
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=2.0, trailing_value=1.0),  # 2% stop loss with 1% trailing
    target=Target(value=4.0, trailing_value=2.0),      # 4% target with 2% trailing
    unit=RiskRewardUnit.PERCENTAGE,
)

# Stop loss only
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=1.5),  # 1.5% stop loss
    unit=RiskRewardUnit.PERCENTAGE,
)
```

#### Points-based Risk Management (Recommended for Derivatives)

```python
from proalgotrader_core.risk_reward import RiskReward, Stoploss, Target
from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

# Simple points-based risk management
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=30),   # 30 points stop loss
    target=Target(value=60),       # 60 points target
    unit=RiskRewardUnit.POINTS,
)

# With trailing stop
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=30, trailing_value=15),   # 30 points stop loss with 15 points trailing
    target=Target(value=60, trailing_value=30),       # 60 points target with 30 points trailing
    unit=RiskRewardUnit.POINTS,
)

# Stop loss only
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=25),   # 25 points stop loss
    unit=RiskRewardUnit.POINTS,
)
```

#### Advanced Configuration with create_risk_reward Method

```python
# For derivatives (futures, options)
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=30),  # 30 points stop-loss
    target=Target(value=60),      # 60 points target
    unit=RiskRewardUnit.POINTS
)

# For equity trading
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=2.0),  # 2% stop-loss
    target=Target(value=4.0),      # 4% target
    unit=RiskRewardUnit.PERCENTAGE
)
```

### Advanced Features

#### RiskRewardManager Class

The `RiskRewardManager` class provides advanced risk management capabilities including trailing stop-loss and target monitoring.

```python
from proalgotrader_core.risk_reward import RiskRewardManager
from proalgotrader_core.protocols.order import OrderProtocol

# Create a risk reward manager for advanced monitoring
risk_manager = RiskRewardManager(
    stoploss_order=stoploss_order,           # OrderProtocol for stoploss
    stoploss_trailing_price=trailing_price,  # Price to trail stoploss
    target_order=target_order,               # OrderProtocol for target (optional)
    target_trailing_price=target_trailing,   # Price to trail target (optional)
    on_trail_callback=trail_callback         # Callback function for trailing events
)

# Monitor trailing in your strategy
await risk_manager.monitor_trailing()
```

**Key Features:**

- **Trailing Stop-loss**: Automatically adjusts stop-loss as price moves favorably
- **Trailing Target**: Automatically adjusts target as price moves favorably
- **Custom Callbacks**: Define custom behavior when trailing occurs
- **Order Management**: Manages both stop-loss and target orders

#### Trailing Stop-loss

```python
# Trailing stop-loss with 10 points trail
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=50, trailing_value=10),
    target=Target(value=100),
    unit=RiskRewardUnit.POINTS
)
```

#### Stop-loss Only

```python
# Only set stop-loss without target
await self.create_risk_reward(
    position=position,
    stoploss=Stoploss(value=25),
    unit=RiskRewardUnit.POINTS
)
```

### Complete Strategy Example

```python
from datetime import timedelta
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.risk_reward import Stoploss, Target
from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

class RiskManagedStrategy(Algorithm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_interval(interval=timedelta(seconds=1))

    async def on_position_open(self, position):
        # Different risk management based on position type
        if position.position_type == "BUY":
            # Use create_risk_reward method for easier configuration
            await self.create_risk_reward(
                position=position,
                stoploss=Stoploss(value=40),  # 40 points stop loss
                target=Target(value=80),      # 80 points target
                unit=RiskRewardUnit.POINTS
            )
        else:  # SELL position
            await self.create_risk_reward(
                position=position,
                stoploss=Stoploss(value=35),  # 35 points stop loss
                target=Target(value=70),      # 70 points target
                unit=RiskRewardUnit.POINTS
            )

    async def next(self):
        # Your trading logic here
        pass
```

### Strategy Integration

The Algorithm class provides position event methods that you can override in your strategy:

```python
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.protocols.position import PositionProtocol

class Strategy(Algorithm):
    async def on_position_open(self, position: PositionProtocol) -> None:
        """Called when a position is opened - override this method in your strategy."""
        print(f"Position opened: {position.broker_symbol.symbol_name}")

        # Set risk-reward in the strategy (not in position manager)
        from proalgotrader_core.risk_reward import RiskReward, Stoploss, Target
        from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

        await self.create_risk_reward(
            position=position,
            stoploss=Stoploss(value=2.0, trailing_value=1.0),  # 2% stop loss with 1% trailing
            target=Target(value=4.0, trailing_value=2.0),      # 4% target with 2% trailing
            unit=RiskRewardUnit.PERCENTAGE,
        )

    async def on_position_closed(self, position: PositionProtocol) -> None:
        """Called when a position is closed - override this method in your strategy."""
        print(f"Position closed: {position.broker_symbol.symbol_name} | P&L: {position.pnl.profit}")

    async def next(self) -> None:
        # Your trading logic here
        pass
```

**Note**: These methods have default empty implementations in the Algorithm class, so you only need to override them if you want to handle position events.

### Best Practices

1. **Always set stop-loss**: Never trade without risk management
2. **Use RiskReward objects**: Create RiskReward objects with appropriate Stoploss and Target configurations
3. **Use appropriate units**: Points for derivatives, percentage for equity
4. **Set realistic targets**: Aim for 1:2 or better risk-reward ratio
5. **Test thoroughly**: Use paper trading to validate risk parameters
6. **Monitor positions**: Check that risk management is working correctly
7. **Use trailing stops**: Enable trailing stops for better profit protection

### Method Comparison

| Method                 | Use Case            | Complexity | Flexibility |
| ---------------------- | ------------------- | ---------- | ----------- |
| `create_risk_reward()` | All risk management | Medium     | High        |

### Parameters Reference

#### RiskReward Object

- **position**: The position object from `on_position_open` callback
- **stoploss**: `Stoploss` object with value and optional trailing_value
- **target**: `Target` object (optional) with value and optional trailing_value
- **unit**: `RiskRewardUnit.POINTS` or `RiskRewardUnit.PERCENTAGE`

### Troubleshooting

**Risk reward not set**: Ensure you're calling `create_risk_reward` in the `on_position_open` method.

**Orders not placed**: Check that your broker supports stop-loss and target orders.

**Incorrect values**: Verify the unit type matches your trading instrument.
