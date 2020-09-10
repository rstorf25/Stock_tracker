import ezgmail
ezgmail.EMAIL_ADDRESS

import yfinance as yf
import schedule
import time
from datetime import datetime, timedelta, date
from decimal import Decimal


yesterday = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
print(yesterday)
todays_date = date.today()
print(todays_date)
tomorrow = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
print(tomorrow)
one_day_ago = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
print(one_day_ago)

class Stock:
    def __init__(self, Name, Ticker, Shares, Change):
        self.Name = Name
        self.Ticker = Ticker
        self.Shares = Shares
        self.Change = Change
ba_stock = Stock("Boeing" , "BA", "13", "A")
vug_stock = Stock("Vanguard Growth Index Fund EtF Shares", "VUG","1.5", "A")
stx_stock = Stock("Seagate Technology plc", "STX", "1.5", "A")
trrmx_stock = Stock("T.Rowe Price Retirement 2050 Fund", "TRRMX","1.5", "B")
svaix_stock = Stock("Federated Strategic Value Dividend Fund Institutional Shares", "SVAIX", "1.5", "B")
veirx_stock = Stock("Vanguard Equity-Income Fund Admiral Shares", "VEIRX", "1.5", "B")
rds_a_stock = Stock("Royal Dutch Shell plc", "RDS-A", "1.5", "A")
ldlfx_stock = Stock("Lord Abbett Short Duration Income Fund Class F ", "LDLFX", "1.5", "B")

my_stocks = [ba_stock, vug_stock, stx_stock, trrmx_stock, svaix_stock, veirx_stock, rds_a_stock, ldlfx_stock]
a_stocks = [ba_stock, rds_a_stock, stx_stock, vug_stock]
b_stocks = [trrmx_stock, ldlfx_stock,svaix_stock, veirx_stock]
subject_text = """{} {}""".format("Stocks Closing Price:", todays_date)


individual_stock_data = yf.Ticker("VEIRX")
open_val = (individual_stock_data.history(period= "3d").Open[-2] * 114.568)
close_val = (individual_stock_data.history(period="3d").Close[-1] * 114.568)
change_val = Decimal(close_val - open_val)



def close():
    close_body = ""
    a_stocks_body_text = ""
    b_stocks_body_text = ""
    a_sum_day_list = []
    b_sum_day_list = []
    for stocks in my_stocks:
        header = ("Stock name: " + stocks.Name + ",  Ticker :" + stocks.Ticker)
        individual_stock_data = yf.Ticker(stocks.Ticker)
        individual_stock_data.history(period="2d")
        num_shares = stocks.Shares

    for stocks in a_stocks:
        header_a = ("Stock Name: " + stocks.Name + ", Ticker: " + stocks.Ticker)
        num_shares = stocks.Shares
        individual_stock_data = yf.Ticker(stocks.Ticker)
        open_string_data_1_d = str(individual_stock_data.history(period="1d").Open[0])
        close_string_data_1_d = str(individual_stock_data.history(period="1d").Close[0])
        day_change_1d = (float(close_string_data_1_d) - float(open_string_data_1_d))
        close_value_1d = float(num_shares) * float(close_string_data_1_d)
        open_value_1 = float(open_string_data_1_d) * float(num_shares)
        change_value_1 = (close_value_1d - open_value_1)
        change_percent_a = ((change_value_1/ open_value_1)*100)
        a_sum_day = a_sum_day_list.append(change_value_1)
        a_stocks_body_text += """{} \n {} \n {} \n {} \n {} \n {} \n {} \n \n""".format(header_a, "Close: " + str(todays_date) + " " + "$" + str(close_string_data_1_d),
                                                                                  "Shares :" + stocks.Shares,"Current Value : $" + ('%.2f' % close_value_1d),
                                                                                  "Daily $ Price Change:  $" + ('%.2f' % day_change_1d),
                                                                                  "Daily % Price Change: " + ('%.2f' % change_percent_a + " %"),
                                                                                  "Daily Value Change: $" + ('%.2f' % change_value_1))

    for stocks in b_stocks:
        header_b = ("Stock Name: " + stocks.Name + ", Ticker: " + stocks.Ticker)
        num_shares = stocks.Shares
        individual_stock_data = yf.Ticker(stocks.Ticker)
        open_string_data_2_d = str(individual_stock_data.history(period="3d").Open[-2])
        close_string_data_2_d = str(individual_stock_data.history(period="3d").Close[-1])
        day_change_2d = Decimal(float(close_string_data_2_d) - float(open_string_data_2_d))
        day_change_rounded = round(day_change_2d, 2)
        close_value_2d = float(num_shares) * float(close_string_data_2_d)
        open_value_2 = float(open_string_data_2_d) * float(num_shares)
        change_value_2 = (close_value_2d - open_value_2)
        change_percent = ((change_value_2/ open_value_2) *100)
        b_sum_day = b_sum_day_list.append(change_value_2)
        b_stocks_body_text += """ \n {} \n {} \n {} \n {} \n {} \n {} \n {} \n \n""".format(header_b, "Close: " + str(todays_date) + " " + "$" + str(close_string_data_2_d),
                                                                                      "Shares :" + stocks.Shares,"Current Value: $" + ('%.2f' % close_value_2d),
                                                                                      "Daily $ Price Change: $" + ('%.2f' % day_change_2d),
                                                                                      "Daily % Price Change: " + ('%.2f' % change_percent + " %"),
                                                                                      "Daily Value Change: $" + ('%.2f' % change_value_2))
    a_total = sum(a_sum_day_list)
    b_total = sum(b_sum_day_list)
    day_total = a_total + b_total
    total_text = "Day Totals: $ "
    close_body = str(a_stocks_body_text) + str(b_stocks_body_text) + str(total_text + ('%.2f' % day_total) )

    email_to_send = ezgmail.send('Any_email.com', subject_text, close_body)

schedule.every().day.at("17:01").do(close)
while True:
    schedule.run_pending()
    time.sleep(1)



