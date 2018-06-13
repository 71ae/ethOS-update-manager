#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os


def main() : 
	process = os.popen("ps -aux | grep ethOS-update-manager").readlines()
	is_working = ["src/main.py" in p for p in process]

	if True not in is_working :  
		print("ethOS-update-manager first launch")
		os.system("nohup python3 /home/ethos/ethOS-update-manager/src/main.py >> /home/ethos/ethOS-update-manager/logs/log 2>&1 &")
	else : 
		print("ethOS-update-manager already running")


if __name__ == '__main__':
	main()