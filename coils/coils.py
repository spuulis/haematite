import time

import nidaqmx
from nidaqmx.constants import AcquisitionType, RegenerationMode
from nidaqmx.stream_writers import AnalogMultiChannelWriter
import numpy as np

import config
from coils.waveform import Waveform


def turn_off():
    with nidaqmx.Task() as task_o:
        # Define voltage output channels for coil control ([X, Y])
        task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OX)
        task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OY)

        # Set current through coils to zero
        task_o.write([0, 0])


class Coils():
    def __init__(self):
        self.waveform = Waveform()
        self._field = {'x': 0, 'y': 0, 't': time.time_ns()}
        self.task_o = None
        self.writer = None

    def update_params(self, new_params, override=False):
        self.waveform.update_parameters(new_params, override)
        self.write_to_coils()

    def set_function(self, func):
        self.waveform.set_function(func)
        self.write_to_coils()

    def initialize(self):
        try:
            self.task_o = nidaqmx.Task()
            # Define voltage output channels for coil control ([X, Y])
            self.task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OX)
            self.task_o.ao_channels.add_ao_voltage_chan(config.COILS_NAME_OY)
            self.task_o.ao_channels.all.ao_max = config.COILS_MAX_CURRENT
            self.task_o.ao_channels.all.ao_min = -config.COILS_MAX_CURRENT
            # Set up timing for the DAQmx output task
            self.task.timing.cfg_samp_clk_timing(
                config.COILS_SAMPLE_RATE,
                sample_mode=AcquisitionType.CONTINUOUS,
            )
            # Configure stream so that the values outputted are looped
            self.task_o.out_stream.regen_mode = (
                RegenerationMode.ALLOW_REGENERATION)
            # Create the writer
            self.writer = AnalogMultiChannelWriter(
                self.task_o.out_stream, auto_start=False)
        except Exception as e:
            raise Exception(f"Coils could not be initialized:\n\n{e}")

    def stop(self):
        if self.task_o is not None:
            # Turn off coils
            self.task_o.stop()
            self.task_o.write(np.array([[0.], [0.]]))
            self.task_o.start()
            # Release task_o
            self.task_o.stop()
            self.task_o.close()

    def write_to_coils(self):
        if self.writer is not None:
            field = self.waveform.generate(config.COILS_SAMPLE_RATE)
            self.task_o.stop()
            self.writer.write_many_sample(np.array([
                field['x'] * config.COILS_T_TO_V_X,
                field['y'] * config.COILS_T_TO_V_Y,
            ]))
            self.task_o.start()
