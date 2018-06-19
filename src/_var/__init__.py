#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
var functions
"""


# import 

import pickle, random, urllib.request


# sys params

SLEEPER 	= 10 * 60		# IN SECONDS think to multiply by 60 for minutes ;)
LAP_STAMP	= 6 * 4			# update normal status each LAP_STAMP * SLEEPER sec

AUTO_REBOOT = True			# enable auto reboot if min hashrate threshold reached
AUTO_LAUNCH = True			# enable auto lauch at system boot

HASH_MODE	= True			# enable if hashraste is too low
MIN_HASH 	= 179			# 30 ou 120 ou 180 ... depends of your perf and GPU's number

TEMP_MODE	= True			# enable reboot if over warming 
MAX_TEMP	= 75			# 70, 75, 80 ... depends of the care you have for your GPUs

JET_LAG 	= 8				# depends of your local/sys time 
LATENCY 	= True			# if LATENCY additionnal sleeper added to give time 
							# to rig to be fully operational (STRONGLY RECOMMANDED)
LOGGING_LEVEL = 100

SYS_VAR_PAIRS = [ 	("SLEEPER", SLEEPER), ("LAP_STAMP", LAP_STAMP),
	      			("AUTO_REBOOT",AUTO_REBOOT), ("AUTO_LAUNCH", AUTO_LAUNCH), 
	      			("HASH_MODE", HASH_MODE), ("MIN_HASH", MIN_HASH), 	
	      			("TEMP_MODE", TEMP_MODE), ("MAX_TEMP", MAX_TEMP), 
	      			("JET_LAG", JET_LAG), ("LATENCY",LATENCY), ("LOGGING_LEVEL", LOGGING_LEVEL)]


# sys paths

ROOT_FOLDER = "/home/ethos/ethOS-update-manager/"
VAR_FOLDER 	=  ROOT_FOLDER + "src/var/"
DATA_FOLDER	=  ROOT_FOLDER + "data/"
DOC_FOLDER 	=  ROOT_FOLDER + "docs/"


# telegram params

TELEGRAM_MODE 	= False 	
TOKEN 			= "YourToken"
CHAT_ID 		= "YourChatId"
RIG 			= "YourRigName"


# functions 

def var_manager(filename, mode, var=None, folder=VAR_FOLDER) : 
	""" """

	if mode == "r" : 
		with open(folder+filename, mode) as f : res = f.read()
		try : 
			res = int(res)
		except : 
			pass
		return res

	elif mode == "i" : 
		with open(folder+filename, "r") as f : res = f.read()
		try : 
			res = str(int(res) + 1)
			with open(folder+filename, "w") as f :  f.write(res)
		except : 
			raise ValueError("incrementation not possible, txt/bin format confusion")

	elif mode == "w" : 
		with open(folder + filename, mode) as f : f.write(str(var))
		return 1

	elif mode =="rb" :
		with open(folder+filename, mode) as f : res = pickle.load(f)	
		try : 
			res = int(res)
		except : 
			pass
		return res
	
	elif mode == "wb" :
		try : 
			var = int(var)
		except : 
			pass 
		with open(folder + filename, mode) as f : pickle.dump(var, f)
		return 1

	elif  mode == "ib" : 
		with open(folder+filename, "rb") as f : res = pickle.load(f)
		try : 
			res = int(res) + 1
			with open(folder+filename, "wb") as f : pickle.dump(res, f)
		except : 
			raise ValueError("incrementation not possible, txt/bin format confusion")

	else : 
		raise ValueError("Fatal Error")


def var_list(folder=VAR_FOLDER): 
	""" """ 

	print(os.listdir(folder))
	return(os.listdir(folder)) 


def var_read(folder=VAR_FOLDER, verbose=False) : 
	""" """

	file_list = os.listdir(folder)
	if verbose : 
		print(file_list) 

	for file in file_list : 
		print(str(file + " : "), end="  ")
		try : 
			with open(folder+file, "r") as f : var = f.read()
			if verbose : 
				print("txt format : ")
			print(var)
		
		except : 
			with open(folder+file, "rb") as f : var = str(pickle.load(f))
			if verbose : 
				print("bin format : ")
			print(str(var), str(type(var)))


def handle_choice(*li) : 
	"""read a bool response"""

	# ans = input("y/n\n")
	
	# while True: 

	# 	if ans.lower() == "y" : 
	# 		return True
	# 	elif ans.lower() == "n":
	# 		return False
	# 	else : 
	# 		ans = input("\nwrong input, expected 'y' or 'n'\n")


def handle_bool(default=None) : 
	"""read a bool response"""

	if default : 

		ans = input("'y' / 'n' -- 'd' for default value\n")
		
		while True: 

			if ans.lower() == "y" : 
				return True
			elif ans.lower() == "n":
				return False
			elif  ans.lower() == "d" : 
				return default
			else : 
				ans = input("\nwrong input, expected 'y', 'n', or  'd'\n")

	else : 
		ans = input("'y' / 'n'\n")
		
		while True: 

			if ans.lower() == "y" : 
				return True
			elif ans.lower() == "n":
				return False
			else : 
				ans = input("\nwrong input, expected 'y', 'n'\n")
			

def handle_int(mi=0, ma=10000, default=None) : 
	"""read a int response"""

	if default : 

		ans = input("number between {} and {}  --  'd' for defalut value\n".format(mi, ma))

		if ans.lower() == "d" : 
			return default
		
		while True: 

			try : 
				ans = int(ans)
				if (ans > mi) and (ans < ma) : 
					return ans
				else : 
					ans = input("\nwrong input, expected number between {} and {}, or 'd'\n".format(mi, ma))
			except :  
				ans = input("\nwrong input, expected number between {} and {}, or 'd'\n".format(mi, ma))

	else : 
		ans = input("number between {} and {}\n".format(mi, ma))
		
		while True: 

			try : 
				ans = int(ans)
				if (ans > mi) and (ans < ma) : 
					return ans
				else : 
					ans = input("\nwrong input, expected number between {}\n".format(mi, ma))
			except :  
				ans = input("\nwrong input, expected number between {}\n".format(mi, ma))



def set_system_var(mode="wb", pairs=SYS_VAR_PAIRS, folder=VAR_FOLDER) : 
	""" """

	print("do you want to use system default var ?")
	ans = handle_bool()

	if ans : 
		[var_manager(f, mode, var, folder=folder) for (f, var) in pairs]
		

	else : 
		print("\n\nSLEEPER : the time of loop processing -- in seconds --, \ndefault value (STRONGLY RECOMMANDED) : {}".format(SLEEPER))
		print("\ndefine sleeper : ", end ="")
		ans = handle_int(60, 60*60, SLEEPER)
		var_manager("SLEEPER", mode, ans, folder=folder)

		print("\n\nLAP_STAMP : the rate of info logging (inform you if everything is fine), the more it is important the less you will be informed -- in lap --, \ndefault value (STRONGLY RECOMMANDED) : {}".format(LAP_STAMP))
		print("\ndefine lap_stamp : ", end ="")
		ans = handle_int(1, 6*24, LAP_STAMP)
		var_manager("LAP_STAMP", mode, ans, folder=folder)		


		print("\n\nAUTO_REBOOT : Boolean value -- 'y'/'n'--, if set, your miner will reboot if MIN_HASH threshold is reached, \ndefault value (STRONGLY RECOMMANDED) : {}".format("'y'"))		
		print("\ndefine auto reboot : ", end ="")
		ans = handle_bool(AUTO_REBOOT)
		var_manager("AUTO_REBOOT", mode, ans, folder=folder)

		print("\n\nAUTO_LAUNCH: Boolean value -- 'y'/'n'--, if set, your program will be launched automaticly when your miner will boot, \ndefault value (STRONGLY RECOMMANDED) : {}".format("'y'"))		
		print("\ndefine auto reboot : ", end ="")
		ans = handle_bool(AUTO_LAUNCH)
		var_manager("AUTO_LAUNCH", mode, ans, folder=folder)


		print("\n\nHASH_MODE : Boolean value -- 'y'/'n'--, do you allow your system to check and take care of your hashrate ? \ndefault value (STRONGLY RECOMMANDED) : {}".format("'y'"))
		print("\ndefine min_hash : ", end ="")
		ans = handle_bool(HASH_MODE)
		var_manager("HASH_MODE", mode, ans, folder=folder)

		print("\n\nMIN_HASH : if your miner's hashrate fall bellow this threshold you will be warned and miner will reboot. Consider nb of GPUS x min GPU expected rate -- in global summed hashrate --, \ndefault value : {}".format(MIN_HASH))
		print("\ndefine min_hash : ", end ="")
		ans = handle_int(15, 12 * 35, MIN_HASH)
		var_manager("MIN_HASH", mode, ans, folder=folder)


		print("\n\nTEMP_MODE : Boolean value -- 'y'/'n'--, do you allow your system to check and take care of your GPUs temperature ? \ndefault value (STRONGLY RECOMMANDED) : {}".format("'y'"))
		print("\ndefine min_hash : ", end ="")
		ans = handle_bool(TEMP_MODE)
		var_manager("TEMP_MODE", mode, ans, folder=folder)

		print("\n\nMAX_TEMP : if one of your GPUs temp is too hot  -- in °C -- your miner will be stoped for 30 min or 1 hour, you will be warned and miner will reboot, \ndefault value : {}".format(MIN_HASH))
		print("\ndefine min_hash : ", end ="")
		ans = handle_int(15, 12 * 35, MIN_HASH)
		var_manager("MIN_HASH", mode, ans, folder=folder)


		print("\n\nJET_LAG : the time stamp -- in hours -- between your local time and your system time, \ndefault value : {}".format(JET_LAG))		
		print("\ndefine jet_lag : ", end ="")
		ans = handle_int(-24, +24, JET_LAG)
		var_manager("JET_LAG", mode, ans, folder=folder)
	
		print("\n\nLATENCY : Boolean value -- 'y'/'n'--, if set, your miner will have the time to wake up and to launch all GPUs before being scanned, \ndefault value (STRONGLY RECOMMANDED) : {}".format("'y'"))		
		print("\ndefine latency : ",end ="")
		ans = handle_bool(LATENCY)
		var_manager("LATENCY", mode, ans, folder=folder)

		print("\n\nLOGGING_LEVEL : Boolean value -- 'y'/'n'--, not implemented yet :), \ndefault value (STRONGLY RECOMMANDED) : {}".format("'y'"))		
		print("\ndefine logging_level : ",end ="")
		ans = handle_bool(LOGGING_LEVEL, end ="")
		var_manager("LOGGING_LEVEL", mode, ans, folder=folder)


def set_telegram_var(mode="wb", folder=VAR_FOLDER) :
	""" """ 
	
	print("do you want to enable telegram auto push logging ?")
	ans = handle_bool()

	if ans : 

		while True :  

			var_manager("TELEGRAM_MODE", mode, True)

			print("\ndefine token : ")
			token = input("alphanumeric input\n")
			var_manager("TOKEN", mode, token)

			print("\ndefine chat_id : ")
			chat_id = input("alphanumeric input\n")
			var_manager("CHAT_ID", mode, chat_id)		

			print("\ndefine rig_name : ")
			rig = input("alphanumeric input\n")
			var_manager("RIG", mode, rig)

			connect_not_confirmed = confirm_connexion(token, chat_id)
			
			if connect_not_confirmed == 0 : 
				break
			elif connect_not_confirmed == 1 : 
				pass
			elif connect_not_confirmed == 2 : 
				var_manager("TELEGRAM_MODE", mode, False)
				print("\n" *2)
				print("################################")
				print()
				print("WARNING : TELEGRAM_MODE DISABLED")
				print()
				print("################################")
				print("\n"*2)
				print("please type <Enter> to continue...")
				input()
				break
			else : 
				print("Fatal error")
	
	else :
		var_manager("TELEGRAM_MODE", mode, False)


def confirm_connexion(token, chat_id, mi=100000, ma=999999) : 
	""" """

	code = random.randint(mi, ma)

	try : 
		code = "connection+code+is+{}".format(code)
		req = str('https://api.telegram.org/bot' + str(token) + '/sendMessage?chat_id=' + str(chat_id) + '&parse_mode=Markdown&text=' + str(code))	
		urllib.request.urlopen(req)

		print("\nto autorize connection, a personnal code was sent to your telegram account, please check")
		print("\nconnection code : ")
		ans = handle_int(mi, ma)

		if ans == code : 	
			print("\nconnection established")
			return 0
		else : 
			print("\nconnection error, try again (ie 'y') or disable telegram mode (ie 'n')")
			ans = handle_bool()

			if ans  : return 1
			else 	: return 2 
	
	except : 
		print("\nconnection error, try again (ie 'y') or disable telegram mode (ie 'n')")
		ans = handle_bool()

		if ans  : return 1
		else 	: return 2 


def load_system_var(mode="rb", pairs=SYS_VAR_PAIRS, folder=VAR_FOLDER) : 
	""" """

	return (var_manager(f, mode, folder=folder) for (f, var) in pairs)


def load_telegram_var(mode="rb", folder=VAR_FOLDER) : 
	""" """

	TELEGRAM_MODE 	= var_manager("TELEGRAM_MODE", mode)

	if not TELEGRAM_MODE : 
		return False, None, None, None

	else :
		TOKEN 	= var_manager("TOKEN", mode)
		CHAT_ID	= var_manager("CHAT_ID", mode)
		RIG 	= var_manager("RIG", mode)

		return True, TOKEN, CHAT_ID, RIG



