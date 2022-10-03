from signal import signal
import numpy as np
import sounddevice as sd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# samples per second
smpl_rate = 8000

# Record in seconds
duration = 0.05
 
 # Define default sounddevice setting
sd.default.samplerate = smpl_rate
sd.default.channels = 1

###### Function Definition ######

def playStartBeep():
    beepArr = np.linspace(0, 1, 1 * smpl_rate, False)
    beepArr = np.sin(440 * beepArr * 2 * np.pi) * 0.05
    sd.play(beepArr, smpl_rate)
    sd.wait()
    sd.stop()

def playEndBeep():
    beepArr = np.linspace(0, 1, 1 * smpl_rate, False)
    beepArr = np.sin(380 * beepArr * 2 * np.pi) * 0.05
    sd.play(beepArr, smpl_rate)
    sd.wait()
    sd.stop()

def DFT_computeCoef(record, k):
    coef = 0+0j
    N = record.size
    for n in range(N):
        coef += record[n] * np.exp(-1j*((2*np.pi)/N)*n*k)
    
    return coef

def DFT_analyse(record):
    N = record.size
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

#################################

##### Computation Function ######

def _2_WkN(N, k):
    N_vec = np.arange(1, N)
    k_vec = N_vec / 2
    result = np.exp(-1j*((2*np.pi)/N_vec)*k_vec)
    displayPlot(result)
    
    result = np.exp(-1j*((2*np.pi)/N_vec)+N_vec)
    displayPlot(result)

def _3():
    f = np.sqrt(2)
    n = np.arange(-50, 50)
    signal = np.exp(-1j*f*n) + np.exp(+1j*f*n)
    displayPlot(signal)

    signal = np.sin(n)
    displayPlot(signal)

    t = np.linspace(-1000, 1000, 20000)
    signal = t - np.floor(t)
    displayPlot(signal)

    f = 5
    phi = 90
    signal = np.cos(2*np.pi*f*t + phi)
    displayPlot(signal)

def _4():
    N = 64
    n = np.arange(N)
    signal = np.power(-1, n)
    DFT_analyseAndDisplay(signal)

    L = N/2
    phi = 90
    signal = np.cos(((2*np.pi)/N)*L*n + phi)

    for k in range(N):
        coef = DFT_computeCoef(signal, k)
        if coef == ((N/2)*np.exp(1j*phi)) and (not k == L):
            print("error\n")
        elif coef == 0 and k == L:
            print("error\n")
        
    DFTed_Signal = DFT_analyse(signal)
    displayPlot(np.real(DFTed_Signal))
    print(((N/2)*np.exp(1j*phi)))
    print(DFT_computeCoef(signal, L))
    print(((N/2)*np.exp(-1j*phi)))
    print(DFT_computeCoef(signal, N-L))

def genSinWave(N, f = 1, a = 1, phi = 0):
    n = np.arange(N)
    signal = a * np.cos(n * f + (phi*np.pi/180))
    #signal = a*np.exp(1j*(f*n+phi)) provoks a dephased imaginary part
    return signal

def DFT_analyseAndDisplay(signal):
    DFTed_Signal = DFT_analyse(signal)
    displayAllPlot(np.real(DFTed_Signal), np.imag(DFTed_Signal), np.real(signal), np.imag(signal))

def _6():
    phi = 0
    f = 0.4
    N = 64
    n = np.arange(N)
    a = 2

    signal = genSinWave(N, f, a, phi)
    DFT_analyseAndDisplay(signal)

    signal = genSinWave(N, 0.8, 0.5, -90)
    DFT_analyseAndDisplay(signal)

def _7():
    N = 64
    L = 10
    M = N
    n = np.arange(N)
    signal = np.cos(2*np.pi*(L/M)*n)
    DFT_analyseAndDisplay(signal)

    n = np.roll(n,12)
    signal = np.cos(2*np.pi*(L/M)*n)
    DFT_analyseAndDisplay(signal)

def _8():
    signal = genSinWave(65, 0.5, phi=31)
    DFT_analyseAndDisplay(signal)

def _9():
    N = 65
    n = np.arange(N)
    signal = -np.power(-1, n)
    DFT_analyseAndDisplay(signal)

#################################

_7()