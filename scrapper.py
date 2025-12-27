LinkTemplate = """https://gw.yad2.co.il/feed-search-legacy/products/%s?category=%d&item=%d&page=%d&forceLdLoad=true"""
import requests 
import csv
import json
from itertools import chain

def fetch_json(section : str  , catgeory : int, item : int , printIt= False , page : int =0, limit : int = None, count : int = 0):
    '''generator to get all yad2 item and category pages and results 
    
    Args:
        section: section name (e.g., 'realestate', 'cellular')
        catgeory: category ID (e.g., 2 for sale, 1 for rent)
        item: item/subcategory ID
        printIt: whether to print items as they're fetched
        page: current page number (used internally)
        limit: maximum number of items to fetch (None = unlimited)
        count: current count (used internally for recursion)
    '''
    jsonRes = requests.get(LinkTemplate%( section , catgeory , item , page )).json()
    for itemJson in jsonRes["data"]["feed"]["feed_items"]: 
        if limit is not None and count >= limit:
            return
        yield itemJson
        count += 1
        if printIt :
            print(json.dumps(itemJson,ensure_ascii=False))
    if jsonRes["data"]["pagination"]["current_page"] < jsonRes["data"]["pagination"]["last_page"]: 
        if limit is None or count < limit:
            yield from fetch_json(section , catgeory , item  , printIt, page+1, limit, count)

def items(section , catgeory : int , searchTerm):
    cats = requests.get(f"https://gw.yad2.co.il/search-options/products/{section}?fields={searchTerm}&category={catgeory}").json()
    yield from cats["data"][searchTerm] 

def extract_rooms(area_rooms_field):
    '''Extract number of rooms from "Area and rooms of apartment" field
    
    Args:
        area_rooms_field: string containing room info (e.g., "3.5-4", "2-3", "4.5-5.5")
    
    Returns:
        string in format "X-Y" or None if not found
    '''
    import re
    if not area_rooms_field:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)', str(area_rooms_field))
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    return None

def to_csv(name, jsonList : list ):
    with open(name, 'w', newline='',encoding="utf-16") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t')
        first = next(jsonList)
        spamwriter.writerow(first.keys() )
        for item in chain(jsonList,(first,)):
            spamwriter.writerow(map(lambda val : str(val).replace("\t","     "),item.values()))


# Example usage:
# Limit to 10 items
#to_csv("items_in_section.csv", items("cellular", 5, "item"))     
#to_csv("areas_codes.csv", items("cellular", 5, "area"))    
#to_csv("fetched_data.csv", fetch_json("cellular", 5, 29, True, limit=10))

# For real estate - limit to 50 properties for sale
to_csv("realestate_sale_data.csv", fetch_json("realestate", 2, 1, True, limit=50))

# For real estate - limit to 100 properties for rent
# to_csv("realestate_rent_data.csv", fetch_json("realestate", 1, 1, True, limit=100))