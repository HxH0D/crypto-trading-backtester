from datetime import datetime
import config
import csv
from binance import Client
import winsound

# Set sound parameters
duration = 1000  # milliseconds
freq = 440  # Hz

# Binance client setup
client = Client(config.apiKey, config.secretKey)

# List of symbols for which historical data will be fetched
symbolList = ["ETHUSDT"]
startingDate = "1 January, 2023 00:00:00"
endingDate = "1 January, 2024 23:59:59"
timeRange = Client.KLINE_INTERVAL_15MINUTE ## 15 minutes interval for each candlestick data ## Client.KLINE_INTERVAL_1DAY for daily data ## Client.KLINE_INTERVAL_1HOUR for hourly data

# Function to write historical data to a CSV file
def write_historical_data_to_csv(symbol, candlesticks):

    # Format the date and time for the CSV file name
    formatted_starting_date = datetime.strptime(startingDate, "%d %B, %Y %H:%M:%S").strftime("%Y")
    formatted_ending_date = datetime.strptime(endingDate, "%d %B, %Y %H:%M:%S").strftime("%Y")

    # Create a CSV file path with symbol, starting date, ending date, and time range
    csv_file_path = f"{symbol}-{formatted_starting_date}-{formatted_ending_date}-{timeRange}.csv"
    
    with open(csv_file_path, "w", newline='') as csv_file:
        klines_writer = csv.writer(csv_file, delimiter=",")

        # Write each candlestick data to the CSV file
        for candlestick in candlesticks:
            klines_writer.writerow(candlestick)

    print(f"Historical data for {symbol} has been written to {csv_file_path}")

# Loop through each symbol in the list
for symbol in symbolList:
    print("Fetching data for symbol:", symbol)

    # Get historical candlestick data from Binance API
    candlesticks = client.get_historical_klines(
        symbol,
        timeRange,
        startingDate,
        endingDate,
    )

    # Write the fetched data to a CSV file
    write_historical_data_to_csv(symbol, candlesticks)

# Notify with a beep sound when the process is completed
winsound.Beep(freq, duration)