import math

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
    print(f"avg value: {avg:.5f}, count: {count}")

    # start, end, freqbin(increment) per idx
    freq_inc = 10e6 / count
    print(f"freq increment: {freq_inc:.5f}")

    # # get each number and compare wrt threshold
    # # identify a cluster spike when the indexes are "close" to each other
    # for i in range(count):
    #     if data[i] > threshold:
    #         print(i, data[i])

    center_freq = 743.3e6
    bandwidth = 10e6
    start_freq = center_freq - 0.5*bandwidth
    end_freq = center_freq + 0.5*bandwidth
    print(f"start freq: {start_freq}, center_freq: {center_freq}, end_freq: {end_freq}")

    # compute idx nearest to this center freq
    center_idx = math.ceil((center_freq - start_freq) / freq_inc)
    left_bound_idx = center_idx - 3
    right_bound_idx = center_idx + 3
    print(f"searching: {left_bound_idx} -> {right_bound_idx}")

    max = -1000
    for i in range(left_bound_idx, right_bound_idx+1):
        if data[i] > max:
            max = data[i]
    print(f"found max: {max:.5f}")
