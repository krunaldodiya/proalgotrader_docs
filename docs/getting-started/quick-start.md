# Quick Start Guide

## Overview

This guide will help you get started with ProAlgoTrader Core, a powerful algorithmic trading framework for Python. ProAlgoTrader is a comprehensive SaaS platform that consists of:

1. **proalgotrader.com** - Web platform for project management and strategy marketplace
2. **proalgotrader_core** - Python framework for building and running trading strategies locally

## How It Works

1. **Sign up** at proalgotrader.com
2. **Create a project** with your chosen broker and strategy
3. **Get session credentials** (ALGO_SESSION_KEY and ALGO_SESSION_SECRET)
4. **Clone strategy repository** (for custom strategies) or use marketplace strategy
5. **Install proalgotrader_core** locally
6. **Run your strategy** with `python main.py`

## Prerequisites

- **Web Browser**: For accessing proalgotrader.com
- **Python 3.13+**: Required for proalgotrader_core
- **Git**: For cloning strategy repositories (for custom strategies)
- **pip** (Python package installer)
- **Broker Account**: Active account with Fyers, Angel One, or Shoonya
- **GitHub Account**: For custom strategy development (optional)

## Installation

### 1. Sign Up and Create Project

1. **Sign up** at [proalgotrader.com](https://proalgotrader.com)
2. **Create a project** with your chosen broker and strategy
3. **Get session credentials** (ALGO_SESSION_KEY and ALGO_SESSION_SECRET)

### 2. Clone Strategy Repository (Custom Strategies)

```bash
# Clone your strategy repository
git clone <your-strategy-repo-url>
cd <strategy-name>
```

### 3. Set Up Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
# Install all dependencies (including proalgotrader-core)
pip install -r requirements.txt
```

### 5. Project Structure

Your strategy repository already includes the following structure:

```
my-trading-bot/
├── main.py                    # Entry point
├── project/
│   ├── strategy.py            # Your trading strategy
│   └── position_manager.py    # Position management logic
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
└── .env                      # Your environment variables (created from .env.example)
```

## Basic Setup

### 1. Your main.py is Ready!

Your strategy repository already includes `main.py` with the correct setup:

```python
# main.py
from project.strategy import Strategy

from proalgotrader_core.start import run_strategy


if __name__ == "__main__":
    run_strategy(strategy=Strategy)
```

### 2. Your Strategy Files Are Ready!

Your strategy repository already includes all the necessary files:

- **`project/strategy.py`** - Main trading strategy (ready to customize)
- **`project/position_manager.py`** - Position management logic

You can start editing these files to implement your trading logic.

### 4. Configure Environment Variables

Your strategy repository comes with a `.env.example` file. You need to:

```bash
# Copy the environment template
cp .env.example .env

# Edit with your actual credentials
nano .env  # or use your preferred editor
```

**What's in .env.example:**

```env
# ProAlgoTrader session credentials
ALGO_SESSION_KEY=your_session_key_here
ALGO_SESSION_SECRET=your_session_secret_here
```

**Important:** Replace the placeholder values with your actual credentials from proalgotrader.com

## Running Your First Strategy

### 1. Install Dependencies

```bash
# Install all dependencies (including proalgotrader-core)
pip install -r requirements.txt
```

### 2. Configure Session Credentials

Edit the `.env` file with your ProAlgoTrader session credentials:

- **ALGO_SESSION_KEY**: From your project dashboard at proalgotrader.com
- **ALGO_SESSION_SECRET**: From your project dashboard at proalgotrader.com

**Note**: Your strategy repository includes a `.env.example` file as a template.

### 3. Run the Strategy

```bash
python main.py
```

Your strategy will start running and:

- Connect to your broker
- Subscribe to market data
- Execute trades based on your logic
- Manage positions automatically

## Understanding the Code

### The `Strategy` Class

The `Strategy` class is the heart of your trading algorithm. It's where you'll define your trading logic, manage symbols, and configure the behavior of your bot.

Here is a basic `strategy.py` file to get you started:

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
        # This is where you will add symbols, charts, and indicators
        pass

    async def next(self) -> None:
        # This is where you will implement your trading logic
        pass
```

### Key Components

- **`Strategy(Algorithm)`**: Your main class inherits from `Algorithm`, giving you access to all the trading functionalities.
- **`__init__()`**: This is the constructor of your strategy. It's the perfect place to set up your algorithm's configuration.
  - `set_account_type()`: Define the account type you'll be trading with (e.g., `DERIVATIVE_POSITIONAL`, `CASH_INTRADAY`).
  - `set_position_manager()`: Assign your custom `PositionManager` to handle position-related events.
  - `set_interval()`: Set the frequency (in `timedelta`) for the `next()` method to be called.

### Data Access

Both charts and indicators provide easy access to their data:

**Chart Data Access:**

```python
# Get current close price
current_close = await chart.get_data(0, "close")

# Get previous high price
previous_high = await chart.get_data(1, "high")

# Get full DataFrame
chart_data = chart.data
```

**Indicator Data Access:**

```python
# Get current RSI value
current_rsi = await rsi.get_data(0, "rsi")

# Get previous RSI value
previous_rsi = await rsi.get_data(1, "rsi")

# Get full indicator DataFrame
indicator_data = rsi.data
```

**Row Number System:**

- Row 0: Most recent data point
- Row 1: Previous data point
- Row 2: Two periods ago

- **`initialize()`**: This asynchronous method is called once at the start of the trading session. Use it to:
  - Add the symbols you want to trade (`add_equity`, `add_future`, `add_option`).
  - Create charts for your symbols (`add_chart`).
  - Register any indicators you need.
- **`next()`**: This asynchronous method is called repeatedly at the interval you defined. This is where you'll implement your core trading logic, such as:
  - Checking for trading signals.
  - Placing `buy` or `sell` orders.
  - Managing your open positions.

## Next Steps

Now that you have a basic understanding of the `Strategy` class, you can move on to:

- **Adding Indicators**: Learn how to add technical indicators to your charts.
- **Implementing Risk Management**: Set up rules to manage your risk.
- **Trading with Multiple Symbols**: Expand your strategy to trade more than one symbol.
- **Exploring Options Trading**: Dive into the world of options trading.

Check out the rest of the documentation for more in-depth guides and examples.

---

**Ready to start trading?** Follow this guide to create your first algorithmic trading strategy with ProAlgoTrader Core! 🚀
