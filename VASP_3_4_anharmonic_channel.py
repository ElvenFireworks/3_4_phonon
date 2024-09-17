import numpy as np
from tqdm import tqdm
import random

def read_frequency_mesh(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            q_position = list(map(float, parts[:3]))
            frequency = float(parts[3])
            data.append((q_position, frequency))
    return data

def energy_conservation_three(omega0, omega1, omega2, n):
    return np.isclose(omega0, omega1 + omega2, atol=10**-n) or np.isclose(omega0 + omega1, omega2, atol=10**-n)

def energy_conservation_four(omega0, omega1, omega2, omega3, n):
    return np.isclose(omega0, omega1 + omega2 + omega3, atol=10**-n) or np.isclose(omega0 + omega1, omega2 + omega3, atol=10**-n)

def momentum_conservation(q0, q1, q2, q3=None):
    if q3 is None:
        return np.allclose(np.add(q0, q1), q2, atol=1e-7)
    else:
        return np.allclose(np.add(q0, np.add(q1, q2)), q3, atol=1e-7)

def random_select_omegas(data, num_omegas):
    return random.sample(data, num_omegas)

def find_three_phonon_channels(data, omega0, n, three_phonon_file):
    q0 = [0.0, 0.0, 0.0]
    with open(three_phonon_file, 'w') as file:
        for i in tqdm(range(len(data)), desc="Processing three-phonon channels"):
            q1, omega1 = data[i]
            for j in range(len(data)):
                if i != j:
                    q2, omega2 = data[j]
                    if energy_conservation_three(omega0, omega1, omega2, n):
                        momentum_conservation_status = momentum_conservation(q0, q1, q2)
                        file.write(f"{omega0:.10f} {omega1:.10f} {omega2:.10f} {q1[0]:.7f} {q1[1]:.7f} {q1[2]:.7f} {q2[0]:.7f} {q2[1]:.7f} {q2[2]:.7f} {momentum_conservation_status}\n")

def find_four_phonon_channels(data, omega0, n, four_phonon_file, selected_omegas):
    q0 = [0.0, 0.0, 0.0]
    with open(four_phonon_file, 'w') as file:
        for selected in selected_omegas:
            q1, omega1 = selected
            for j in tqdm(range(len(data)), desc="Processing four-phonon channels"):
                q2, omega2 = data[j]
                for k in range(len(data)):
                    if k != j:
                        q3, omega3 = data[k]
                        if energy_conservation_four(omega0, omega1, omega2, omega3, n):
                            momentum_conservation_status = momentum_conservation(q0, q1, q2, q3)
                            file.write(f"{omega0:.10f} {omega1:.10f} {omega2:.10f} {omega3:.10f} {q1[0]:.7f} {q1[1]:.7f} {q1[2]:.7f} {q2[0]:.7f} {q2[1]:.7f} {q2[2]:.7f} {q3[0]:.7f} {q3[1]:.7f} {q3[2]:.7f} {momentum_conservation_status}\n")


data = read_frequency_mesh('Frequency-mesh.dat')


omega0 = 2.500265
n = 3


num_random_omegas = 6


selected_omegas = random_select_omegas(data, num_random_omegas)


three_phonon_file = 'P4-Three_phonon.dat'
four_phonon_file = 'P4-Four_phonon.dat'


find_three_phonon_channels(data, omega0, n, three_phonon_file)
find_four_phonon_channels(data, omega0, n, four_phonon_file, selected_omegas)

print("saved to 'Three_phonon.dat' 和 'Four_phonon.dat'")
