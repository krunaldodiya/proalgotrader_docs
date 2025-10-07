# Custom Indicators Quick Reference

## Built-in Indicators with Build Method

All built-in indicators now include a `build()` method that returns a `pl.Expression`:

```python
from proalgotrader_core.indicators import RSI, MACD, SMA

# Get raw expressions from any indicator
rsi = RSI(timeperiod=14)
raw_rsi_expr = rsi.build()  # Returns pl.Expr

macd = MACD()
raw_macd_expr = macd.build()  # Returns pl.Expr with struct

# Use in custom calculations
custom_expr = raw_rsi_expr + raw_macd_expr.struct.field("macd")
```

**Available Built-in Indicators:**

- **Momentum**: RSI, MACD, ADX, CCI, STOCH, STOCHRSI, WilliamsR, AROON
- **TV Momentum**: RSI_TV, MACD_TV, ADX_TV, STOCH_TV
- **Overlap**: SMA, EMA, BBANDS
- **TV Overlap**: SMA_TV, EMA_TV, BBANDS_TV
- **Volatility**: ATR, ATR_TV
- **Volume**: OBV, MFI, VWAP
- **Trend**: Supertrend

## Basic Template

```python
import polars as pl
import polars_talib as pta
from proalgotrader_core.indicators import CustomIndicator

class MyIndicator(CustomIndicator):
    def __init__(self, param: int = 14):
        super().__init__()
        self.param = param

    def build(self) -> pl.Expr:
        return pta.indicator(pl.col("close"), self.param).alias("my_indicator")

    def window_size(self) -> int:
        return self.param

    def warmup_size(self) -> int:
        return self.param * 3
    # Auto-generated: output_columns() = ["my_indicator"], required_columns() = ["close"]
```

## Ultra-Simple Template (Auto-Extraction)

```python
class MyMACD(CustomIndicator):
    def __init__(self, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9):
        super().__init__()
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

    def build(self) -> pl.Expr:
        return pta.macd(pl.col("close"), fastperiod=self.fastperiod,
                       slowperiod=self.slowperiod, signalperiod=self.signalperiod)
        # Auto-extracts: macd, macdsignal, macdhist
        # Auto-detects: required_columns = ["close"]

    def window_size(self) -> int:
        return self.slowperiod
```

## Required Methods

| Method    | Purpose                | Example                                            |
| --------- | ---------------------- | -------------------------------------------------- |
| `build()` | Define indicator logic | `return pta.rsi(pl.col("close"), 14).alias("rsi")` |

## Auto-Generated (Optional Override)

| Method               | Purpose              | Auto-Generated From | Example Override             |
| -------------------- | -------------------- | ------------------- | ---------------------------- |
| `output_columns()`   | Output column names  | `.alias()` calls    | `return ["my_rsi"]`          |
| `required_columns()` | Input columns needed | `col("name")` calls | `return ["close", "volume"]` |

## Optional Methods

| Method          | Purpose             | Default | Example                      |
| --------------- | ------------------- | ------- | ---------------------------- |
| `window_size()` | Minimum lookback    | `0`     | `return self.timeperiod`     |
| `warmup_size()` | Extra stabilization | `0`     | `return self.timeperiod * 3` |

## Common Patterns

### Single Output

```python
def build(self) -> pl.Expr:
    return pta.rsi(pl.col("close"), self.timeperiod).alias(self.output_name)
```

### Multi Output (Auto-Extraction)

```python
def build(self) -> pl.Expr:
    return pta.macd(pl.col("close"), fastperiod=12, slowperiod=26, signalperiod=9)
    # Auto-extracts: macd, macdsignal, macdhist
```

### Multi Output (Manual)

```python
def build(self) -> pl.Expr:
    result = pta.macd(pl.col("close"))
    return pl.struct([
        result.struct.field("macd").alias("macd_line"),
        result.struct.field("macdsignal").alias("macd_signal")
    ])
```

### Conditional Logic

```python
def build(self) -> pl.Expr:
    rsi = pta.rsi(pl.col("close"), self.timeperiod)
    return pl.when(rsi > 70).then(1).when(rsi < 30).then(-1).otherwise(0).alias("signal")
```

### With Custom Prefix

```python
def __init__(self, timeperiod: int = 14):
    super().__init__(output_prefix="my_rsi")
    self.timeperiod = timeperiod

def build(self) -> pl.Expr:
    return pta.rsi(pl.col("close"), self.timeperiod)
    # Auto-generates: my_rsi_rsi
```

### Combining Built-in Indicators

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

## Usage in Strategy

```python
# Import
from project.custom_indicators import MyIndicator

# Create and use
async def get_indicator(self):
    indicator = MyIndicator(param=14)
    return await self.chart.add_indicator("indicator", indicator)

async def next(self) -> None:
    self.indicator = await self.get_indicator()
    value = await self.indicator.get_data(0, "my_indicator")
    print(f"Value: {value}")
```

## Popular polars_talib Functions

### Momentum

- `pta.rsi(close, timeperiod)` - RSI
- `pta.macd(close, fast, slow, signal)` - MACD (auto-extracts: macd, macdsignal, macdhist)
- `pta.macdext(close, fast, slow, signal, fastmatype, slowmatype, signalmatype)` - MACD Extended
- `pta.macdfix(close, signalperiod)` - MACD Fixed
- `pta.stoch(high, low, close, fastk, slowk, slowd)` - Stochastic (auto-extracts: slowk, slowd)
- `pta.stochf(high, low, close, fastk, fastd)` - Stochastic Fast (auto-extracts: fastk, fastd)
- `pta.stochrsi(close, timeperiod, fastk, fastd)` - Stochastic RSI (auto-extracts: fastk, fastd)
- `pta.aroon(high, low, timeperiod)` - Aroon (auto-extracts: aroondown, aroonup)
- `pta.cci(high, low, close, timeperiod)` - CCI
- `pta.mfi(high, low, close, volume, timeperiod)` - MFI

### Overlap

- `pta.sma(close, timeperiod)` - Simple MA
- `pta.ema(close, timeperiod)` - Exponential MA
- `pta.bbands(close, timeperiod, nbdevup, nbdevdn)` - Bollinger Bands (auto-extracts: upperband, middleband, lowerband)
- `pta.mama(close, fastlimit, slowlimit)` - MESA Adaptive MA (auto-extracts: mama, fama)

### Volatility

- `pta.atr(high, low, close, timeperiod)` - ATR

### Math Operators

- `pta.minmax(close, timeperiod)` - Min/Max (auto-extracts: min, max)
- `pta.minmaxindex(close, timeperiod)` - Min/Max Index (auto-extracts: minidx, maxidx)

### Hilbert Transform

- `pta.ht_phasor(close)` - Phasor Components (auto-extracts: inphase, quadrature)
- `pta.ht_sine(close)` - Sine Wave (auto-extracts: sine, leadsine)

### **🎯 Dynamic Field Extraction**

The system automatically detects and extracts fields from **all 13 polars_talib functions** that return structs:

**Hilbert Transform:**

- `pta.ht_phasor()` → `["inphase", "quadrature"]`
- `pta.ht_sine()` → `["sine", "leadsine"]`

**Math Operators:**

- `pta.minmax()` → `["min", "max"]`
- `pta.minmaxindex()` → `["minidx", "maxidx"]`

**Momentum Indicators:**

- `pta.aroon()` → `["aroondown", "aroonup"]`
- `pta.macd()` → `["macd", "macdsignal", "macdhist"]`
- `pta.macdext()` → `["macd", "macdsignal", "macdhist"]`
- `pta.macdfix()` → `["macd", "macdsignal", "macdhist"]`
- `pta.stoch()` → `["slowk", "slowd"]`
- `pta.stochf()` → `["fastk", "fastd"]`
- `pta.stochrsi()` → `["fastk", "fastd"]`

**Overlap Studies:**

- `pta.bbands()` → `["upperband", "middleband", "lowerband"]`
- `pta.mama()` → `["mama", "fama"]`

**100% accurate mapping** based on polars_talib's official `get_functions_output_struct()` function!

## File Structure

```
project/
├── strategy.py
├── custom_indicators.py    # Your custom indicators
└── position_manager.py
```

## Common Issues & Solutions

| Issue                           | Solution                                               |
| ------------------------------- | ------------------------------------------------------ |
| "Column not found"              | Check `required_columns()` includes all needed columns |
| "build() method must be called" | Ensure `super().__init__()` in `__init__`              |
| Wrong output names              | Match `output_columns()` with aliases in `build()`     |
| Performance issues              | Set appropriate `window_size()` and `warmup_size()`    |

## Best Practices

✅ **One indicator per class** - Each `CustomIndicator` represents one specific indicator  
✅ Use descriptive class and column names  
✅ Validate parameters in `__init__`  
✅ Document your indicator with docstrings  
✅ Test indicators in isolation  
✅ Follow consistent naming conventions  
✅ Handle errors gracefully  
✅ Leverage built-in indicators' `build()` method for complex combinations

## Example: Complete RSI Indicator

```python
class MyRSI(CustomIndicator):
    """
    Custom RSI indicator.

    Parameters:
        timeperiod (int): RSI period (default: 14)
        output_name (str): Output column name (default: "my_rsi")
    """

    def __init__(self, timeperiod: int = 14, output_name: str = "my_rsi"):
        super().__init__()
        if timeperiod <= 0:
            raise ValueError("timeperiod must be positive")
        self.timeperiod = timeperiod
        self.output_name = output_name

    def build(self) -> pl.Expr:
        return pta.rsi(pl.col("close"), timeperiod=self.timeperiod).alias(self.output_name)

    def window_size(self) -> int:
        return self.timeperiod

    def warmup_size(self) -> int:
        return self.timeperiod * 3
    # Auto-generated: output_columns() = ["my_rsi"], required_columns() = ["close"]
```

## Example: Combining Built-in Indicators

```python
class MyAdaptiveSMA(CustomIndicator):
    """
    Adaptive SMA that adjusts based on RSI levels.
    """

    def __init__(self, rsi_period: int = 14, sma_period: int = 20):
        super().__init__()
        self.rsi = RSI(timeperiod=rsi_period)
        self.sma = SMA(period=sma_period)

    def build(self) -> pl.Expr:
        rsi_expr = self.rsi.build()
        sma_expr = self.sma.build()

        # Adaptive logic: adjust SMA based on RSI
        adaptive_sma = (
            pl.when(rsi_expr > 70)
            .then(sma_expr * 1.1)  # 10% above when overbought
            .when(rsi_expr < 30)
            .then(sma_expr * 0.9)  # 10% below when oversold
            .otherwise(sma_expr)
            .alias("adaptive_sma")
        )

        return pl.struct([
            rsi_expr.alias("rsi"),
            sma_expr.alias("sma"),
            adaptive_sma
        ])

    def output_columns(self) -> list[str]:
        return ["rsi", "sma", "adaptive_sma"]

    def window_size(self) -> int:
        return max(self.rsi.window_size(), self.sma.window_size())
```
