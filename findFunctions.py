def findDict(dictionnary, func):
    for key in dictionnary.keys():
        if(func(dictionnary.get(key), key, dictionnary)):
            return dictionnary.get(key)
    return None

def findDictKey(dictionnary, func):
    for key in dictionnary.keys():
        if(func(dictionnary.get(key), key, dictionnary)):
            return key
    return None

def findList(l, func):
    for i, elem in enumerate(l):
        if(func(elem, i, l)):
            return elem
    return None

def findListIndex(l, func):
    for i, elem in enumerate(l):
        if(func(elem, i, l)):
            return i
    return None