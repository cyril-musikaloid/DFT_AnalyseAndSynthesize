import numpy as np
import sounddevice as sd
import matplotlib as mpl
import matplotlib.pyplot as plt

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
    N = record.size
    coef = 0

    for n in range(N):
        coef += record[n] * np.exp(-1j*((2*np.pi)/N)*n*k)
    
    return coef

def DFT_analyse(record):
    N = record.size
    coefVector = np.linspace(0, (int)(N/2), (int)(N/2), True, dtype=complex)
    
    for k in range((int)(N/2)):
        coefVector[k] = DFT_computeCoef(record, k)

    return coefVector

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print(ix)
    print("\t")
    print(iy)
    print("\n")

#################################

playStartBeep()

 # Record the sound
record = sd.rec(int(duration * smpl_rate), dtype='int')
sd.wait()
 
playEndBeep()

sd.play(record, smpl_rate)
sd.wait()
sd.stop()

fig, ax = plt.subplots()
ax.plot(record)
fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

coefVector = DFT_analyse(record)

realVector = np.real(coefVector)

fig, ax = plt.subplots()
ax.plot(np.absolute(realVector))
plt.show()

imagVector = np.imag(coefVector)

fig, ax = plt.subplots()
ax.plot(np.absolute(imagVector))
plt.show()