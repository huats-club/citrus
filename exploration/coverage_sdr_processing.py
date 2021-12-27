import copy

import numpy as np
import pycitrus


def read_sdr():
    p = pycitrus.CitrusProcessor(743.3e6, 10e6)
    p.init()
    out = p.run()
    p.close()
    return out


def write_to_out(name):
    p = pycitrus.CitrusProcessor(743.3e6, 10e6)
    p.init()
    data = p.run()
    p.close()
    with open(f"exploration/coverage_sdr_data/output_{name}.txt", "w") as f:
        for item in data:
            f.write(str(item) + '\n')


def save_npy(name):
    p = pycitrus.CitrusProcessor(743.3e6, 10e6)
    p.init()
    data = p.run()
    p.close()
    out = np.asarray(data)
    np.save(f"exploration/coverage_sdr_data/output_{name}", out)


if __name__ == "__main__":
    # load data
    data = np.load("C:/Users/65844/Desktop/citrus/exploration/coverage_sdr_data/output_test.npy")

    # get stats to locate the spikes
    avg = np.average(data)
    count = np.size(data)
    print(avg, count)

    threshold = -50

    # start, end, freqbin(increment) per idx
    freq_inc = 10e6 / count
    print(f"freq increment: {freq_inc}")

    # get each number and compare wrt threshold
    # identify a cluster spike when the indexes are "close" to each other
    for i in range(count):
        if data[i] > threshold:
            print(i, data[i])
