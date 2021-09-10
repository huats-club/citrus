import numpy as np  # use numpy for buffers
import pandas as pd
import SoapySDR
from matplotlib import pyplot as plt
from SoapySDR import SOAPY_SDR_CF32, SOAPY_SDR_RX

# enumerate devices
results = SoapySDR.Device.enumerate()
for result in results:
    print(result)

# create device instance
# args can be user defined or from the enumeration result
args = dict(driver="lime")
sdr = SoapySDR.Device(args)

# query device info
print(sdr.listAntennas(SOAPY_SDR_RX, 0))
print(sdr.listGains(SOAPY_SDR_RX, 0))
freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
for freqRange in freqs:
    print(freqRange)  # Prints 0, 3.8e+09 --> corresponds to board's 10MHz up to 3.5GHz

# apply settings
bandwidth = 10
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
for ii in range(10):
    sr = sdr.readStream(rxStream, [buff], len(buff))

    out = pd.DataFrame()
    real = []
    imag = []
    for i in range(len(buff)):
        real.append(buff[i].real)
        imag.append(buff[i].imag)

    df = pd.DataFrame(list(zip(real, imag)), columns=['real', 'imag'])
    #df.to_csv('out' + str(ii) + '_' + str(bandwidth) + "mhz" + '.csv')

    # time[ii] = sr.timeNs / 10 ^ 6

# shutdown the stream
sdr.deactivateStream(rxStream)  # stop streaming
sdr.closeStream(rxStream)
