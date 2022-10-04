from array import array
from signal import signal
import numpy as np
import sounddevice as sd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# samples per second
_smpl_rate = 8000

# Record in seconds
_duration = 0.05
 
 # Define default sounddevice setting
sd.default.samplerate = _smpl_rate
sd.default.channels = 1

###### Function Definition ######

def playStartBeep():
    beepArr = np.linspace(0, 1, 1 * _smpl_rate, False)
    beepArr = np.sin(440 * beepArr * 2 * np.pi) * 0.05
    sd.play(beepArr, _smpl_rate)
    sd.wait()
    sd.stop()

def playEndBeep():
    beepArr = np.linspace(0, 1, 1 * _smpl_rate, False)
    beepArr = np.sin(380 * beepArr * 2 * np.pi) * 0.05
    sd.play(beepArr, _smpl_rate)
    sd.wait()
    sd.stop()

def DFT_computeCoef(record, k):
    coef = 0+0j
    N = record.size
    for n in range(N):
        coef += record[n] * np.exp(-1j*((2*np.pi)/N)*n*k)
    
    return coef

def DFT_analyse(record, L = 0):
    N = record.size
    if L:
        N = L
    
    coefVector = np.linspace(0, (N-1), N, False, dtype=complex)

    for k in range((N)):
        coefVector[k] = DFT_computeCoef(record, k)

    return coefVector

def DFT_computeDiscretValue(vector, n):
    dValue = 0

    for k in range (N):
        dValue += (vector[k] * np.exp(1j * ((2*np.pi)/N)*n*k))
    
    dValue /= N

    return dValue

def DFT_synthesize(vector):
    buffer = np.linspace(0, N-1, N, False, dtype=complex)

    for n in range (N):
        buffer[n] = DFT_computeDiscretValue(vector, n)

    return buffer


def onclick(event):
    realVector[(int)(event.xdata)] = (int)(event.ydata)

def onkey(event):
    buffer = DFT_synthesize(realVector + imagVector * 1j)
    realBuffer = np.int32(np.round(np.real(buffer)))
    imagBuffer = np.imag(buffer)
    displayAllPlot(realBuffer, imagBuffer, record)
    sd.play(np.int32(np.round(np.real(buffer))), loop=True, blocking=False)

def displayAllPlot(realBuffer, imagBuffer, record_real, record_imag):
    aFig, axd = plt.subplot_mosaic([['freq'],
                                    ['.'],
                                    ['phase'],
                                    ['.'],
                                    ['record_real'],
                                    ["."],
                                    ["record_imag"]])

    axd['freq'].set_title('frequencies')
    axd['phase'].set_title('phase')
    axd['record_real'].set_title('record real')
    axd['record_imag'].set_title('record imag')

    axd['freq'].plot(realBuffer)
    axd['phase'].plot(imagBuffer)
    axd['record_real'].plot(record_real)
    axd['record_imag'].plot(record_imag)

    plt.show()

def displayPlot(buffer):
    dfig, dax = plt.subplots()
    dax.plot(buffer)
    plt.show()

def updatePlot(i):
    plot1.set_ydata(realVector)

def findPatternPosition(ascending, buffer, value):

    for i in range(20, buffer.size):
        indexAscending = buffer[i] < buffer[i-1]

        if buffer[i] > value > buffer[i-1] & ascending & indexAscending:
            return i-1
        elif buffer[i] < value < buffer[i-1] & (not ascending) & (not indexAscending):
            return i-1

    return 20


def reworkRecord(buffer):
    ascending = buffer[buffer.size-1] > buffer[buffer.size-2]
    pos = findPatternPosition(ascending, buffer, buffer[buffer.size-1])
    return buffer[pos : ]


def genSinWave(N, f = 1, a = 1, phi = 0):
    n = np.arange(N)
    signal = a * np.cos(n * f + (phi*np.pi/180))
    #signal = a*np.exp(1j*(f*n+phi)) provoks a dephased imaginary part
    return signal

def DFT_analyseAndDisplay(signal):
    DFTed_Signal = DFT_analyse(signal)
    displayAllPlot(np.real(DFTed_Signal), np.imag(DFTed_Signal), np.real(signal), np.imag(signal))

def Record(duration = _duration, sampleRate = _smpl_rate):
    playStartBeep()

    record=sd.rec(int(duration * sampleRate))
    sd.wait()

    playEndBeep()
    return record

def Play(record):
    sd.play(record)
    sd.wait()

def ComputeSpectrogram(signal, windowSize = 256):
    N = signal.size
    L = windowSize

    numberOfSlice = np.int32(np.ceil(N/L))

    spectrogram = np.empty((numberOfSlice, np.int32(L/2)))

    for sliceIndex in range(numberOfSlice):
        spectrogram[sliceIndex] = np.abs(np.real(DFT_analyse(signal[sliceIndex*L:(sliceIndex+1)*L],  np.int32(L/2))))

    return spectrogram

def DisplaySpectrogram(spectrogram):
    dfig, dax = plt.subplots()
    im = dax.imshow(spectrogram, cmap='plasma', origin='upper')
    
    plt.show()

#################################

##### Computation Function ######

#################################

record = Record(duration=2)

Play(record)

spectrogram = ComputeSpectrogram(record, windowSize=128)

DisplaySpectrogram(spectrogram)