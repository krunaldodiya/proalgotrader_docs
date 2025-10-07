# Iron Condor Options Strategy Example

This example demonstrates a comprehensive Iron Condor options selling strategy with hedging for income generation and risk management.

## Files

- `main.py` - Entry point to run the strategy
- `strategy.py` - Main Iron Condor strategy implementation
- `position_manager.py` - Position manager for options trades
- `README.md` - This documentation

## Strategy Logic

The Iron Condor is a **neutral options strategy** that profits from low volatility and time decay with a **wider profit zone** than Iron Butterfly:

- **Sell OTM Call & Put**: Generate premium income
- **Buy Further OTM Call & Put**: Limit maximum loss (hedging)
- **Net Credit**: Receive more premium than paid
- **Wider Profit Zone**: Between the inner strikes
- **Max Loss**: Limited to net debit paid

## Strategy Components

### Iron Condor Structure

```
Strike Prices: [Far OTM Put] [OTM Put] [OTM Call] [Far OTM Call]
Positions:     [BUY]         [SELL]    [SELL]    [BUY]
```

### Example with Nifty at 19,000:

- **Buy PE 18,800** (Far OTM Put) - Hedge
- **Sell PE 18,900** (OTM Put) - Income
- **Sell CE 19,100** (OTM Call) - Income
- **Buy CE 19,200** (Far OTM Call) - Hedge

## Key Features

- ✅ **Premium Collection**: Sells OTM options for income
- ✅ **Risk Hedging**: Buys further OTM options to limit losses
- ✅ **Wider Profit Zone**: Larger range for profit than Iron Butterfly
- ✅ **Neutral Strategy**: Profits from low volatility
- ✅ **Time Decay**: Benefits from theta (time decay)
- ✅ **Risk Management**: Limited maximum loss
- ✅ **Weekly Expiry**: Trades current week options

## Strategy Parameters

### Option Selection

```python
# Strike price offsets from ATM
inner_strike_offset = 10  # 10 points OTM for selling
outer_strike_offset = 20  # 20 points OTM for hedging

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

## Iron Condor vs Iron Butterfly

### Iron Condor

- **4 Different Strikes**: Wider profit zone
- **Sell OTM Options**: Lower premium but wider range
- **Buy Further OTM**: Cheaper hedging
- **Profit Zone**: Between inner strikes

### Iron Butterfly

- **3 Strikes (2 Same)**: Narrower profit zone
- **Sell ATM Options**: Higher premium but narrow range
- **Buy Adjacent OTM**: More expensive hedging
- **Profit Zone**: Around ATM strike

## Iron Condor Explained

### What is Iron Condor?

The Iron Condor is a **four-leg options strategy** that combines:

1. **Short Strangle** (Sell OTM Call + Put)
2. **Long Strangle** (Buy Further OTM Call + Put)

### Profit & Loss Profile

- **Maximum Profit**: Net premium received
- **Maximum Loss**: Net debit paid (limited)
- **Breakeven Points**: 2 breakeven levels
- **Profit Zone**: Between inner strikes (wider than Iron Butterfly)

### When to Use

- **Low Volatility**: When expecting sideways movement
- **Wider Range**: When price can move within a range
- **Time Decay**: Close to expiry for maximum theta
- **Income Generation**: Regular premium collection
- **Lower Risk**: Compared to Iron Butterfly

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
# Far OTM Call (Hedge)
ce_far_otm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="CE",
    strike_price_input=20,  # 20 points OTM
)

# OTM Call (Sell)
ce_otm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="CE",
    strike_price_input=10,  # 10 points OTM
)

# OTM Put (Sell)
pe_otm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="PE",
    strike_price_input=-10,  # 10 points OTM
)

# Far OTM Put (Hedge)
pe_far_otm = await self.add_option(
    symbol_name=SymbolType.Index.NIFTY,
    expiry_input=("Weekly", 0),
    option_type="PE",
    strike_price_input=-20,  # 20 points OTM
)
```

### Order Execution

```python
order_items = [
    # Buy Far OTM Call (Hedge)
    OrderItem(ce_far_otm, PositionType.BUY, 1),
    # Sell OTM Call (Income)
    OrderItem(ce_otm, PositionType.SELL, 1),
    # Sell OTM Put (Income)
    OrderItem(pe_otm, PositionType.SELL, 1),
    # Buy Far OTM Put (Hedge)
    OrderItem(pe_far_otm, PositionType.BUY, 1),
]

await self.create_multiple_orders(order_items=order_items)
```

## Risk Management

### Position Sizing

- **Lot Size**: 1 lot per trade (adjustable)
- **Capital Allocation**: Based on risk tolerance
- **Maximum Positions**: 1 Iron Condor at a time

### Loss Limits

- **Maximum Loss**: ₹500 per trade
- **Stop Loss**: Exit if loss exceeds threshold
- **Position Monitoring**: Real-time P&L tracking

### Hedging Benefits

- **Limited Risk**: Maximum loss is net debit paid
- **Premium Collection**: Earn from time decay
- **Wider Range**: More forgiving than Iron Butterfly
- **Lower Cost**: Cheaper hedging options

## Example Scenarios

### Scenario 1: Profitable Trade

```
Nifty Price: 19,000
Strategy: Iron Condor 18,800/18,900/19,100/19,200

Entry:
- Buy PE 18,800: ₹30 (debit)
- Sell PE 18,900: ₹80 (credit)
- Sell CE 19,100: ₹80 (credit)
- Buy CE 19,200: ₹30 (debit)

Net Credit: ₹100 (₹160 credit - ₹60 debit)

Exit at Expiry (Nifty = 19,000):
- All options expire worthless
- Profit: ₹100 (net credit received)
```

### Scenario 2: Partial Loss Scenario

```
Nifty Price: 19,000 → 19,050 (moves up slightly)

Exit at Expiry:
- PE 18,800: Expires worthless (₹0)
- PE 18,900: Expires worthless (₹0)
- CE 19,100: Exercise value ₹50 (loss)
- CE 19,200: Expires worthless (₹0)

Net Loss: ₹50 (₹50 loss - ₹0 gain)
```

### Scenario 3: Maximum Loss Scenario

```
Nifty Price: 19,000 → 19,300 (moves up significantly)

Exit at Expiry:
- PE 18,800: Expires worthless (₹0)
- PE 18,900: Expires worthless (₹0)
- CE 19,100: Exercise value ₹200 (loss)
- CE 19,200: Exercise value ₹100 (gain)

Net Loss: ₹100 (₹200 loss - ₹100 gain)
```

## Performance Tracking

### Key Metrics

- **Total Trades**: Number of Iron Condor trades
- **Win Rate**: Percentage of profitable trades
- **Average Profit**: Average profit per trade
- **Maximum Drawdown**: Largest consecutive losses
- **Premium Collected**: Total premium received
- **Profit Zone Hit Rate**: How often price stays in profit zone

### Trade Logging

```
🦅 IRON CONDOR TRADE EXECUTED
   Symbol: NIFTY
   Expiry: Weekly
   Strikes: 18,800/18,900/19,100/19,200
   Net Credit: ₹100
   Max Loss: ₹100
   Profit Zone: 18,900 - 19,100
==================================================
```

## Best Practices

### Market Conditions

- **Low Volatility**: Best for Iron Condor
- **Range Bound**: Price stays within profit zone
- **Time Decay**: Close to expiry preferred
- **Liquidity**: Ensure good option liquidity

### Strike Selection

- **Inner Strikes**: Choose based on expected range
- **Outer Strikes**: Far enough to limit risk
- **Strike Width**: Balance between premium and risk
- **Volatility**: Consider implied volatility

### Risk Management

- **Position Sizing**: Start with small lot sizes
- **Loss Limits**: Set strict maximum loss
- **Monitoring**: Watch position closely
- **Exit Strategy**: Have clear exit rules

## Configuration

### Strike Price Offsets

```python
# Conservative (wider wings)
inner_strike_offset = 15  # 15 points OTM
outer_strike_offset = 30  # 30 points OTM

# Aggressive (narrower wings)
inner_strike_offset = 10  # 10 points OTM
outer_strike_offset = 20  # 20 points OTM
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
- Create Iron Condor positions
- Monitor positions for exit
- Manage risk according to limits

## Example Output

```
🦅 IRON CONDOR STRATEGY STARTED
📊 Market: NIFTY
⏰ Expiry: Weekly
💰 Max Loss: ₹500
==================================================

🦅 IRON CONDOR TRADE EXECUTED
   Symbol: NIFTY
   Expiry: Weekly
   Strikes: 18,800/18,900/19,100/19,200
   Net Credit: ₹120
   Max Loss: ₹80
   Profit Zone: 18,900 - 19,100
==================================================

📈 POSITION MONITORING
   Current P&L: ₹45
   Time to Expiry: 2 days
   Status: Profitable
   Nifty Price: 19,025 (In Profit Zone)
==================================================
```

## Iron Condor vs Other Strategies

### vs Iron Butterfly

- **Wider Profit Zone**: More forgiving
- **Lower Premium**: Less income per trade
- **Lower Risk**: Cheaper hedging
- **Better for Beginners**: More room for error

### vs Straddle

- **Limited Risk**: Defined maximum loss
- **Lower Premium**: Less income
- **Wider Range**: More forgiving
- **Hedged**: Protected against big moves

### vs Strangle

- **Limited Risk**: Defined maximum loss
- **Lower Premium**: Less income
- **Wider Range**: More forgiving
- **Hedged**: Protected against big moves

## Next Steps

- Check out [Iron Butterfly Strategy](../iron-butterfly-strategy/) for comparison
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
