import numpy as np
import qutip as qt


def ramsey(time_array_s, detuning_hz=0):
    H = detuning_hz * 2 * np.pi * qt.sigmaz() / 2.0
    initial_state = 1 / np.sqrt(2) * (qt.basis(2, 0) + qt.basis(2, 1))
    result = qt.mesolve(H, initial_state, time_array_s, e_ops=[qt.sigmax()])
    sx_timetrace = result.expect[0]
    return sx_timetrace