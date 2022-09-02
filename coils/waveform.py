import numpy as np


def sine(t, parameters):
    return parameters.get('amp', 0.) * np.sin(
        parameters.get('freq', 0.) * t - parameters.get('phase', 0.))


def triangle(t, parameters):
    return 2 * parameters.get('amp', 0.) / np.pi * np.arcsin(np.sin(
        parameters.get('freq', 0.) * t - parameters.get('phase', 0.)))


def sawtooth(t, parameters):
    return 2 * parameters.get('amp', 0.) / np.pi * np.arctan(np.tan(
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
        self.disabled = False

    def generate(self, t):
        if self.disabled:
            return {'t': t, 'x': 0., 'y': 0.}
        return {
            't': t,
            'x': self._function(t, self.parameters['x']),
            'y': self._function(t, self.parameters['y']),
        }

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
        if self.disabled:
            return {
                'ts': np.array([0, length]),
                'xs': np.array([0., 0.]),
                'ys': np.array([0., 0.])
            }
        ts = np.arange(0, length, dt)
        xs = self._function(ts, self.parameters['x'])
        ys = self._function(ts, self.parameters['y'])
        self.profile = {'ts': ts, 'xs': xs, 'ys': ys}
        return self.profile
