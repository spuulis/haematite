import numpy as np


def sine(
    t: float, parameters: dict, amplitude: float = None,
):
    if amplitude is None:
        amplitude = parameters.get('amp', 0.)
    return amplitude * np.sin(
        parameters.get('freq', 0.) * t - parameters.get('phase', 0.))


def triangle(
    t: float, parameters: dict, amplitude: float = None,
):
    if amplitude is None:
        amplitude = parameters.get('amp', 0.)
    return 2 * amplitude / np.pi * np.arcsin(np.sin(
        parameters.get('freq', 0.) * t - parameters.get('phase', 0.)))


def sawtooth(
    t: float, parameters: dict, amplitude: float = None,
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
            'ts': [],
            'xs': [],
            'ys': [],
        }

        self._hold = False
        self.hold_amplitude = {'x': 0., 'y': 0.}

    def generate(self, sample_rate: int):
        if self._hold is True:
            ts = [0., 1.]
            return {
                'ts': ts,
                'xs': self._function(
                    ts, self.parameters['x'],
                    amplitude=self.hold_amplitude['x']
                ),
                'ys': self._function(
                    ts, self.parameters['y'],
                    amplitude=self.hold_amplitude['y']
                ),
            }
        period = 2 * np.pi / self.parameters['x']
        ts = np.linspace(
            0, period, num=int(sample_rate * period), endpoint=False)
        return {
            'ts': ts,
            'xs': self._function(
                ts, self.parameters['x']),
            'ys': self._function(
                ts, self.parameters['y']),
        }

    def hold(self, hold_amplitude: dict = {'x': 0., 'y': 0.}):
        self.hold_amplitude = hold_amplitude.copy()
        self._hold = True

    def release(self):
        self._hold = False

    def set_function(self, _function):
        self._function = _function
        self.generate_profile()

    def update_parameters(self, new_parameters, override=False):
        if override:
            self.clear_parameters()
        if 'x' in new_parameters:
            self.parameters['x'].update(new_parameters['x'])
        if 'y' in new_parameters:
            self.parameters['y'].update(new_parameters['y'])
        self.generate_profile()

    def clear_parameters(self):
        self.parameters = {'x': {}, 'y': {}}

    def generate_profile(self, length=3., dt=0.006):
        if self._hold:
            return {
                'ts': np.array([0., length]),
                'xs': np.array([1., 1.]) * self._function(
                    0., self.parameters['x'],
                    amplitude=self.hold_amplitude['x'],
                ),
                'ys': np.array([1., 1.]) * self._function(
                    0., self.parameters['y'],
                    amplitude=self.hold_amplitude['y'],
                ),
            }
        ts = np.arange(0, length, dt)
        xs = self._function(ts, self.parameters['x'])
        ys = self._function(ts, self.parameters['y'])
        self.profile = {'ts': ts, 'xs': xs, 'ys': ys}
        return self.profile
