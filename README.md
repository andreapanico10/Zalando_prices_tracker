# Zalando prices Tracker
 Subject: Zalando Web scraping with Python 

IMPORTANT. this is a basic example for beginners and as it is it will be quite brittle. To improve I recommend users add some error handling for expected errors, like site unavailable, data missing from element selectors, along with some basic logging. These things are not included in this version to keep the level of entry as low as possible. 

<h1> System Architecture</h1>
 <div align="center">
    <img src="https://github.com/andreapanico10/Zalando_prices_tracker/blob/main/Pictures/system%20architecture.png" width="800px"</img> 
</div>
An automator app run the script on user' needs during the day (for example, once per hour), the script acquires data from Zalando site and check if there are changes compared to the local DB; if there are any, save them on the DB and triggers the sending of a message on telegram to the user in the case of discount.

<h1>1) WEB SCRAPING: prices_tracker.py Usage</h1>
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

<h1>2) FETCHING API: prices_tracker_requests.py Usage</h1>
<h3>In this second version, I took the info of the dresses from graph ql API intercepted by Zalando website</h3>

<ol>
 <li> Install requirements using terminal or command line. You should run this command <code> pip install -r requirements.txt. </code></li>
 <li> Copy as cURL the first graphql/ API</li>
 <div align="center">
    <img src="https://github.com/andreapanico10/Zalando_prices_tracker/blob/main/Pictures/graphql.png" width="700px"</img> 
</div>
  <li> Use a tool like "Insomnia" to get some important info about your API requests parameter as cookies and graph ql ID</li>
 Send a POST request
 <div align="center">
    <img src="https://github.com/andreapanico10/Zalando_prices_tracker/blob/main/Pictures/send_request.png" width="700px"</img> 
</div>
 <li> 
  <ol>
   <li>Get the ID, we need it in the next steps where GRAPHQL_QUERY_ID is required;</li>
   <li>Cancel the likedItemsCursor field (it manage the website scroll - 20 items at a time -, if we remove it, we get all the items);</li>
   <li>Increase the field likedEntitiesCount to support the favourites total count</li>
  </ol>
  </li>
 <div align="center">
    <img src="https://github.com/andreapanico10/Zalando_prices_tracker/blob/main/Pictures/insomnia.png" width="700px"</img> 
</div>
 <li> Scrolling down we get another fundamental info: COOKIES, copy and paste the 'cookie' field in the .env file
 <div align="center">
    <img src="https://github.com/andreapanico10/Zalando_prices_tracker/blob/main/Pictures/cookies.png" width="700px"</img> 
</div>
 </li>
 <li> As before, copy as cURL the second graphql/ API in zalando network tab, this is the request for the items; in the API in picture we can see a payload, there is an object in the payload for any dress in our catalog; we need just to copy the first Id and put it in the .env variable REQUEST_ID; the second Id in the picture is the dress Id in Zalando DB
<div align="center">
    <img src="https://github.com/andreapanico10/Zalando_prices_tracker/blob/main/Pictures/graphql2insomnia.png" width="700px"</img> 
</div>
  
 </li>
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


## Like this project?

If you are feeling stimulated by this project and want to make me smile -> 
<a href="https://www.buymeacoffee.com/andreapynico" target="_blank">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*VJdus0nKuy1uNoByh5BN3w.png" width="135" height="30">
</a>
