import time
import sys
from pynput import mouse, keyboard
import win32api

LOG_FILE = "mouse_telemetry.log"

def log_event(event_str):
    timestamp = time.time()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp},{event_str}\n")

def get_monitors():
    monitors = []
    for m in win32api.EnumDisplayMonitors():
        hMonitor, hdcMonitor, rect = m
        monitors.append(rect)
    return monitors

def get_monitor_index(x, y, monitors):
    for idx, rect in enumerate(monitors, start=1):
        left, top, right, bottom = rect
        if left <= x < right and top <= y < bottom:
            return idx
    return None

monitors = []
global_mouse_listener = None
global_keyboard_listener = None

def on_move(x, y):
    monitor_index = get_monitor_index(x, y, monitors)
    log_event(f"{monitor_index},MOVE,{x},{y}")

def on_click(x, y, button, pressed):
    monitor_index = get_monitor_index(x, y, monitors)
    event = "CLICK_DOWN" if pressed else "CLICK_UP"
    log_event(f"{monitor_index},{event},{x},{y},{button}")

def on_scroll(x, y, dx, dy):
    monitor_index = get_monitor_index(x, y, monitors)
    log_event(f"{monitor_index},SCROLL,{x},{y},{dx},{dy}")

def on_press(key):
    global global_mouse_listener, global_keyboard_listener
    if key == keyboard.Key.esc:
        print("Escape pressed, exiting...")
        if global_mouse_listener is not None:
            global_mouse_listener.stop()
        if global_keyboard_listener is not None:
            global_keyboard_listener.stop()
        sys.exit(0)

def main():
    global monitors, global_mouse_listener, global_keyboard_listener
    monitors = get_monitors()
    print("Detected monitors:")
    for idx, rect in enumerate(monitors, start=1):
        print(f"  Monitor {idx}: {rect}")
    
    print("Starting mouse telemetry capture. Logging events to:", LOG_FILE)
    
    global_mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    global_keyboard_listener = keyboard.Listener(
        on_press=on_press
    )
    
    global_mouse_listener.start()
    global_keyboard_listener.start()
    
    global_mouse_listener.join()
    global_keyboard_listener.join()

if __name__ == '__main__':
    main()
