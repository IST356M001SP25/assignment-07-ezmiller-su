import re
from playwright.sync_api import Playwright, sync_playwright
# from menuitemextractor import extract_menu_item
if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


def clean_price(price:str) -> float:
    price = price.replace('$','').replace(',','')
    return float(price)

def clean_scraped_text(scraped_text: str) -> list[str]:
    scraped_text_list = scraped_text.split('\n')
    clean_text_list = []
    unwanted_text = ['NEW!', 'NEW', "S", "V", "GS", "P", '']
    for x in scraped_text_list:
        if x not in unwanted_text:
            clean_text_list.append(x)
    return clean_text_list

def extract_menu_item(title:str, scraped_text: str) -> MenuItem:
    clean_text = clean_scraped_text(scraped_text)
    item = MenuItem(category=title, name="", price=0.0, description="")
    item.name = clean_text[0]
    item.price = clean_price(clean_text[1])
    if len(clean_text) > 2:
        item.description = clean_text[2]
    else:
        item.description = "No description available."
    return item



if __name__=='__main__':
    pass


# from menuitem import MenuItem
from dataclasses import dataclass, asdict

@dataclass
class MenuItem:
    # these are built-in properties
    category: str
    name: str
    price: float
    description: str

    # convert to a dictionary
    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return MenuItem(**data)
    
if __name__=='__main__':
    # example of howto use the dataclass

    # create a new MenuItem    
    mozz = MenuItem(name = "Mozzarella Sticks", 
                    price = 8.99, 
                    category="Apps", 
                    description="Fried cheese sticks served with marinara sauce.")

    # can assign a new category
    mozz.category = "Appetizers"
    print(mozz)
    # convert back to a dictionary
    print(mozz.to_dict())

    # create a new MenuItem from a dictionary
    burger = MenuItem.from_dict({"name": "Burger", 
                                 "price": 9.99, 
                                 "description": "A delicious burger.", 
                                 "category": "Entrees"})
    print(burger)



import pandas as pd


def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")

    items = []
    for title in page.query_selector_all("h3.foodmenu__menu-section-title"):
        title_contents = title.inner_text()
        row = title.query_selector("~ *").query_selector("~ *")
        for item in row.query_selector_all("div.foodmenu__menu-item"):
            item_text = item.inner_text()
            item = extract_menu_item(title_contents, item_text)
            items.append(item.to_dict())
    
    menu = pd.DataFrame(items)
    menu.to_csv("cache/tullys_menu.csv", index=False)

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    tullyscraper(playwright)