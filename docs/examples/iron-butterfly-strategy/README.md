# Iron Butterfly Options Strategy Example

This example demonstrates a comprehensive Iron Butterfly options selling strategy with hedging for income generation and risk management.

## Files

- `main.py` - Entry point to run the strategy
- `strategy.py` - Main Iron Butterfly strategy implementation
- `position_manager.py` - Position manager for options trades
- `README.md` - This documentation

## Strategy Logic

The Iron Butterfly is a **neutral options strategy** that profits from low volatility and time decay:

- **Sell ATM Call & Put**: Generate premium income
- **Buy OTM Call & Put**: Limit maximum loss (hedging)
- **Net Credit**: Receive more premium than paid
- **Profit Zone**: Between the breakeven points
- **Max Loss**: Limited to net debit paid

## Strategy Components

### Iron Butterfly Structure

```
Strike Prices: [OTM Put] [ATM Put] [ATM Call] [OTM Call]
Positions:     [BUY]     [SELL]    [SELL]    [BUY]
```

### Example with Nifty at 19,000:

- **Buy PE 18,900** (OTM Put) - Hedge
- **Sell PE 19,000** (ATM Put) - Income
- **Sell CE 19,000** (ATM Call) - Income
- **Buy CE 19,100** (OTM Call) - Hedge

## Key Features

- ✅ **Premium Collection**: Sells ATM options for income
- ✅ **Risk Hedging**: Buys OTM options to limit losses
- ✅ **Neutral Strategy**: Profits from low volatility
- ✅ **Time Decay**: Benefits from theta (time decay)
- ✅ **Risk Management**: Limited maximum loss
- ✅ **Weekly Expiry**: Trades current week options

## Strategy Parameters

### Option Selection

```python
# Strike price offsets from ATM
otm_strike_offset = 5  # 5 points OTM for hedging
atm_strike_offset = 0  # ATM for selling

# Expiry selection
expiry = ("Weekly", 0)  # Current week expiry
```

### Risk Management

```python
# Maximum loss threshold
max_loss = 500  # ₹500 maximum loss per trade

# Position sizing
lot_size = 1  # 1 lot per trade
```

## Iron Butterfly Explained

### What is Iron Butterfly?

The Iron Butterfly is a **four-leg options strategy** that combines:

1. **Short Straddle** (Sell ATM Call + Put)
2. **Long Strangle** (Buy OTM Call + Put)

### Profit & Loss Profile

- **Maximum Profit**: Net premium received
- **Maximum Loss**: Net debit paid (limited)
- **Breakeven Points**: 2 breakeven levels
- **Profit Zone**: Between breakeven points

### When to Use

- **Low Volatility**: When expecting sideways movement
- **Time Decay**: Close to expiry for maximum theta
- **Range Bound**: When price stays within breakeven points
- **Income Generation**: Regular premium collection

## Strategy Implementation

### Entry Conditions

```python
def should_trade(self):
    # No pending orders
    if len(self.pending_orders) > 0:
        return False

    # No existing positions
    if len(self.positions) > 0:
        return False

    # Within loss limits
    if self.net_pnl.loss >= 500:
        return False

    return True
```

### Option Legs Creation

```python
# OTM Call (Hedge)
ce_otm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="CE",
    strike_price_input=5,  # 5 points OTM
)

# ATM Call (Sell)
ce_atm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="CE",
    strike_price_input=0,  # ATM
)

# ATM Put (Sell)
pe_atm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="PE",
    strike_price_input=0,  # ATM
)

# OTM Put (Hedge)
pe_otm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="PE",
    strike_price_input=-5,  # 5 points OTM
)
```

### Order Execution

```python
order_items = [
    # Buy OTM Call (Hedge)
    OrderItem(ce_otm, PositionType.BUY, 1),
    # Sell ATM Call (Income)
    OrderItem(ce_atm, PositionType.SELL, 1),
    # Sell ATM Put (Income)
    OrderItem(pe_atm, PositionType.SELL, 1),
    # Buy OTM Put (Hedge)
    OrderItem(pe_otm, PositionType.BUY, 1),
]

await self.create_multiple_orders(order_items=order_items)
```

## Risk Management

### Position Sizing

- **Lot Size**: 1 lot per trade (adjustable)
- **Capital Allocation**: Based on risk tolerance
- **Maximum Positions**: 1 Iron Butterfly at a time

### Loss Limits

- **Maximum Loss**: ₹500 per trade
- **Stop Loss**: Exit if loss exceeds threshold
- **Position Monitoring**: Real-time P&L tracking

### Hedging Benefits

- **Limited Risk**: Maximum loss is net debit paid
- **Premium Collection**: Earn from time decay
- **Volatility Protection**: Profits from low volatility

## Example Scenarios

### Scenario 1: Profitable Trade

```
Nifty Price: 19,000
Strategy: Iron Butterfly 18,900/19,000/19,100

Entry:
- Buy PE 18,900: ₹50 (debit)
- Sell PE 19,000: ₹100 (credit)
- Sell CE 19,000: ₹100 (credit)
- Buy CE 19,100: ₹50 (debit)

Net Credit: ₹100 (₹200 credit - ₹100 debit)

Exit at Expiry (Nifty = 19,000):
- All options expire worthless
- Profit: ₹100 (net credit received)
```

### Scenario 2: Loss Scenario

```
Nifty Price: 19,000 → 19,200 (moves up)

Exit at Expiry:
- PE 18,900: Expires worthless (₹0)
- PE 19,000: Expires worthless (₹0)
- CE 19,000: Exercise value ₹200 (loss)
- CE 19,100: Exercise value ₹100 (gain)

Net Loss: ₹100 (₹200 loss - ₹100 gain)
```

## Performance Tracking

### Key Metrics

- **Total Trades**: Number of Iron Butterfly trades
- **Win Rate**: Percentage of profitable trades
- **Average Profit**: Average profit per trade
- **Maximum Drawdown**: Largest consecutive losses
- **Premium Collected**: Total premium received

### Trade Logging

```
🦋 IRON BUTTERFLY TRADE EXECUTED
   Symbol: NIFTY
   Expiry: Weekly
   Strikes: 18,900/19,000/19,100
   Net Credit: ₹100
   Max Loss: ₹100
   Breakeven: 18,900 - 19,100
==================================================
```

## Best Practices

### Market Conditions

- **Low Volatility**: Best for Iron Butterfly
- **Range Bound**: Price stays within breakeven
- **Time Decay**: Close to expiry preferred
- **Liquidity**: Ensure good option liquidity

### Risk Management

- **Position Sizing**: Start with small lot sizes
- **Loss Limits**: Set strict maximum loss
- **Monitoring**: Watch position closely
- **Exit Strategy**: Have clear exit rules

### Option Selection

- **Strike Selection**: Choose appropriate strikes
- **Expiry Selection**: Weekly options preferred
- **Liquidity**: Ensure good bid-ask spreads
- **Greeks**: Understand delta, gamma, theta

## Configuration

### Strike Price Offsets

```python
# Conservative (wider wings)
otm_strike_offset = 10  # 10 points OTM

# Aggressive (narrower wings)
otm_strike_offset = 5   # 5 points OTM
```

### Risk Parameters

```python
# Conservative risk
max_loss = 300  # ₹300 maximum loss

# Aggressive risk
max_loss = 500  # ₹500 maximum loss
```

## Usage

```bash
python main.py
```

The strategy will automatically:

- Connect to your broker
- Check market conditions
- Create Iron Butterfly positions
- Monitor positions for exit
- Manage risk according to limits

## Example Output

```
🦋 IRON BUTTERFLY STRATEGY STARTED
📊 Market: NIFTY
⏰ Expiry: Weekly
💰 Max Loss: ₹500
==================================================

🦋 IRON BUTTERFLY TRADE EXECUTED
   Symbol: NIFTY
   Expiry: Weekly
   Strikes: 18,900/19,000/19,100
   Net Credit: ₹120
   Max Loss: ₹80
   Breakeven: 18,900 - 19,100
==================================================

📈 POSITION MONITORING
   Current P&L: ₹45
   Time to Expiry: 2 days
   Status: Profitable
==================================================
```

## Next Steps

- Check out [Basic Strategy](../basic-strategy/) for a simple template
- Read the [API Reference](../../api-reference/) for detailed documentation
- Explore [Trading and Strategy](../../trading-and-strategy/) for advanced topics
- Study [Options Trading](../../trading-and-strategy/) for more strategies

## Disclaimer

This is an educational example. Options trading involves significant risk:

- **Limited Risk**: Maximum loss is net debit paid
- **Time Decay**: Options lose value over time
- **Volatility Risk**: High volatility can cause losses
- **Assignment Risk**: Early assignment possible
- **Liquidity Risk**: May be difficult to exit

Always:

- Understand the risks involved
- Start with paper trading
- Use proper position sizing
- Have clear exit strategies
- Consult with financial advisors
- Never invest more than you can afford to lose
