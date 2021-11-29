from flask import Flask, request, jsonify
import datetime as dt
import yfinance as yf


app = Flask(__name__)


@app.route('/api/v1/returns', methods=["POST"])
def retrieve_performance():

    # breakdown request arguments
    if 'start' not in request.json.keys():
        start = dt.datetime.strptime("2020-10-04", '%Y-%m-%d')
    else:
        start = dt.datetime.strptime(request.json["start"], '%Y-%m-%d')

    end = dt.datetime.now()
    ticker = request.json['ticker']
    index = request.json['index']

    # download data
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    tickers = ticker + " " + index
    data = yf.download(tickers, start=start, end=end, group_by='tickers')

    if ticker == index:
        ticker_performance = (data['Close'][-1] - data['Close'][0]) / data['Close'][0]

        # return performance
        return jsonify([['-',
                        ticker_performance,
                        '-']])
    else:
        # percent change for both ticker and index
        ticker_performance = (data[ticker]['Close'][-1] - data[ticker]['Close'][0]) / data[ticker]['Close'][0]
        index_performance = (data[index]['Close'][-1] - data[index]['Close'][0]) / data[index]['Close'][0]

        # return performance
        return jsonify([[ticker_performance - index_performance,
                        ticker_performance,
                        index_performance]])


@app.route('/api/v1/info', methods=["POST"])
def retreive_info():
    ticker = request.json['ticker']
    stock = yf.Ticker(ticker)

    # error handling so the entire call doesn't fail
    if 'ebitda' in stock.info.keys():
        ebitda = stock.info['ebitda'] // 1000000
    else:
        ebitda = '-'

    if 'priceToBook' in stock.info.keys():
        ptb = stock.info['priceToBook']
    else:
        ptb = '-'

    if 'trailingPE' in stock.info.keys():
        pe = stock.info['trailingPE']
    else:
        pe = '-'

    return jsonify([[ebitda,
                    ptb,
                    pe]])


@app.route('/api/v1/categories', methods=["POST"])
def retrieve_categories():
    return jsonify([['Over/Under Performance', 'Ticker Performance',
                     'Index Performance', 'EBITDA (in millions)',
                     'Price To Book', 'Price To Earnings']])


@app.route('/', methods=["GET"])
def home():
    return "Hello"


if __name__ == "__main__":
    app.run()
