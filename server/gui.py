import os.path
import tkinter as tk
import logging
import types
from types import SimpleNamespace
import sys
sys.path.append("../src/wakeword_service")
from listener import WakewordListener
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)s %(message)s')

def load_config(filepath="./wakeword_service_gui_config.xml"):
    config = SimpleNamespace()
    tree = ET.parse(filepath)
    root_elm = tree.getroot()
    for root_child_elm in root_elm:
        if root_child_elm.tag == 'command_on_wakeword':
            config.command_on_wakeword = root_child_elm.text
        elif root_child_elm.tag == 'chunk_size':
            config.chunk_size = int(root_child_elm.text)
        elif root_child_elm.tag == 'model_wakeword':
            config.model_wakeword = root_child_elm.text
        elif root_child_elm.tag == 'inference_framework':
            config.inference_framework = root_child_elm.text
        elif root_child_elm.tag == 'channels':
            config.channels = int(root_child_elm.text)
        elif root_child_elm.tag == 'rate':
            config.rate = int(root_child_elm.text)
        elif root_child_elm.tag == 'sleep_after_detection_in_seconds':
            config.sleep_after_detection_in_seconds = float(root_child_elm.text)
        else:
            raise NotImplementedError(f"gui.load_config(): Not implemented element <{root_child_elm.tag}>")
    return config

config_filepath = "./wakeword_service_gui_config.xml"
if not os.path.exists(config_filepath):
    raise FileNotFoundError(f"gui.py: Could not find filepath '{config_filepath}'. Did you forget to copy './wakeword_service_gui_config.xml.example'?")

config = load_config(config_filepath)

global_params = SimpleNamespace()
global_params.is_running = False
global_params.start_stop_btn = None
global_params.indicator_light = None
global_params.wakerword_listener = WakewordListener(
    command_on_wakeword=config.command_on_wakeword,
    chunk_size=config.chunk_size,
    model_path=config.model_wakeword,
    inference_framework=config.inference_framework,
    channels=config.channels,
    rate=config.rate,
    sleep_after_detection_in_seconds=config.sleep_after_detection_in_seconds
)
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