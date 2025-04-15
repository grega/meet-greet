# Automated greets on Google Meet

Either:
* Uses Python to capture a video feed which is then sent to Google Meet, along with a script to detect when someone joins the call. When someone joins, they will be automatically greeted with a waving animation overlaid on the video feed
* Uses Python and the Build HAT library, running on a Raspberry Pi (with Build HAT connected), to rotate a motor which can have some sort of hand-waving mechanism attached to it. When someone joins, they will be automatically greeted with a waving robotic hand

## Requirements

Only tested on macOS 15 and using Chrome.

* [asdf](https://asdf-vm.com/)
* [OBS](https://obsproject.com/) (for the video overlay)

## Instructions

Install the requirements:
```bash
asdf install
pip install -r requirements.txt
```

### For the animation / overlay:

1. Run the script:
```bash
python animate-wave.py
```
2. Open OBS and add a new source of type "macOS Screen Capture" with the method "Window Capture" and the window "[python] Video Feed"
3. Start the virtual camera in OBS
4. Open Google Meet and select the OBS virtual camera as the video source
5. In a Google Meet call, open the "People" (or "Participants") panel
6. Run the `browser-console.js` script in the DevTools console and enjoy the automated greets whenever someone joins

### For the Build HAT motor:

1. Run the script on a Raspberry Pi with a Build HAT connected, and a motor connected to port A (build an appropriate hand waving mechanism connceted to the motor), `sudo` is needed for keyboard access:
```bash
sudo python robot-wave.py
```
2. In a Google Meet call, open the "People" (or "Participants") panel
3. Run the `browser-console.js` script (switching out `http://localhost` for the address of the Raspberry Pi) in the DevTools console and enjoy the robot hand wave whenever someone joins

## Notes

Press 'w' when viewing the Python video feed window, or when running the Build HAT service, to toggle a greeting manually.

Work in progress: packaging the `browser-console.js` script into a Chrome extension.

[pyvirtualcam](https://pypi.org/project/pyvirtualcam/) would be preferable to OBS, but it doesn't seem to work yet on macOS 15.
