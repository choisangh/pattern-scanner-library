# pattern-scanner-library

A Python toolkit for detecting candlestick chart patterns in financial time series.

## Features
- Built-in recognizers for common formations like head and shoulders, triangles, wedges and more
- PatternRecognizer utility that attaches pattern detectors to your OHLC data
- Simple helper functions for geometric calculations

## Installation
Install the library with pip from the repository root:

```bash
pip install .
```

## Usage
Example showing how to create a recognizer from pandas Series of OHLCV data:

```python
from pattern_scanner import PatternRecognizer

# timestamp, open_price, high_price, low_price, close_price, volume
recognizer = PatternRecognizer(
    window_size=2,
    timestamp=my_timestamp,
    open_price=my_open,
    high_price=my_high,
    low_price=my_low,
    close_price=my_close,
    volume=my_volume,
)

# available pattern classes
recognizer.get_pattern_list()
# detect specific pattern
patterns = recognizer.HeadAndShoulders.check_pattern()
# make plot
recognizer.HeadAndShoulders.make_plot()
```
![image](https://github.com/user-attachments/assets/a3ed6d2f-26d6-460b-b8f1-5b1b8902d41c)

## Running Tests
Execute the unit tests with:

```bash
python3 -m pytest
```
