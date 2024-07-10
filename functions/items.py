from pymongo import DESCENDING, MongoClient
import os
mongo_connect=os.getenv('M_CONNECTION_STRING')
db= MongoClient(mongo_connect)

players_items = db.userProfiles.userItems

items =[
    {'id':0,"name":'atk up','type':'atk','increase':1,'value':50},
    {'id':1,"name":'def up','type':'def','increase':1,'value':50},
    {'id':2,"name":'poinson claw','type':'eff','value':150},
    {'id':3,"name":'big meat','type':'cons','stat':'hunger','increase':1,'value':150},
]

#player item management 

def add_item_to_player(item_id, player_id):
    itms = players_items.find_one({'player_id': player_id})
    item_to_add = items[item_id]

    if itms is None:
        print('No items for the player')
        players_items.insert_one({'player_id': player_id, 'items': [{'id': item_id, 'name': item_to_add['name'], 'qunty': 1}]})
    else:
        players_item_list = itms['items']
        print(players_item_list)

        # Check if the item is already in the player's items list
        existing_item = next((item for item in players_item_list if item['id'] == item_id), None)

        if existing_item:
            # If the item is already in the list, increase the quantity by 1
            players_items.update_one(
                {"player_id": player_id, "items.id": item_id},
                {'$inc': {'items.$.qunty': 1}}
            )
            print(f"Item {item_to_add['name']} quantity increased.")
        else:
            # If the item is not in the list, add a new item to the list
            players_items.update_one(
                {"player_id": player_id},
                {'$push': {'items': {'id': item_id, 'name': item_to_add['name'], 'qunty': 1}}}
            )
            print(f"Item {item_to_add['name']} added to the list.")

    return 'ok'

def remove_item_from_player(item_id, player_id):
    itms = players_items.find_one({'player_id': player_id})

    if itms is not None:
        players_item_list = itms['items']

        # Check if the item is in the player's items list
        existing_item = next((item for item in players_item_list if item['id'] == item_id), None)

        if existing_item:
            # If the quantity is greater than 1, decrement the quantity by 1
            if existing_item['qunty'] > 1:
                players_items.update_one(
                    {"player_id": player_id, "items.id": item_id},
                    {'$inc': {'items.$.qunty': -1}}
                )
                print(f"Item {existing_item['name']} quantity decreased.")
            else:
                # If the quantity is 1, remove the entire item from the list
                players_items.update_one(
                    {"player_id": player_id},
                    {'$pull': {'items': {'id': item_id}}}
                )
                print(f"Item {existing_item['name']} removed from the list.")
        else:
            print(f"Item with ID {item_id} not found in the player's items list.")
    else:
        print('No items for the player.')

    return 'ok'


def equip_item(item_id):
    
    item_to_equip = items[item_id]
    print(item_to_equip)
def unequip_item(item_id):
    pass




