import numpy as np


# def sine(t, amp, freq, phase):
#     return amp * np.sin(freq * t + phase)
def sine(t, args):
    return args['amp'] * np.sin(args['freq'] * t + args['phase'])


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

    def update_parameters(self, new_prms, override=False):
        if override:
            self.clear_parameters()
        if 'x' in new_prms:
            self._prms['x'].update(new_prms['x'])
        if 'y' in new_prms:
            self._prms['y'].update(new_prms['y'])

    def clear_parameters(self):
        self._prms = {'x': {}, 'y': {}}

    def generate_profile(self, length=5., dt=0.05):
        ts = np.arange(0, length, dt)
        xs = self.func(ts, self._prms['x'])
        ys = self.func(ts, self._prms['y'])
        self.profile = {'ts': ts, 'xs': xs, 'ys': ys}
