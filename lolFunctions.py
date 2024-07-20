#Have to install
import requests

#Handmade
import findFunctions

def getAllData():
    return requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata", verify=False).json()

def getCurrentPlayerData():
    allData = getAllData()
    return findFunctions.findList(allData.get("allPlayers"), lambda e, i, l: e.get("riotId") == allData.get("activePlayer").get("riotId"))

def getCurrentPlayerItems():
    playerData = getCurrentPlayerData()
    return playerData.get("items")

def countItems(items):
    result = {}
    for item in items:
        if result.get(item.get("displayName")):
            result[item.get("displayName")] += 1
        else:
            result[item.get("displayName")] = 0
    return result

def findItem(items, itemName):
    return findFunctions.findList(items, lambda e, i, l: e.get("displayName") == itemName)

def getDdragon(itemId, locale = "en_US"):
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    return requests.get(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/item.json").json().get("data").get(itemId)