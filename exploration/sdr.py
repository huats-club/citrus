import numpy  # use numpy for buffers
import SoapySDR
from SoapySDR import SOAPY_SDR_RX  # SOAPY_SDR_ constants

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
