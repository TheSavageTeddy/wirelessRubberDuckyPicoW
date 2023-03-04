
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


def _sendkeys(keys: list):
    #print("keys", keys)
    try:
        for key in keys:
            if type(key) == str:
                layout.write(key)
            elif type(key) == list:
                if key[0] == "MOUSE":
                    try:
                        mouse.move(x=int(key[1]), y=int(key[2]))
                    except Exception as e:
                        print("MOUSE error:", e)
                        continue
                elif key[0] == "CLICK":
                    try:
                        mouse.click(int(key[1]))
                    except Exception as e:
                        print("CLICK error:", e)
                        continue
                elif key[0] == "SLEEP":
                    try:
                        time.sleep(float(key[1])/1000)
                    except ZeroDivisionError:
                        print("SLEEP error cannot divide by 0, ignoring...")
                        continue
                else:
                    try:
                        if key[1] == "DOWN":
                            keyboard.press(eval(f"Keycode.{key[0]}"))
                        else:
                            keyboard.release(eval(f"Keycode.{key[0]}"))
                    except Exception as e:
                        print("KEYS error:", e)
                        continue
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
    exit(0)
    return


#setup rubber ducky devices
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)

# serve the server
server.serve_forever(str(wifi.radio.ipv4_address))