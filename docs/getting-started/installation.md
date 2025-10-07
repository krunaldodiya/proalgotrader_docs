# Getting Started with Your Strategy

This guide will help you set up and start developing your algorithmic trading strategy using ProAlgoTrader.

## Prerequisites

Before getting started with your strategy, ensure you have:

- **Python 3.13+** - Required for running strategies
- **Git** - For cloning your strategy repository
- **pip** - Python package installer

## Step 1: Clone Your Strategy Repository

When you create a custom strategy at proalgotrader.com, you'll get a GitHub repository URL. Clone it:

```bash
# Clone your strategy repository
git clone <your-strategy-repo-url>
cd <strategy-name>

# Verify the structure
ls -la
```

**Expected Structure:**

```
your-strategy-name/
├── .env.example              # Environment template
├── README.md                 # Strategy documentation
├── requirements.txt          # Dependencies
├── main.py                   # Entry point to run your strategy
├── project/                  # Your strategy implementation
│   ├── strategy.py           # Main trading strategy
│   ├── position_manager.py   # Position management logic
│   └── custom_indicators.py  # Custom technical indicators
└── tests/                    # Strategy tests
```

## Step 2: Install Dependencies

Your strategy repository includes a `requirements.txt` file with all necessary dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies (including proalgotrader-core)
pip install -r requirements.txt
```

## Step 3: Configure Your Environment

### 1. Get Session Credentials

1. **Sign up** at [proalgotrader.com](https://proalgotrader.com)
2. **Create a project** with your chosen broker and strategy
3. **Get session credentials** (ALGO_SESSION_KEY and ALGO_SESSION_SECRET) from your project dashboard

### 2. Configure Environment Variables

Your strategy repository comes with a `.env.example` file that contains the required environment variables. You need to:

```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file with your actual credentials
nano .env  # or use your preferred editor
```

**What's in .env.example:**

The `.env.example` file contains template values that you need to replace with your actual session credentials:

```env
# ProAlgoTrader Session Credentials
ALGO_SESSION_KEY=your_session_key_here
ALGO_SESSION_SECRET=your_session_secret_here
```

**Important:** Never commit your actual `.env` file to version control. The `.env.example` file serves as a template showing what session credentials are needed.

## Step 4: Verify Setup

### 1. Check Dependencies

```bash
# Verify all dependencies are installed
python -c "import proalgotrader_core; print('✓ ProAlgoTrader Core ready!')"
```

### 2. Test Your Strategy

```bash
# Run your strategy
python main.py
```

**Note**: Your strategy will automatically use the appropriate trading mode based on your session configuration.

## Your Strategy Files

Your repository includes these key files ready for customization:

### `project/strategy.py` - Main Trading Logic

```python
from datetime import timedelta

from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.enums.account_type import AccountType
from project.position_manager import PositionManager


class Strategy(Algorithm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.set_account_type(account_type=AccountType.DERIVATIVE_POSITIONAL)

        self.set_position_manager(position_manager=PositionManager)

        self.set_interval(interval=timedelta(seconds=1))

    async def initialize(self) -> None:
        pass

    async def next(self) -> None:
        pass
```

### `project/position_manager.py` - Position Management

ProAlgoTrader supports two types of position managers:

#### Single Position Manager (Global Management)

```python
from proalgotrader_core.protocols.position_manager import PositionManagerProtocol
from proalgotrader_core.protocols.algorithm import AlgorithmProtocol
from proalgotrader_core.protocols.position import PositionProtocol

class PositionManager(PositionManagerProtocol):
    def __init__(self, algorithm: AlgorithmProtocol) -> None:
        self.algorithm = algorithm

    async def initialize(self) -> None:
        # Initialize your position manager
        pass


    async def next(self) -> None:
        # Called on every algorithm iteration
        pass
```

#### Multiple Position Manager (Per-Position Management)

```python
from proalgotrader_core.protocols.multiple_position_manager import MultiplePositionManagerProtocol
from proalgotrader_core.protocols.algorithm import AlgorithmProtocol
from proalgotrader_core.protocols.position import PositionProtocol

class MultiplePositionManager(MultiplePositionManagerProtocol):
    def __init__(self, algorithm: AlgorithmProtocol, position: PositionProtocol) -> None:
        self.algorithm = algorithm
        self.position = position

    async def initialize(self) -> None:
        # Initialize for this specific position
        pass


    async def next(self) -> None:
        # Called on every algorithm iteration for this position
        pass
```

## Development Workflow

### 1. **Edit Your Strategy**

```bash
# Edit strategy files
nano project/strategy.py
nano project/position_manager.py
```

### 2. **Test Changes**

```bash
# Run in paper trading mode
python main.py
```

### 3. **Version Control**

```bash
# Commit your changes
git add .
git commit -m "Update strategy logic"

# Push to your repository
git push origin main
```

## Supported Brokers

ProAlgoTrader supports:

- **Fyers** - Equity, F&O, Currency, Commodity trading
- **Angel One** - Equity, F&O, Currency trading
- **Shoonya** - Equity, F&O trading

## Troubleshooting

### Common Issues

#### 1. Import Errors

```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

#### 2. Session Connection Issues

```bash
# Check credentials
cat .env | grep -E "(ALGO_SESSION_KEY|ALGO_SESSION_SECRET)"

# Verify project status at proalgotrader.com
```

#### 3. Strategy Not Running

```bash
# Check logs
tail -f logs/proalgotrader.log

# Verify market hours
# Strategy only runs during market hours
```

### Getting Help

1. **Documentation**: Check [API Reference](../api-reference/) for framework details
2. **Community**: Join ProAlgoTrader community forums
3. **Support**: Contact support at support@proalgotrader.com

## Next Steps

1. **Read the [Quick Start Guide](quick-start.md)** to build your first strategy
2. **Explore [Built-in Indicators](../indicators/built-in-indicators.md)** for technical analysis
3. **Learn about [Custom Indicators](../indicators/custom-indicators-guide.md)** for advanced strategies
4. **Check [API Reference](../api-reference/)** for complete framework documentation

---

**Ready to start trading?** Your strategy is set up and ready for development! 🚀📈
