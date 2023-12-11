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

SampleStream = List[float]
AudioStream = List[int]
audio_rate = 48000

audio_output = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=audio_rate, output=True)
audio_data = []


def signal_handler(sig, frame):
    global sdr
    sdr.cancel_read_async()
    if args.save:
        save_audio_data_to_file()
    print("Ctrl+C detectado. Liberando recursos...")
    
    sdr.close()
    


def stream_audio(data: AudioStream):
    if args.save:
        audio_data.append(data)
    audio_output.write(data)

def save_audio_data_to_file():
    filename = f"audio_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    audio_data_bytes = np.array(audio_data).tobytes()
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)  # Número de canales (1 para mono, 2 para estéreo)
        wf.setsampwidth(2)  # Ancho en bytes de cada muestra
        wf.setframerate(48000)  # Tasa de muestreo en Hz
        wf.writeframes(audio_data_bytes)

def process(samples: SampleStream, sdr: RtlSdr) -> None:
    sample_rate_fm = 240000
    iq_comercial = sg.decimate(samples, int(sdr.get_sample_rate()) // sample_rate_fm)

    angle_comercial = np.unwrap(np.angle(iq_comercial))
    demodulated_comercial = np.diff(angle_comercial)
    audio_signal = sg.decimate(demodulated_comercial, sample_rate_fm // audio_rate, zero_phase=True)
    audio_signal = np.int16(14000 * audio_signal)

    stream_audio(audio_signal.astype("int16").tobytes())

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

