import tkinter as tk
import logging
from types import SimpleNamespace
import sys
sys.path.append("../src/wakeword_service")
from listener import WakewordListener

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)s %(message)s')

global_params = SimpleNamespace()
global_params.is_running = False
global_params.start_stop_btn = None
global_params.indicator_light = None
global_params.wakerword_listener = WakewordListener()
global_params.wakerword_listener.daemon = True
global_params.wakerword_listener.start()

def start_stop():
    global global_params
    logging.info(f"start_stop() Initially: global_params.is_running = {global_params.is_running}")
    global_params.is_running = not global_params.is_running
    if global_params.is_running:
        global_params.start_stop_btn.config(text="Stop")
        global_params.start_stop_btn.config(bg="red")
    else:
        global_params.start_stop_btn.config(text="Start")
        global_params.start_stop_btn.config(bg="green")
    global_params.wakerword_listener.start_stop()
    logging.info(f"start_stop() Now: global_params.is_running = {global_params.is_running}")


root = tk.Tk()
root.title("Wakeword service")
root.geometry("200x100")
root.maxsize(200, 100)  # width x height

start_stop_lbl = tk.Label(root, text="Run wakeword detection")
start_stop_lbl.grid(row=0, column=0, columnspan=1, padx=6, pady=6)

start_stop_btn = tk.Button(root, text="Start", command=start_stop, bg="green", fg="white")
start_stop_btn.grid(row=0, column=1, columnspan=1, padx=6, pady=6)
global_params.start_stop_btn = start_stop_btn



root.mainloop()