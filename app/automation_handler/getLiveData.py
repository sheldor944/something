
# This script is used to get live data from TradingView using the tvDatafeed library
# from now to the past n_bars
def getLiveData(symbol: str, exchange: str, interval: str, n_bars: int):


        from tvDatafeed import TvDatafeedLive, Interval
        import pandas as pd


        username = 'your_actual_username'
        password = 'your_actual_password'

        tvl = TvDatafeedLive()

        xauusd_data = tvl.get_hist(symbol, exchange, interval=Interval.in_1_minute, n_bars=n_bars, fut_contract=None, extended_session=False, timeout=-1)
        print(xauusd_data)

        # seis = tvl.new_seis('ETHUSDT', 'BINANCE', Interval.in_1_hour)
        # seis2 = tvl.new_seis('ETHUSDT', 'BINANCE', Interval.in_2_hour)

        # ethusdt_data = seis.get_hist(n_bars=10, timeout=-1)
        df = pd.DataFrame(xauusd_data)

        # Save to CSV
        df.to_csv('xauusd_data_24_march.csv', index=True)

        print("Data saved to xauusd_data.csv")
        return df

# getLiveData('XAUUSD', 'FOREXCOM', '1D', 6700)