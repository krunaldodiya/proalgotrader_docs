# SMA Crossover Strategy Example

This example shows a complete SMA 20 vs SMA 50 crossover strategy for Nifty options trading.

## Files

- `main.py` - Entry point to run the strategy
- `strategy.py` - Main SMA crossover strategy implementation
- `position_manager.py` - Position manager for net PnL tracking
- `README.md` - This documentation

## Strategy Logic

- **SMA 20** crosses above **SMA 50** → Buy Nifty CE options
- **SMA 20** crosses below **SMA 50** → Buy Nifty PE options
- **Position Manager**: Exits all positions when net PnL ≥ ₹1000 (profit) or ≤ ₹500 (loss)

## Key Features

- ✅ Uses built-in SMA indicators
- ✅ No interval delay - checks every tick for signals
- ✅ PnL-based position exits (no risk reward needed for options)
- ✅ Only one position at a time
- ✅ Trades current week ATM options

## Usage

```bash
python main.py
```

The strategy will automatically:

- Connect to your broker
- Subscribe to Nifty market data
- Calculate SMA indicators
- Generate crossover signals
- Execute options trades
- Manage positions with risk controls

## Next Steps

- Check out [Basic Strategy](../basic-strategy/) for a simple template
- Read the [API Reference](../../api-reference/) for detailed documentation
