#Installed with python
import time
import asyncio

#Have to install
import simpleobsws

#Handmade
import obsFunctions
import lolFunctions


locales = [
    "en_US","cs_CZ","de_DE","el_GR","en_AU","en_GB","en_PH","en_SG","es_AR","es_ES","es_MX","fr_FR",
    "hu_HU","it_IT","ja_JP","ko_KR","pl_PL","pt_BR","ro_RO","ru_RU","th_TH","tr_TR","vi_VN","zh_CN",
    "zh_MY","zh_TW"
]
locale = "fr_FR" #Choose the one of your game
refreshDelay = 5 #How much seconds between each check for items
showTime = 3 #How much seconds the item informations are shown, 0 or below to keep it until the next item is bought
items = [
    "dark seal",
    "warmog",
    "mejai"
] #What must be in item name to be shown (exemple: if 'a' is in it, all items with an 'a' in name will be shown, so '' means every item)
sceneName = "Scene" #Scene where image will show
password = "" #Password in obs web socket settings

def condition(item):
    for allowedItem in items:
        if item.get("name").lower().find(allowedItem) != -1: return True
    return False

def showItem(item, ws: simpleobsws.WebSocketClient):


async def checkItems(mustShow, show):
    ws = simpleobsws.WebSocketClient(password = password)
    while True:
        if not lolFunctions.isInGame():
            time.sleep(refreshDelay)
            continue
        oldItemsCount = lolFunctions.countItems(lolFunctions.getCurrentPlayerItems())
        time.sleep(refreshDelay)
        newItemsCount = lolFunctions.countItems(lolFunctions.getCurrentPlayerItems())
        if oldItemsCount != newItemsCount:
            for key in newItemsCount.keys():
                if key not in oldItemsCount.keys():
                    completeItem = lolFunctions.getDdragon(lolFunctions.findItem(lolFunctions.getCurrentPlayerItems(), key))
                    if mustShow(completeItem):
                        await show(completeItem, ws)

loop = asyncio.get_event_loop()
loop.run_until_complete(checkItems())