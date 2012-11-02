from alh import alh
from alh.spectrum import *
from alh.common import log
import os
import serial
import string
import sys
import time

def ism_24ghz(time_start_arg, nodef):
	# cognitive terminal, default frequency
	SignalGenerationRun(
			alh = nodef(17),
			time_start = time_start_arg + 5.0,
			time_duration = 25,
			device_id = 0,
			config_id = 0,
			channel = 110,
			power = 0).program()

	# cognitive terminal, moved frequency
	SignalGenerationRun(
			alh = nodef(17),
			time_start = time_start_arg + 35.0,
			time_duration = 20,
			device_id = 0,
			config_id = 0,
			channel = 225,
			power = 0).program()
	
	# non-cognitive terminal's frequency
	SignalGenerationRun(
			alh = nodef(2),
			time_start = time_start_arg + 25.0,
			time_duration = 30,
			device_id = 0,
			config_id = 0,
			channel = 112,
			power = 0).program()

	return MultiNodeSpectrumSensingRun(
			nodes = [nodef(4), nodef(6), nodef(24), nodef(25), nodef(26) ],
			time_start = time_start_arg,
			time_duration = 60,
			device_id = 0,
			config_id = 0,
			ch_start = 0,
			ch_step = 1,
			ch_stop = 255,
			slot_id = 6)

def test_n13(time_start_arg, nodef):
	# cognitive terminal, default frequency
	SignalGenerationRun(
			alh = nodef(13),
			time_start = time_start_arg + 5.0,
			time_duration = 25,
			device_id = 0,
			config_id = 0,
			channel = 110,
			power = 0).program()

	# cognitive terminal, moved frequency
	SignalGenerationRun(
			alh = nodef(13),
			time_start = time_start_arg + 35.0,
			time_duration = 20,
			device_id = 0,
			config_id = 0,
			channel = 225,
			power = 0).program()

	# non-cognitive terminal's frequency
	SignalGenerationRun(
			alh = nodef(11),
			time_start = time_start_arg + 25.0,
			time_duration = 30,
			device_id = 0,
			config_id = 0,
			channel = 112,
			power = 0).program()

	return MultiNodeSpectrumSensingRun(
			nodes = [nodef(6), nodef(15), nodef(4), nodef(26),
					nodef(17), nodef(24) ],
			time_start = time_start_arg,
			time_duration = 60,
			device_id = 0,
			config_id = 0,
			ch_start = 0,
			ch_step = 1,
			ch_stop = 255,
			slot_id = 6)

def test_n11(time_start_arg, nodef):
	# cognitive terminal, default frequency
	SignalGenerationRun(
			alh = nodef(11),
			time_start = time_start_arg + 5.0,
			time_duration = 25,
			device_id = 0,
			config_id = 0,
			channel = 110,
			power = 0).program()

	# cognitive terminal, moved frequency
	SignalGenerationRun(
			alh = nodef(11),
			time_start = time_start_arg + 35.0,
			time_duration = 20,
			device_id = 0,
			config_id = 0,
			channel = 225,
			power = 0).program()


	return MultiNodeSpectrumSensingRun(
			nodes = [nodef(15), nodef(4), nodef(13) ],
			time_start = time_start_arg,
			time_duration = 60,
			device_id = 0,
			config_id = 0,
			ch_start = 0,
			ch_step = 1,
			ch_stop = 255,
			slot_id = 6)


def test_n15(time_start_arg, nodef):
	# cognitive terminal, default frequency
	SignalGenerationRun(
			alh = nodef(15),
			time_start = time_start_arg + 5.0,
			time_duration = 25,
			device_id = 0,
			config_id = 0,
			channel = 110,
			power = 0).program()

	# cognitive terminal, moved frequency
	SignalGenerationRun(
			alh = nodef(15),
			time_start = time_start_arg + 35.0,
			time_duration = 20,
			device_id = 0,
			config_id = 0,
			channel = 225,
			power = 0).program()


	return MultiNodeSpectrumSensingRun(
			nodes = [nodef(11), nodef(4), nodef(13), nodef(6) ],
			time_start = time_start_arg,
			time_duration = 60,
			device_id = 0,
			config_id = 0,
			ch_start = 0,
			ch_step = 1,
			ch_stop = 255,
			slot_id = 6)


def main():
	#f = serial.Serial("/dev/ttyUSB0", 115200, timeout=10)
	#coor = alh.ALHTerminal(f)

	coor = alh.ALHWeb("https://crn.log-a-tec.eu/communicator", 10001)
	coor._log = log

	called = set()

	def nodef(addr):
		n = alh.ALHProxy(coor, addr)

		if addr not in called:
			n.post("prog/firstCall", "1")
			called.add(addr)

		return n
	
	time_start = time.time() + 45

	# experiment = ism_24ghz(time_start, nodef)
	experiment = test_n13(time_start, nodef);

	experiment.program()

	print "waiting 60s so the experiment can finish"
	time.sleep(60);

	while not experiment.is_complete():
		print "waiting..."
		time.sleep(2)

	print "experiment is finished. retrieving data."

	results = experiment.retrieve()

	try:
		os.mkdir("data")
	except OSError:
		pass
	write_results("data", results, experiment)

main()
