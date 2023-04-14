# Zalando_prices_tracker
 Subject: Web scraping with Python 

IMPORTANT. this is a basic example for beginners and as it is it will be quite brittle. To improve I recommend users add some error handling for expected errors, like site unavailable, data missing from element selectors, along with some basic logging. These things are not included in this version to keep the level of entry as low as possible. 

At the moment the process of getting the favorite items is done by taking manually html file (Point 3). But if any reader is able to login with python requests, his/her advice would be greatly appreciated.

<h1>How to use</h1>
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
