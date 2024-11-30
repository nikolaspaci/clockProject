from flask import Flask, jsonify, request
from flasgger import Swagger
from src.services.WeatherStatusServices import publish_weather,getWeather
from src.services.WorkJouneyStatusServices import publish_journey_status,getJourneyStatus

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/clock/publish_weather', methods=['GET'])
def weather_endpoint():
    """
    Publish weather information to the mqtt broker
    ---
    parameters:
      - name: address
        in: query
        type: string
        required: false
        description: The address to get the weather for
    responses:
      200:
        description: Weather published successfully
    """
    address = request.args.get('address')
    publish_weather(address)
    return jsonify({"message": "Weather published successfully"}), 200

@app.route('/clock/publish_journey_status', methods=['GET'])
def journey_status_endpoint():
    """
    Publish journey status information to the mqtt broker
    ---
    parameters:
      - name: fromAddress
        in: query
        type: string
        required: false
        description: The starting address for the journey
      - name: toAddress
        in: query
        type: string
        required: false
        description: The destination address for the journey
    responses:
      200:
        description: Journey status published successfully
    """
    fromAddress = request.args.get('fromAddress')
    toAddress = request.args.get('toAddress')
    publish_journey_status(fromAddress, toAddress)
    return jsonify({"message": "Journey status published successfully"}), 200

@app.route('/journey_status', methods=['GET'])
def get_journey_status():
    """
    Get journey status information
    ---
    parameters:
      - name: fromAddress
        in: query
        type: string
        required: false
        description: The starting address for the journey
      - name: toAddress
        in: query
        type: string
        required: false
        description: The destination address for the journey
    responses:
      200:
        description: Journey status retrieved successfully
    """
    fromAddress = request.args.get('fromAddress')
    toAddress = request.args.get('toAddress')
    timeMin, disruptionsList = getJourneyStatus(fromAddress, toAddress)
    return jsonify({"timeMin": timeMin, "disruptionsList": disruptionsList}), 200


@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Get weather information
    ---
    parameters:
      - name: address
        in: query
        type: string
        required: false
        description: The address to get the weather for
    responses:
      200:
        description: Weather retrieved successfully
    """
    address = request.args.get('address')
    weather = getWeather(address)
    return jsonify({"weather": weather}), 200



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)