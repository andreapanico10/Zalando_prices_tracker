# Zalando_prices_tracker
 Title: Save Product Prices with Python  

IMPORTANT. this is a basic example for beginners and as it is it will be quite brittle. To improve I recommend users add some error handling for expected errors, like site unavailable, data missing from element selectors, along with some basic logging. These things are not included in this version to keep the level of entry as low as possible. 

<h1>How to use</h1>
<ol>
 <li> Install requirements using terminal or command line. You should run this command <code> pip install -r requirements.txt. </code></li>
 <li> Create a file ".env" in the project folder and insert the following lines completing adequately:<br>
      TELEGRAM_BOT_TOKEN = "Token of the telegram bot"<br>
      CHAT_ID = "Telegram chat id between user and telegram bot"<br>
      MACOS_XML_FILE_PATH = 'html file if you run under Macos'<br>
      WINDOWS_XML_FILE_PATH = 'html file if you run under Windows'<br>
      ZALANDO_EMAIL = "login email"<br>
      ZALANDO_PASSWORD = "login password"<br>
 </li>
 <li> Cut and paste the source code of your Zalando favourites page in a file called <code>"favorites.html"</code> </li>
 <li> Run the script: <code> python prices_tracker.py </code> </li>
</ol>
