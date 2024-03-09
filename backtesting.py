from ta.trend import PSARIndicator
import pandas as pd
from datetime import datetime
import pytz

# Functions start
timeZone= "Europe/Istanbul"
tradeCount = 0
winCount = 0
lossCount = 0
winRate = 0
completedTrades = []
inLongTrade = False
inShortTrade = False
longEntryPrice = 0
shortEntryPrice = 0

longEntryTime = ""
longExitTime = ""
shortEntryTime = ""
shortExitTime = ""
def update_metrics(entry_price, exit_price, is_long):
    global initialCapital, minCapital, maxCapital, tradeCount, winCount, lossCount, winRate
    if is_long:
        profit_loss_percentage = ((exit_price - entry_price) / entry_price) * 100 * leverage
    else:
        profit_loss_percentage = ((entry_price - exit_price) / entry_price) * 100 * leverage

    initialCapital = initialCapital + (initialCapital / 100) * profit_loss_percentage
    initialCapital = initialCapital * 0.9998 if profit_loss_percentage > 0 else initialCapital * 0.9995

    if initialCapital < minCapital:
        minCapital = initialCapital
    if initialCapital > maxCapital:
        maxCapital = initialCapital

    tradeCount += 1
    if profit_loss_percentage > 0:
        winCount += 1
    else:
        lossCount += 1

    winRate = (winCount / tradeCount) * 100

def longEnter(i):
    global inLongTrade, longEntryPrice, longEntryTime, stopLossPrice, takeProfitPrice
    longEntryPrice = float(df["close"][i])
    longEntryTime = (datetime.utcfromtimestamp(df["timestamp"][i] / 1000).replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timeZone))).strftime('%Y-%m-%d %H:%M:%S')
    stopLossPrice = longEntryPrice - (longEntryPrice * stopLossPercentage / 100)
    takeProfitPrice = longEntryPrice + (longEntryPrice * takeProfitPercentage / 100)
    inLongTrade = True

def longExit(i, exit_reason, current_price):
    global inLongTrade, longEntryPrice, longExitPrice
    longExitPrice = current_price
    update_metrics(longEntryPrice, longExitPrice, True)
    inLongTrade = False
    exitTime = (datetime.utcfromtimestamp(df["timestamp"][i] / 1000).replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timeZone))).strftime('%Y-%m-%d %H:%M:%S')

    completedTrades.append({
        "Entry Time": longEntryTime,
        "Exit Time": exitTime,
        "Type": "Long",
        "Entry Price": longEntryPrice,
        "Exit Price": longExitPrice,
        "Exit Type": exit_reason
    })

def shortEnter(i):
    global inShortTrade, shortEntryPrice, shortEntryTime, stopLossPrice, takeProfitPrice
    shortEntryPrice = float(df["close"][i])
    stopLossPrice = shortEntryPrice + (shortEntryPrice * stopLossPercentage / 100)
    takeProfitPrice = shortEntryPrice - (shortEntryPrice * takeProfitPercentage / 100)
    shortEntryTime = (datetime.utcfromtimestamp(df["timestamp"][i] / 1000).replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timeZone))).strftime('%Y-%m-%d %H:%M:%S')
    inShortTrade = True

def shortExit(i, exit_reason, current_price):
    global inShortTrade, shortEntryPrice, shortExitPrice
    shortExitPrice = current_price
    update_metrics(shortEntryPrice, shortExitPrice, False)
    inShortTrade = False
    exitTime = (datetime.utcfromtimestamp(df["timestamp"][i] / 1000).replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timeZone))).strftime('%Y-%m-%d %H:%M:%S')

    completedTrades.append({
        "Entry Time": shortEntryTime,
        "Exit Time": exitTime,
        "Type": "Short",
        "Entry Price": shortEntryPrice,
        "Exit Price": shortExitPrice,
        "Exit Type": exit_reason
    })

# Functions end

# Variables start
csvName = "ETHUSDT-2023-2024-15m.csv"
leverage = 0 # Set leverage #Spot 0X
initialCapital = 100
stopLossPercentage = 0.5 # %5
takeProfitPercentage = 0.25 # %2.5

minCapital = initialCapital
maxCapital = initialCapital
# Variables end




print("PREPARING FOR BACKTEST...")
attributes = ["timestamp", "open", "high", "low", "close", "volume", "1", "2", "3", "4", "5", "6"]
df = pd.read_csv(csvName, names=attributes)

# İndicators start

psar_indicator = PSARIndicator(high=df['high'], low=df['low'], close=df["close"], step=0.02, max_step=0.2)
df['PSAR'] = psar_indicator.psar()

# İndicators end


for i in range(96, df.shape[0]):
    print((datetime.utcfromtimestamp(df["timestamp"][i] / 1000).replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Istanbul'))).strftime('%Y-%m-%d %H:%M:%S') + " Close: " + str(df["close"][i]) + " " + str(len(df.index)) + "/" + str(i) + " Backtesting... Initial Capital: " + str(initialCapital))
    #Strategy  start
    
    
    
    # Stop-loss and take-profit logic
    if inLongTrade or inShortTrade:
        current_price = float(df["open"][i])
        if inLongTrade:
            if current_price <= stopLossPrice or current_price >= takeProfitPrice:
                longExit(i, "stop_loss" if current_price <= stopLossPrice else "take_profit", current_price)

        elif inShortTrade:
            if current_price >= stopLossPrice or current_price <= takeProfitPrice:
                shortExit(i, "stop_loss" if current_price >= stopLossPrice else "take_profit", current_price)

    # PSAR Crossover and Crossunder
    sar_crossover = df["close"] > df["PSAR"]
    sar_crossunder = df["close"] < df["PSAR"]

    # LONG ENTER      
    if sar_crossover.iloc[i] and not sar_crossover.iloc[i-1] and not inLongTrade:
        if inShortTrade:
            shortExit(i, "Normal Exit", float(df["close"][i]))
        longEnter(i)

    # SHORT ENTER
    if sar_crossunder.iloc[i] and not sar_crossunder.iloc[i-1] and not inShortTrade:
        if inLongTrade:
            longExit(i, "Normal Exit", float(df["close"][i]))
        shortEnter(i)
        
    #Strategy  end
print("BACKTEST COMPLETED. TRADE RESULTS: ")
for trade in completedTrades:
    print(f"Entry Time: {trade['Entry Time']}, Exit Time: {trade['Exit Time']}, Type: {trade['Type']}, Entry Price: {trade['Entry Price']}, Exit Price: {trade['Exit Price'] }, Exit Type: {trade['Exit Type']}")
print("/////////////////////////////////////////////////////////////////////////////////")
print("BACKTEST COMPLETED. RESULTS: ")
print(csvName)
print("Total Capital: ", initialCapital)
print("Minimum Capital: ", minCapital)
print("Maximum Capital: ", maxCapital)
print("Completed Trades Count: ", tradeCount)
print("Wins: ", winCount, " Losses: ", lossCount, " Win Rate: ", winRate)
