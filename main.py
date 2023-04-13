import requests

STOCK_NAME = "TSLA" #EXAMPLE
COMPANY_NAME = "Tesla Inc" #EXAMPLE

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
News_Api_Key = "YOUR API KEY"
Stocks_Api_Key = "STOCK API KEY"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stocks_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "STOCK API KEY"

}
stock_response = requests.get(STOCK_ENDPOINT, params=stocks_params)
stock_response.raise_for_status()
data = stock_response.json()

days_dict = data["Time Series (Daily)"]
days_list = [close for (day, close) in days_dict.items()]
yesterdays_data = days_list[0]
yesterdays_close_price = days_list[0]["4. close"]
day_before_yesterdays_data = days_list[1]
day_before_yesterdays_close = days_list[1]["4. close"]



# diff in dollars between yesterdays and the day before yesterday
difference = float(yesterdays_close_price)-float(day_before_yesterdays_close)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
# diff in precent yesterdays and the day before yesterday
diff_precent = round(difference / float(yesterdays_close_price) * 100)

# if difference bigger then 5% send import the news:
if abs(diff_precent) > 1:
    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": "API KEY"
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]

#Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
three_articles = articles[:3]

# Create a new list of the first 3 article's headline and description using list comprehension.
formatted_articles = [f"{STOCK_NAME}:{up_down}{diff_precent}% Headline:{article['title']} Brief: {article['description']}" for article in three_articles]

####Email alert!!#####
my_email = "EMAIL@PROVIDER.COM"
password = "PASSWORD"

for article in formatted_articles:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(from_addr=my_email,
                            to_addrs="EMAIL",
                            msg=f"Subject:Stock Alert! \n\n{article}!")



