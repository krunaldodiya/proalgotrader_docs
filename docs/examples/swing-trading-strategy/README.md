# Swing Trading Strategy Example

This example demonstrates a comprehensive swing trading strategy using the Golden Crossover signal (50-day SMA crossing above 200-day SMA) for long-term trend following.

## Files

- `main.py` - Entry point to run the strategy
- `strategy.py` - Main swing trading strategy implementation
- `signal_manager.py` - Golden crossover signal detection
- `position_manager.py` - Position manager for swing trades
- `README.md` - This documentation

## Strategy Logic

- **Golden Crossover**: 50-day SMA crosses above 200-day SMA → **BUY** signal
- **Death Cross**: 50-day SMA crosses below 200-day SMA → **SELL** signal
- **Position Management**: Hold positions for days/weeks (swing trading)
- **Risk Management**: Stop loss and take profit levels

## Key Features

- ✅ **Daily Timeframe**: Uses daily candles for proper moving average calculation
- ✅ **Golden Crossover Detection**: 50-day vs 200-day SMA crossover signals
- ✅ **Swing Trading**: Holds positions for extended periods
- ✅ **Multiple Symbols**: Can trade multiple stocks simultaneously
- ✅ **Risk Management**: Built-in stop loss and position sizing
- ✅ **Signal Manager**: Modular signal detection system

## Strategy Components

### Signal Manager (`signal_manager.py`)

- Detects golden crossover and death cross signals
- Uses daily candles for accurate moving average calculation
- Provides clear signal output with SMA values

### Position Manager (`position_manager.py`)

- Manages swing trade positions
- Implements stop loss and take profit
- Tracks position performance over time

### Main Strategy (`strategy.py`)

- Orchestrates the entire swing trading system
- Manages multiple symbols
- Coordinates between signal detection and position management

## Usage

```bash
python main.py
```

The strategy will automatically:

- Connect to your broker
- Subscribe to market data for selected symbols
- Calculate 50-day and 200-day SMA indicators
- Detect golden crossover signals
- Execute swing trades
- Manage positions with risk controls

## Configuration

### Symbol Selection

```python
# Add your preferred swing trading symbols
symbols = [
    "RELIANCE-EQ",
    "TCS-EQ",
    "HDFCBANK-EQ",
    "INFY-EQ",
    "BHARTIARTL-EQ"
]
```

### Risk Management

```python
# Position sizing (percentage of capital)
position_size = 0.1  # 10% of capital per trade

# Stop loss and take profit
stop_loss_pct = 0.08   # 8% stop loss
take_profit_pct = 0.20 # 20% take profit
```

## Golden Crossover Explained

The Golden Crossover is one of the most reliable long-term trend indicators:

- **50-day SMA**: Represents medium-term trend
- **200-day SMA**: Represents long-term trend
- **Crossover Above**: Indicates bullish momentum
- **Crossover Below**: Indicates bearish momentum

### Why Daily Timeframe?

- Moving averages need sufficient data points
- Daily candles provide stable trend signals
- Reduces noise from intraday volatility
- Perfect for swing trading timeframes

## Signal Detection

The strategy detects two key signals:

### 🟢 Golden Crossover (BUY Signal)

```
Current: SMA 50 > SMA 200
Previous: SMA 50 ≤ SMA 200
→ BUY Signal Generated
```

### 🔴 Death Cross (SELL Signal)

```
Current: SMA 50 < SMA 200
Previous: SMA 50 ≥ SMA 200
→ SELL Signal Generated
```

## Position Management

### Entry Rules

- Enter long position on golden crossover
- Exit position on death cross
- One position per symbol maximum

### Risk Management

- **Stop Loss**: 8% below entry price
- **Take Profit**: 20% above entry price
- **Position Sizing**: 10% of capital per trade

## Performance Tracking

The strategy tracks:

- Total trades executed
- Win/loss ratio
- Average holding period
- Maximum drawdown
- Total P&L

## Example Output

```
🟢 GOLDEN CROSSOVER DETECTED for RELIANCE-EQ
Current SMA 50: 2450.50
Current SMA 200: 2420.75
Previous SMA 50: 2418.25
Previous SMA 200: 2425.10
==================================================

🔴 DEATH CROSS DETECTED for TCS-EQ
Current SMA 50: 3850.20
Current SMA 200: 3865.40
Previous SMA 50: 3870.15
Previous SMA 200: 3860.25
==================================================
```

## Best Practices

### Symbol Selection

- Choose liquid, large-cap stocks
- Avoid highly volatile stocks
- Focus on fundamentally strong companies
- Consider sector diversification

### Risk Management

- Never risk more than 2% per trade
- Use position sizing based on volatility
- Set appropriate stop losses
- Take profits at predetermined levels

### Market Conditions

- Golden crossover works best in trending markets
- Avoid trading during high volatility periods
- Consider market sentiment and news
- Monitor economic indicators

## Next Steps

- Check out [Basic Strategy](../basic-strategy/) for a simple template
- Read the [API Reference](../../api-reference/) for detailed documentation
- Explore [Trading and Strategy](../../trading-and-strategy/) for advanced topics
- Study [Indicators](../../indicators/) for more technical analysis tools

## Disclaimer

This is an educational example. Always:

- Test strategies on paper trading first
- Understand the risks involved
- Consider your risk tolerance
- Consult with financial advisors
- Never invest more than you can afford to lose
