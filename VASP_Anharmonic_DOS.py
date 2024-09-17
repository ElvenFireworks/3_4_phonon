import numpy as np
import pandas as pd

def read_data(file_path):
    data = pd.read_csv(file_path, delim_whitespace=True, header=None)
    data.columns = ['Frequency1', 'Frequency2', 'Direction', 'Process']
    return data

def compute_dos(data, broadening, freq_range):
    dos = np.zeros_like(freq_range)
    for freq in data['Frequency1']:
        dos += np.exp(-(freq_range - freq)**2 / (2 * broadening**2))
    return dos

def compute_combined_dos(data, broadening, freq_range, direction, process):
    filtered_data = data[(data['Direction'] == direction) & (data['Process'] == process)]
    return compute_dos(filtered_data, broadening, freq_range)

def main():
    broadening = 0.15  # Example broadening value, adjust as needed
    freq_range = np.linspace(0, 20, 1000)  # Example frequency range, adjust as needed
    
    three_phonon_data = read_data('Four_phonon_channel.dat')
    
    total_dos = compute_dos(three_phonon_data, broadening, freq_range)
    merging_normal_dos = compute_combined_dos(three_phonon_data, broadening, freq_range, 'Merging', 'Normal')
    merging_umklapp_dos = compute_combined_dos(three_phonon_data, broadening, freq_range, 'Merging', 'Umklapp')
    splitting_normal_dos = compute_combined_dos(three_phonon_data, broadening, freq_range, 'Splitting', 'Normal')
    splitting_umklapp_dos = compute_combined_dos(three_phonon_data, broadening, freq_range, 'Splitting', 'Umklapp')
    
    dos_data = pd.DataFrame({
        'Frequency': freq_range,
        'Merging-Normal': merging_normal_dos,
        'Merging-Umklapp': merging_umklapp_dos,
        'Splitting-Normal': splitting_normal_dos,
        'Splitting-Umklapp': splitting_umklapp_dos,
        'Total_DOS': total_dos
    })
    
    dos_data.to_csv('Anharmonic_DOS.dat', index=False, sep=' ')

if __name__ == '__main__':
    main()
