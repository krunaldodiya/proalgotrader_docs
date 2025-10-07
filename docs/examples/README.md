# Examples

This section contains practical examples of ProAlgoTrader strategies.

## Available Examples

### [Basic Strategy](basic-strategy/)

A minimal strategy template showing the basic structure and setup required to create a trading strategy.

**Features:**

- Basic strategy class setup
- Symbol and chart initialization
- Lifecycle method examples
- Minimal configuration

### [SMA Crossover Strategy](sma-crossover-strategy/)

A complete SMA 20 vs SMA 50 crossover strategy for Nifty options trading.

**Features:**

- Built-in SMA indicators
- Real-time signal generation
- Options trading (CE/PE)
- Position management with net PnL tracking
- Risk management

### [Swing Trading Strategy](swing-trading-strategy/)

A comprehensive swing trading strategy using Golden Crossover signals (50-day vs 200-day SMA) for long-term trend following.

**Features:**

- Golden Crossover signal detection
- Daily timeframe for swing trading
- Multiple symbol support
- Position management with stop loss/take profit
- Risk management and performance tracking

### [Iron Butterfly Strategy](iron-butterfly-strategy/)

A comprehensive Iron Butterfly options selling strategy with hedging for income generation and risk management.

**Features:**

- Neutral options strategy for income generation
- Four-leg options structure (Buy OTM, Sell ATM)
- Risk hedging with limited maximum loss
- Premium collection from time decay
- Weekly options trading with risk management

### [Iron Condor Strategy](iron-condor-strategy/)

A comprehensive Iron Condor options selling strategy with wider profit zone and hedging for income generation.

**Features:**

- Neutral options strategy with wider profit zone
- Four-leg options structure (Buy Far OTM, Sell OTM)
- Risk hedging with limited maximum loss
- Premium collection from time decay
- More forgiving than Iron Butterfly strategy

## Getting Started

1. Choose an example that matches your needs
2. Navigate to the example directory
3. Read the README.md for detailed information
4. Copy the strategy code to your project
5. Customize as needed

## Next Steps

- Read the [API Reference](../api-reference/) for detailed documentation
- Check out [Core Concepts](../core-concepts/) for fundamental understanding
- Explore [Trading and Strategy](../trading-and-strategy/) for advanced topics
