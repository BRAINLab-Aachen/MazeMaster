from psychopy.sound import Sound
from time import time, sleep
import _thread


def _play_sound_for_thread(freq):
    sound_obj = Sound(value=freq, octave=8, volume=0.1, secs=0.2, loops=0)
    sound_obj.play()
    sleep(0.5)
    sound_obj.stop()

    return 0
#


def run():
	# reward_on_freq = 2000.
	# reward_off_freq = 10000.
	freq = 2000.
	_thread.start_new_thread(_play_sound_for_thread, (freq,))
#
