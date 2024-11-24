from services.WorkJouneyStatusServices import publish_journey_status
from services.WeatherStatusServices import publish_weather


if __name__ == "__main__":
    publish_weather("Clichy FR")
    publish_journey_status()
    print("End of the program")