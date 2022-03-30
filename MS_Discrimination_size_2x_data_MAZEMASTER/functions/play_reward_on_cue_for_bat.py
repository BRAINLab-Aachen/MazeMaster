from psychopy.sound import Sound
from time import sleep

reward_on_freq = 2000.
# reward_off_freq = 10000.

sound_obj = Sound(value=reward_on_freq , octave=8, volume=0.01, secs=0.2, loops=0)
sound_obj.play()
sleep(0.3)
sound_obj.stop()
#
