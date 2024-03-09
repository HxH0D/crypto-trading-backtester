# Binance Historical Data Fetcher and Backtesting

**ATTENTION: This sample project for pulling Binance Historical data and backtesting is purely for educational purposes. Usage and results are entirely up to the user. Users need to make their own strategies and settings. This project is provided as an example only. Please be careful.**

This project is designed to fetch historical cryptocurrency data from the Binance exchange and conduct backtesting. The project consists of two main folders: `getBinanceHistoryData` and `backtesting`.

## getBinanceHistoryData

This folder contains the necessary code to pull cryptocurrency data using the Binance API. Users can choose the desired cryptocurrency pair and date range. For example, for `ETHUSDT`, you can pull 15 minutes of data from January 1, 2023, to January 1, 2024.

### Usage

1. Open the `getHistoryData.py` file.
2. Set the `symbolList`, `startingDate`, `endingDate`, and `timeRange` variables to the desired cryptocurrency pair and date range.
3. Run: `getHistoryData.py`

## backtesting.py

This file contains the necessary codes to perform backtesting on the extracted data. In the `backtesting.py` file, users can define strategies and set backtest settings.

### Usage

1. In `backtesting.py`, define your strategy between #strategy start and #strategy end.
2. In `backtesting.py`, replace the variable `csvName` with the name of the data file you extracted.
3. In `backtesting.py`, set your `leverage`, `stop_loss`, `take_profit` backtest settings according to your strategy.
4. Run it: `backtesting.py`
5. The project currently includes the parabolic SAR strategy. If you want to test it against the spot market, you can disable the short trading code in the `backtesting.py` file and set the leverage to 0.

## Results

Backtest results include detailed information such as total funds, lowest/highest funds, the number of completed transactions, win/loss ratio.

## Example

The project currently includes the parabolic SAR strategy. If you want to test it against the spot market, you can disable the short trading code in the `strategy.py` file and set the leverage to 0.

## Requirements

- `ta` package: 
- `pandas` package: 
- `pytz` package:
- `python` package: 
- `ccxt` package: 
### To install requirements:
-`pip install -r requirements.txt`

## Contributions

We look forward to your contributions! Please share suggestions and bugs in [issues](https://github.com/HxH0D/crypto-trading-backtester/issues).

## Connect with me:
<div align="center">
  <a href="https://www.instagram.com/emre_altun.08/" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Instagram&logo=instagram&label=&color=E4405F&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="instagram logo"  />
  </a>
  <a href="mailto:yusufemrealtun1@gmail.com" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Gmail&logo=gmail&label=&color=D14836&logoColor=white&labelColor=&style=for-the-badge"  height="25" alt="gmail logo"  />
  </a>
  <a href="https://www.linkedin.com/in/yusufemrealtun/" target="_blank">
    <img src="https://img.shields.io/static/v1?message=LinkedIn&logo=linkedin&label=&color=0077B5&logoColor=white&labelColor=&style=for-the-badge"  height="25" alt="linkedin logo"  />
  </a>
</div>

## License

This project is licensed under the MIT license. See [LICENSE](https://github.com/HxH0D/crypto-trading-backtester/LICENSE.md) for more information.
