import alh
import serial
import string
import sys
import pickle

def add_communication_options(parser):
	parser.add_option("-U", "--url", dest="url", metavar="URL",
			help="Use URL for communication with coordinator")
	parser.add_option("-u", "--cluster", dest="cluster_id", metavar="ID", type="int",
			help="Cluster ID to pass to the web API")

	parser.add_option("-D", "--device", dest="device", metavar="PATH",
			help="Use serial terminal for communication with coordinator")
	parser.add_option("-d", "--debug", dest="debug", action="store_true",
			help="Enable debug output on standard error")

def log(msg):
	if all(c in string.printable for c in msg):
		sys.stderr.write("%s\n" % (msg.decode("ascii", "ignore"),))
	else:
		sys.stderr.write("Unprintable packet\n")

def get_coordinator(options):
	if options.url and not options.device:
		coordinator = alh.ALHWeb(options.url, options.cluster_id)
	elif options.device and not options.url:
		f = serial.Serial(options.device, 115200, timeout=10)
		coordinator = alh.ALHTerminal(f)
	else:
		raise Exception("Please give either -U or -D option")

	if options.debug:
		coordinator._log = log

	return coordinator


def load_auth():
	'''
	Try to load authentication information from "auth.pickle".
	If it succeeds, it returns the user-name and password
	in a 2-element array.
	If it fails, a 2-element array of empty string is returned.
	'''
	# TODO it would be nice to be able to specify the authentication file name
	#	from the command line
	try:
		f = open("auth.pickle", "r")
	except IOError as e:
		print "authentication file open error:", e
		return [ "", "" ]
	pwd_pass_dict = pickle.load(f)
	f.close()
	return [pwd_pass_dict['user'], pwd_pass_dict['pwd']]
