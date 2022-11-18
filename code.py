
#webserver stuff
import socketpool
import wifi
from adafruit_httpserver import HTTPServer, HTTPResponse

#rubber ducky stuff
import time
import os
import usb_hid
import json
import creds
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


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


@server.route("/")
def base(request):  # pylint: disable=unused-argument
    """Default reponse is /index.html"""
    return HTTPResponse(filename="/index.html")

@server.route("/sendkeys", "POST")
def sendkeys(keys):
    print(len(keys.raw_request))
    print(bytes(keys.raw_request).decode())
    keys = bytes(keys.raw_request).decode().split("\r\n")[6].replace("User-Agent: ","")
    keys = json.loads(keys)
    print(keys)

    try:
        for key in keys["keys"]:
            if type(key) == str:
                layout.write(key)
            elif type(key) == list:
                print(key)
                if key[0] == "SLEEP":
                    print(f"SLEEPING for {key[1]}ms")
                    time.sleep(float(key[1])/1000)
                else:
                    if key[1] == "DOWN":
                        keyboard.press(eval(f"Keycode.{key[0]}"))
                    else:
                        keyboard.release(eval(f"Keycode.{key[0]}"))
    except Exception as e:
        print(f"An error occured: {e}")
                    
    return HTTPResponse(filename="/index.html")

@server.route("/terminate", "POST")
def terminate(request):
    exit(0)
    return


#setup rubber ducky devices
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# serve the server
server.request_buffer_size = 110000
server.serve_forever(str(wifi.radio.ipv4_address))