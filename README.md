# anno-items-api

API for [Anno 1800 Expeditions Helper](https://www.anno-expeditions.app/) project.

## Getting list of Items

### Request
`GET /items`

`curl -i -H 'Accept: application/json' http://localhost:5050/items`

### Response

```
HTTP/1.1 200 OK
Server: gunicorn
Date: Wed, 26 Apr 2023 16:55:25 GMT
Connection: close
Content-Type: application/json
Content-Length: 8563137
Access-Control-Allow-Origin: *

{
    "_filters": {
        "dlc": [
            "Empire of the Skies",
            "Land of Lions",
            "Seeds of Change",
            "Sunken Treasures",
            "The Anarchist",
            "The High Life",
            "The Passage",
            "Tourist Season",
            "Tourist Season or The High Life"
        ],
        "rarity": [
            "character item",
            "common",
            "uncommon",
            "rare",
            "epic",
            "legendary"
        ],
        "traits": [
            "Anthropologist",
            "Archaeologist",
            "Diver",
            "Entertainer",
            "Hypnotist",
            "Jack Of All Traits",
            "Military Ship",
            "Pirate",
            "Polyglot",
            "Zoologist"
        ]
    },
    "objects": [
        {
            "_id": "64024eac56410170518d75eb",
            "bonuses": {
                "crafting": 0,
                "diplomacy": 0,
                "faith": 0,
                "force": 0,
                "hunting": 0,
                "medicine": 0,
                "naval_power": 40,
                "navigation": 0
            },
            "dlc": [],
            "equipped_in": "Military Ships",
            "image_src": "data:image/png;base64,UklGRlgeAABXRUJQVlA4WAoAAAAQAAAAfwAAfwAAQUxQSP0GAAABP+...+caHW1IabPpdL6OT9T3JCOMKiISD4FBFAi0rgnIfbS3evaTQAAAA",
            "name": "\"Blown-Apart\" 12-Pounder",
            "rarity": "epic",
            "rarity_order": 3,
            "traits": []
        },
        ...
    ]
}
```

### Available options
| URL                                      | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| `/items`                                 | Retrieve all items.                      |
| `/items?sort=name`                       | Retrieve all items sorted by name in ascending order. |
| `/items?name__contains=cap&sort=-name`   | Retrieve items filtered by name and sorted by name in descending order. |
| `/items?rarity=rare&sort=-bonuses.faith` | Retrieve items filtered by rarity and sorted by faith bonus in descending order. |
| `/items?dlc=Land of Lions&sort=rarity_order` | Retrieve items filtered by dlc and sorted by rarity in ascending order. |
| `/items?traits=Polyglot&sort=equipped_in` | Retrieve items filtered by trait and sorted due to 'equipped in' data. |

## Getting list of Ships

### Request
`GET /ships`

`curl -i -H 'Accept: application/json' http://localhost:5050/ships`

### Response
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Wed, 26 Apr 2023 17:26:33 GMT
Connection: close
Content-Type: application/json
Content-Length: 525277
Access-Control-Allow-Origin: *

{
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
    },
    "objects": [
        {
            "_id": "64024d8a56410170518d735a",
            "bonuses": {
                "naval_power": 70,
                "navigation": 0
            },
            "cargo_slots": 3,
            "equipped_in": [
                "Ships",
                "Steamships",
                "Military Ships"
            ],
            "image_src": "data:image/png;base64,UklGRvZfAABXRUJQVlA4WAoAAAAQAAAA/...+WOjbTET21C9TCREapGgEhae9YJpLkMXLYpf4t8fObmjP4KMqj9zuoAAA==",
            "item_slots": 4,
            "name": "Battle Cruiser",
            "total_slots": 7,
            "types": [
                "Steam ship",
                "Military ship"
            ]
        },
        ...
    ]
}
```

### Available options
| URL                                      | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| `/ships`                                 | Retrieve all ships.                      |
| `/ships?types=Unique`                    | Retrieve ships filtered by type. |
| `/ships?sort=name`                       | Retrieve all ships sorted by name in ascending order. |
| `/ships?sort=-total_slots`               | Retrieve all ships sorted by number of all slots in descending order. |

## Getting list of Supplies

### Request
`GET /supplies`

`curl -i -H 'Accept: application/json' http://localhost:5050/supplies`

### Response
```
HTTP/1.1 200 OK
Server: gunicorn
Date: Wed, 26 Apr 2023 18:40:55 GMT
Connection: close
Content-Type: application/json
Content-Length: 1378479
Access-Control-Allow-Origin: *

{
    "_filters": {},
    "objects": [
        {
            "_id": "641b089f4f252f6af8a4e039",
            "base_morale": 0,
            "bonuses": {
                "crafting": 0,
                "diplomacy": 0,
                "faith": 0,
                "force": 0,
                "hunting": 0,
                "medicine": 0,
                "naval_power": 30,
                "navigation": 0
            },
            "combined_morale_per_50t": 30,
            "extra_rations": false,
            "image_src": "data:image/png;base64,UklGRtAnAABXRUJQVlA4WAoAAAAUAAAAfwAAfwAAQUxQSP8LAAABl8cgkqQ49OBfNeSPgIjI4X+...+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+",
            "name": "Advanced Weapons"
        },
        ...
    ]
}
```

### Available options
| URL                                      | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| `/supplies`                              | Retrieve all supplies.                   |
| `/supplies?&name__contains=sa`           | Retrieve supplies filtered by name. |
| `/supplies?sort=-bonuses.medicine`       | Retrieve all supplies ordered by medicine bonuse in descending order. |

_____

## Technology stack

- Flask -- for API implementation. 
- PyMongo -- to interact with MongoDB.
- pytest -- for testing.
