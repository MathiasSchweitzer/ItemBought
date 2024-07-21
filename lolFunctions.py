#Have to install
import requests
import requests.certs

#Handmade
import findFunctions

def getAllData():
    return requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata", verify="./riotgames.pem").json()

def getAllCurrentPlayerData():
    allData = getAllData()
    return findFunctions.findList(allData.get("allPlayers"), lambda e, i, l: e.get("riotId") == allData.get("activePlayer").get("riotId"))

def getCurrentPlayerItems():
    playerData = getAllCurrentPlayerData()
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

def getVersion():
    return requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]

def getDdragon(itemId, locale = "en_US"):
    return requests.get(f"https://ddragon.leagueoflegends.com/cdn/{getVersion()}/data/{locale}/item.json").json().get("data").get(itemId)

def isInGame():
    try:
        requests.get("https://127.0.0.1:2999/liveclientdata/allgamedata", verify="./riotgames.pem").ok
        return True
    except:
        return False