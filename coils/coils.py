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
        self.field = None

        self.task_o = None
        self.writer = None

        self.t0 = None

    def get_field(self, time_now):
        if self.t0 is None or self.field is None:
            return {'x': 0., 'y': 0.}
        sample_index = int(
            ((time_now - self.t0) * config.COILS_SAMPLE_RATE)
            % len(self.field['xs'])
        )
        return {
            'x': self.field['xs'][sample_index],
            'y': self.field['ys'][sample_index],
        }

    def get_current_parameters(self, time_now):
        if self.t0 is None or self.field is None:
            return {
                'x': {'amp': 0., 'freq': 0.},
                'y': {'amp': 0., 'freq': 0.},
            }
        sample_index = int(
            ((time_now - self.t0) * config.COILS_SAMPLE_RATE)
            % len(self.waveform.parameters_t['x']['amp'])
        )
        return {
            'x': {
                'amp': (
                    self.waveform
                    .parameters_t['x']['amp'][sample_index]
                ),
                'freq': (
                    self.waveform
                    .parameters_t['x']['freq'][sample_index]
                ),
            },
            'y': {
                'amp': (
                    self.waveform
                    .parameters_t['y']['amp'][sample_index]
                ),
                'freq': (
                    self.waveform
                    .parameters_t['y']['freq'][sample_index]
                ),
            },
        }

    def update_params(self, new_params, override=False):
        self.waveform.update_parameters(new_params, override)
        self.waveform.generate(config.COILS_SAMPLE_RATE)
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
            self.task_o.timing.cfg_samp_clk_timing(
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
        self.field = self.waveform.generate(config.COILS_SAMPLE_RATE)
        if self.writer is not None:
            self.task_o.stop()
            self.writer.write_many_sample(np.array([
                self.field['xs'] * config.COILS_T_TO_V_X,
                self.field['ys'] * config.COILS_T_TO_V_Y,
            ]))
            self.task_o.start()
        self.t0 = time.time_ns() * 1.e-9
