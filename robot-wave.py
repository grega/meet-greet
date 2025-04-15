from flask import Flask
from flask_cors import CORS
from buildhat import Motor
import threading
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

new_participant_event = False
motor = Motor('A')

@app.route('/participant-joined', methods=['GET'])
def participant_joined():
    global new_participant_event
    new_participant_event = True
    return "Participant join detected", 200

def handle_motor_event():
    global new_participant_event
    while True:
        if new_participant_event:
            print("Motor event triggered")

            for i in range(3):
                motor.run_to_position(25, speed=100)
                time.sleep(0.2)
                motor.run_to_position(0, speed=100)
                time.sleep(0.2)

                motor.run_to_position(-25, speed=100)
                time.sleep(0.2)
                motor.run_to_position(0, speed=100)
                time.sleep(0.2)

            new_participant_event = False
        time.sleep(0.1)

def run_flask():
    app.run(port=5000, host='0.0.0.0', debug=False, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=handle_motor_event, daemon=True).start()
    run_flask()
