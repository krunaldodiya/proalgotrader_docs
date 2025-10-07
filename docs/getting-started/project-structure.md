# Strategy Project Structure

This document explains the structure of your algorithmic trading strategy project, helping you understand how to organize your code and where to implement different components.

## Your Strategy Project Structure

When you clone a strategy repository from ProAlgoTrader, you'll see this structure:

```
your-strategy-name/
├── .env.example              # Environment template
├── README.md                 # Strategy documentation
├── requirements.txt          # Dependencies
├── main.py                   # Entry point to run your strategy
├── project/                  # Your strategy implementation
│   ├── __init__.py
│   ├── strategy.py           # Main trading strategy
│   └── position_manager.py   # Position management logic
└── tests/                    # Strategy tests
    └── test_strategy.py
```

## Key Files Explained

### 1. `main.py` - Entry Point

This is the main file you run to start your strategy:

```python
from project.strategy import Strategy

from proalgotrader_core.start import run_strategy


if __name__ == "__main__":
    run_strategy(strategy=Strategy)
```

**To run your strategy:**

```bash
python main.py
```

### 2. `project/strategy.py` - Your Trading Logic

This is where you implement your trading strategy:

```python
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.protocols.strategy import StrategyProtocol

class Strategy(StrategyProtocol):
    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm
        # Configure your strategy here

    async def initialize(self) -> None:
        # Set up symbols, charts, and indicators
        pass

    async def next(self) -> None:
        # Implement your trading logic here
        pass
```

### 3. `project/position_manager.py` - Position Management

Handle position-related events and risk management:

```python
from proalgotrader_core.protocols.position_manager import PositionManagerProtocol

class PositionManager(PositionManagerProtocol):
    def __init__(self, algorithm: AlgorithmProtocol) -> None:
        self.algorithm = algorithm

    async def initialize(self) -> None:
        # Initialize position manager
        pass

    async def next(self) -> None:
        # Called on every algorithm iteration
        # Handle position management logic here
        pass
```

## Environment Configuration

### Environment Configuration

Your strategy repository includes a `.env.example` file that serves as a template for the required environment variables:

```env
# Session credentials from proalgotrader.com
ALGO_SESSION_KEY=your_session_key_here
ALGO_SESSION_SECRET=your_session_secret_here
```

**Setup Process:**

1. Copy `.env.example` to `.env`
2. Replace placeholder values with your actual session credentials
3. Never commit the `.env` file to version control

### `requirements.txt`

Your project dependencies:

```txt
proalgotrader-core>=1.0.0
python-dotenv>=1.0.0
```

## Strategy Development Workflow

### 1. **Setup**

```bash
# Clone your strategy repository
git clone <your-strategy-repo-url>
cd <strategy-name>

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configure**

```bash
# Copy environment template
cp .env.example .env

# Edit with your session credentials
nano .env
```

### 3. **Develop**

```bash
# Edit your strategy files
nano project/strategy.py
nano project/position_manager.py
```

### 4. **Test**

```bash
# Run your strategy
python main.py
```

### 5. **Deploy**

```bash
# Deploy your strategy
python main.py
```

## Best Practices

### 1. **Code Organization**

- Keep trading logic in `strategy.py`
- Separate position management in `position_manager.py`

### 2. **Version Control**

```bash
# Commit your changes
git add .
git commit -m "Update strategy logic"

# Push to your repository
git push origin main
```

### 3. **Testing**

- Always test your strategy thoroughly before live trading
- Use the `tests/` directory for unit tests
- Validate your strategy logic before live trading

### 4. **Risk Management**

- Implement stop-losses in `position_manager.py`
- Set position size limits
- Monitor daily loss limits

## Common Patterns

### 1. **Simple Strategy Structure**

```python
async def next(self) -> None:
    # Check if we can open new positions
    if len(self.algorithm.positions) >= self.max_positions:
        return

    # Get market data
    current_price = self.symbol.ltp

    # Generate signals
    if self.should_buy(current_price):
        await self.algorithm.buy(
            broker_symbol=self.symbol,
            quantities=self.position_size
        )
```

### 2. **Position Management**

```python
async def manage_risk(self) -> None:
    for position in self.algorithm.positions:
        # Check stop loss
        if self.is_stop_loss_hit(position):
            await self.algorithm.exit_position(position)

        # Check take profit
        if self.is_take_profit_hit(position):
            await self.algorithm.exit_position(position)
```

### 3. **Indicator Usage**

```python
async def initialize(self) -> None:
    # Add RSI indicator
    self.rsi = await self.chart.add_indicator(
        key="rsi_14",
        indicator=Indicators.Momentum.RSI(period=14)
    )

async def next(self) -> None:
    # Get RSI value
    rsi_value = await self.rsi.get_data(0, "close")

    # Use in trading logic
    if rsi_value < 30:  # Oversold
        # Generate buy signal
        pass
```

## Next Steps

1. **Read the [Quick Start Guide](quick-start.md)** to build your first strategy
2. **Explore [Built-in Indicators](../indicators/built-in-indicators.md)** for technical analysis
3. **Learn about [Custom Indicators](../indicators/custom-indicators-guide.md)** for advanced strategies
4. **Check [API Reference](../api-reference/)** for complete framework documentation

---

**Ready to build your strategy?** Start with the quick start guide and begin developing profitable algorithmic trading strategies! 🚀📈
