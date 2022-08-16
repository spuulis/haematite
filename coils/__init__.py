from contextlib import nullcontext
import csv
import time

import nidaqmx
import numpy as np
import threading

import config

class Waveform(threading.Thread):
    def __init__(self, amp, freq):
        threading.Thread.__init__(self)
        self.daemon = True

        self.amp = amp
        self.freq = freq
        self.phase = np.pi / 2

        # File name for csv output
        self.output = None

        self._stopper = threading.Event()

    def stopit(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def set_output_file(self, file_name):
        self.output = file_name

    # Sine wave generator (freq in rad / s)
    def f(self, t, amp, freq, phase):
        return amp * np.sin(freq * t + phase)

    def run(self):
        with (
            nidaqmx.Task() as task_o,
            open(self.output, 'w') if self.output is not None else nullcontext() as output_file,
        ):
            # Define voltage output channels for coil control ([X, Y])
            task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OX)
            task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OY)

            # Set maximum permittable voltage for output channels
            task_o.ao_channels.all.ao_max = config.COILS_MAX_CURRENT
            task_o.ao_channels.all.ao_min = -config.COILS_MAX_CURRENT

            if output_file is not None:
                out_writer = csv.writer(output_file)
                out_writer.writerow(['Time', 'B_x', 'B_y'])

            # Waveform generation loop
            time_start = time.time_ns() * 1e-9
            while not self.stopped():
                time_now = time.time_ns() * 1e-9
                t = time_now - time_start

                # Set coil voltages (effectively, coil current)
                sent_t = np.array([
                    self.f(t, self.amp, self.freq, 0),
                    self.f(t, self.amp, self.freq, self.phase),
                ])
                task_o.write(
                    sent_t * np.array([config.COILS_T_TO_V_X, config.COILS_T_TO_V_Y])
                )

                # Write coil voltages
                if output_file is not None:
                    out_writer.writerow(np.concatenate([t], sent_t))

                # Limit frame rate
                time.sleep(max(1./config.COILS_FPS - (time.time_ns() * 1e-9 - time_now), 0))

            # Set current through coils to zero upon exit
            task_o.write([0, 0])