from alh import alh
from alh.spectrum import *
from alh.common import log
import serial
import string
import sys
import time

def ism_24ghz(time_start, nodef):

	return MultiNodeSpectrumSensingRun(
			# [nodef(2), nodef(6), nodef(4)],
			[ nodef(2)],
			time_start = time_start,
			time_duration = 20,
			device = 0,
			config = 0,
			ch_start = 0,
			ch_step = 1,
			ch_stop = 255,
			slot_id = 6)

def uhf_multiplex(time_start, nodef):
	return MultiNodeSpectrumSensingRun(
			[nodef(19)],
			time_start = time_start,
			time_duration = 120,
			device = 0,
			config = 0,
			ch_start = 76000,
			ch_step = 500,
			ch_stop = 116000,
			slot_id = 5)

def uhf_wireless_mic(time_start, nodef):
	SignalGenerationRun(
			nodef(8),
			time_start = time_start + 30.0,
			time_duration = 60,
			device = 0,
			config = 0,
			channel = 0,
			power = 0).program()

	SignalGenerationRun(
			nodef(8),
			time_start = time_start + 90.0,
			time_duration = 60,
			device = 0,
			config = 0,
			channel = 40,
			power = 0).program()

	SignalGenerationRun(
			nodef(10),
			time_start = time_start + 90.0,
			time_duration = 60,
			device = 0,
			config = 0,
			channel = 0,
			power = 0).program()

	SignalGenerationRun(
			nodef(8),
			time_start = time_start + 150.0,
			time_duration = 60,
			device = 0,
			config = 0,
			channel = 0,
			power = 0).program()

	SignalGenerationRun(
			nodef(7),
			time_start = time_start + 30.0,
			time_duration = 180,
			device = 0,
			config = 0,
			channel = 80,
			power = 0).program()

	return MultiNodeSpectrumSensingRun(
			[nodef(19)],
			time_start = time_start,
			time_duration = 240,
			device = 0,
			config = 0,
			ch_start = 290000,
			ch_step = 500,
			ch_stop = 350000,
			slot_id = 5)

def main():
	#f = serial.Serial("/dev/ttyUSB0", 115200, timeout=10)
	#coor = alh.ALHTerminal(f)

	coor = alh.ALHWeb("https://crn.log-a-tec.eu/communicator", 9502)
	coor._log = log

	called = set()

	def nodef(addr):
		n = alh.ALHProxy(coor, addr)

		if addr not in called:
			n.post("prog/firstCall", "1")
			called.add(addr)

		return n

	time_start = time.time() + 15

	experiment = ism_24ghz(time_start, nodef)
	#experiment = uhf_multiplex(time_start, nodef)
	#experiment = uhf_wireless_mic(time_start, nodef)

	experiment.program()

	while not experiment.is_complete():
		print "waiting..."
		time.sleep(2)

	print "experiment is finished. retrieving data."

	results = experiment.retrieve()

	write_results("h", results, experiment)

main()
