import finnhub


class StockWrapper:
    def __init__(self, stock_names):
        self.stock_names = stock_names
        self.client = finnhub.Client(api_key="c73t9liad3i8g8erel3g")

    def all_stock_prices(self):
        stock_price_list = []
        for stock_name in self.stock_names:
            data = self.client.quote(stock_name)
            price = data['c']
            if isinstance(price, float) and price > 100:
                price = round(price, 1)
            else:
                price = round(price, 2)
            stock_price_list.append(price)
        return stock_price_list

if __name__ == "__main__":
    # Setup client
    finnhub_client = finnhub.Client(api_key="c73t9liad3i8g8erel3g")

    # Convert to Pandas Dataframe
    print(finnhub_client.quote('AAPL'))
