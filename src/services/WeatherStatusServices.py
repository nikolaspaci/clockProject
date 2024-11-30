from src.backApiCaller.WeatherApiCaller import weatherCallApi
from src.mqtt.MQTTPublisher import ClockMQTTPublisher
from src.backApiCaller.GeoCodeApi import getLatitudeAndLongitude
from datetime import datetime

mapWeatherMainToIdIcon = {
    "Thunderstorm": "2981",
    "Drizzle": "0",
    "Rain": "72",
    "Snow": "2289",
    "Mist": "0",
    "Smoke": "0",
    "Haze": "0",
    "Dust": "0",
    "Fog": "0",
    "Sand": "511",
    "Ash": "0",
    "Squall": "0",
    "Tornado": "2153",
    "Clear": "1246",
    "Clear_night": "26086",
    "Clouds": "22315"
}

def getWeatherCity(address):
    coord=getLatitudeAndLongitude(address)
    lat=coord['lat']
    lon=coord['lon']
    params = {
        "lat": lat,
        "lon": lon
    }
    data = weatherCallApi(params)
    return data


def configure_icon(sunrise, sunset,weatherType):
    now = datetime.now()
    if sunrise <= now <= sunset:
        return mapWeatherMainToIdIcon[weatherType]
    else:
        nightType= str.format("{0}_night",weatherType)
        if(nightType in mapWeatherMainToIdIcon):
            return mapWeatherMainToIdIcon[nightType]
        return mapWeatherMainToIdIcon[weatherType]


def getWeatherMessageMainAndTemperatureAndIcon(address):
    data = getWeatherCity(address)
    main = data["weather"][0]["main"]
    icon=None
    sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(data['sys']['sunset'])
    icon = configure_icon(sunrise, sunset,main)
    temperature = data["main"]["temp"]
    temperatureToDegree = round(temperature - 273.15,1)
    message={
        "duration":5,
        "text":str.format("{0}°C",temperatureToDegree),
        "icon":icon,
        "retain":True
    }
    return message

def getWeather(address):
    data = getWeatherCity(address)
    main = data["weather"][0]["main"]
    temperature = data["main"]["temp"]
    temperatureToDegree = round(temperature - 273.15,1)
    return {"main":main,"temperature":temperatureToDegree}

def publish_weather(address):
    publisher = ClockMQTTPublisher()
    message = getWeatherMessageMainAndTemperatureAndIcon(address)
    publisher.publish(message, "/custom/weather")
    publisher.disconnect()