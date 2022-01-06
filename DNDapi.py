from dataclasses import dataclass,field
import requests
from bs4 import BeautifulSoup

@dataclass
class equipment:
    index: str
    name: str
    category: str
    cost: str
    # weapon_category: str
    # weapon_range: str
    # range: list
    # weight: int
    # properties: list
    def __str__(self):
        print(f'index: {self.index}')
        print(f'name: {self.name}')
        print(f'cost: {self.cost}')
        print(f'category: {self.category}')
        return '\r'

@dataclass
class classes:
    index: str
    name: str
    hit_die : int #health
    proficiencies: list
    saving_throws: list
    subclasses: list
    # spells: str
    # startingEquipment: equipment #list of objects

    def __str__(self):
        print(f"Name: {self.name}")
        print(f"Hit Die: {self.hit_die}")
        print(f"Proficiencies: {self.proficiencies}")
        print(f"Saving Throws: {self.saving_throws}")
        print(f"Subclasses: {self.subclasses}")
        return "\r"

@dataclass
class races:
    index: str
    name: str
    speed: int
    size: str
    traits: dict
    subraces: dict
    # alignment: str #desc
    # age: str #desc
    # size_desc: str #desc
    # starting_proficiencies: list
    # language: list
    # language_desc: list

    def __str__(self):
        print(f'index: {self.index}')
        print(f'name: {self.name}')
        print(f'speed: {self.speed}')
        print(f'size: {self.size}')
        print(f'traits: {", ".join(self.traits.keys())}')
        print(f'subraces: {", ".join(self.subraces.keys())}')
        return '\r'

@dataclass
class spells:
    index: str
    name: str
    description: str
    range: str
    material: str
    ritual: bool
    casting_time: str
    #level: int
    #damage: dict

    def __str__(self):
        print(f"Name: {self.name}")
        print(f"Range: {self.range}")
        print(f"Casting Time: {self.casting_time}")
        return '\r'
     
@dataclass
class monsters:
    index: str
    name: str
    hit_points: int
    size: str
    alignment: str

    def __str__(self):
        print(f'index: {self.index}')
        print(f'name: {self.name}')
        print(f'hit_points: {self.hit_points}')
        print(f'size: {self.size}')
        print(f'alignment: {self.alignment}')
        return '\r'

#read html data into json
def getJSON(url):
    return requests.get(url).json()

# import races data
def importRaces():
    _races = {}
    _race = {}
    _url_main = 'https://www.dnd5eapi.co'
    _url_sub = '/api/races'
    _json = getJSON(_url_main + _url_sub)
    for x in _json['results']:
        _traits = {}
        _subraces = {}
        #specific detail nested in url
        _temp_dict = getJSON(_url_main + x['url'])
        #subrace list
        for s in _temp_dict['subraces']:
            _subraces[s['name']] = s['index']
        #trait list
        for s in _temp_dict['traits']:
            _traits[s['name']] = s['index']
            
        _races[x['index']] = races(x['index'],x['name'],_temp_dict['speed'],_temp_dict['size'],_traits,_subraces)
    return _races

#import classes data
def importClasses():
    url_list = []
    class_dict = {}
    response = requests.get('https://www.dnd5eapi.co/api/classes/')
    data = response.json()
    for result in data['results']:
        class_url = "https://www.dnd5eapi.co" + result['url']
        url_list.append(class_url)  
    for url in url_list:
        response = requests.get(url)
        data = response.json()
        class_dict[data['index']] = classes(data['index'], data['name'], data['hit_die'], data['proficiencies'],  data['saving_throws'], data['subclasses'])
    return class_dict

#import spell data
def importSpells():
    url_list = []
    spell_dict = {}
    response = requests.get('https://www.dnd5eapi.co/api/spells/')
    data = response.json()
    for result in data['results']:
        spell_url = "https://www.dnd5eapi.co" + result['url']
        url_list.append(spell_url)
    for url in url_list:
        response = requests.get(url)
        print (f'Now reading {url}')
        data = response.json()
        spell_dict[data['index']] = spells(data['index'], data['name'], data['desc'], data['range'],\
                    data['ritual'], data['casting_time'], data['level'])
    return spell_dict

#import monster data
def importMonster():
    totalMonsterResponse = requests.get("https://www.dnd5eapi.co/api/monsters")

    totalMonsterResponseList = totalMonsterResponse.json()

    monsterList = []

    for monster in totalMonsterResponseList["results"]:
        monsterResponse = requests.get("https://www.dnd5eapi.co/api/monsters/" + monster["index"])
        print (f'Now reading {monster["index"]}')
        monsterJSON = monsterResponse.json()
        monsterList.append(monsterJSON)

    monsterDictionary = {}

    for monster in monsterList:
        tempMonster = monsters(monster["index"],monster["name"],monster["hit_points"],monster["size"],monster["alignment"])
        monsterDictionary[monster["index"]] = tempMonster

    return monsterDictionary

#import equipment data
def importEquipment():
    equipmentResponse = requests.get("https://www.dnd5eapi.co/api/equipment")

    equipList = equipmentResponse.json()

    itemList = []

    for item in equipList["results"]:
        itemResponse = requests.get("https://www.dnd5eapi.co/api/equipment/"+item["index"])
        print (f'Now reading {item["index"]}')
        itemJSON = itemResponse.json()
        itemList.append(itemJSON)

    equipmentDictionary = {}

    for item in itemList:
        tempItem = equipment(item["index"],item["name"],item["equipment_category"]["index"],str(item["cost"]["quantity"]) + item["cost"]["unit"])
        equipmentDictionary[item["index"]] = tempItem
    
    return equipmentDictionary

# Test
# _classes = importClasses()
# for x in _classes:
#     print(_classes[x])

# _spells = importSpells()
# for x in _spells:
#     print(_spells[x])

# _equipment = importEquipment()
# for x in _equipment:
#     print(_equipment[x])

# _races = importRaces()
# for x in _races:
#     print(_races[x])

# _monsters = importMonster()
# for x in _monsters:
#     print(_monsters[x])