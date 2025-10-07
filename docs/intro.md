---
sidebar_position: 1
title: Introduction
description: Welcome to ProAlgoTrader - a powerful algorithmic trading platform
---

# ProAlgoTrader Documentation

Welcome to the comprehensive documentation for ProAlgoTrader - a powerful algorithmic trading platform that helps you build and run profitable trading strategies.

## 🚀 Quick Start

Get up and running with your algorithmic trading strategy in minutes:

```bash
# Clone your strategy repository
git clone <your-strategy-repo-url>
cd <strategy-name>

# Install dependencies
pip install -r requirements.txt

# Run your strategy
python main.py
```

## 📚 Documentation Structure

### Getting Started

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quick-start.md)
- [Project Structure](getting-started/project-structure.md)

### Core Concepts

- [Algorithm Overview](core-concepts/algorithm-overview.md)
- [Data Access Guide](core-concepts/data-access.md)
- [Session Management](core-concepts/session-management.md)
- [API Integration](core-concepts/api-integration.md)

### Indicators

- [Built-in Indicators](indicators/built-in-indicators.md)
- [Custom Indicators Guide](indicators/custom-indicators-guide.md)
- [Indicator Quick Reference](indicators/indicator-quick-reference.md)
- [TradingView Indicators](indicators/tradingview-indicators.md)

### Trading & Strategy

- [Order Management](trading/order-management.md)
- [Position Management](trading/position-management.md)
- [Signal Management](trading/signal-management.md)
- [Risk Management](trading/risk-management.md)

### Brokers & Integration

- [Supported Brokers](brokers/supported-brokers.md)
- [Fyers Integration](brokers/fyers-integration.md)
- [Angel One Integration](brokers/angel-one-integration.md)
- [Shoonya Integration](brokers/shoonya-integration.md)

### Development

- [Development Setup](development/development-setup.md)
- [Contributing Guidelines](development/contributing.md)
- [Testing Guide](development/testing.md)
- [Deployment Guide](development/deployment.md)

### API Reference

- [Core API Reference](api-reference/core-api.md)
- [Indicators API](api-reference/indicators-api.md)
- [Trading API](api-reference/trading-api.md)

### Examples

- [Basic Examples](examples/basic-examples.md)
- [Advanced Examples](examples/advanced-examples.md)
- [Strategy Examples](examples/strategy-examples.md)

## 🎯 Key Features

- ✅ **Strategy Templates**: Pre-built strategy templates ready for customization
- ✅ **Built-in Indicators**: RSI, MACD, Bollinger Bands, ATR, and more
- ✅ **Custom Indicators**: Create any indicator using polars_talib
- ✅ **High Performance**: Built on Polars for fast data processing
- ✅ **Multi-Broker Support**: Fyers, Angel One, Shoonya, and more
- ✅ **Real-time Trading**: Live market data and order execution
- ✅ **Paper Trading**: Test strategies risk-free before going live

## 📖 Quick Example

```python
from proalgotrader_core.algorithm import Algorithm
from proalgotrader_core.protocols.strategy import StrategyProtocol

class MyStrategy(StrategyProtocol):
    def __init__(self, algorithm: Algorithm) -> None:
        self.algorithm = algorithm

    async def initialize(self) -> None:
        # Set up your trading symbols and indicators
        pass

    async def next(self) -> None:
        # Implement your trading logic here
        pass
```

## 🤝 Community

Join our community of algorithmic traders:

- 📖 Documentation: This site
- 💬 Forums: Connect with other traders
- 🎥 Tutorials: Video guides and examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@proalgotrader.com
- 📖 Documentation: This site
- 💬 Community: Join our forums

---

**ProAlgoTrader** - Build profitable algorithmic trading strategies with ease! 🚀📈
