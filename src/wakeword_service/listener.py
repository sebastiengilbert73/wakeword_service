# Cf. https://github.com/dscripka/openWakeWord/blob/main/examples/detect_from_microphone.py
import pyaudio
import numpy as np
from openwakeword.model import Model
import time
import threading
import subprocess
import logging

class WakewordListener(threading.Thread):
    def __init__(self,
                 command_on_wakeword,
                 chunk_size=1280,
                 model_path="hey jarvis",
                 inference_framework='onnx',
                 channels=1,
                 rate=16000,
                 sleep_after_detection_in_seconds=4.0
                 ):
        super(WakewordListener, self).__init__()
        self._command_on_wakeword = command_on_wakeword
        self._must_listen = False
        self._chunk_size = chunk_size
        self._model_path = model_path
        self._inference_framework = inference_framework

        # Get microphone stream
        self._format = pyaudio.paInt16
        self._channels = channels
        self._rate = rate
        self._sleep_after_detection_in_seconds = sleep_after_detection_in_seconds

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
        #print(f"WakewordListener.__init__(): self._n_models = {self._n_models}")

    def start_stop(self):
        self._must_listen = not self._must_listen
        logging.info(f"WakewordListener.start_stop(): self._must_listen = {self._must_listen}")

    def run(self):
        while True:
            if self._must_listen:
                wakeword_is_detected = False
                # Get audio
                audio = np.frombuffer(self._mic_stream.read(self._chunk_size), dtype=np.int16)

                # Feed to openWakeWord model
                prediction = self._oww_model.predict(audio)
                #print(f"WakewordListener.run(): prediction = {prediction}")
                for wakeword, score in prediction.items():
                    if score > 0.5:
                        logging.info(f"WakewordListener.run(): Wakeword detected! score = {score}")
                        wakeword_is_detected = True
                        self._oww_model.reset()

                if wakeword_is_detected:
                    returned_value = subprocess.call(self._command_on_wakeword, shell=True)
                    logging.info(f"WakewordListener.run(): returned_value = \n{returned_value}")
                    time.sleep(self._sleep_after_detection_in_seconds)
            else:
                time.sleep(0.01)