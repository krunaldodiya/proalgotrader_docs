# Custom Indicators Guide

This guide explains how to create and use custom indicators in the ProAlgoTrader framework using the `CustomIndicator` base class, and how to use the new `build` method available in all indicators.

## Table of Contents

1. [Overview](#overview)
2. [Built-in Indicators with Build Method](#built-in-indicators-with-build-method)
3. [Creating Custom Indicators](#creating-custom-indicators)
4. [Required Methods](#required-methods)
5. [Optional Methods](#optional-methods)
6. [Usage Examples](#usage-examples)
7. [Best Practices](#best-practices)
8. [Common Patterns](#common-patterns)
9. [Troubleshooting](#troubleshooting)

## Overview

The `CustomIndicator` class allows you to create custom indicators using any function from the `polars_talib` library. This gives you complete flexibility to implement indicators that aren't yet available in the main library or create custom combinations of indicators.

### Key Benefits

- ✅ **Flexibility**: Use any polars_talib function
- ✅ **Reusability**: Create once, use in multiple strategies
- ✅ **Performance**: Same performance as built-in indicators
- ✅ **Integration**: Seamless integration with charts and strategies
- ✅ **Maintainability**: Clean, testable code structure

## Built-in Indicators with Build Method

All built-in indicators now include a `build()` method that returns a `pl.Expression`, providing direct access to the raw indicator calculation. This is in addition to the existing `_exprs()` method that returns a list of `pl.Expression` with proper column aliases.

### Available Built-in Indicators

**Momentum Indicators:**

- `RSI` - Relative Strength Index
- `MACD` - Moving Average Convergence/Divergence
- `ADX` - Average Directional Movement Index
- `CCI` - Commodity Channel Index
- `STOCH` - Stochastic Oscillator
- `STOCHRSI` - Stochastic RSI
- `WilliamsR` - Williams %R
- `AROON` - Aroon Indicator

**TradingView (TV) Momentum Indicators:**

- `RSI_TV` - TradingView-style RSI
- `MACD_TV` - TradingView-style MACD
- `ADX_TV` - TradingView-style ADX
- `STOCH_TV` - TradingView-style Stochastic

**Overlap Indicators:**

- `SMA` - Simple Moving Average
- `EMA` - Exponential Moving Average
- `BBANDS` - Bollinger Bands

**TradingView (TV) Overlap Indicators:**

- `SMA_TV` - TradingView-style SMA
- `EMA_TV` - TradingView-style EMA
- `BBANDS_TV` - TradingView-style Bollinger Bands

**Volatility Indicators:**

- `ATR` - Average True Range
- `ATR_TV` - TradingView-style ATR

**Volume Indicators:**

- `OBV` - On Balance Volume
- `MFI` - Money Flow Index
- `VWAP` - Volume Weighted Average Price

**Trend Indicators:**

- `Supertrend` - Supertrend Indicator

### Using Build Method with Built-in Indicators

```python
from proalgotrader_core.indicators import RSI, MACD, SMA

# Get the raw expression from any indicator
rsi = RSI(timeperiod=14)
raw_rsi_expr = rsi.build()  # Returns pl.Expr

macd = MACD(fastperiod=12, slowperiod=26, signalperiod=9)
raw_macd_expr = macd.build()  # Returns pl.Expr with struct

sma = SMA(period=20)
raw_sma_expr = sma.build()  # Returns pl.Expr

# Use in custom calculations
custom_expr = raw_rsi_expr + raw_sma_expr
```

### Build vs Exprs Methods

- **`build()`**: Returns a single `pl.Expression` representing the raw indicator calculation
- **`_exprs()`**: Returns a list of `pl.Expression` with proper column aliases for DataFrame integration

```python
# Example with MACD
macd = MACD()

# build() returns the raw struct
raw_expr = macd.build()  # pta.macd(...)

# _exprs() returns aliased expressions
exprs = macd._exprs()  # [raw_expr.struct.field("macd").alias("macd_12_26_9_close"), ...]
```

## Creating Custom Indicators

### Basic Structure

To create a custom indicator, extend the `CustomIndicator` class and implement the required methods:

```python
import polars as pl
import polars_talib as pta
from proalgotrader_core.indicators import CustomIndicator

class MyCustomIndicator(CustomIndicator):
    def __init__(self, timeperiod: int = 14):
        super().__init__()
        self.timeperiod = timeperiod

    def build(self) -> pl.Expr:
        # Your indicator logic here
        return pta.rsi(pl.col("close"), timeperiod=self.timeperiod).alias("my_rsi")

    def output_columns(self) -> list[str]:
        return ["my_rsi"]

    def required_columns(self) -> list[str]:
        return ["close"]
```

### File Organization

Create a separate file for your custom indicators:

```
project/
├── strategy.py
├── custom_indicators.py    # Your custom indicators
└── position_manager.py
```

## Required Methods

### 1. `build() -> pl.Expr`

**Purpose**: Define the indicator calculation logic using polars_talib functions.

**Returns**: A single polars expression that defines your indicator

**Example**:

```python
def build(self) -> pl.Expr:
    return pta.rsi(pl.col("close"), timeperiod=self.timeperiod).alias("my_rsi")
```

### 2. `output_columns() -> list[str]`

**Purpose**: Define the names of the output columns your indicator produces.

**Returns**: List of column names that match the aliases in your `build()` method

**Example**:

```python
def output_columns(self) -> list[str]:
    return ["my_rsi"]
```

## Auto-Calculation Feature

The `CustomIndicator` base class now automatically calculates `window_size()` and `warmup_size()` from your indicator parameters, making it much easier to create custom indicators.

### How It Works

1. **Parameter Detection**: Automatically detects common parameter names like `timeperiod`, `period`, `fastperiod`, `slowperiod`, etc.
2. **Window Size**: Calculated as the maximum of all numeric parameters
3. **Warmup Size**: Calculated as `window_size * 3` for stabilization

### Supported Parameter Names

The auto-calculation recognizes these parameter names:

- `timeperiod`, `period`, `length`
- `fastperiod`, `slowperiod`, `signalperiod`
- `fastlength`, `slowlength`, `signal_smoothing`
- `fastk_period`, `slowk_period`, `slowd_period`
- And many more TA-Lib parameter names

### Examples

```python
class SimpleRSI(CustomIndicator):
    def __init__(self, timeperiod: int = 14):
        super().__init__()
        self.timeperiod = timeperiod

    def build(self) -> pl.Expr:
        return pta.rsi(pl.col("close"), timeperiod=self.timeperiod).alias("rsi")
        # Auto-calculated: window_size = 14, warmup_size = 42

class MACDIndicator(CustomIndicator):
    def __init__(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        super().__init__()
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

    def build(self) -> pl.Expr:
        return pta.macd(pl.col("close"), fastperiod=self.fastperiod,
                       slowperiod=self.slowperiod, signalperiod=self.signalperiod)
        # Auto-calculated: window_size = 26, warmup_size = 78
```

## Optional Methods

### `required_columns() -> list[str]`

**Purpose**: Define which input columns your indicator needs.

**Default**: Returns empty list `[]`

**Example**:

```python
def required_columns(self) -> list[str]:
    return ["high", "low", "close", "volume"]
```

### `window_size() -> int`

**Purpose**: Define the minimum lookback period required for accurate calculation.

**Default**: Auto-calculated from indicator parameters (max of all numeric parameters)

**Example**:

```python
# Auto-calculated (no need to implement):
# For RSI with timeperiod=14: window_size = 14
# For MACD with fastperiod=12, slowperiod=26, signalperiod=9: window_size = 26

# Manual override if needed:
def window_size(self) -> int:
    return self.timeperiod * 2  # Custom logic
```

### `warmup_size() -> int`

**Purpose**: Define extra lookback period for indicator stabilization.

**Default**: Auto-calculated as `window_size() * 3`

**Example**:

```python
# Auto-calculated (no need to implement):
# For RSI with timeperiod=14: warmup_size = 42
# For MACD with slowperiod=26: warmup_size = 78

# Manual override if needed:
def warmup_size(self) -> int:
    return self.timeperiod * 5  # Custom logic
```

## Usage Examples

### Example 1: Simple RSI Indicator

```python
# custom_indicators.py
import polars as pl
import polars_talib as pta
from proalgotrader_core.indicators import CustomIndicator

class MyRSI(CustomIndicator):
    def __init__(self, timeperiod: int = 14, output_name: str = "my_rsi"):
        super().__init__()
        self.timeperiod = timeperiod
        self.output_name = output_name

    def build(self) -> pl.Expr:
        return pta.rsi(pl.col("close"), timeperiod=self.timeperiod).alias(self.output_name)

    def output_columns(self) -> list[str]:
        return [self.output_name]

    def required_columns(self) -> list[str]:
        return ["close"]

    def window_size(self) -> int:
        return self.timeperiod

    def warmup_size(self) -> int:
        return self.timeperiod * 3

# strategy.py
from project.custom_indicators import MyRSI

class Strategy(StrategyProtocol):
    async def get_indicator(self):
        custom_rsi = MyRSI(timeperiod=14, output_name="my_rsi")
        return await self.chart.add_indicator("indicator", custom_rsi)

    async def next(self) -> None:
        self.indicator = await self.get_indicator()
        rsi_value = await self.indicator.get_data(0, "my_rsi")
        print(f"RSI: {rsi_value}")
```

### Example 2: Multi-Output Indicator (MACD)

```python
class MyMACD(CustomIndicator):
    def __init__(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        super().__init__()
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

    def build(self) -> pl.Expr:
        return pta.macd(
            pl.col("close"),
            fastperiod=self.fastperiod,
            slowperiod=self.slowperiod,
            signalperiod=self.signalperiod
        )

    def output_columns(self) -> list[str]:
        return ["macd_line", "macd_signal", "macd_histogram"]

    def required_columns(self) -> list[str]:
        return ["close"]

    def window_size(self) -> int:
        return self.slowperiod

# Usage in strategy
async def next(self) -> None:
    self.indicator = await self.get_indicator()
    macd_line = await self.indicator.get_data(0, "macd_line")
    macd_signal = await self.indicator.get_data(0, "macd_signal")
    print(f"MACD Line: {macd_line}, Signal: {macd_signal}")
```

### Example 3: Complex Indicator with Conditional Logic

```python
class MyRSISignal(CustomIndicator):
    def __init__(self, timeperiod: int = 14, overbought: int = 70, oversold: int = 30):
        super().__init__()
        self.timeperiod = timeperiod
        self.overbought = overbought
        self.oversold = oversold

    def build(self) -> pl.Expr:
        rsi = pta.rsi(pl.col("close"), timeperiod=self.timeperiod)

        # Create signal based on RSI levels
        signal = (
            pl.when(rsi > self.overbought)
            .then(1)  # Overbought signal
            .when(rsi < self.oversold)
            .then(-1)  # Oversold signal
            .otherwise(0)  # Neutral
            .alias("rsi_signal")
        )

        return pl.struct([
            rsi.alias("rsi_value"),
            signal
        ])

    def output_columns(self) -> list[str]:
        return ["rsi_value", "rsi_signal"]

    def required_columns(self) -> list[str]:
        return ["close"]
```

### Example 4: Combining Multiple Indicators

```python
class MyMultiIndicator(CustomIndicator):
    def __init__(self, rsi_period: int = 14, sma_period: int = 20):
        super().__init__()
        self.rsi_period = rsi_period
        self.sma_period = sma_period

    def build(self) -> pl.Expr:
        return pl.struct([
            pta.rsi(pl.col("close"), timeperiod=self.rsi_period).alias("rsi"),
            pta.sma(pl.col("close"), timeperiod=self.sma_period).alias("sma")
        ])

    def output_columns(self) -> list[str]:
        return ["rsi", "sma"]

    def required_columns(self) -> list[str]:
        return ["close"]

    def window_size(self) -> int:
        return max(self.rsi_period, self.sma_period)
```

### Example 5: Using Built-in Indicators with Build Method

```python
class MyCombinedIndicator(CustomIndicator):
    def __init__(self):
        super().__init__()
        # Create built-in indicators
        self.rsi = RSI(timeperiod=14)
        self.sma = SMA(period=20)
        self.macd = MACD()

    def build(self) -> pl.Expr:
        # Get raw expressions from built-in indicators
        rsi_expr = self.rsi.build()
        sma_expr = self.sma.build()
        macd_expr = self.macd.build()

        # Combine them in custom logic
        combined = (
            pl.when(rsi_expr > 70)
            .then(sma_expr * 1.1)  # 10% above SMA when overbought
            .when(rsi_expr < 30)
            .then(sma_expr * 0.9)  # 10% below SMA when oversold
            .otherwise(sma_expr)
            .alias("adaptive_sma")
        )

        return pl.struct([
            rsi_expr.alias("rsi"),
            sma_expr.alias("sma"),
            macd_expr.struct.field("macd").alias("macd_line"),
            combined
        ])

    def output_columns(self) -> list[str]:
        return ["rsi", "sma", "macd_line", "adaptive_sma"]
```

## Best Practices

### 1. Naming Conventions

- Use descriptive class names: `MyRSI`, `MyMACD`, `MyBollingerBands`
- Use descriptive output column names: `"my_rsi_14"`, `"macd_line"`, `"bb_upper"`
- Use consistent parameter naming: `timeperiod`, `fastperiod`, `slowperiod`

### 2. Parameter Validation

```python
def __init__(self, timeperiod: int = 14):
    super().__init__()
    if timeperiod <= 0:
        raise ValueError("timeperiod must be positive")
    self.timeperiod = timeperiod
```

### 3. Documentation

```python
class MyRSI(CustomIndicator):
    """
    Custom Relative Strength Index (RSI) indicator.

    Parameters:
        timeperiod (int): The period for RSI calculation (default: 14)
        output_name (str): Name of the output column (default: "my_rsi")

    Output:
        - Single column with RSI values (0-100)

    Usage:
        rsi = MyRSI(timeperiod=14, output_name="my_rsi")
    """
```

### 4. Error Handling

```python
def build(self) -> pl.Expr:
    try:
        return pta.rsi(pl.col("close"), timeperiod=self.timeperiod).alias(self.output_name)
    except Exception as e:
        raise ValueError(f"Failed to build RSI indicator: {e}")
```

## Common Patterns

### 1. Single Output Indicator

```python
class MySingleIndicator(CustomIndicator):
    def __init__(self, param: int = 14):
        super().__init__()
        self.param = param

    def build(self) -> pl.Expr:
        return pta.indicator(pl.col("close"), self.param).alias("my_indicator")
```

### 2. Multi-Output Indicator

```python
class MyMultiOutputIndicator(CustomIndicator):
    def build(self) -> pl.Expr:
        result = pta.multi_output_indicator(pl.col("close"))
        return pl.struct([
            result.struct.field("field1").alias("output1"),
            result.struct.field("field2").alias("output2")
        ])
```

### 3. Conditional Indicator

```python
class MyConditionalIndicator(CustomIndicator):
    def build(self) -> pl.Expr:
        base_indicator = pta.base_indicator(pl.col("close"))
        signal = pl.when(base_indicator > 50).then(1).otherwise(0).alias("signal")
        return pl.struct([
            base_indicator.alias("base"),
            signal
        ])
```

### 4. Combining Built-in Indicators

```python
class MyCombinedIndicator(CustomIndicator):
    def __init__(self):
        super().__init__()
        self.rsi = RSI(timeperiod=14)
        self.sma = SMA(period=20)

    def build(self) -> pl.Expr:
        rsi_expr = self.rsi.build()
        sma_expr = self.sma.build()

        # Custom combination logic
        ratio = (rsi_expr / 100) * sma_expr
        return ratio.alias("rsi_weighted_sma")
```

## Troubleshooting

### Common Issues

1. **"Column not found" error**

   - Check that `required_columns()` includes all needed columns
   - Verify column names match your data: `"close"`, `"high"`, `"low"`, `"volume"`

2. **"build() method must be called" error**

   - Ensure you're calling `super().__init__()` in your `__init__` method
   - Check that your `build()` method returns a single expression

3. **Wrong output column names**

   - Make sure `output_columns()` matches the aliases in your `build()` method
   - Check for typos in column names

4. **Performance issues**
   - Set appropriate `window_size()` and `warmup_size()` values
   - Avoid unnecessary calculations in `build()` method

### Debug Tips

1. **Test your indicator separately**:

```python
# Test in isolation
indicator = MyRSI(timeperiod=14)
print(f"Output columns: {indicator.output_columns()}")
print(f"Required columns: {indicator.required_columns()}")
print(f"Window size: {indicator.window_size()}")
print(f"Build expression: {indicator.build()}")
```

2. **Check polars_talib documentation** for correct function signatures

3. **Use simple test data** to verify your indicator works correctly

## Available polars_talib Functions

Here are some commonly used polars_talib functions you can use in your custom indicators:

### Momentum Indicators

- `pta.rsi()` - Relative Strength Index
- `pta.macd()` - MACD
- `pta.stoch()` - Stochastic
- `pta.willr()` - Williams %R
- `pta.cci()` - Commodity Channel Index
- `pta.mfi()` - Money Flow Index

### Overlap Studies

- `pta.sma()` - Simple Moving Average
- `pta.ema()` - Exponential Moving Average
- `pta.bbands()` - Bollinger Bands
- `pta.wma()` - Weighted Moving Average

### Volatility Indicators

- `pta.atr()` - Average True Range
- `pta.natr()` - Normalized ATR

### Volume Indicators

- `pta.obv()` - On Balance Volume
- `pta.ad()` - Chaikin A/D Line

For a complete list, refer to the [polars_talib documentation](https://pypi.org/project/polars-talib/).

## Conclusion

The `CustomIndicator` class provides a powerful and flexible way to create custom indicators using polars_talib. With the new `build()` method available in all indicators, you can now easily combine built-in indicators with custom logic to create sophisticated trading strategies.

Remember to:

- Always implement the required methods (`build()` and `output_columns()`)
- Override optional methods when needed
- Use descriptive names and proper documentation
- Test your indicators thoroughly
- Follow the established patterns for consistency
- Leverage the `build()` method from built-in indicators for complex combinations

Happy coding! 🚀
