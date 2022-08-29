from contextlib import nullcontext
import time

import nidaqmx
import numpy as np
import threading

import config
from coils.waveform import Waveform


def turn_off():
    with nidaqmx.Task() as task_o:
        # Define voltage output channels for coil control ([X, Y])
        task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OX)
        task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OY)

        # Set current through coils to zero
        task_o.write([0, 0])


class Coils(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.waveform = Waveform()

        self._field = {'x': 0, 'y': 0, 't': time.time_ns()}
        self.initialized = False

        self._stopper = threading.Event()

    def update_params(self, new_params, override=False):
        self.waveform.update_parameters(new_params, override)

    def set_function(self, func):
        self.waveform.func = func

    def stop(self):
        self._stopper.set()

    def initialize(self):
        try:
            with nidaqmx.Task() as task_o:
                task_o = nidaqmx.Task()
                # Define voltage output channels for coil control ([X, Y])
                task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OX)
                task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OY)
        except Exception:
            raise Exception("Coils could not be initialized")
        else:
            self.initialized = True

    @property
    def field(self):
        return self._field.copy()

    def run(self):
        with nidaqmx.Task() if self.initialized else nullcontext() as task_o:
            # Waveform generation loop
            while not self._stopper.is_set():
                time_now = time.time_ns() * 1e-9

                # Set coil voltages (effectively, coil current)
                self._field = self.waveform.generate(time_now)
                sent_t = np.array([
                    self._field['x'],
                    self._field['y'],
                ])
                if task_o is not None:
                    task_o.write(
                        sent_t * np.array([
                            config.COILS_T_TO_V_X,
                            config.COILS_T_TO_V_Y,
                        ])
                    )

                # Limit frame rate
                time.sleep(max(
                    1./config.COILS_FPS - (time.time_ns() * 1e-9 - time_now),
                    0,
                ))

            # Set current through coils to zero upon exit
            if task_o is not None:
                task_o.write([0, 0])
