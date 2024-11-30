from src.backApiCaller.SncfApiCaller import callForJourney, callForStatus
from src.mqtt.MQTTPublisher import ClockMQTTPublisher
from src.utils.ColorsUtils import hex_to_rgb
from src.backApiCaller.GeoCodeApi import getLatitudeAndLongitude
import html

def getDataOfJourney(params):
    data = callForJourney(params)
    return data

def constructJourneyParams(fromPoint,toPoint):
    params = {
        "from": fromPoint,
        "to": toPoint,
        "max_nb_journeys":"1"
    }
    return params

def getDurationOfJourney(data):
    duration = data["journeys"][0]["duration"]#take the first journey and get the duration
    durationMin=duration/60
    return int(durationMin)

#https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/line_reports/physical_modes/physical_mode%3AMetro/lines/line%3AIDFM%3AC01383/line_reports?
def statusLine(data):
    #for each elments of list in data.sections , go to fiels links that is a list and take element objetc that have obj.type="line" and  "type": "physical_mode",
    arrayLineInfo = []
    for section in data["journeys"][0]["sections"]:
        if(section["type"]!="public_transport"):
            continue
        objInfoLine = {}
        links = section["links"]
        for link in links:
            if link["type"]=="line" :
                objInfoLine["line"]=link
            elif link["type"]=="physical_mode":
                objInfoLine["physical_mode"]=link
            else:
                continue
        if(objInfoLine not in arrayLineInfo):
            arrayLineInfo.append(objInfoLine)
    listOfDisruptions = []
    # for each element of arrayLineInfo, get the line_id and call the api to get the status of the line
    for lineInfo in arrayLineInfo:
        physical_mode = lineInfo["physical_mode"]
        line = lineInfo["line"]
        paths = f"physical_modes/{physical_mode['id']}/lines/{line['id']}/line_reports"
        data = callForStatus(paths,None)
        if data is None:
            continue
        status = data["disruptions"]
        print(status)
        #filter on each status to have only where object is status=active and tags contains "Actualité"
        filtered = [s for s in status if s["status"] == "active" and "tags" in s and "Actualité" in s["tags"]]
        if len(filtered)!=0:
            listOfDisruptions.append(filtered)
    return listOfDisruptions

def constructStatusAndJourneyMessage(durationMin,disruptionsList):
    # Valeurs par défaut
    statusColor = [0, 255, 0]
    statusMessage = ""
    # Mise à jour des valeurs si le statut est disponible
    if len(disruptionsList)!=0:
        statusColor = hex_to_rgb(disruptionsList[0][0]['severity']['color'])
    # Construction du message principal
    message = [
        {
            "duration": 10,
            "icon": "1395",
            "text": f"{durationMin} min",
            "noscroll": True,
            "color": statusColor,
            "retain": True  # Garde uniquement le dernier message
        }
    ]
    # Ajout des messages de disruption lis
    for disruptionsByline in disruptionsList:
        for disruption in disruptionsByline:
            statusMessage = next((msg["text"] for msg in disruption["messages"] if msg["channel"]["content_type"] == "text/plain"),None)            
            statusColor = hex_to_rgb(disruption["severity"]["color"])
            message.append(
            {
                "text": statusMessage,
                "icon": "620",
                "color": statusColor,
                "retain": True
            }
            )
    return message


def constructJourneyParamsAndCall(fromAddress,toAddress):
    coordFrom = getLatitudeAndLongitude(fromAddress)
    coordTo = getLatitudeAndLongitude(toAddress)
    coordFromStr = str.format("{0};{1}", coordFrom['lon'], coordFrom['lat'])
    coordToStr = str.format("{0};{1}", coordTo['lon'], coordTo['lat'])
    params=constructJourneyParams(coordFromStr, coordToStr)
    data = getDataOfJourney(params)
    timeMin = getDurationOfJourney(data)
    disruptionsList = statusLine(data)
    return timeMin,disruptionsList


def publish_journey_status(fromAddress="23 rue leon blum Clichy 92110,FR", toAddress="40 rue du colisee , Paris, FR"):   
    publisher = ClockMQTTPublisher()
    timeMin, disruptionsList = constructJourneyParamsAndCall(fromAddress,toAddress)
    objmessage = constructStatusAndJourneyMessage(timeMin, disruptionsList)
    publisher.publishJourneyDurationAndTrainStatus(objmessage)
    publisher.disconnect()

def getJourneyStatus(fromAddress="23 rue leon blum Clichy 92110,FR", toAddress="40 rue du colisee , Paris, FR"):
    timeMin, disruptionsList = constructJourneyParamsAndCall(fromAddress,toAddress)
    return timeMin, disruptionsList