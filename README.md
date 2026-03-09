# Automated greet on Google Meet

Consists of some JavaScript which detects when a new participant joins a Google Meet call, then either:

* They will be greeted by a waving animation overlaid on your video feed
* A [Build HAT](https://www.raspberrypi.com/products/build-hat/), connected to a Raspberry Pi, rotates a Lego motor with a hand-waving mechanism attached to it to greet them, eg:

  https://github.com/user-attachments/assets/4f15fe1c-9a65-493a-97ef-2f3a92965a57

## Requirements

Only tested on macOS 15 and using Chrome.

* [asdf](https://asdf-vm.com/)
* [OBS](https://obsproject.com/) (for the video overlay)

## Instructions

Install the requirements:

```bash
asdf install
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

For the Build HAT / robot hand wave (ie. anything that's not hosted on the local machine), the script running in the browser console in Google Meet requires HTTPS for all `fetch()` requests, so install ngrok on the Pi (https://ngrok.com/docs/guides/device-gateway/raspberry-pi/) followed by:

```bash
ngrok http 5000
```

This will set up a tunnel to the local server running on port 5000, and give you a URL over HTTPS that you can use in the browser console script which you can append the participant joined path to, eg. `https://11e4-xxx-xxx-xxx-xxx.ngrok-free.app/participant-joined`. Use this URL in the `browser-console.js` script (below) in place of `http://localhost:5000`.

A self-signed certificate could also be used, but this involves a bit more faff.

### For the animation / overlay:

1. Run the HTTP server and video feed:
```bash
python animate-wave.py
```
2. Open OBS and add a new source of type "macOS Screen Capture" with the method "Window Capture" and the window "[python] Video Feed"
3. Start the virtual camera in OBS
4. Open Google Meet and select the OBS virtual camera as the video source
5. In a Google Meet call, open the "People" (or "Participants") panel
6. Run the `browser-console.js` script in the DevTools console and enjoy the automated greets whenever someone joins

Press 'w' when viewing the Python video feed window to toggle a greeting manually.

[pyvirtualcam](https://pypi.org/project/pyvirtualcam/) would be preferable to OBS, but it doesn't seem to work yet on macOS 15.

### For the Build HAT motor:

1. Run the script on a Raspberry Pi with a Build HAT connected, and a motor connected to port A (build an appropriate hand waving mechanism connceted to the motor), `sudo` is needed for keyboard access:
```bash
python robot-wave.py
```
2. In a Google Meet call, open the "People" (or "Participants") panel
3. Run the `browser-console.js` script (switching out `http://localhost` for the address of the Raspberry Pi / ngrok tunnel, as above) in the DevTools console and enjoy the robot hand wave whenever someone joins

## Notes

Work in progress: packaging the `browser-console.js` script into a Chrome extension.
