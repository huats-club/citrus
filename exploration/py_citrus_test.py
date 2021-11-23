import datetime

import numpy as np  # use numpy for buffers
import pycitrus
import SoapySDR
from SoapySDR import SOAPY_SDR_CF32, SOAPY_SDR_RX

# enumerate devices
args = dict(driver="lime")
sdr = SoapySDR.Device(args)

# apply settings
sdr.setAntenna(SOAPY_SDR_RX, 0, 'LNAW')
sdr.setGainMode(SOAPY_SDR_RX, 0, False)
sdr.setGain(SOAPY_SDR_RX, 0, "LNA", 0)
sdr.setGain(SOAPY_SDR_RX, 0, "PGA", -12)
sdr.setGain(SOAPY_SDR_RX, 0, "TIA", 0)
sdr.setFrequency(SOAPY_SDR_RX, 0, 740.3 * (10**6))
sdr.setSampleRate(SOAPY_SDR_RX, 0, 4 * (10**6))
sdr.setBandwidth(SOAPY_SDR_RX, 0, 0*(10 ** 6))

# setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream)  # start streaming

# create a re-usable buffer for rx samples
buff = np.array([0]*4080, np.complex64)

# receive some samples
sr = sdr.readStream(rxStream, [buff], len(buff))

# shutdown the stream
sdr.deactivateStream(rxStream)  # stop streaming
sdr.closeStream(rxStream)

p = pycitrus.CitrusProcessor()
out = p.process(buff.tolist())
out2 = out[10:len(out)-11]

name = "{:%Y-%m-%d-%H-%M-%S}".format(datetime.datetime.now())
with open(f'pycitrus_data/output_{name}_1.txt', "w") as f:
    for item in out:
        f.write(str(item) + '\n')

with open(f'pycitrus_data/output_{name}_2.txt', "w") as f:
    for item in out2:
        f.write(str(item) + '\n')
