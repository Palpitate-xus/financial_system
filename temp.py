import akshare as ak
import pandas
stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sz399552")
for item in stock_zh_index_daily_df.values:
    print((item[4]-item[1])/item[1])