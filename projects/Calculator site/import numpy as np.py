import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from IPython.display import Audio

# Sampling frequency
fs = 44100
Ts = 1 / fs

# Reference frequency for A4
A4 = 440

# Example notes and durations
notes = ['C3', 'E3', 'G3', 'A3']  # Define your note sequence here
durations = [0.5, 0.5, 0.5, 0.5]  # Define your note durations here

def note_to_number(note):
    note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    octave = int(note[-1])
    key = note[:-1]
    return note_map[key] + (octave - 4) * 12

n = np.array([note_to_number(note) for note in notes])

frequencies = A4 * 2 ** (n / 12)
tempo = 120  # Beats per minute
quarter_note_duration = 60 / tempo  # Duration of a quarter note in seconds
note_durations = np.array(durations) * quarter_note_duration  # Convert to seconds
t = np.arange(0, sum(note_durations), Ts)  # Time vector
waveform = np.array([])  # Initialize waveform

for i in range(len(frequencies)):
    duration = note_durations[i]
    freq = frequencies[i]
    t_note = np.arange(0, duration, Ts)
    waveform = np.concatenate((waveform, np.sin(2 * np.pi * freq * t_note)))

# Play the synthesized waveform
audio = Audio(waveform, rate=fs)
display(audio)

# Plot the waveform
plt.figure(figsize=(10, 4))
plt.plot(np.arange(0, len(waveform)) * Ts, waveform)
plt.title('Waveform of the Synthesized Music')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Plot the spectrogram
plt.figure(figsize=(10, 4))
f, t, Sxx = spectrogram(waveform, fs, nperseg=512)
plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
plt.title('Spectrogram of Synthesized Music')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.ylim([0, 2000])
plt.colorbar(label='Intensity (dB)')
plt.show()
