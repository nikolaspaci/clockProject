from flask import Flask, jsonify, request
from flasgger import Swagger
from src.services.WeatherStatusServices import publish_weather
from src.services.WorkJouneyStatusServices import publish_journey_status

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/publish_weather', methods=['GET'])
def weather_endpoint():
    """
    Publish weather information
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

@app.route('/publish_journey_status', methods=['GET'])
def journey_status_endpoint():
    """
    Publish journey status information
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)