
#webserver stuff
import socketpool
import wifi
from adafruit_httpserver.server import *
from adafruit_httpserver.request import *
from adafruit_httpserver.response import *
from adafruit_httpserver.route import *


#rubber ducky stuff
import time
import os
import usb_hid
import json
import creds
import binascii
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from adafruit_hid.mouse import Mouse


'''
rubber duck! made by TheSavageTeddy (github)

note: if the filename is 'code.py', it is automatically ran when the pico W is powered
'''


ssid = creds.ssid
wifipassword = creds.wifipassword


print("Connecting to", ssid)
wifi.radio.connect(ssid, wifipassword)
print("Connected to", ssid)
print(f"Listening on http://{wifi.radio.ipv4_address}:80")

pool = socketpool.SocketPool(wifi.radio)
server = HTTPServer(pool)

def _mouseMove(x, y):
    print("moving mouse",x,y)
    mouse.move(x=x, y=y)

def _mouseClick(button):
    mouse.click(button)

def _mouseButton(button, release):
    if release:
        mouse.release(button)
    else:
        mouse.press(button)

def _modifierKey(key, release):
    print(key, release)
    if release:
        keyboard.release(eval(f"Keycode.{key}"))
    else:
        keyboard.press(eval(f"Keycode.{key}"))

def _sendkeys(keys: list):
    try:
        for key in keys:
            print(key)
            if type(key) == str:
                # Write text by typing the string
                layout.write(key)
            elif type(key) == list:
                command = key[0].upper()
                if command == "MOUSE":
                    mouse_command = key[1].upper()
                    if mouse_command == "MOVE":
                        x_pos = int(key[2])
                        y_pos = int(key[3])
                        _mouseMove(x_pos, y_pos)
                    else:
                        try:
                            mouse_button = int(key[2])
                        except IndexError:
                            # some people might forget to put the mouse button, so default to left
                            mouse_button = 1
                        if mouse_command == "DOWN":
                            _mouseButton(mouse_button, False)
                        elif mouse_command == "UP":
                            _mouseButton(mouse_button, True)
                        elif mouse_command == "CLICK":
                            _mouseClick(mouse_button)
                        else:
                            print(f"Mouse command {mouse_command} not found, ignoring...")
                elif command == "SLEEP":
                    time.sleep(float(key[1])/1000)
                else:
                    release = key[1].upper() == "UP"
                    modifier_key = key[0].upper()
                    _modifierKey(modifier_key, release)
    except Exception as e:
        print(f"An error occured: {e}")


@server.route("/")
def base(request):  # pylint: disable=unused-argument
    """Default reponse is /index.html"""
    return HTTPResponse(filename="/index.html")

@server.route("/sendkeys", "GET")
def sendkeys(keys):
    request = HTTPRequest(raw_request=keys.raw_request)
    request_data = request.query_params
    
    try:
        keys = binascii.unhexlify(request_data["keys"])
        keys = json.loads(keys)
        keys = keys["keys"]
    except ValueError as e:
        print(f"payload not sent: error {e}")
        
        return HTTPResponse(filename="/index.html")

    _sendkeys(keys)
                    
    return HTTPResponse(filename="/index.html")

@server.route("/terminate", "POST")
def terminate(request):
    exit(0) # apparently exit isn't even a function so it crashes anyways
    return


#setup rubber ducky devices
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)

# serve the server
server.serve_forever(str(wifi.radio.ipv4_address))
