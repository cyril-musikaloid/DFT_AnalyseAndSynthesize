import numpy as np
import sounddevice as sd
import matplotlib as mpl
import matplotlib.pyplot as plt

# samples per second
smpl_rate = 44100

# Record in seconds
duration = 3 
 
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
plt.show()