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
