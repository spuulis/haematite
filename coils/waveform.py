import numpy as np


def sine(t, args):
    return args.get('amp', 0.) * np.sin(
        args.get('freq', 0.) * t - args.get('phase', 0.))


def triangle(t, args):
    return 2 * args.get('amp', 0.) / np.pi * np.arcsin(np.sin(
        args.get('freq', 0.) * t - args.get('phase', 0.)))


def sawtooth(t, args):
    return 2 * args.get('amp', 0.) / np.pi * np.arctan(np.tan(
        args.get('freq', 0.) * t - args.get('phase', 0.)))


class Waveform():
    def __init__(self):
        # Function arguments and function
        self._prms = {'x': {}, 'y': {}}
        self.func = lambda t, args: 0
        self.profile = {
            'ts': [],
            'xs': [],
            'ys': [],
        }

    def generate(self, t):
        return {
            't': t,
            'x': self.func(t, self._prms['x']),
            'y': self.func(t, self._prms['y']),
        }

    def set_function(self, func):
        self.func = func
        self.generate_profile()

    def update_parameters(self, new_prms, override=False):
        if override:
            self.clear_parameters()
        if 'x' in new_prms:
            self._prms['x'].update(new_prms['x'])
        if 'y' in new_prms:
            self._prms['y'].update(new_prms['y'])
        self.generate_profile()

    def clear_parameters(self):
        self._prms = {'x': {}, 'y': {}}

    def generate_profile(self, length=3., dt=0.006):
        ts = np.arange(0, length, dt)
        xs = self.func(ts, self._prms['x'])
        ys = self.func(ts, self._prms['y'])
        self.profile = {'ts': ts, 'xs': xs, 'ys': ys}
        return self.profile
