from services.WeatherStatusServices import publish_weather


if __name__ == "__main__":
    publish_weather("Clichy FR")
    print("End of weather program")