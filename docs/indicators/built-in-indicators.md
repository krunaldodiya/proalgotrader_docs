# Built-in Indicators

ProAlgoTrader Core comes with a comprehensive set of built-in technical indicators, all optimized for high-performance trading using the Polars data processing library.

## Overview

All built-in indicators inherit from the base `Indicator` class and provide:

- ✅ **High Performance**: Built on Polars for fast data processing
- ✅ **Consistent API**: Uniform interface across all indicators
- ✅ **Data Access**: `data` property and `get_data()` method for easy value retrieval
- ✅ **Build Method**: Direct access to raw calculations
- ✅ **TradingView Support**: Many indicators have TradingView-compatible versions
- ✅ **Easy Integration**: Seamless integration with strategies and charts

## Data Access

All indicators expose two main ways to access their calculated values:

### Data Property

```python
# Get full DataFrame with all indicator data
indicator_data = rsi.data
print(indicator_data)

# Access specific columns
rsi_values = rsi.data.select("rsi")
print(rsi_values)
```

### Get Data Method

```python
# Get current RSI value (row 0 = most recent)
current_rsi = await rsi.get_data(0, "rsi")
print(f"Current RSI: {current_rsi}")

# Get previous RSI value (row 1 = previous value)
previous_rsi = await rsi.get_data(1, "rsi")
print(f"Previous RSI: {previous_rsi}")

# Get current indicator data as Series
current_data = await rsi.get_data(0)
print(current_data)
```

### Debugging Data Structure

```python
# Print DataFrame structure
print(rsi.data)
print(rsi.data.columns)
print(rsi.data.dtypes)
```

## Indicator Categories

### 📈 Momentum Indicators

Momentum indicators help identify the strength and direction of price movements.

#### RSI (Relative Strength Index)

```python
from proalgotrader_core.indicators import RSI

# Standard RSI
rsi = RSI(timeperiod=14)

# Get values
rsi_value = bar.get_indicator_value("rsi")
```

**Parameters:**

- `timeperiod` (int): Period for RSI calculation (default: 14)

**Usage:**

- **Oversold**: RSI < 30 (potential buy signal)
- **Overbought**: RSI > 70 (potential sell signal)
- **Divergence**: Price making new highs while RSI making lower highs

#### MACD (Moving Average Convergence/Divergence)

```python
from proalgotrader_core.indicators import MACD

macd = MACD(fastperiod=12, slowperiod=26, signalperiod=9)

# Get values
macd_line = bar.get_indicator_value("macd")
macd_signal = bar.get_indicator_value("macd_signal")
macd_histogram = bar.get_indicator_value("macd_histogram")
```

**Parameters:**

- `fastperiod` (int): Fast EMA period (default: 12)
- `slowperiod` (int): Slow EMA period (default: 26)
- `signalperiod` (int): Signal line period (default: 9)

**Usage:**

- **Bullish**: MACD line crosses above signal line
- **Bearish**: MACD line crosses below signal line
- **Divergence**: Price and MACD moving in opposite directions

#### ADX (Average Directional Movement Index)

```python
from proalgotrader_core.indicators import ADX

adx = ADX(timeperiod=14)

# Get values
adx_value = bar.get_indicator_value("adx")
plus_di = bar.get_indicator_value("plus_di")
minus_di = bar.get_indicator_value("minus_di")
```

**Parameters:**

- `timeperiod` (int): Period for ADX calculation (default: 14)

**Usage:**

- **Strong Trend**: ADX > 25
- **Weak Trend**: ADX < 20
- **Trend Direction**: +DI > -DI (bullish), +DI < -DI (bearish)

#### CCI (Commodity Channel Index)

```python
from proalgotrader_core.indicators import CCI

cci = CCI(timeperiod=14)

# Get values
cci_value = bar.get_indicator_value("cci")
```

**Parameters:**

- `timeperiod` (int): Period for CCI calculation (default: 14)

**Usage:**

- **Oversold**: CCI < -100
- **Overbought**: CCI > +100
- **Mean Reversion**: CCI crossing zero line

#### Stochastic Oscillator

```python
from proalgotrader_core.indicators import STOCH

stoch = STOCH(fastk_period=14, slowk_period=3, slowd_period=3)

# Get values
stoch_k = bar.get_indicator_value("stoch_k")
stoch_d = bar.get_indicator_value("stoch_d")
```

**Parameters:**

- `fastk_period` (int): Fast %K period (default: 14)
- `slowk_period` (int): Slow %K period (default: 3)
- `slowd_period` (int): Slow %D period (default: 3)

**Usage:**

- **Oversold**: %K < 20
- **Overbought**: %K > 80
- **Bullish Crossover**: %K crosses above %D
- **Bearish Crossover**: %K crosses below %D

#### Williams %R

```python
from proalgotrader_core.indicators import WilliamsR

williams_r = WilliamsR(timeperiod=14)

# Get values
williams_r_value = bar.get_indicator_value("williams_r")
```

**Parameters:**

- `timeperiod` (int): Period for Williams %R calculation (default: 14)

**Usage:**

- **Oversold**: Williams %R < -80
- **Overbought**: Williams %R > -20

#### Aroon Indicator

```python
from proalgotrader_core.indicators import AROON

aroon = AROON(timeperiod=14)

# Get values
aroon_up = bar.get_indicator_value("aroon_up")
aroon_down = bar.get_indicator_value("aroon_down")
aroon_oscillator = bar.get_indicator_value("aroon_oscillator")
```

**Parameters:**

- `timeperiod` (int): Period for Aroon calculation (default: 14)

**Usage:**

- **Strong Uptrend**: Aroon Up > 70, Aroon Down < 30
- **Strong Downtrend**: Aroon Down > 70, Aroon Up < 30
- **Consolidation**: Both values between 30-70

### 📊 Overlap Indicators

Overlap indicators are plotted on the same chart as price data.

#### SMA (Simple Moving Average)

```python
from proalgotrader_core.indicators import SMA

sma = SMA(period=20)

# Get values
sma_value = bar.get_indicator_value("sma")
```

**Parameters:**

- `period` (int): Period for SMA calculation (default: 20)

**Usage:**

- **Support/Resistance**: Price bouncing off SMA
- **Trend Direction**: Price above/below SMA
- **Crossovers**: Fast SMA crossing slow SMA

#### EMA (Exponential Moving Average)

```python
from proalgotrader_core.indicators import EMA

ema = EMA(period=20)

# Get values
ema_value = bar.get_indicator_value("ema")
```

**Parameters:**

- `period` (int): Period for EMA calculation (default: 20)

**Usage:**

- **Trend Following**: More responsive than SMA
- **Support/Resistance**: Dynamic support/resistance levels
- **Golden Cross**: Fast EMA crosses above slow EMA

#### Bollinger Bands

```python
from proalgotrader_core.indicators import BBANDS

bbands = BBANDS(period=20, nbdevup=2, nbdevdn=2)

# Get values
bb_upper = bar.get_indicator_value("bb_upper")
bb_middle = bar.get_indicator_value("bb_middle")
bb_lower = bar.get_indicator_value("bb_lower")
```

**Parameters:**

- `period` (int): Period for calculation (default: 20)
- `nbdevup` (float): Upper band standard deviation (default: 2)
- `nbdevdn` (float): Lower band standard deviation (default: 2)

**Usage:**

- **Volatility**: Band width indicates volatility
- **Mean Reversion**: Price touching bands
- **Breakouts**: Price breaking out of bands

### 📈 Volatility Indicators

Volatility indicators measure the rate of price changes.

#### ATR (Average True Range)

```python
from proalgotrader_core.indicators import ATR

atr = ATR(timeperiod=14)

# Get values
atr_value = bar.get_indicator_value("atr")
```

**Parameters:**

- `timeperiod` (int): Period for ATR calculation (default: 14)

**Usage:**

- **Stop Loss**: Dynamic stop loss based on volatility
- **Position Sizing**: Risk-based position sizing
- **Volatility Breakouts**: High ATR indicates potential breakouts

### 📊 Volume Indicators

Volume indicators incorporate trading volume in their calculations.

#### OBV (On Balance Volume)

```python
from proalgotrader_core.indicators import OBV

obv = OBV()

# Get values
obv_value = bar.get_indicator_value("obv")
```

**Usage:**

- **Volume Confirmation**: OBV confirming price trends
- **Divergence**: Price and OBV moving in opposite directions
- **Breakouts**: OBV breaking out of patterns

#### MFI (Money Flow Index)

```python
from proalgotrader_core.indicators import MFI

mfi = MFI(timeperiod=14)

# Get values
mfi_value = bar.get_indicator_value("mfi")
```

**Parameters:**

- `timeperiod` (int): Period for MFI calculation (default: 14)

**Usage:**

- **Oversold**: MFI < 20
- **Overbought**: MFI > 80
- **Volume-weighted RSI**: Similar to RSI but includes volume

#### VWAP (Volume Weighted Average Price)

```python
from proalgotrader_core.indicators import VWAP

vwap = VWAP()

# Get values
vwap_value = bar.get_indicator_value("vwap")
```

**Usage:**

- **Intraday Trading**: Key level for day trading
- **Fair Value**: Represents average price weighted by volume
- **Support/Resistance**: Price often respects VWAP levels

### 📈 Trend Indicators

Trend indicators help identify the direction and strength of trends.

#### Supertrend

```python
from proalgotrader_core.indicators import Supertrend

supertrend = Supertrend(period=10, multiplier=3)

# Get values
supertrend_value = bar.get_indicator_value("supertrend")
supertrend_direction = bar.get_indicator_value("supertrend_direction")
```

**Parameters:**

- `period` (int): ATR period (default: 10)
- `multiplier` (float): ATR multiplier (default: 3)

**Usage:**

- **Trend Direction**: Green (bullish), Red (bearish)
- **Stop Loss**: Dynamic trailing stop
- **Trend Following**: Follows the trend direction

## TradingView Indicators

Many indicators have TradingView-compatible versions that match the exact calculations used in TradingView:

### Available TradingView Indicators

- `RSI_TV` - TradingView RSI
- `MACD_TV` - TradingView MACD
- `ADX_TV` - TradingView ADX
- `STOCH_TV` - TradingView Stochastic
- `SMA_TV` - TradingView SMA
- `EMA_TV` - TradingView EMA
- `BBANDS_TV` - TradingView Bollinger Bands
- `ATR_TV` - TradingView ATR

### Usage Example

```python
from proalgotrader_core.indicators import RSI_TV, MACD_TV

# TradingView-compatible indicators
rsi_tv = RSI_TV(timeperiod=14)
macd_tv = MACD_TV(fastperiod=12, slowperiod=26, signalperiod=9)

# Values match TradingView exactly
rsi_value = bar.get_indicator_value("rsi_tv")
macd_line = bar.get_indicator_value("macd_tv")
```

## Using Indicators in Strategies

### Basic Usage

```python
from proalgotrader_core.protocols import Strategy
from proalgotrader_core.indicators import RSI, SMA, MACD

class MyStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.rsi = RSI(timeperiod=14)
        self.sma_20 = SMA(period=20)
        self.macd = MACD()

    async def on_bar(self, bar):
        rsi = bar.get_indicator_value("rsi")
        sma_20 = bar.get_indicator_value("sma_20")
        macd_line = bar.get_indicator_value("macd")
        macd_signal = bar.get_indicator_value("macd_signal")

        # Trading logic
        if rsi < 30 and bar.close > sma_20 and macd_line > macd_signal:
            await self.buy(bar.symbol, quantity=100)
```

### Advanced Usage with Build Method

```python
class AdvancedStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.rsi = RSI(timeperiod=14)
        self.atr = ATR(timeperiod=14)

    async def on_bar(self, bar):
        # Get raw expressions for custom calculations
        rsi_expr = self.rsi.build()
        atr_expr = self.atr.build()

        # Custom logic using raw expressions
        rsi_value = bar.get_indicator_value("rsi")
        atr_value = bar.get_indicator_value("atr")

        # Dynamic stop loss based on ATR
        stop_loss = bar.close - (2 * atr_value)
        take_profit = bar.close + (3 * atr_value)

        if rsi_value < 30:
            await self.buy(
                symbol=bar.symbol,
                quantity=100,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
```

## Performance Optimization

### Indicator Caching

```python
class OptimizedStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.rsi = RSI(timeperiod=14)
        self.sma_20 = SMA(period=20)
        self.sma_50 = SMA(period=50)

    async def on_bar(self, bar):
        # Cache indicator values to avoid recalculation
        indicators = {
            'rsi': bar.get_indicator_value("rsi"),
            'sma_20': bar.get_indicator_value("sma_20"),
            'sma_50': bar.get_indicator_value("sma_50")
        }

        # Use cached values
        if indicators['rsi'] < 30 and indicators['sma_20'] > indicators['sma_50']:
            await self.buy(bar.symbol, quantity=100)
```

## Best Practices

### 1. Choose Appropriate Timeframes

```python
# Different timeframes for different purposes
rsi_short = RSI(timeperiod=7)    # Short-term signals
rsi_medium = RSI(timeperiod=14)  # Medium-term signals
rsi_long = RSI(timeperiod=21)    # Long-term signals
```

### 2. Combine Multiple Indicators

```python
# Don't rely on single indicators
if (rsi < 30 and
    macd_line > macd_signal and
    bar.close > sma_20):
    # Multiple confirmations
    await self.buy(bar.symbol, quantity=100)
```

### 3. Use Proper Risk Management

```python
# Always use stop losses
atr_value = bar.get_indicator_value("atr")
stop_loss = bar.close - (2 * atr_value)

await self.buy(
    symbol=bar.symbol,
    quantity=100,
    stop_loss=stop_loss
)
```

### 4. Avoid Over-optimization

```python
# Use standard parameters
rsi = RSI(timeperiod=14)  # Standard 14-period RSI
macd = MACD()             # Standard MACD parameters
```

## Troubleshooting

### Common Issues

1. **Indicator Not Updating**

   - Ensure indicator is properly initialized in `__init__`
   - Check that required data columns are available

2. **Incorrect Values**

   - Verify indicator parameters
   - Check data quality and completeness
   - Use TradingView version for exact matches

3. **Performance Issues**
   - Cache indicator values when possible
   - Avoid unnecessary recalculations
   - Use appropriate timeframes

## Next Steps

- **Custom Indicators**: Learn to create your own indicators in [Custom Indicators Guide](custom-indicators-guide.md)
- **Indicator Combinations**: See [Strategy Examples](../examples/strategy-examples.md) for advanced usage
- **TradingView Integration**: Read [TradingView Indicators](tradingview-indicators.md) for exact matches
- **Performance Optimization**: Check [Development Guide](../development/development-setup.md) for optimization tips

---

**Need help with specific indicators?** Check our [Indicator Quick Reference](indicator-quick-reference.md) or [API Reference](../api-reference/indicators-api.md).
