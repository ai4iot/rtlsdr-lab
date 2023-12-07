# Instalación en Linux

Crea un entorno virtual de conda con versión de Python 3.6

```bash
conda create -n sdr_fm python=3.6
conda activate sdr_fm
```

```
pip install numpy pyaudio pyrtlsdr scipy 
```

Tenemos los siguientes parámetros de configuración:

* --freq: frecuencia en Hz a la que vamos a escuchar la radio

* --gain: Ganancia que queremos aplicar

* --verbose: Si queremos que no se escuche la radio por la salida de audio y se guarde en un archivo

* --ppm: Corrección de errores, en principio si no especificamos este parámetro debería funcionar bien

Ejemplo de ejecución:

```
python radio.py --freq=98000000 --gain=20
```
