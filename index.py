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
refreshDelay = 1 #How much seconds between each check for items
showTime = 2 #How much seconds the item informations are shown, 0 or below to keep it until the next item is bought
items = [
    "dark seal",
    "warmog",
    "mejai"
] #What must be in item name to be shown (exemple: if 'a' is in it, all items with an 'a' in name will be shown, so '' means every item)
sceneName = "TestLol" #Scene where image will show
imageName = "ItemBought" #The image source name that will change (if already created, it must be a browser source)
textName = "ItemBoughtText" #The text source name that will change (if already created, it must be a gdi+ text)
password = "1kSWUJH7GSNZauCt" #Password in obs web socket settings

def condition(item):
    for allowedItem in items:
        if item.get("name").lower().find(allowedItem) != -1:
            return True
    return False

async def showItem(item, id, ws: simpleobsws.WebSocketClient):
    await obsFunctions.setImage(ws, sceneName, imageName, f"https://ddragon.leagueoflegends.com/cdn/{lolFunctions.getVersion()}/img/item/{id}.png")
    await obsFunctions.setText(ws, sceneName, textName, f"{item.get('name')} bought", fontSize=64, textColor=color(150, 150, 0))
    time.sleep(0.1)
    await obsFunctions.setTransform(ws, sceneName, imageName, align="center", verticalAlign="middle", y=-100, width=200)
    await obsFunctions.setTransform(ws, sceneName, textName, align="center", verticalAlign="middle", y=100)
    await obsFunctions.showSource(ws, sceneName, imageName)
    await obsFunctions.showSource(ws, sceneName, textName)
    if(showTime > 0):
        time.sleep(showTime)
        await obsFunctions.hideSource(ws, sceneName, imageName)
        await obsFunctions.hideSource(ws, sceneName, textName)



def color(r, g, b):
    return r + g * 256 + b * 256 * 256 

async def checkItems(mustShow, show):
    ws = simpleobsws.WebSocketClient(password = password)
    while True:
        try:
            if not lolFunctions.isInGame():
                time.sleep(refreshDelay)
                continue
            oldItemsCount = lolFunctions.countItems(lolFunctions.getCurrentPlayerItems())
            time.sleep(refreshDelay)
            newItemsCount = lolFunctions.countItems(lolFunctions.getCurrentPlayerItems())
            if oldItemsCount != newItemsCount:
                for key in newItemsCount.keys():
                    if key not in oldItemsCount.keys():
                        itemId = str(lolFunctions.findItem(lolFunctions.getCurrentPlayerItems(), key).get("itemID"))
                        completeItem = lolFunctions.getDdragon(itemId, locale)
                        if mustShow(completeItem):
                            await show(completeItem, itemId, ws)
        except:
            time.sleep(refreshDelay)

loop = asyncio.get_event_loop()
loop.run_until_complete(checkItems(condition, showItem))