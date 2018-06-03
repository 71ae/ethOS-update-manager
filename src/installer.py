#!/usr/bin/env python3
#--*-- coding: utf-8 --*--


# update install.pk
with open("/home/ethos/ethOS-update-manager/_ethuper/var/install.pk", "w") as f:
	f.write("True")

	
# prepare sys
os.system("cd")
os.system("chmod +x /home/ethos/ethOS-update-manager/autolaunch-updater")
os.system("chmod +x /home/ethos/ethOS-update-manager/ethuper")

os.system("chmod +x /home/ethos/ethOS-update-manager/_ethuper/updater.py")
os.system("chmod +x /home/ethos/ethOS-update-manager/_ethuper/ethuper.py")


# create alias
os.system("""echo "alias ethuper='/home/ethos/ethOS-update-manager/ethuper'" >>  /home/ethos/.bashrc""")

# for automatic program launch (background) at each ethos stratup : 
os.system("echo '/home/ethos/ethOS-update-manager/autolaunch-updater' >> /home/ethos/.bashrc")


# reboot 
print("for full install, system will reboot in : ")
for i in range(3, 0, -1) : 
	print(str(i))
	time.sleep(1)

#auto reboot 
os.system("r")