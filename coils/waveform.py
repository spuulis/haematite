import numpy as np

import config


def sine(
    t: np.ndarray, parameters: dict, amplitude: float = None,
):
    if amplitude is None:
        amplitude = parameters.get('amp', 0.)
    return amplitude * np.sin(
        parameters.get('freq', 0.) * t - parameters.get('phase', 0.))


def triangle(
    t: np.ndarray, parameters: dict, amplitude: float = None,
):
    if amplitude is None:
        amplitude = parameters.get('amp', 0.)
    return 2 * amplitude / np.pi * np.arcsin(np.sin(
        parameters.get('freq', 0.) * t - parameters.get('phase', 0.)))


def sawtooth(
    t: np.ndarray, parameters: dict, amplitude: float = None,
):
    if amplitude is None:
        amplitude = parameters.get('amp', 0.)
    return 2 * amplitude / np.pi * np.arctan(np.tan(
        parameters.get('freq', 0.) * t - parameters.get('phase', 0.)))


class Waveform():
    def __init__(self):
        # Function arguments and function
        self.parameters = {'x': {}, 'y': {}}
        self._function = lambda t, args: 0

        self.profile = {
            'ts': np.array([]),
            'xs': np.array([]),
            'ys': np.array([]),
        }

        self._hold = False
        self.hold_amplitude = {'x': 0., 'y': 0.}

    def generate(self, sample_rate: int):
        if self._hold is True:
            ts = np.array([0., 0.])
            self.profile = {
                'ts': ts,
                'xs': self._function(
                    ts, {'phase': self.parameters['x'].get('phase', 0.)},
                    amplitude=self.hold_amplitude['x']
                ),
                'ys': self._function(
                    ts, {'phase': self.parameters['y'].get('phase', 0.)},
                    amplitude=self.hold_amplitude['y']
                ),
            }
            return self.profile

        period = self.parameters.get('period', 1.)
        number_of_samples = sample_rate * period
        ts = np.linspace(0, period, num=int(number_of_samples), endpoint=False)
        self.parameters_t = {
            coil: {
                'amp': np.linspace(
                    self.parameters[coil].get('amp', [0., 0.])[0],
                    self.parameters[coil].get('amp', [0., 0.])[1],
                    num=int(number_of_samples), endpoint=False,
                ),
                'freq': np.linspace(
                    self.parameters[coil].get('freq', [0., 0.])[0],
                    self.parameters[coil].get('freq', [0., 0.])[1],
                    num=int(number_of_samples), endpoint=False,
                ),
                'phase': self.parameters[coil].get('phase', 0.),
            } for coil in ['x', 'y']
        }
        self.profile = {
            'ts': ts,
            'xs': self._function(
                ts, self.parameters_t['x']),
            'ys': self._function(
                ts, self.parameters_t['y']),
        }
        return self.profile

    def hold(self, hold_amplitude: dict = {'x': 0., 'y': 0.}):
        self.hold_amplitude = hold_amplitude.copy()
        self._hold = True
        self.generate(config.COILS_SAMPLE_RATE)

    def release(self):
        self._hold = False
        self.generate(config.COILS_SAMPLE_RATE)

    def set_function(self, _function):
        self._function = _function
        self.generate(config.COILS_SAMPLE_RATE)
        self.generate_profile()

    def update_parameters(self, new_parameters, override=False):
        if override:
            self.clear_parameters()
        if 'x' in new_parameters:
            self.parameters['x'].update(new_parameters['x'])
        if 'y' in new_parameters:
            self.parameters['y'].update(new_parameters['y'])
        if 'period' in new_parameters:
            self.parameters['period'] = new_parameters['period']
        self.generate_profile()

    def clear_parameters(self):
        self.parameters = {'x': {}, 'y': {}, 'period': 0.}

    def generate_profile(self):
        return self.profile
