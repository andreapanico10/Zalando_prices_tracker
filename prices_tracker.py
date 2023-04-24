from datetime import datetime
import requests
from bs4 import BeautifulSoup
from pony import orm
import telepot
import numpy as np
import platform
from dotenv import load_dotenv
import os 

"""
Title: Save Product Prices with Python

IMPORTANT. this is a basic example for beginners and as it is it will be quite brittle. To improve
I recommend users add some error handling for expected errors, like site unavailable, data missing
from element selectors, along with some basic logging. These things are not included in this version
to keep the level of entry as low as possible.
"""

load_dotenv()

### TELEGRAM BOT ###
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ZALANDO_EMAIL = os.getenv("ZALANDO_EMAIL")
ZALANDO_PASSWORD = os.getenv("ZALANDO_PASSWORD")
WRITE_TO_DB = True
PLATFORM = platform.system()
MACOS_XML_FILE_PATH = os.getenv("MACOS_XML_FILE_PATH")
WINDOWS_XML_FILE_PATH = os.getenv("WINDOWS_XML_FILE_PATH")

if PLATFORM == "Windows":
    XML_FILE_PATH = WINDOWS_XML_FILE_PATH
else:
    XML_FILE_PATH = MACOS_XML_FILE_PATH

# set user agent header
headers = {
    "Access-Control-Allow-Origin": "*",
    "accept": "application/json",
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 '
                    'Safari/537.36',
    "upgrade-insecure-requests":"1"}

# Set up the Database and define the model
db = orm.Database()
db.bind(provider='sqlite', filename='zalandoDB_scrape.sqlite', create_db=True)

class Dress(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    url = orm.Required(str, unique=True)
    brand = orm.Optional(str)
    dress_type = orm.Optional(str)
    date_created = orm.Required(datetime)
    daily_prices = orm.Set('DailyPrice')

class DailyPrice(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    price = orm.Required(float)
    date_updated = orm.Required(datetime)
    dress = orm.Required(Dress)

# creates the table
db.generate_mapping(create_tables=True)


# web scraping functions
def zalando(session, headers, link):
    url = link
    try:
        resp = session.get(url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        try:
            brand = soup.find('h3', class_='_5Yd-hZ').text.strip()
        except:
            brand = "no brand"
        try:
            name = soup.find('span', class_='R_QwOV').text.strip()
        except: 
            name = "no-name"

        price = np.inf
        try:
            price = float(soup.find('p', class_='_3SrjVh').text.strip().replace("€", "").replace(" ", "").replace(",",".").replace("da",""))
        except:
            price = np.inf
        if price == np.inf:
            try:
                price = float(soup.find('p', class_="KxHAYs _4sa1cA FxZV-M _4F506m").text.strip().replace("€", "").replace(" ", "").replace(",",".").replace("da","")) 
            except:
                price = np.inf
        if price == np.inf:
            try:
                price = float(soup.find('p', class_='KxHAYs _4sa1cA dgII7d _3SrjVh _65i7kZ').text.strip().replace("€", "").replace(" ", "").replace(",",".").replace("da",""))
            except:
                    price = np.inf
    
        try:
            rating = soup.find('div', class_='_0xLoFW FCIprz').find('div', class_="_0xLoFW")['aria-label'].strip()
        except:
            rating = 'no rating'
        try:
            color = soup.find('p', class_='KxHAYs lystZ1 dgII7d _4F506m zN9KaA').text.strip()
        except:
            color = "no-color"
        try:
            image = soup.find('img', class_='KxHAYs lystZ1 FxZV-M _2Pvyxl JT3_zV EKabf7 mo6ZnF _1RurXL mo6ZnF _7ZONEy')['src'].split('=')[0]+'=1800'
        except:
            image = 'no-image'
        try:
            reviews_num = soup.find('h5', class_='KxHAYs e6UiOt FxZV-M _4F506m').text.strip()
        except:
            reviews_num = 'no-num'
    

        dress_data = (
            url,
            brand,
            name,
            price,
            image,
        )
        return dress_data
    except: # if resp.status_code != 200
        print("Dress not available ({})".format(link))
        return None


def print_dress_data( ):
    dress_table = Dress.select_by_sql("SELECT * FROM Dress")
    daily_price_table = DailyPrice.select_by_sql("SELECT * FROM DAILYPRICE")
    
    print(dress_table[-1].id, dress_table[-1].brand, daily_price_table[-1].price, "€")

def get_links_from_my_favorites(XML_FILE_PATH):
    
    with open(XML_FILE_PATH, "r+") as input_file:
        # Reading from a file
        favorites_source_html = (input_file.read())
    
    soup = BeautifulSoup(favorites_source_html, "html.parser")
    fav_links = ([url['href'] for url in soup.select("a.ZkIJC-")])
    return fav_links
            
def save_to_DB(dress_data):
    # loop through the data to save to the sqlite db
    with orm.db_session:
        for dress_item in dress_data:
            dress = Dress(url=dress_item[0], brand=dress_item[1], dress_type=dress_item[2], date_created=datetime.now())
            daily_price = DailyPrice(price=dress_item[3], date_updated=dress.date_created, dress=dress )
        print_dress_data()

def add_dresses_first_time(session):

    favourites_links = get_links_from_my_favorites(XML_FILE_PATH)
    new_links = check_new_dress(favourites_links)
    last_update = check_last_db_update()
    
    if len(new_links) == 0:
        print("\n*No item added from last time: {}*\n".format(last_update).upper())

    for link in new_links:
        dress_data = [(zalando(session, headers, link))]

        if  dress_data[0] != None and WRITE_TO_DB:
            save_to_DB(dress_data)

    return last_update

def check_new_dress(favourites_links):
    
    favourites_links_set = set(favourites_links)

    with orm.db_session:
        saved_link_set =  set( entry.url for entry in Dress.select_by_sql("SELECT id,url FROM Dress"))
    
    new_links = [link for link in favourites_links_set - saved_link_set]
    #have to do to respect the order (set data structure miss the order from origin list)
    new_links_ordered = [link for link in favourites_links if link in new_links]
    return new_links_ordered

def check_last_db_update():
    
    # This information can be gathered from the last update in DAILYPRICES table
    with orm.db_session:
        daily_price_table = DailyPrice.select_by_sql("SELECT * FROM DAILYPRICE")
        last_element_added = daily_price_table[-1].date_updated if len(daily_price_table) > 0 else None
        return last_element_added

def update_prices(session):
    with orm.db_session:
        dress_table = Dress.select_by_sql("SELECT * FROM DRESS")
        url_list = [dress.url for dress in dress_table]
        dress_id_list = [dress.id for dress in dress_table]

        prices_changed_num = 0
        for link, dress_id in zip(url_list, dress_id_list):
            dress_data = (zalando(session, headers, link))
            last_price_value = DailyPrice.select_by_sql("SELECT id,price FROM DAILYPRICE WHERE Dress = {}".format(dress_id))[-1].price
            
            ### Send notification ### 
            caption = ""
            if last_price_value > dress_data[3] and dress_data is not None:
                caption = '*SALE*\nPrice from: {} € to *{}* €\n-{}%\n{}'.format(last_price_value, dress_data[3], np.round(100*(1 - (float(dress_data[3])/float(last_price_value))),2), link)
                bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
                bot.sendPhoto(CHAT_ID, dress_data[4].replace("imwidth=156", "imwidth=1800"), caption=caption, parse_mode= 'Markdown' )

                #Add row to db
                DailyPrice(price=dress_data[3], date_updated=datetime.now(), dress=dress_id )
                prices_changed_num += 1

    return prices_changed_num

# main function to run everything
def main():

    print("\nStart scipt:",datetime.now(),"\n")
    # use a Requests session
    s = requests.Session()

    ## PHASE 1: ADDING NEW DRESSES
    last_update = add_dresses_first_time(s)
    
    ## PHASE 2: UPDATING PRICES
    if last_update is not None:
        if datetime.now() > last_update:
            print("\n\nUpdate of {} of the {}\n... Updating prices operation ...\n".format(datetime.now().strftime("%H:%M"), datetime.now()))

            n_updates = update_prices(s)
            print(" Updated {} items".format(n_updates))

    print("\nEnd scipt:",datetime.now())
    print("--------------------------------------------------------------------------------------------------------")

if __name__ == '__main__':
    main()