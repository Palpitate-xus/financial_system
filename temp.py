import akshare as ak

stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000001").values[2][1]
print(stock_individual_info_em_df.values[2][1])
