# Cf. https://github.com/dscripka/openWakeWord/blob/main/examples/detect_from_microphone.py
import pyaudio
import numpy as np
from openwakeword.model import Model
import time
import threading

class WakewordListener(threading.Thread):
    def __init__(self):
        super(WakewordListener, self).__init__()
        self._must_listen = False
        self._chunk_size = 1280
        self._model_path = "hey jarvis"
        self._inference_framework = 'onnx'

        # Get microphone stream
        self._format = pyaudio.paInt16
        self._channels = 1
        self._rate = 16000

        audio = pyaudio.PyAudio()
        self._mic_stream = audio.open(format=self._format, channels=self._channels,
                                      rate=self._rate, input=True,
                                      frames_per_buffer=self._chunk_size)

        # Load pre-trained openwakeword models
        if self._model_path != "":
            self._oww_model = Model(wakeword_models=[self._model_path],
                                    inference_framework=self._inference_framework)
        else:
            self.oww_model = Model(inference_framework=self._inference_framework)

        self._n_models = len(self._oww_model.models.keys())
        print(f"WakewordListener.__init__(): self._n_models = {self._n_models}")

    def start_stop(self):
        self._must_listen = not self._must_listen

    def run(self):
        while True:
            if self._must_listen:
                # Get audio
                audio = np.frombuffer(self._mic_stream.read(self._chunk_size), dtype=np.int16)

                # Feed to openWakeWord model
                prediction = self._oww_model.predict(audio)

                for mdl in self._oww_model.prediction_buffer.keys():
                    # Add scores in formatted table
                    scores = list(self._oww_model.prediction_buffer[mdl])
                    if scores[-1] >= 0.5:
                        print(f"WakewordListener.run(): scores[-1] = {scores[-1]}")
                    #print(f"WakewordListener.run(): scores = {scores}")
                    #curr_score = format(scores[-1], '.20f').replace("-", "")

                    #output_string_header += f"""{mdl}{" " * (n_spaces - len(mdl))}   | {curr_score[0:5]} | {"--" + " " * 20 if scores[-1] <= 0.5 else "Wakeword Detected!"}
            else:
                #print("WakewordListener.run(): Not listening...")
                time.sleep(0.01)