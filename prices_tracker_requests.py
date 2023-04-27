import requests
import pandas as pd
import os 
import platform 
from pony import orm
from datetime import datetime
import telepot
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# DB QUERY

# DELETE FROM DRESS WHERE Id > 0
# DELETE FROM DAILYPRICE WHERE Id > 0

# SELECT * FROM DRESS 
# SELECT * FROM DAILYPRICE 

def search_favorites():
    url = "https://www.zalando.it/api/graphql"

    payload = [
        {
        "id": os.getenv("GRAPHQL_QUERY_ID"),
        "variables": {
            "likedEntitiesCount": 1000,
            "likedOutfitsCount": 0,
            "ownedEntitiesCount": 0,
            "tradeinEntitiesCount": 0,
            "curatedWardrobeListsCount": 0,
            "curatedWardrobeListsItemsCount": 4,
            "likedOutfitsCursor": None,
            "ownedItemsCursor": None,
            "filters": None,
            "tradeinItemsCursor": None,
            "curatedWardrobeListsCursor": None,
            "shouldRequestLiked": True,
            "shouldRequestOwned": False,
            "shouldRequestTradein": False,
            "shouldRequestOutfits": False,
            "shouldRequestCuratedWardrobeLists": True,
            "shouldRequestCuratedWardrobeListsItems": False
            }
        }
    ]

    headers ={
    "cookie": os.getenv("COOKIES"),
    "authority": "www.zalando.it",
    "accept": "*/*",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "dpr": "3",
    "origin": "https://www.zalando.it",
    "referer": "https://www.zalando.it/wardrobe/lists/liked/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    "viewport-width": "390",
    "x-xsrf-token": "AAAAAOgOL_sytSieTPerl7qR0k0CtifKpd_cVJ_3uRvR8mEaFWF3tqeBswJhM6pnEBEiknf_6r8CO3lCzHxMJO_jsSaCHH6LikNIjEiXEFskp3Dn4mfgoR9JREgqOKO7OeiS0kNcoH_fKwsiYZ_Lc-M=",
    "x-zalando-experiments": "b891eec6-b3d5-4760-b685-fe1fbe3ce330=THE_LABEL_IS_ENABLED;90aa955b-d7f6-4fe1-a14f-2522788af1bb=fdbe-release1-enabled;b951ad11-ec05-4c78-9772-1eb1100c5c96=ABB_DISABLED",
    "x-zalando-feature": "wardrobe",
    "x-zalando-intent-context": "navigationTargetGroup=MEN",
    "x-zalando-request-uri": "/wardrobe/lists/liked/"
    }
    
    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()

    product_ids = []
    nodes = data[0]['data']['customer']['likedItems']['entities']['nodes']
    for i in range (len(nodes)):
        product_ids.append((nodes[i]['id']))

    payload = []
    for id in product_ids: 
        product_request = {}
        product_request['id'] = os.getenv("REQUEST_ID")
        product_request ['variables'] =  {
                "id": id,
                "isImageOnly": False
            }
        payload.append(product_request)

    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()

    dress_list = []

    for i in range(len(data)):
        price =  brand = uri = target_group = silhouette = group = model_media = media = original_price = ""
        in_stock = is_available = False

        base_data = data[i]['data']['productLike']

        # Is available
        if 'inStock' in base_data:
            if base_data['inStock'] == True:
                in_stock = True
        # Brand
        if 'brand' in base_data.keys():
            brand = base_data['brand']['name'] 
        elif 'inactiveBrand' in base_data.keys():
            brand = base_data['inactiveBrand']['name'] 
        
        # Price
        if 'displayPrice' in base_data.keys():
            if 'promotional' in base_data['displayPrice'].keys() and base_data['displayPrice']['promotional'] != None:
                price = float(base_data['displayPrice']['promotional']['formatted'].strip().replace("€", "").replace(u'\xa0', u'').replace(',','.'))
                original_price = float(base_data['displayPrice']['original']['formatted'].strip().replace("€", "").replace(u'\xa0', u'').replace(',','.'))
            elif 'original' in base_data['displayPrice'].keys():
                price = float(base_data['displayPrice']['original']['formatted'].strip().replace("€", "").replace(u'\xa0', u'').replace(',','.'))
                original_price = price
        # Url
        if 'uri' in base_data.keys():
            uri = base_data['uri']
            is_available = True

        # Target sex
        if 'navigationTargetGroup' in base_data.keys():
            target_group = base_data['navigationTargetGroup']

        # Silhouette
        if 'silhouette' in base_data.keys():
            silhouette = base_data['silhouette']

        # Group
        if 'group' in base_data.keys():
            group = base_data['group']

        # Model media
        if 'modelShot' in base_data.keys() and base_data['modelShot'] != None:
            model_media = base_data['modelShot']['uri']
        
        # Media
        if 'primaryImage' in base_data.keys():
            media = base_data['primaryImage']['uri']
        
        if not is_available:
            model_media = media
            model_media = ""
            print("Dress not available ({})".format(brand))
            
        if price == "":
            price = None

        if original_price == "":
            original_price = None

        dress = { 
            'product_id' : product_ids[i],
            'brand' : brand,
            'price' : price,
            'original_price' : original_price,
            'link' : uri,
            'media' : media,
            'model_media' : model_media, 
            'is_in_stock' : in_stock,
            'is_available' : is_available,
            'target_group' : target_group,
            'silhouette' : silhouette,
            'group' : group
            }
        dress_list.append(dress)
    
        with orm.db_session:
            dress_exist = True if Dress.select_by_sql("SELECT id,product_id FROM DRESS WHERE product_id = '{}'".format(dress['product_id'])) else False
        ## SAVE TO DB
        if not dress_exist:
            save_to_DB(dress)

    df = pd.DataFrame(dress_list)
    df.to_csv("dresses.csv")
    
    #f = open("output_requests.txt", "w")
    #f.write(response.text)
    #f.close()

    ## UPDATING EXISTING DRESSES

    with orm.db_session:
        dress_table = Dress.select_by_sql("SELECT * FROM DRESS")
        saved_product_ids = [dress.product_id for dress in dress_table]
        dress_id_list = [dress.id for dress in dress_table]

        prices_changed = []
        for product_id, dress_id in zip(saved_product_ids, dress_id_list):
            dress_data = list(filter(lambda dress: dress['product_id'] == product_id, dress_list))[0]
            last_price_value = DailyPrice.select_by_sql("SELECT id,price FROM DAILYPRICE WHERE Dress = {}".format(dress_id))[-1].price

            if dress_data['price'] != last_price_value:
                #Add row to db
                DailyPrice(price=dress_data['price'], original_price = last_price_value, date_updated=datetime.now(), dress=dress_id )
                prices_changed.append(dress_data)

            ### Send notification ###  if <
            
            caption = ""
            if last_price_value != None and dress_data != None and last_price_value > dress_data['price']:
                caption = '*SALE {}*\nPrice from: {} € to *{}* €\n-{}%\n{}'.format(dress_data['brand'], last_price_value, dress_data['price'], np.round(100*(1 - (float(dress_data['price'])/float(last_price_value))),2), dress_data['link'])
                bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
                photo = dress_data['model_media'] if dress_data['model_media'] else dress_data['media']
                bot.sendPhoto(CHAT_ID, photo, caption=caption, parse_mode= 'Markdown' )

    return prices_changed

### TELEGRAM BOT ###
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Set up the Database and define the model
db = orm.Database()
db.bind(provider='sqlite', filename='zalandoDB.sqlite', create_db=True)

class Dress(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    product_id = orm.Required(str, unique=True)
    link = orm.Optional(str)
    brand = orm.Optional(str)
    dress_type = orm.Optional(str)
    date_created = orm.Required(datetime)
    original_price = orm.Optional(float)
    media = orm.Optional(str)
    model_media = orm.Optional(str)
    is_in_stock = orm.Optional(bool)
    is_available = orm.Optional(bool)
    target_group = orm.Optional(str)
    silhouette = orm.Optional(str)
    group = orm.Optional(str)
    daily_prices = orm.Set('DailyPrice')

class DailyPrice(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    price = orm.Optional(float)
    original_price = orm.Optional(float)
    date_updated = orm.Required(datetime)
    dress = orm.Required(Dress)

# creates the table
db.generate_mapping(create_tables=True)

def print_dress_data():
    dress_table = Dress.select_by_sql("SELECT * FROM Dress")
    daily_price_table = DailyPrice.select_by_sql("SELECT * FROM DAILYPRICE")
    
    print(dress_table[-1].id, dress_table[-1].brand, daily_price_table[-1].price, "€")

def save_to_DB(dress_data):
    # loop through the data to save to the sqlite db
    with orm.db_session:
        dress = Dress(link=dress_data['link'],
                      product_id = dress_data['product_id'],
                        brand=dress_data['brand'],
                        original_price = dress_data['original_price'], 
                        media = dress_data['media'],
                        model_media = dress_data['model_media'],
                        is_in_stock = dress_data["is_in_stock"],
                        is_available = dress_data["is_available"],
                        target_group = dress_data["target_group"],
                        silhouette = dress_data["silhouette"],
                        group = dress_data["group"],
                        date_created=datetime.now()
                        )
        daily_price = DailyPrice(price=dress_data['price'],
                                    original_price = dress_data['original_price'],
                                    date_updated=dress.date_created,
                                    dress=dress 
                                    )
        print_dress_data()

def check_last_db_update():
    # This information can be gathered from the last update in DAILYPRICES table
    with orm.db_session:
        daily_price_table = DailyPrice.select_by_sql("SELECT * FROM DAILYPRICE")
        last_element_added = daily_price_table[-1].date_updated if len(daily_price_table) > 0 else None
        return last_element_added
    
# main function to run everything
def main():

    print("\nStart scipt:",datetime.now(),"\n")
    
    ## PHASE 1: ADDING NEW DRESSES
    last_update = check_last_db_update()
    if last_update is None:
        print("First execution ... creating DB ...")
        search_favorites()
        print("\nDB created\n")

    ## PHASE 2: UPDATING PRICES
    if last_update is not None:
        if datetime.now() > last_update:
            print("\n\nUpdate of {} of the {}\n... Updating prices operation ...\n".format(datetime.now().strftime("%H:%M"), datetime.now()))
            updates = search_favorites()
            print("\n Updated {} items".format(len(updates)))
            for i in range(len(updates)):
                print('  ',i+1, updates[i]['brand'])


    print("\nEnd scipt:",datetime.now())
    print("--------------------------------------------------------------------------------------------------------")

if __name__ == '__main__':
    main()