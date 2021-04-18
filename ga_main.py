from ebay_api import search_items
from collections import namedtuple


list_dict = search_items(keyword=str(input("Enter an item name: ")))
[*list_item] = list_dict


# for i, j in enumerate(list_item):
#    list_indexer = [i]
#    list_element = [j]
#    [*list_id] = list_item[i].itemid
#    [*list_price] = list_item[i].currentprice
#    print([list_indexer])
#    print([list_element])
#    print(f"ID: {[list_id]}")
#    print(f"Value: {[list_price]}")
#    print("---BREAKLINE---")


# Store item in a namedtuple (items data structure)
for i, j in enumerate(list_item):
    [*list_id] = list_item[i].itemid
    [*list_title] = list_item[i].title
    [*list_price] = list_item[i].currentprice
    item_structure = namedtuple('item', ['id', 'title', 'price'])
    [*item_list] = [
        item_structure(list_id, list_title, list_price)
    ]
    print(item_list)

"""
item_structure = namedtuple('item', ['id', 'title', 'price'])
    [*item_list] = [
        item_structure(list_item[0].itemid, list_item[0].title, list_item[0].currentprice)
    ]
    print(item_list[0])
"""
