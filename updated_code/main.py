import requests
from bs4 import BeautifulSoup
from pony import orm
from datetime import datetime

db = orm.Database()
db.bind(provider='sqlite',filename='products.db', create_db=True)

class Product(db.Entity):
    name = orm.Required(str)
    price = orm.Required(float)
    created_date = orm.Required(datetime)
    
db.generate_mapping(create_tables=True)

# This is the function that scrap the price from the product from different websites
def gears4(session):
    url = "https://www.gear4music.com/Recording-and-Computers/Shure-SM7B-Dynamic-Studio-Microphone/G6X"
    
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "gears4",
        float(soup.select_one("span.info-row-price span.c-val").text)
    )
    
    return data

def amazon(session):
    url = "https://www.amazon.co.uk/Shure-SM7B-Microphone/dp/B0002E4Z8M"
    
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "amazon",
        float(soup.select_one("div.a-box-group span.a-offscreen").text.replace("£", ""))
    )
    
    return data

def thomann(session):
    url = "https://www.thomann.de/gb/shure_sm_7b_studiomikro.htm"
    
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "thomann",
        float(soup.select_one("div.price-wrapper div.price").text.replace("£", ""))
    )
    
    return data

def main():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    })
    
    data = [
        amazon(session),
        gears4(session),
        thomann(session)
    ]
    
    with orm.db_session:
        for item in data:
            Product(name=item[0], price=item[1], created_date=datetime.now())
    
if __name__ == '__main__':
    main()