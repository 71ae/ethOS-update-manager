#!/usr/bin/env python3
# -*- coding: utf-8 -*-



# import

import os, subprocess, pickle, time, logging
from logging import debug, warning, info

from _var_manager import * 
from confs.params import * 
from confs.filepaths import * 



# functions

def data_from_cmd(cmd=CMD) :
	"""create a txt from a popen command, for ex "update" """ 

	logging.info("data_from_cmd called")
	v = os.system(cmd) 
	if v : 
		logging.warning("command problem")
	
	wrap = os.popen(cmd)
	txt = str()

	for i in wrap : 
		txt +=i

	if not txt : 

		logging.info("txt is None")

	return txt


def load_temp_file(folder=DATA_FOLDER, filename=TEMP_FILE) : 
	"""load data from file"""

	logging.info("load_data called")
	
	txt = var_manager(filename, "r", folder=folder)
	subtxt = txt[:300]
	
	logging.info(subtxt)

	return txt


def convert_txt(txt):
	"""from the str version of cli "update", create and return a list of
	key, values"""

	logging.info("convert_txt called")

	# fist split lines
	li1 = txt.splitlines()

	# separate key, value with ":"
	li2 = [i.split(":") for i in li1]

	# delete null values
	li2 = [i for i in li2 if i[0]]

	# info some key values encoded on sevral lines
	li3 = [["None", i[0]] if len(i) == 1 else i for i in li2]

	# strip everything
	li3 = [[i[0].strip(), i[1].strip()] for i in li3]
	
	logging.debug(li3)

	return li3


def convert_organized_txt(data, header=HEADER) : 
	"""from dict and in a specific order, build text to record"""

	logging.info("convert_organized_txt called")

	li = [str(data[i]) for i in header]

	logging.debug(li)

	txt = ",".join(li)
	txt+="\n"

	logging.debug(txt)

	return txt


def fake_cmd() : 
	""" """

	# to code
	pass