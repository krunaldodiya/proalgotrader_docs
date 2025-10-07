# Algorithm API Reference

This document provides the complete API reference for the `Algorithm` class, focusing only on the public methods and properties that users should interact with.

## Class: Algorithm

The main interface for algorithmic trading in ProAlgoTrader Core.

### Properties

#### Market and Time Properties

| Property                | Type       | Description                                |
| ----------------------- | ---------- | ------------------------------------------ |
| `market_start_time`     | `time`     | The start time of the trading session.     |
| `market_end_time`       | `time`     | The end time of the trading session.       |
| `market_start_datetime` | `datetime` | The start datetime of the trading session. |
| `market_end_datetime`   | `datetime` | The end datetime of the trading session.   |
| `pre_market_time`       | `datetime` | The time for pre-market activities.        |
| `current_datetime`      | `datetime` | The current datetime of the algorithm.     |
| `current_timestamp`     | `int`      | The current timestamp of the algorithm.    |
| `current_date`          | `date`     | The current date of the algorithm.         |
| `current_time`          | `time`     | The current time of the algorithm.         |

#### Order and Position Properties

| Property         | Type             | Description                                        |
| ---------------- | ---------------- | -------------------------------------------------- |
| `orders`         | `List[Order]`    | A list of all orders placed.                       |
| `pending_orders` | `List[Order]`    | A list of currently pending orders.                |
| `positions`      | `List[Position]` | A list of all positions (both open and closed).    |
| `net_pnl`        | `PnlCalculator`  | The net profit and loss for all positions.         |
| `unrealized_pnl` | `PnlCalculator`  | The unrealized profit and loss for open positions. |
| `pnl`            | `PnlCalculator`  | An alias for `unrealized_pnl`.                     |

### Methods

#### Configuration Methods

##### `set_interval(interval)`

Sets the execution interval for the algorithm's main loop.

- **Parameters:**
  - `interval` (`timedelta`): The time interval between executions.
- **Example:**
  ```python
  from datetime import timedelta
  algorithm.set_interval(timedelta(seconds=1))
  ```

##### `set_position_manager(*, position_manager_class)`

Sets a custom position manager for the algorithm. Supports both single and multiple position manager types.

- **Parameters:**
  - `position_manager_class` (`Type[PositionManagerProtocol | MultiplePositionManagerProtocol]`): The class of the position manager.
- **Example:**

  ```python
  # Single position manager (global management)
  from project.position_manager import PositionManager
  algorithm.set_position_manager(position_manager_class=PositionManager)

  # Multiple position manager (per-position management)
  from project.position_manager import MultiplePositionManager
  algorithm.set_position_manager(position_manager_class=MultiplePositionManager)
  ```

##### `get_position_manager(position)`

Gets the position manager instance for a specific position. Used internally by the framework.

- **Parameters:**
  - `position` (`PositionProtocol`): The position to get the manager for.
- **Returns:** `PositionManagerProtocol | MultiplePositionManagerProtocol | None` - The position manager instance or None if not set.

##### `set_account_type(*, account_type)`

Sets the account type for trading, which can affect order validation.

- **Parameters:**
  - `account_type` (`AccountType`): The account type to use.
- **Example:**
  ```python
  from proalgotrader_core.enums.account_type import AccountType
  algorithm.set_account_type(account_type=AccountType.CASH_POSITIONAL)
  ```

#### Market Data and Symbol Methods

##### `add_chart(*, broker_symbol, timeframe, candle_type, **kwargs)`

Registers a new chart to receive market data.

- **Parameters:**
  - `broker_symbol` (`BrokerSymbol`): The symbol to create the chart for.
  - `timeframe` (`timedelta`): The timeframe for the chart's candles.
  - `candle_type` (`CandleType`, optional): The type of candle. Defaults to `CandleType.REGULAR`.
- **Returns:** `Chart` - The newly created chart instance.
- **Example:**

  ```python
  from datetime import timedelta
  from proalgotrader_core.enums.candle_type import CandleType

  chart = await algorithm.add_chart(
      broker_symbol=equity_symbol,
      timeframe=timedelta(minutes=5),
      candle_type=CandleType.HEIKEN_ASHI
  )
  ```

##### `add_equity(*, symbol_name)`

Adds an equity symbol to the algorithm.

- **Parameters:**
  - `symbol_name` (`str`): The name of the equity (e.g., "RELIANCE").
- **Returns:** `BrokerSymbol` - The broker symbol instance.
- **Example:**
  ```python
  equity_symbol = await algorithm.add_equity(symbol_name="RELIANCE")
  ```

##### `add_future(*, symbol_name, expiry_input)`

Adds a future symbol to the algorithm.

- **Parameters:**
  - `symbol_name` (`str`): The name of the underlying symbol (e.g., "NIFTY").
  - `expiry_input` (`Tuple[Literal["Weekly", "Monthly"], int]`, optional): The expiry to use.
- **Returns:** `BrokerSymbol` - The broker symbol instance.
- **Example:**
  ```python
  future_symbol = await algorithm.add_future(symbol_name="NIFTY", expiry_input=("Monthly", 0))
  ```

##### `add_option(*, symbol_name, expiry_input, strike_price_input, option_type)`

Adds an option symbol to the algorithm.

- **Parameters:**
  - `symbol_name` (`str`): The name of the underlying symbol (e.g., "BANKNIFTY").
  - `expiry_input` (`Tuple[Literal["Weekly", "Monthly"], int]`, optional): The expiry to use.
  - `strike_price_input` (`int`, optional): The desired strike price relative to the current price (e.g., 0 for ATM).
  - `option_type` (`Literal["CE", "PE"]`, optional): The option type.
- **Returns:** `BrokerSymbol` - The broker symbol instance.
- **Example:**
  ```python
  option_symbol = await algorithm.add_option(
      symbol_name="BANKNIFTY",
      expiry_input=("Weekly", 0),
      strike_price_input=0,
      option_type="CE"
  )
  ```

#### Signal and Strategy Methods

##### `add_signals(*, signal_manager, symbol_names)`

Adds one or more signal managers to the algorithm.

- **Parameters:**
  - `signal_manager` (`Type[SignalManagerProtocol]`): The class of the signal manager.
  - `symbol_names` (`List[str]`): A list of symbol names to attach the signal manager to.
- **Example:**
  ```python
  from project.signal_manager import MySignalManager
  await algorithm.add_signals(
      signal_manager=MySignalManager,
      symbol_names=["RELIANCE", "TCS"]
  )
  ```

#### Trading Methods

##### `buy(*, broker_symbol, market_type, product_type, order_type, quantities)`

Places a buy order.

- **Parameters:**
  - `broker_symbol` (`BrokerSymbolProtocol`): The symbol to buy.
  - `market_type` (`MarketType`): The market type (e.g., `Cash`, `Derivative`).
  - `product_type` (`ProductType`): The product type (e.g., `Intraday`, `Delivery`).
  - `order_type` (`OrderType`): The order type (e.g., `Market`, `Limit`).
  - `quantities` (`int`): The number of units to buy.
- **Example:**
  ```python
  await algorithm.buy(
      broker_symbol=equity_symbol,
      market_type=MarketType.Cash,
      product_type=ProductType.INTRADAY,
      order_type=OrderType.MARKET,
      quantities=10
  )
  ```

##### `sell(*, broker_symbol, market_type, product_type, order_type, quantities)`

Places a sell order.

- **Parameters:**
  - `broker_symbol` (`BrokerSymbolProtocol`): The symbol to sell.
  - `market_type` (`MarketType`): The market type.
  - `product_type` (`ProductType`): The product type.
  - `order_type` (`OrderType`): The order type.
  - `quantities` (`int`): The number of units to sell.
- **Example:**
  ```python
  await algorithm.sell(
      broker_symbol=equity_symbol,
      market_type=MarketType.Cash,
      product_type=ProductType.INTRADAY,
      order_type=OrderType.MARKET,
      quantities=10
  )
  ```

##### `create_order(*, order_item)`

Creates and places a single order using an `OrderItem`.

- **Parameters:**
  - `order_item` (`OrderItem`): The order item to create and place.
- **Example:**

  ```python
  from proalgotrader_core.order_item import OrderItem

  order_item = OrderItem(...)
  await algorithm.create_order(order_item=order_item)
  ```

##### `create_multiple_orders(*, order_items)`

Creates and places multiple orders at once.

- **Parameters:**
  - `order_items` (`List[OrderItem]`): A list of order items to create and place.
- **Example:**
  ```python
  await algorithm.create_multiple_orders(order_items=[order_item1, order_item2])
  ```

##### `exit_all_positions()`

Exits all currently open positions.

- **Example:**
  ```python
  await algorithm.exit_all_positions()
  ```

#### Position Event Methods

##### `on_position_open(position)`

Called when a position is opened. Override this method in your strategy to handle position opening events.

- **Parameters:**
  - `position` (`PositionProtocol`): The position that was opened.
- **Example:**

  ```python
  async def on_position_open(self, position: PositionProtocol) -> None:
      print(f"Position opened: {position.broker_symbol.symbol_name}")
      # Set risk-reward for the position
      from proalgotrader_core.risk_reward import RiskReward, Stoploss, Target
      from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

      await self.create_risk_reward(
          position=position,
          stoploss=Stoploss(value=2.0),  # 2% stop loss
          target=Target(value=4.0),      # 4% target
          unit=RiskRewardUnit.PERCENTAGE,
      )
  ```

##### `on_position_closed(position)`

Called when a position is closed. Override this method in your strategy to handle position closing events.

- **Parameters:**
  - `position` (`PositionProtocol`): The position that was closed.
- **Example:**
  ```python
  async def on_position_closed(self, position: PositionProtocol) -> None:
      print(f"Position closed: {position.broker_symbol.symbol_name} | P&L: {position.pnl.profit}")
  ```

**Note**: These methods have default empty implementations in the Algorithm class, so you only need to override them if you want to handle position events.

#### Risk Management Methods

##### `create_risk_reward(*, position, stoploss, target, unit)`

Creates and sets risk-reward for a position with stoploss and target configuration.

- **Parameters:**
  - `position` (`PositionProtocol`): The position to set risk-reward for.
  - `stoploss` (`Stoploss | Any`, optional): The stoploss configuration.
  - `target` (`Target | Any`, optional): The target configuration.
  - `unit` (`RiskRewardUnit`, optional): The unit for risk-reward calculation. Defaults to `RiskRewardUnit.POINTS`.
- **Example:**

  ```python
  from proalgotrader_core.risk_reward import Stoploss, Target
  from proalgotrader_core.enums.risk_reward_unit import RiskRewardUnit

  await algorithm.create_risk_reward(
      position=position,
      stoploss=Stoploss(value=50),
      target=Target(value=100),
      unit=RiskRewardUnit.POINTS
  )
  ```

#### Data Access Methods

##### `data` (Chart Property)

Returns the full Polars DataFrame with all available chart data up to the current algorithm time.

- **Returns:** `pl.DataFrame` - Filtered DataFrame containing chart data
- **Example:**

  ```python
  # Get full chart data
  chart_data = chart.data
  print(chart_data)

  # Access specific columns
  close_prices = chart.data.select("close")
  print(close_prices)
  ```

##### `get_data(row_number, column_name)` (Chart Method)

Helper method to get specific values from the chart data.

- **Parameters:**
  - `row_number` (`int`): Row number (0 = current candle, 1 = previous candle)
  - `column_name` (`str`, optional): Specific column name to retrieve
- **Returns:** `Any` - Scalar value if column specified, Series if not
- **Example:**

  ```python
  # Get current close price
  current_close = await chart.get_data(0, "close")

  # Get previous high price
  previous_high = await chart.get_data(1, "high")

  # Get current candle data as Series
  current_candle = await chart.get_data(0)
  ```

##### `data` (Indicator Property)

Returns the full Polars DataFrame with all available indicator data up to the current algorithm time.

- **Returns:** `pl.DataFrame` - Filtered DataFrame containing indicator data
- **Example:**

  ```python
  # Get full indicator data
  indicator_data = indicator.data
  print(indicator_data)

  # Access specific indicator columns
  rsi_values = indicator.data.select("rsi")
  print(rsi_values)
  ```

##### `get_data(row_number, column_name)` (Indicator Method)

Helper method to get specific values from the indicator data.

- **Parameters:**
  - `row_number` (`int`): Row number (0 = current value, 1 = previous value)
  - `column_name` (`str`, optional): Specific column name to retrieve
- **Returns:** `Any` - Scalar value if column specified, Series if not
- **Example:**

  ```python
  # Get current RSI value
  current_rsi = await indicator.get_data(0, "rsi")

  # Get previous MA20 value
  previous_ma20 = await indicator.get_data(1, "ma20")

  # Get current indicator data as Series
  current_data = await indicator.get_data(0)
  ```

#### Utility Methods

##### `between_time(first, second)`

Checks if the current algorithm time is between two specified times.

- **Parameters:**
  - `first` (`time`): The start of the time range.
  - `second` (`time`): The end of the time range.
- **Returns:** `bool` - `True` if the current time is within the range, `False` otherwise.
- **Example:**

  ```python
  from datetime import time

  if algorithm.between_time(time(9, 30), time(15, 00)):
      print("Within trading hours.")
  ```
