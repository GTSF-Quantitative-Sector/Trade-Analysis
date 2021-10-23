from flask import Flask, request, jsonify  
import datetime as dt
import yfinance as yf

app = Flask(__name__)


@app.route('/api/v1/returns', methods=["POST"])
def retrieve_performance():
    print(request.json)

    # breakdown request arguments
    if 'start' not in request.json.keys():
        start = dt.datetime.strptime("2020-10-04", '%Y-%m-%d')
    else:
        start = dt.datetime.strptime(request.json["start"], '%Y-%m-%d')
    end = dt.datetime.now()
    ticker = request.json['ticker']
    index = request.json['index']

    # download data
    data = yf.download(ticker + " " + index, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"), group_by='tickers')

    # percent change for both ticker and index
    ticker_performance = (data[ticker]['Close'][-1] - data[ticker]['Close'][0]) / data[ticker]['Close'][0]
    index_performance = (data[index]['Close'][-1] - data[index]['Close'][0]) / data[index]['Close'][0]

    # return performance
    return jsonify({'over/under': ticker_performance - index_performance,
                    'index performance': index_performance,
                    'ticker performance': ticker_performance})


@app.route('/', methods=["GET"])
def home():
    return "Hello"


if __name__ == "__main__":
    app.run()