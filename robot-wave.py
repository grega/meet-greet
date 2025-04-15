from flask import Flask
from flask_cors import CORS
from buildhat import Motor
import threading
import time
import keyboard

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
            for _ in range(6): # 6 alternating 90 degree rotations at 50% speed
                motor.run_for_degrees(90, 50)
                time.sleep(0.5)
                motor.run_for_degrees(-90, 50)
                time.sleep(0.5)
            new_participant_event = False
        time.sleep(0.1)

def handle_key_press():
    global new_participant_event
    while True:
        if keyboard.is_pressed('w'):
            print("Keypress 'w' detected")
            new_participant_event = True
            time.sleep(0.5) # debounce
        time.sleep(0.1)

def run_flask():
    app.run(port=5000, host='0.0.0.0', debug=False, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=handle_motor_event, daemon=True).start()
    threading.Thread(target=handle_key_press, daemon=True).start()
    run_flask()
