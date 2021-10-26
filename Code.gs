function DOUBLE(input) {
  return input * 2;
}

function RETURNS_ANALYSIS(ticker, index, start_date) {
  baseURL = 'https://returns-analysis.herokuapp.com/api/v1/returns';

  var data = {"ticker":ticker, "index": index}
  var options = {
    'method' : 'post',
    'contentType': 'application/json',
    'payload' : JSON.stringify(data)
  };

  var response = UrlFetchApp.fetch(baseURL, options);
  data = JSON.parse(response.getContentText());
  
  return data;
}

function RETURNS_CATEGORIES() {
  baseURL = 'https://returns-analysis.herokuapp.com/api/v1/categories'
  var options = {
    'method' : 'post'
  }

  var response = UrlFetchApp.fetch(baseURL, options);
  data = JSON.parse(response.getContentText());
  console.log(data)
  return data;
}

RETURNS_CATEGORIES();