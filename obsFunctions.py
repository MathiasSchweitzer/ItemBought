#Installed with python
import math

#Have to install
import simpleobsws

async def setImage(ws: simpleobsws.WebSocketClient, url, sceneName, sourceName, enabled = True):
    await setInput(ws, sceneName, sourceName, "browser_source", {
        "url": url
    }, enabled)

async def setInput(ws: simpleobsws.WebSocketClient, sceneName, sourceName, inputKind, inputSettings = {}, enabled = True):
    await ws.connect()
    await ws.wait_until_identified()
    
    idRet = await ws.call(simpleobsws.Request("GetSceneItemId", {
        "sourceName": sourceName,
        "sceneName": sceneName
    }))

    if not idRet.ok():
        if idRet.requestStatus.code == 600:
            await addInput(ws, sceneName, sourceName, inputKind, inputSettings, enabled)

        else:
            print(idRet.requestStatus)
            await ws.disconnect()
            return
    else:
        editSettingsRet = await ws.call(simpleobsws.Request("SetInputSettings", {
            "inputName": sourceName,
            "sceneName": sceneName,
            "inputSettings": inputSettings
        }))
        if not editSettingsRet.ok():
            print(editSettingsRet.requestStatus)
            await ws.disconnect()
            return

    await ws.disconnect()

async def addInput(ws: simpleobsws.WebSocketClient, sceneName, sourceName, inputKind, inputSettings = {}, enabled = True):
    await ws.connect()
    await ws.wait_until_identified()

    createRet = await ws.call(simpleobsws.Request("CreateInput", {
        "inputName": sourceName,
        "sceneName": sceneName,
        "inputKind": inputKind,
        "inputSettings": inputSettings,
        "sceneItemEnabled": enabled
    }))
    await ws.disconnect()
    if not createRet.ok():
        print(createRet.requestStatus)

def rgbToDecimal(r, g, b):
    return b * 256 * 256 + g * 256 + r

async def setText(ws: simpleobsws.WebSocketClient, sceneName, sourceName, text, font = "Arial", fontSize = 256, textColor = 16777215, textOpacity = 100, backgroundColor = 0, backgroundOpacity = 0, textAlign = "left", textVerticalAlign = "top", enabled = True):
    await setInput(ws, sceneName, sourceName, "text_gdiplus_v3", {
        "text": text,
        "font": {
            "face": font,
            "size": fontSize
        },
        "align": textAlign,
        "valign": textVerticalAlign,
        "color": textColor,
        "opacity": textOpacity,
        "bk_color": backgroundColor,
        "bk_opacity": backgroundOpacity
    }, enabled)

async def removeInput(ws: simpleobsws.WebSocketClient, sourceName):
    await ws.connect()
    await ws.wait_until_identified()

    removeRet = await ws.call(simpleobsws.Request("RemoveInput", {
        "inputName": sourceName
    }))

    await ws.disconnect()

    if not removeRet.ok():
        print(removeRet.requestStatus)

async def setTransform(ws: simpleobsws.WebSocketClient, sceneName, sourceName, align = None, verticalAlign = None, x = None, y = None, rotation = None, cropBottom = None, cropLeft = None, cropRight = None, cropTop = None, width = None, height = None, scaleX = None, scaleY = None):
    await ws.connect()
    await ws.wait_until_identified()
    
    idRet = await ws.call(simpleobsws.Request("GetSceneItemId", {
        "sourceName": sourceName,
        "sceneName": sceneName
    }))

    if not idRet.ok():
        print(idRet.requestStatus)
        await ws.disconnect()
        return
    id = idRet.responseData.get("sceneItemId")

    getTransformRet = await ws.call(simpleobsws.Request("GetSceneItemTransform", {
        "sceneItemId": id,
        "sceneName": sceneName
    }))

    if not getTransformRet.ok():
        print(getTransformRet.requestStatus)
        await ws.disconnect()
        return
    
    transform = getTransformRet.responseData.get("sceneItemTransform")

    if scaleX == None and scaleY == None:
        if width == None and height == None:
            scaleX, scaleY = transform.get("scaleX"), transform.get("scaleY")
        elif height == None:
            scaleX, scaleY = width / transform.get('sourceWidth'), width / transform.get('sourceWidth')
        elif width == None:
            scaleX, scaleY = height / transform.get('sourceHeight'), height / transform.get('sourceHeight')
        else:
            scaleX, scaleY = width / transform.get('sourceWidth'), height / transform.get('sourceHeight')
    elif scaleX == None:
        scaleX = scaleY
    elif scaleY == None:
        scaleY = scaleX
    positionX, positionY = None, None
    if align == "left":
        positionX = 0
    elif align == "center":
        positionX = 1920 / 2 - transform.get('sourceWidth') * scaleX / 2
    elif align == "right":
        positionX = 1920 - transform.get('sourceWidth') * scaleX
    if verticalAlign == "top":
        positionY = 0
    elif verticalAlign == "middle":
        positionY = 1080 / 2 - transform.get('sourceHeight') * scaleY / 2
    elif verticalAlign == "bottom":
        positionY = 1080 - transform.get('sourceHeight') * scaleY
    if positionX != None and x != None:
        positionX += x
    if positionY != None and y != None:
        positionY += y

    options = {
        "sceneName": sceneName,
        "sceneItemId": id,
        "sceneItemTransform": {}
    }

    finalWidth = transform.get('sourceWidth') * scaleX
    finalHeight = transform.get('sourceHeight') * scaleY
    if rotation != None:
        cos = round(math.cos(math.radians(-rotation)), 5)
        sin = round(math.sin(math.radians(-rotation)), 5)
        oldCos = round(math.cos(math.radians(-transform.get("rotation"))), 5)
        oldSin = round(math.sin(math.radians(-transform.get("rotation"))), 5)
        if positionX == None:
            positionX = transform.get("positionX") - finalWidth / 2 + oldCos * finalWidth / 2 + oldSin * finalHeight / 2
        if positionY == None:
            positionY = transform.get("positionY") - finalHeight / 2 + oldCos * finalHeight / 2 - oldSin * finalWidth / 2
        positionX += finalWidth / 2 - cos * finalWidth / 2 - sin * finalHeight / 2
        positionY += finalHeight / 2 - cos * finalHeight / 2 + sin * finalWidth / 2
    if positionX != None:
        options.get("sceneItemTransform")["positionX"] = positionX

    if positionY != None:
        options.get("sceneItemTransform")["positionY"] = positionY

    if scaleX != None:
        options.get("sceneItemTransform")["scaleX"] = scaleX

    if scaleY != None:
        options.get("sceneItemTransform")["scaleY"] = scaleY
    
    if rotation != None:
        options.get("sceneItemTransform")["rotation"] = rotation
    
    if cropBottom != None:
        options.get("sceneItemTransform")["cropBottom"] = cropBottom
    
    if cropLeft != None:
        options.get("sceneItemTransform")["cropLeft"] = cropLeft
    
    if cropRight != None:
        options.get("sceneItemTransform")["cropRight"] = cropRight
    
    if cropTop != None:
        options.get("sceneItemTransform")["cropTop"] = cropTop

    setTransformReq = await ws.call(simpleobsws.Request("SetSceneItemTransform", options))
    await ws.disconnect()
    if not setTransformReq.ok():
        print(setTransformReq.requestStatus)