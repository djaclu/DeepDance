import timeit
import numpy as np
from matplotlib import pyplot as plt

def tempo(wave, sensitivity):
    # consider using weighted average? w/np.average
    # consider capturing "sub beat"
    # avg_energy = np.mean((wave * wave).sum(1))

    # wave properties
    length = len(wave)
    hz = 44100
    seconds = length/hz

    # parameters
    samplerate = 4
    samples = int(samplerate * seconds)

    intervals, window = np.linspace(0, length, num=samples, endpoint=False, retstep=True)
    intervals = np.int32(intervals)
    window = np.int32(window)

    uniwave = np.int32(wave)
    max_energy = np.max((uniwave*uniwave).sum(1))
    threshold = max_energy * sensitivity


    beatcount = 0
    for i in intervals:
        wave_window = uniwave[i: i + window]
        energy = np.max((wave_window * wave_window).sum(1))
        if energy > threshold:
            beatcount += 1
    bpm = (beatcount/seconds)*60

    return bpm, threshold, intervals

def vizWAV(wave, sr, threshold = 0, interval = []):

    #todo plot average energy for each sample

    samples = len(wave)
    seconds = int(samples/sr)
    sec_marks = np.linspace(sr, samples, seconds)
    x = np.linspace(0, samples, samples)

    #unified stero L+R wave
    uniwave = np.int32(wave)
    uniwave = uniwave*uniwave
    uniwave = np.add(uniwave[:, 0], uniwave[:, 1])
    #linear_fit = np.polyfit(samples, uniwave, 1)
    #print(linear_fit)

    fig1, ax1 = plt.subplots()
    plt.plot(x, uniwave, c="red")
    plt.legend(["both channels"])
    plt.axhline(y=threshold, c="purple")

    for i in interval:
        plt.axvline(x=i, c="grey", ls="--")
    for s in sec_marks:
        plt.axvline(x=s, c="black", ls="--")
    plt.xlabel("#Samples")
    plt.ylabel("Energy")

    fig2, ax2 = plt.subplots()
    plt.plot(x, wave[:, 0], c="red")
    plt.plot(x, wave[:, 1], c="blue")
    plt.legend(["left channel", "right channel"])
    for i in interval:
        plt.axvline(x=i, c="grey", ls=":", alpha = 0.30)
    for s in sec_marks:
        plt.axvline(x=s, c="black", ls=":", alpha = 0.30)
    plt.xlabel("#Samples")
    plt.ylabel("Energy")

    plt.show()

