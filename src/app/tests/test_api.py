import json


def test_items(client, mongo):
    items_data = [
        {"name": "Sword of Fury", "rarity": "common", "rarity_order": 0, "dlc": [], "traits": ["Furious"]},
        {"name": "Amulet of Fate", "rarity": "rare", "rarity_order": 2, "dlc": [], "traits": ["Mystical"]},
        {"name": "Dragon Shield", "rarity": "rare", "rarity_order": 2, "dlc": [], "traits": []},
        {"name": "Wand of Wishing", "rarity": "epic", "rarity_order": 3, "dlc": ["DLC 1"], "traits": []},
        {"name": "Ring of Power", "rarity": "legendary", "rarity_order": 4, "dlc": ["DLC 2"], "traits": ["Dominating"]},
    ]
    inserted = mongo.db.items.insert_many(items_data).inserted_ids
    for index, item in enumerate(items_data):
        item["_id"] = str(inserted[index])

    response = client.get('items')
    assert response.status_code == 200
    expected = {
        "objects": sorted(items_data, key=lambda item: (item["name"], item["rarity_order"])),
        "_filters": {
            "rarity": ["common", "rare", "epic", "legendary"],
            "dlc": ["DLC 1", "DLC 2"],
            "traits": ["Dominating", "Furious", "Mystical"],
        }
    }
    assert expected == json.loads(response.get_data(as_text=True))


def test_ships(client, mongo):
    ships_data = [
        {"name": "Battle Cruiser", "cargo_slots": 3, "item_slots": 4, "total_slots": 7, "types": ["Steam ship", "Military ship"]},
        {"name": "Cargo Ship", "cargo_slots": 6, "item_slots": 2, "total_slots": 8, "types": ["Steam ship", "Trade ship"]},
        {"name": "Clipper", "cargo_slots": 4, "item_slots": 1, "total_slots": 5, "types": ["Sailing ship", "Trade ship"]},
        {"name": "Flagship", "cargo_slots": 3, "item_slots": 2, "total_slots": 5, "types": ["Hybrid", "Unique"]},
        {"name": "Great Eastern", "cargo_slots": 8, "item_slots": 3, "total_slots": 11, "types": ["Special ship", "Trade ship", "Unique"]},
    ]
    equipped_in = [
        ["Ships", "Steamships", "Military Ships"],
        ["Ships", "Steamships"],
        ["Ships", "Sailing Ships"],
        ["Ships", "Military Ships", "Sailing Ships"],
        ["Ships", "Steamships"]
    ]
    inserted = mongo.db.ships.insert_many(ships_data).inserted_ids
    for index, ship in enumerate(ships_data):
        ship["_id"] = str(inserted[index])
        ship["equipped_in"] = equipped_in[index]

    response = client.get("ships")
    assert response.status_code == 200
    expected = {
        "objects": sorted(ships_data, key=lambda ship: ship["name"]),
        "_filters": {
            "types": [
                "Hybrid",
                "Military ship",
                "Sailing ship",
                "Special ship",
                "Steam ship",
                "Trade ship",
                "Unique"
            ]
        }
    }
    assert expected == json.loads(response.get_data(as_text=True))

def test_supplies(client, mongo):
    supplies_data = [
        {
            "bonuses": {
                "crafting": 10,
                "diplomacy": 0,
                "faith": 0,
                "force": 0,
                "hunting": 0,
                "medicine": 0,
                "naval_power": 0,
                "navigation": 0
            },
            "name": "Alpaca Wool"
        },
        {
            "bonuses": {
                "crafting": 0,
                "diplomacy": 0,
                "faith": 0,
                "force": 0,
                "hunting": 0,
                "medicine": 5,
                "naval_power": 0,
                "navigation": 0
            },
            "name": "Sugar"
        },
        {
            "bonuses": {
                "crafting": 0,
                "diplomacy": 0,
                "faith": 0,
                "force": 10,
                "hunting": 0,
                "medicine": 0,
                "naval_power": 0,
                "navigation": 0
            },
            "name": "Huskies"
        },
        {
            "bonuses": {
                "crafting": 0,
                "diplomacy": 0,
                "faith": 0,
                "force": 0,
                "hunting": 20,
                "medicine": 0,
                "naval_power": 0,
                "navigation": 0
            },
            "name": "Huskies"
        },
    ]
    inserted = mongo.db.supplies.insert_many(supplies_data).inserted_ids
    for index, supply in enumerate(supplies_data):
        supply["_id"] = str(inserted[index])
    expected_objects = supplies_data[:3]
    expected_objects[2]["bonuses"]["hunting"] = 20

    response = client.get("supplies")
    assert response.status_code == 200
    expected = {
        "objects": sorted(expected_objects, key=lambda supply: supply["name"]),
        "_filters": {}
    }
    assert expected == json.loads(response.get_data(as_text=True))
