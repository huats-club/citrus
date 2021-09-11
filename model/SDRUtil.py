import math

import numpy as np  # use numpy for buffers
import pandas as pd
import SoapySDR
from SoapySDR import SOAPY_SDR_CF32, SOAPY_SDR_RX


def process_spectrum(pipe, center_freq, stop_pipe):

    # enumerate devices
    results = SoapySDR.Device.enumerate()
    for result in results:
        print(result)

    # create device instance
    # args can be user defined or from the enumeration result
    args = dict(driver="lime")
    sdr = SoapySDR.Device(args)

    print(sdr.listSampleRates(SOAPY_SDR_RX, 0))
    # apply settings
    bandwidth = 40
    sdr.setSampleRate(SOAPY_SDR_RX, 0, 1e6)
    sdr.setFrequency(SOAPY_SDR_RX, 0, 740.3 * (10**6))
    sdr.setAntenna(SOAPY_SDR_RX, 0, 'Auto')
    sdr.setGainMode(SOAPY_SDR_RX, 0, automatic=True)
    sdr.setBandwidth(SOAPY_SDR_RX, 0, bandwidth*(10 ** 6))

    # setup a stream (complex floats)
    rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
    sdr.activateStream(rxStream)  # start streaming

    # create a re-usable buffer for rx samples
    buff = np.array([0]*1024, np.complex64)

    # receive some samples
    while True:
        # sr = sdr.readStream(rxStream, [buff], len(buff))
        sdr.readStream(rxStream, [buff], len(buff))
        real = []
        imag = []
        power = [-33]
        for i in range(len(buff)):
            real.append(buff[i].real)
            imag.append(buff[i].imag)
            magnitude = math.sqrt(pow(buff[i].real, 2) + pow(buff[i].imag, 2))

            try:
                power_val = -10 * math.log10(magnitude/pow(10, -3))
            except ValueError:
                power_val = min(power)

            power.append((power_val))

        df = pd.DataFrame(list(zip(real, imag, power)),
                          columns=['real', 'imag', 'power'])
        pipe.send(df['power'])

        if stop_pipe.poll(timeout=0):
            print("stop in process")
            stop_pipe.recv()
            break

    # shutdown the stream
    sdr.deactivateStream(rxStream)  # stop streaming
    sdr.closeStream(rxStream)
