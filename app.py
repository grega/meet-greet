from flask import Flask
from flask_cors import CORS
from threading import Thread
import cv2
import numpy as np
import math
import time

# Flask bit for handling incoming requests / notifications...
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
new_participant_event = False 

@app.route('/participant-joined', methods=['GET'])
def participant_joined():
    global new_participant_event
    new_participant_event = True
    return "Participant join detected", 200

def run_flask():
    app.run(port=5000, host='0.0.0.0', debug=False, use_reloader=False)

# animation params
wave_amplitude = 30 # vertical motion amplitude (pixels)
wave_frequency = 0.1 # wave speed
animation_duration = 3

def display_video():
    # open the default webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Cannot access the webcam")
        return

    hand_image = cv2.imread('hand.png', cv2.IMREAD_UNCHANGED)
    if hand_image is None:
        print("Error: Cannot load the hand image")
        return

    hand_height, hand_width = hand_image.shape[:2]

    frame_count = 0
    show_animation = False
    animation_start_time = None

    while True:
        # read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video")
            break

        # check if a new participant event was triggered
        global new_participant_event
        if new_participant_event:
            show_animation = True
            animation_start_time = time.time()
            new_participant_event = False  # reset the flag

        # check for manual wave trigger (press 'w')
        if cv2.waitKey(1) & 0xFF == ord('w'):
            show_animation = True
            animation_start_time = time.time()

        # show waving...
        if show_animation:
            elapsed_time = time.time() - animation_start_time 
            if elapsed_time <= animation_duration:

                wave_offset = int(wave_amplitude * math.sin(frame_count * wave_frequency))

                # rotate the hand image
                hand_height, hand_width = 250, 250
                resized_hand = cv2.resize(hand_image, (hand_width, hand_height))

                # calculate rotation angle (oscillating back and forth)
                angle = 15 * math.sin(frame_count * wave_frequency) # 15 degrees max rotation
                center = (hand_width // 2, hand_height // 2)
                rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                rotated_hand = cv2.warpAffine(resized_hand, rotation_matrix, (hand_width, hand_height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))

                # set the hand overlay position
                frame_height, frame_width, _ = frame.shape
                x_offset = frame_width - hand_width - 300 + wave_offset
                y_offset = frame_height - hand_height - 60 + wave_offset

                # ensure the overlay doesn't exceed frame boundaries
                y_end = min(y_offset + hand_height, frame_height)
                x_end = min(x_offset + hand_width, frame_width)
                y_offset = max(y_offset, 0)
                x_offset = max(x_offset, 0)

                rotated_hand = rotated_hand[:y_end - y_offset, :x_end - x_offset]

                # handle transparency (alpha channel)
                if rotated_hand.shape[2] == 4:
                    hand_rgb = rotated_hand[:, :, :3]
                    hand_alpha = rotated_hand[:, :, 3] / 255.0 # normalize alpha values to [0, 1]
                    roi = frame[y_offset:y_end, x_offset:x_end]

                    for c in range(3): # blend each color channel
                        roi[:, :, c] = (hand_alpha * hand_rgb[:, :, c] +
                                        (1 - hand_alpha) * roi[:, :, c])

                    frame[y_offset:y_end, x_offset:x_end] = roi
        else:
            show_animation = False

        cv2.imshow("Video Feed", frame)
        frame_count += 1

        # check for quit (press 'q')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# start Flask server and video display
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    try:
        display_video()
    except KeyboardInterrupt:
        print("Shutting down...")
