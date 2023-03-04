# Wireless Rubber Ducky for Raspberry Pico W

## Info

This is a Rubber Ducky for Pico W that can be controlled wirelessly, over wifi (is there a name for this kind of rubber ducky?). Note that you need a **Raspberry Pico W**, not a Pico, as you need the wireless functionality in order to host a webserver.

![](https://i.imgur.com/ecBBiUv.png)

## Installation & Usage
First, clone the repository onto your computer. Then:
1. Hold down the BOOTSEL button on the Raspberry Pico W as you plug it in.
2. Drag the `adafruit-circuitpython-raspberry_pi_pico_w-en_US-8.0.0-beta.4.uf2` file into the drive. It will disconnect and boot again with `CircuitPython`. Note that **all previous data on the pico will be erased**.
3. Drag `code.py`, `creds.py` and `index.html` from this repository onto the Pico W. Note: the Pico W will automatically run `code.py` when it is powered on.
4. In `creds.py`, replace `"SSID HERE"` and `"WIFI PASSWORD HERE"` with your wifi SSID and password.
5. ~~Install the required libraries using `circup`. Install circup through `pythom3 -m pip install circup`, then do `circup install --auto` to automatically install the required libraries based on imports in `code.py`.~~ New release of `adafruit_httpserver` was not in circup, please drag the `lib` folder onto the drive (it contains all the required libraries `adafruit_hid` and `adafruit_httpserver`).
6. Now the wireless rubber ducky is done. Upon being powered, it should host a webserver at port 80. You can search for its IP address through `nmap your_local_ip/24 -p 80` and looking for a name such as `PicoW.lan` with port 80 open.
7. Visit the IP address at port 80, to be prompted with a webpage. There, you can enter keystrokes to be sent:
    - To type text, simply type the text on the same line. Use special keys such as `> ENTER DOWN` for line breaks (see below).
    - To press special keys, the format is `> KEY UP/DOWN` such as `> TAB DOWN`. There is a special `> SLEEP <milliseconds>` command for delays. You can see all the available special keys [here](https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html).
    - To move the mouse, use `> MOUSE x y` to move the mouse `x` right and `y` down, for example, `MOUSE 100 -50` moves the mouse 100 right and 50 up.
    - To click, use `> CLICK button` to perform a mouse click, for example, `> CLICK 1` to left click. `1` is left click, `2` is right click, and `4` is middle click.
    - Seperate these per line. There is a default reverese shell payload you can use as reference.
    - Click `submit` button to send the payload.
8. To terminate the webserver, press `Terminate` button on the webpage. The server will crash itself, and will only be up again when the Pico W is restarted (such as plugged in again).

# Additional

You may want to hide the USB by preventing the Pico W from showing up as a USB drive when plugged into a victim's computer. If so, read carefully:
- `boot.py`, which is ran before `code.py` when powered, contains code that will do so. **HOWEVER**, this will soft-lock the Pico W. **Also**, uncomment the line of code which does so. It's there to prevent accidentally soft-lock.
- If you ever soft-lock it, you can either hold down the BOOTSEL button, and nuke the flash by dragging `flash_nuke.uf2` (from [here](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)) into the Pico W drive, which will make it show up as a USB when configured again.
- The other option is to exploit the RCE in the code, since the server will still run, so you may be able to edit contents of `boot.py` from that. See #TODO and have fun exploiting!

## TODO

- It's possible to gain RCE because of how special keys are parsed. This should be fixed (or can serve as a backdoor if needed?? not a bug it's a feature)
```py
keyboard.press(eval(f"Keycode.{key[0]}"))
```

## Contribution

Open any issues in the issues tab in github (not working, crashing, etc).
Feel free to open pull requests that improves code / adds features / user experience.

# DISCLAIMER

This is for educational purposes only, I am not responsible for any actions committed using this code.