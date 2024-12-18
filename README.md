# Automated greet on Google Meet

Uses Python to capture a video feed which is then sent to Google Meet, along with a JS script to detect new participants. When someone joins, they will be automatically greeted with a waving animation overlaid on the video feed.

Robot hand waving coming next...

## Requirements

Only tested on macOS 15 and using Chrome.

* [asdf](https://asdf-vm.com/)
* [OBS](https://obsproject.com/)

## Instructions

1. Install the requirements:
```bash
asdf install
pip install -r requirements.txt
```
2. Run the script:
```bash
python main.py
```
3. Open OBS and add a new source of type "macOS Screen Capture" with the method "Window Capture" and the window "[python] Video Feed"
4. Start the virtual camera in OBS
5. Open Google Meet and select the OBS virtual camera as the video source
6. In a Google Meet call, open the "People" (or "Participants") panel
7. Run the `browser-console.js` script in the DevTools console and enjoy the automated greets whenever someone joins

## Notes

Press 'w' when viewing the Python video feed window to toggle a greeting.

Work in progress: packaging the `browser-console.js` script into a Chrome extension.

[pyvirtualcam](https://pypi.org/project/pyvirtualcam/) would be preferable to OBS, but it doesn't seem to work yet on macOS 15.
