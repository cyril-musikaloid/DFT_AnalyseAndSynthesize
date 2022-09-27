import numpy as np
import sounddevice as sd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# samples per second
smpl_rate = 2000

# Record in seconds
duration = 0.05
 
 # Define default sounddevice setting
sd.default.samplerate = smpl_rate
sd.default.channels = 1

###### Function Definition ######

def playStartBeep():
    beepArr = np.linspace(0, 1, 1 * smpl_rate, False)
    beepArr = np.sin(440 * beepArr * 2 * np.pi)
    sd.play(beepArr, smpl_rate)
    sd.wait()
    sd.stop()

def playEndBeep():
    beepArr = np.linspace(0, 1, 1 * smpl_rate, False)
    beepArr = np.sin(380 * beepArr * 2 * np.pi)
    sd.play(beepArr, smpl_rate)
    sd.wait()
    sd.stop()

def DFT_computeCoef(record, k):
    coef = 0

    for n in range(N):
        coef += record[n] * np.exp(-1j*((2*np.pi)/N)*n*k)
    
    return coef

def DFT_analyse(record):
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
    buffer = np.linspace(0, 100*N-1, 100*N, False, dtype=complex)

    for n in range (100*N):
        buffer[n] = DFT_computeDiscretValue(vector, n)

    return buffer


def onclick(event):
    realVector[(int)(event.xdata)] = (int)(event.ydata)

def onkey(event):
    buffer = DFT_synthesize(coefVector)
    displayPlot(np.round(np.real(buffer)))
    displayPlot(np.imag(buffer))
    displayPlot(record)
    #sd.play(np.round(np.real(buffer)), loop=True, blocking=True)

def displayPlot(buffer):
    dfig, dax = plt.subplots()
    dax.plot(buffer)
    plt.show()

def updatePlot(i):
    plot1.set_ydata(realVector)

#################################

playStartBeep()

 # Record the sound
record = sd.rec(int(duration * smpl_rate), dtype='int')
sd.wait()
N = record.size


playEndBeep()


sd.play(record, blocking=True)

displayPlot(record)

coefVector = DFT_analyse(record)

realVector = np.real(np.absolute(coefVector))

fig, ax = plt.subplots()
plot1, =  ax.plot(realVector)
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', onkey)
ani = FuncAnimation(fig,
                    updatePlot,
                    interval=1)
plt.show()
