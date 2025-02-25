from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import CoDrone_mini
from CoDrone_mini import Direction
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

drone = CoDrone_mini.CoDrone()
drone.pair()

@app.route('/api/drone/status')
def get_drone_status():
    return jsonify({
        'battery': drone.get_battery_percentage(),
        'altitude': drone.get_altitude(),
        'angle': drone.get_angle(),
        'pressure': drone.get_pressure(),
        'temperature': drone.get_drone_temp(),
        'height': drone.get_height()
    })

@socketio.on('drone_command')
def handle_command(data):
    command = data.get('command')
    if command == 'takeoff':
        drone.takeoff()
    elif command == 'land':
        drone.land()
    elif command in ['forward', 'backward', 'left', 'right', 'up', 'down']:
        direction = getattr(Direction, command.upper())
        drone.go(direction, duration=1, power=30)
    elif command == 'flip':
        drone.flip(Direction.FORWARD)
    emit('status_update', {'status': 'success', 'command': command})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
