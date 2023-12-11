# Práctica RTL-SDR
En esta práctica vamos a escuchar la radio con un dispositivo RTL-SDR. Para ello vamos a utilizar el script radio.py que se encuentra en este repositorio. La idea es que el script nos permita escuchar la radio en tiempo real en la salida de audio que nosotros prefiramos. Para ello vamos a utilizar la librería pyrtlsdr que nos permite interactuar con el dispositivo RTL-SDR.

Un dispositivo RTL-SDR es un dispositivo que nos permite recibir señales de radio en un rango de frecuencias de 24 MHz a 1.7 GHz. Este dispositivo es muy barato y se puede comprar en cualquier tienda online. En este caso vamos a utilizar el dispositivo RTL2832U que se puede comprar en Amazon por 30€. 

![Alt text](images/image.png)

Las aplicaciones de este dispositivo son prácticamente infinitas, solo estamos limitados en la tasa de muestreo que nos permite el dispositivo. Podríamos conseguir una tasa de muestreo superior si utilizamos un dispositivo Ettus USRP por ejemplo, pero estos dispositivos son mucho más caros.

La máxima tasa de muestreo que admite este dispositivo es de 3.2 MS/s, lo que nos permite recibir señales de radio FM sin problemas, ya que la tasa de muestreo de la señal de radio FM es de 1.5 MHz.
## Instalación de dependencias
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
python listen.py --freq=98000000 
```
