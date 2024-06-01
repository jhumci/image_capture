
# Kleines UI zur Aufzeichnung von Bildern auf einer Drehplatte

## Hardware:

- Raspberry Pi 5
- Canon EOS 70D
- Steppermotor ULN2003
- [ ] Größerer Motor 

## Installation

- `ssh bob@raspberrypi.local`, pw: `letmein`
- conenct to wifi `raspi-config`
- Install for camera: `$ sudo apt install gphoto2 && sudo apt install libgphoto2-6`
- make venv: `python3 -m venv .venv`
- activate venv: `source .venv/bin/activate`
- install requirements: `pip install -r requirements.txt`
- run the script: `streamlit run app.py`

- To test the motor:
   - `python schrittmotor_ULN2003_rp5.py`
- To test the camera:
   - `camera.py`

## Issues

- Known Problems: Streamlit does not work on RasPi 3 due to 32 Bit
- [x] GPIO interface is different on Raspberry Pi 5 changes in [schrittmotor_ULN2003.py](./schrittmotor_ULN2003.py) reqired
- [x] Camera with `gphoto2` - if `Could not claim the USB device`
   - https://askubuntu.com/questions/993876/gphoto2-could-not-claim-the-usb-device

## User Interface

- Tab1: Used to capture images from the camera
- Tab2: Used for showing the captured images and playing with canny edge detection



