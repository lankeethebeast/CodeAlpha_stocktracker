import requests
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Set your API Key (Replace with your own key)
API_KEY = "BDTLMRLZWV50ZAKE"
BASE_URL = "https://www.alphavantage.co/query"

# Portfolio Dictionary (Stock Symbol -> Shares)
portfolio = {}


def get_stock_price(symbol):
    """Fetch real-time stock price using Alpha Vantage API."""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:
        latest_time = list(data["Time Series (5min)"].keys())[0]
        price = float(data["Time Series (5min)"][latest_time]["1. open"])
        return round(price, 2)
    except KeyError:
        return None  # Invalid stock or API limit reached


def add_stock(symbol, shares):
    """Add a stock to the portfolio."""
    symbol = symbol.upper()
    if symbol in portfolio:
        portfolio[symbol] += shares
    else:
        portfolio[symbol] = shares
    print(f"✅ Added {shares} shares of {symbol} to portfolio.")


def remove_stock(symbol):
    """Remove a stock from the portfolio."""
    symbol = symbol.upper()
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"❌ Removed {symbol} from portfolio.")
    else:
        print("Stock not found in portfolio.")


def show_portfolio():
    """Display portfolio with real-time prices."""
    if not portfolio:
        print("📉 Portfolio is empty.")
        return

    table = PrettyTable(["Stock", "Shares", "Current Price ($)", "Total Value ($)"])
    total_value = 0

    for symbol, shares in portfolio.items():
        price = get_stock_price(symbol)
        if price:
            value = shares * price
            table.add_row([symbol, shares, price, round(value, 2)])
            total_value += value
        else:
            table.add_row([symbol, shares, "N/A", "N/A"])

    print(table)
    print(f"💰 Portfolio Total Value: ${round(total_value, 2)}")


def plot_stock(symbol):
    """Fetch and plot historical stock price trend."""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:
        history = data["Time Series (Daily)"]
        dates = list(history.keys())[:30]  # Get last 30 days
        prices = [float(history[date]["4. close"]) for date in dates]

        plt.figure(figsize=(10, 5))
        plt.plot(dates[::-1], prices[::-1], marker="o", linestyle="-", label=f"{symbol} Price")
        plt.xlabel("Date")
        plt.ylabel("Stock Price ($)")
        plt.title(f"{symbol} Stock Price Trend (Last 30 Days)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid()
        plt.show()
    except KeyError:
        print("⚠️ Invalid stock symbol or API limit exceeded!")


def main():
    """Main menu for the Stock Portfolio Tracker."""
    while True:
        print("\n📈 Stock Portfolio Tracker")
        print("1️⃣ Add Stock")
        print("2️⃣ Remove Stock")
        print("3️⃣ Show Portfolio")
        print("4️⃣ Plot Stock Trend")
        print("5️⃣ Exit")

        choice = input("Select an option: ")
        if choice == "1":
            symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").upper()
            shares = int(input("Enter number of shares: "))
            add_stock(symbol, shares)
        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == "3":
            show_portfolio()
        elif choice == "4":
            symbol = input("Enter stock symbol to plot: ").upper()
            plot_stock(symbol)
        elif choice == "5":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
