# RTL-SDR lab
In this practice, we are going to listen to the radio using an RTL-SDR device. To do this, we will use the ``listen.py`` script found in this repository. The idea is for the script to allow us to listen to the radio in real-time on the audio output of our choice. To achieve this, we will use the`` pyrtlsdr`` library, which enables us to interact with the RTL-SDR device.

An RTL-SDR device is a tool that allows us to receive radio signals within a frequency range of 24 MHz to 1.7 GHz. This device is very affordable and can be purchased from any online store. In this case, we'll be using the RTL2832U device, available on Amazon for 30€.

![Alt text](images/image.png)

The applications of this device are practically limitless; our only limitation lies in the sampling rate that the device allows. We could achieve a higher sampling rate by using an Ettus USRP device, for example, but these devices are much more expensive.

The maximum sampling rate supported by this device is 3.2 MS/s, allowing us to receive FM radio signals without issues, as the sampling rate for FM radio signals is 1.5 MHz.
## Instalación de dependencias
Create a Conda virtual environment with Python version 3.6

```bash
conda create -n sdr_fm python=3.6
conda activate sdr_fm
```

```
pip install numpy pyaudio pyrtlsdr scipy 
```
## Script Execution
We have the following configuration parameters:
* --freq (``int``): frequency in Hz at which we will listen to the radio
* --save (``bool``): if specified, saves the radio signal to an audio file
  
Execution example:

```
python listen.py --freq 98000000 --save True
```
---
## Script Explanation

Firstly, we import the necessary libraries for the project's development.

```python
import sys
from typing import List
from rtlsdr import RtlSdr
import argparse
import datetime
import numpy as np
import pyaudio
import scipy.signal as sg
import signal
import wave
```

We initialize the variables that we will use and the audio output for our device. Here, we specify the audio channel where we want to redirect the flow and the audio buffer (`audio_data`).

```python
SampleStream = List[float]
AudioStream = List[int]
audio_rate = 48000
# Inicializar dispositivo de salida de audio
audio_output = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=audio_rate, output=True)
audio_data = []
```
This function will save the audio data to a file. It takes as parameters the filename and the audio data until the script execution stops.

```python
def save_audio_data_to_file():
    filename = f"audio_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    audio_data_bytes = np.array(audio_data).tobytes()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Número de canales (1 para mono, 2 para estéreo)
        wf.setsampwidth(2)  # Ancho en bytes de cada muestra
        wf.setframerate(48000)  # Tasa de muestreo en Hz
        wf.writeframes(audio_data_bytes)
```
**Function to handle keyboard interruption (Ctrl+C)**: With this function, we can interrupt the script execution at any time, stopping the audio playback and closing the RTL-SDR device. If we specified in the configuration that we want to save the audio, the file will be saved and closed.


```python
def signal_handler(sig, frame):
    global sdr
    sdr.cancel_read_async()
    if args.save:
        save_audio_data_to_file()
    print("Ctrl+C detectado. Liberando recursos...")
    sdr.close()
```
With this function, we control the audio playback, directing it to the audio output of our device. If we want to save the audio upon execution completion, we'll add the audio data to a list.

```python
def stream_audio(data: AudioStream):
    if args.save:
        audio_data.append(data)
    audio_output.write(data)
```
The *process* function transforms radio frequency samples into an audio signal that can be played.

```python
def process(samples: SampleStream, sdr: RtlSdr) -> None:
    sample_rate_fm = 240000
    iq_comercial = sg.decimate(samples, int(sdr.get_sample_rate()) // sample_rate_fm)

    angle_comercial = np.unwrap(np.angle(iq_comercial))
    demodulated_comercial = np.diff(angle_comercial)
    audio_signal = sg.decimate(demodulated_comercial, sample_rate_fm // audio_rate, zero_phase=True)
    audio_signal = np.int16(14000 * audio_signal)

    stream_audio(audio_signal.astype("int16").tobytes())
```
Finally, we initialize the RTL-SDR device and start listening to the frequency specified in the configuration.

```python
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--freq', type=int, default=93900000,
                    help='frequency to listen to, in Hertz')
parser.add_argument('--save', type=bool, default=False,
                    help='Store audio to file')

args = parser.parse_args()
sdr =  RtlSdr()
signal.signal(signal.SIGINT, signal_handler) 
try:
    sdr.rs = 240000
    sdr.fc = args.freq
    sdr.gain = 'auto'
    sdr.err_ppm = 40
    sdr.read_samples_async(process, int(sdr.get_sample_rate()) // 16)
finally:
    sys.exit(0)
```