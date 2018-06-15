#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
ethOS-update-manager - main - v0.4.3

Just handle results from a CMD 'show stats' or 'update' and reboot 
if nedeed, ie your hashrate is too low (aka MIN_HASH).

Please update with your personal settings CMD, 
SLEEPER, JET_LAG and MIN_HASH. You can of course use default settings
"""


# Import 

import os, time, logging
from logging import debug, warning, info


# Enable loging 

logging.basicConfig(	level=logging.INFO, 
						format='%(levelname)s - %(message)s')


# Consts

CMD = "show stats"	# CMD = "show stats" # or update
SLEEPER = 10 * 60 	# 5/10/15 minutes
MIN_HASH = 49		# 30 ou 120 ou 180 ...
JET_LAG = 7			# depends o fyour local time and your system time

# Functions

def one_process_already_runing() : 
	""" check if on porcess is already running"""

	time.sleep(10)
	process = os.popen("ps -aux | grep ethOS-update-manager").readlines()
	working = [p for p in process if "src/main.py" in p]
	nb = len(working)

	if not nb : return False
	else : return True


def data_from_cmd(cmd="show stats", fake_file=None) :
	"""create a txt from a popen command, for ex "show stats" """ 

	debug("data_from_cmd called")

	# define default fake file
	if not fake_file : 
		fake_file = "/home/ethos/ethOS-update-manager/.show_stats.txt"
	
	# handle cmd result
	if not os.system(cmd)	: 
		li = os.popen(cmd).readlines()
	else :
		msg = "{} : command unknown --> simulation mode ON".format(_time())
		warning(msg)
		li = os.popen("cat {}".format(fake_file))
	
	if not li : 
		msg = "{} : txt is None".format(_time())
		warning(msg)

	# list operations
	li = [i.replace("\n", "") for i in li if i.replace("\n", "")] # delete '\n' and null lines
	li = [i for i in li if i[0] != " "] # delete lines with no keys (mem info and models)
	li = [i.split(":") for i in li] # separate key, value with ":"
	li = [i for i in li if i[0]] 	# delete null keys
	li = [i for i in li if i[1]] # delete null values
	li = [[i[0].strip(), i[1].strip()] for i in li] # strip everything

	# dict operations
	data = {i[0] : i[1] for i in li} # create dict
	for i, j in data.items() : # auto cast
		try : data[i] = float(j)
		except : data[i] = str(j)

	return data


def return_hash(data, key="hash") : 
	""" return hash float"""

	try : 
		k = float(data[key])
		debug("good type 'float' of hash")
		return k
	except : 
		k = str(data["hash"])
		msg = "{} : error reading 'hash' as a float for : {}".format(
				_time(), k)
		warning(msg) 
		return k


def _time(jet_lag=JET_LAG) : 
	""" give local time in personal str format"""
	
	debug("_time called") 
	
	t = time.localtime()
	txt = "{:0>2}/{:0>2}/{:0>2} at {:0>2}:{:0>2}".format(
		t.tm_mday, t.tm_mon, t.tm_year - 2000, t.tm_hour+jet_lag, t.tm_min)

	return txt


# Main

def main() : 

	# if program already launched :  break
	if one_process_already_runing() : 
		return 0

	# init logging
	print("\n\n\n")
	msg = "{} : init new session!".format(_time())
	warning(msg)
			# send_bot(msg) 

	# main loop
	while True : 

		# wait
		time.sleep(SLEEPER) # to avoid multiple short reboot 
		
		# proceed 
		data = data_from_cmd("show stats") 	# extract data from cmd 
		hashrate = return_hash(data, "hash")

		# reboot option
		if isinstance(hashrate, float) : 
			if hashrate < MIN_HASH : 
				msg = " {} rebooting due to hashrate : {}\n".format(
				_time(), hashrate)
				warning(msg)
						# send_bot(msg) 
				os.system("r")
			else : 
				debug(" {} hashrate OK : {}\n".format(
				_time(), hashrate))
		else : 
			msg = " {} invalid hrate type {} \n".format(
				_time(), type(hashrate))
			warning()
					# send_bot(msg) 

		# record uptime
		uptime  = os.popen("uptime").readlines()[0].split(",")[0]
		uptime = uptime.split("up")[1]
		msg = "{} : uptime at {}".format(_time(), uptime)
		info(msg)


if __name__ == '__main__':
	main()

