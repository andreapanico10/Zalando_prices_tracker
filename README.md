# Zalando_prices_tracker
 Subject: Zalando Web scraping with Python 

IMPORTANT. this is a basic example for beginners and as it is it will be quite brittle. To improve I recommend users add some error handling for expected errors, like site unavailable, data missing from element selectors, along with some basic logging. These things are not included in this version to keep the level of entry as low as possible. 

<h1>1) prices_tracker.py Usage</h1>
<h3>In this first version, favorite items scraping is done from static html file (Point 3)</h3>
<ol>
 <li> Install requirements using terminal or command line. You should run this command <code> pip install -r requirements.txt. </code></li>
 <li> Create a file ".env" in the project folder and insert the following lines completing adequately:<br>
  <pre>
      TELEGRAM_BOT_TOKEN = "Token of the telegram bot"
      CHAT_ID = "Telegram chat id between user and telegram bot"
      MACOS_XML_FILE_PATH = 'html file if you run under Macos'
      WINDOWS_XML_FILE_PATH = 'html file if you run under Windows'
      ZALANDO_EMAIL = "login email"
      ZALANDO_PASSWORD = "login password"
  </pre>
 </li>
 <li> Cut and paste the html code of your Zalando favourites page in a file called <code>favorites.html</code> </li>
 <li> Run the script: <code> python prices_tracker.py </code> </li>
</ol>

<h1>2) prices_tracker_requests.py Usage</h1>
<h3>In this second version, I took the info of the dresses from graph ql API intercepted by Zalando website</h3>

<ol>
 <li> Install requirements using terminal or command line. You should run this command <code> pip install -r requirements.txt. </code></li>
 <li> Use a tool like "Insomnia" to get some important info about your API requests parameter as cookies and graph ql ID</li>
 https://github.com/andreapanico10/Zalando_prices_tracker/blob/main/Pictures/graphql.png
 <li> Create a file ".env" in the project folder and insert the following lines completing adequately:<br>
  <pre>
      TELEGRAM_BOT_TOKEN = "Token of the telegram bot"
      CHAT_ID = "Telegram chat id between user and telegram bot"
      REQUEST_ID = "request id"
      GRAPHQL_QUERY_ID = "graphql query id"
      COOKIES = "Cookies string"
  </pre>
 </li>
 <li> Run the script: <code> python prices_tracker_requests.py </code> </li>
</ol>
