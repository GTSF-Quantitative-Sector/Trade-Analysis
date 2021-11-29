function TRADE_ANALYSIS(ticker, index, start_date) {
  baseURL = 'https://returns-analysis.herokuapp.com/api/v1/returns';

  if (start_date != null) {
    start = start_date.toISOString().split('T')[0];
    var data = {"ticker":ticker, "index": index, "start": start};
  } else {
    var data = {"ticker":ticker, "index": index}
  }
  
  return apiCall(baseURL, data);
}

function TRADE_INFO(ticker) {
  baseURL = 'https://returns-analysis.herokuapp.com/api/v1/info'
  var data = {"ticker": ticker};

  return apiCall(baseURL, data);
}

function TRADE_CATEGORIES() {
  baseURL = 'https://returns-analysis.herokuapp.com/api/v1/categories'
  var data = {};

  return apiCall(baseURL, data);
}

function apiCall(url, data) {
  var options = {
    'method' : 'post',
    'contentType': 'application/json',
    'payload' : JSON.stringify(data)
  };

  var response = UrlFetchApp.fetch(url, options);
  data = JSON.parse(response.getContentText());
  return data;
}

function importAllHoldings() {
    ss = SpreadsheetApp.getActiveSpreadsheet();
    holdingsRange = ss.getSheetByName("Unorganized Holdings").getDataRange();
    holdingsValues = holdingsRange.getValues();
    var sectorHoldings = [];
    var sector = ""
    var holdings = []
    var i = 0
    while (i < holdingsValues.length - 3) {
      sector = holdingsValues[i][0]
      holdings = []
      if (sector != "" && sector != "Sector Total" && sector != "Equities Total" && sector != "Fixed Income") {
        i++;
        holdings.push(sector)
        while (holdingsValues[i][0] != "Sector Total") {
          holdings.push(holdingsValues[i][1]);
          i++;
        }
        sectorHoldings.push(holdings);
      }
      i++;
    }
    return sectorHoldings;
 }

