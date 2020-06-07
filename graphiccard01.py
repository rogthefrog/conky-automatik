# -*- encoding: utf-8 -*-
import os
from translations import *

DEBUG=0

# determine installed language
Language_installed=os.popen("locale | grep LANG").read()
if "fr" in Language_installed:
	Language="French"
elif "de" in Language_installed:
	Language="German"
elif "pt" in Language_installed:
	Language="Portuguese"
elif "it" in Language_installed:
	Language="Italian"
else:
	Language="English"


def writefile( str ):
	f = open('graphiccardfile', 'w')
	f.write(str)  # python will convert \n to os.linesep
	f.close()  # you can omit in most cases as the destructor will call it


#----------------------------------------------------
# -------- Load header of conky file-----------------
#----------------------------------------------------

header = open('header.py', 'r').read()


Conky_Text=[]

txt01="""
gap_x 1020
gap_y 0

lua_load allcombined.lua

TEXT
${image img/graphic_card.png -p 0,0 -s 30x30}
${offset 35}${font Good Times:size=12}${color Tan1}"""+GraphicCard[Language]+"""${color}${hr 2}${font}"""


#----------------------------------------------------
# ------------- Get cards and Monitor names ---------
#----------------------------------------------------

# is nvidia installed
IsNvidia_Xconfig_Installed=os.popen("which nvidia-xconfig").read()

IsScreen_Detected_VAL_LOG=os.popen("cat /var/log/Xorg.0.log | grep -E -i -w connected| tail -10 | cut -c 19- | sort | uniq | sed 's/.....................$//g' | cut -d: -f2-").read()

Detect_Via_Script=os.popen("sh detect_screen.sh").read().rstrip()
Detect_Via_Script=Detect_Via_Script.split('\n')


if Detect_Via_Script!="" and IsNvidia_Xconfig_Installed=="":
	Screen_Detected=[]
	for i in Detect_Via_Script:
		#i=i.split(':')
		#a=i[1]
		print (i)
		Screen_Detected.append(i)
	All_Screens_Detected='${color red} _${color}'.join(Screen_Detected)	



elif IsNvidia_Xconfig_Installed!="": # Yes it is installed
	Screen_Detected=[]
	Screen_Detection=os.popen("nvidia-xconfig --query-gpu-info | grep EDID").read()
	Screen_Detection=Screen_Detection.strip()
	Screen_Detection=Screen_Detection.split('\n')
	for i in Screen_Detection:
		i=i.split(':')
		a=i[1]
		print (a)
		Screen_Detected.append(a)
	All_Screens_Detected='${color red} _${color}'.join(Screen_Detected)		

	


elif IsScreen_Detected_VAL_LOG!="":
	Screen_Detected=os.popen("cat /var/log/Xorg.0.log | grep -E -i -w connected| tail -10 | cut -c 19- | sort | uniq | sed 's/.....................$//g' | cut -d: -f2-").read()
	try:
		IsScreen_Detected_VAL_LOG=IsScreen_Detected_VAL_LOG.strip()
	except:
		pass
	All_Screens_Detected=IsScreen_Detected_VAL_LOG.replace('\n','${color red} _${color}')

else:
	All_Screens_Detected=" N/A"


Display_Brand=ScreenDisplay[Language]+" :${alignr}"+str(All_Screens_Detected)





#----------------------------------------------------
# ------------- Find all the VGA cards --------------
#----------------------------------------------------

#Available_Cards=os.popen("cat lspci-v.txt | grep -i VGA").read().lower().rstrip()
Available_Cards=os.popen("lspci -v | grep -E -i 'VGA compatible controller|3D|Display'").read().lower().rstrip()
Available_Cards=Available_Cards.split('\n')

if DEBUG==1:
	Available_Cards=['00:00.0 Host bridge: Intel Corporation 2nd Generation Core Processor Family DRAM Controller (rev 09)','01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Whistler [Radeon HD 6730M/6770M/7690M XT] (rev ff) (prog-if ff)'] # DEBUG for INTEL+RADEON GPU cards
	Available_Cards=['01:00.0 VGA compatible controller: NVIDIA Corporation GK106 [GeForce GTX 660] (rev a1) (prog-if 00 [VGA controller])','02:00.0 VGA compatible controller: NVIDIA Corporation GK106 [GeForce GTX 780] (rev a1) (prog-if 00 [VGA controller])'] # DEBUG for Double NVIDIA GPU cards	
	g=len(Available_Cards)
if DEBUG==1:
	print (Available_Cards[0]) # DEBUG
	#print (Available_Cards[1]) # DEBUG
List_Of_Cards_ID=[]
for Card in range(int(len(Available_Cards))):
	List_Of_Cards_ID.append(Available_Cards[Card][:7])


#----------------------------------------------------
# ------------- Resolution --------------------------
#----------------------------------------------------

Resolutions=os.popen("xrandr | grep \* | awk '{print $1}'").read() 

Resolutions="${color red} _${color}".join(Resolutions.split())



#----------------------------------------------------
# ------------- Connector ---------------------------
#----------------------------------------------------

ConnectorToDisplay=os.popen("xrandr | grep 0+0 | awk '{print $1}'").read() 
ConnectorToDisplay="${color red} _${color} ".join(ConnectorToDisplay.split())







Height_conky=0
# ---------------------------------------------------------------------------

# #################### Loop for each graphic cards ##########################

# ---------------------------------------------------------------------------
Nvidia_Number=0
for ID in range(int(len(List_Of_Cards_ID))):



	#print (List_Of_Cards_ID[ID])
	Vendor=os.popen("lspci -s "+str(List_Of_Cards_ID[ID])).read().lower()
	if DEBUG==1:
		if ID==0:
			#Vendor="00:00.0 Host bridge: Intel Corporation 2nd Generation Core Processor Family DRAM Controller (rev 09)".lower() # DEBUG INTEL
			Vendor="01:00.0 VGA compatible controller: NVIDIA Corporation GK106 [GeForce GTX 660] (rev a1) (prog-if 00 [VGA controller])".lower() # DEBUG 1st NVIDIA
		if ID==1:
			#Vendor="01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Whistler [Radeon HD 6730M/6770M/7690M XT] (rev ff) (prog-if ff)".lower () # DEBUG AMD
			Vendor="01:00.0 VGA compatible controller: NVIDIA Corporation GK106 [GeForce GTX 660] (rev a1) (prog-if 00 [VGA controller])".lower () # DEBUG second nvidia			
	#Vendor=os.popen("cat lspci-mm.txt -s  | grep "+str(List_Of_Cards_ID[ID])).read().lower()

	# --------------------------------------------------
	# ------------- Card Name --------------------------
	# --------------------------------------------------
	#CardName=os.popen("LC_ALL=C lshw -class display | grep -i product").read() # find the cards
	CardName=os.popen("lspci -m -s "+str(List_Of_Cards_ID[ID])).read().rstrip()

	if DEBUG==1:
		if ID==0:
			#CardName="""00:02.0 "VGA compatible controller" "Intel Corporation" "2nd Generation Core Processor Family Integrated Graphics Controller" -r09 "Hewlett-Packard Company" "2nd Generation Core Processor Family Integrated Graphics Controller""" # DEBUG INTEL
			CardName="""01:00.0 "VGA compatible controller" "NVIDIA Corporation" "GK106 [GeForce GTX 660]" -ra1 "Gigabyte Technology Co., Ltd" "GK106 [GeForce GTX 660]""" # DEBUG 1st NVIDIA
		if ID==1:
			#CardName="""01:00.0 "VGA compatible controller" "Advanced Micro Devices, Inc. [AMD/ATI]" "Whistler [Radeon HD 6730M/6770M/7690M XT]" -rff -pff """ # DEBUG AMD
			CardName="""01:00.0 "VGA compatible controller" "NVIDIA Corporation" "GK106 [GeForce GTX 780]" -ra1 "Gigabyte Technology Co., Ltd" "GK106 [GeForce GTX 660]""" # DEBUG 2dn NVIDIA
	#CardName=os.popen("cat lspci-mm.txt -s  | grep "+str(List_Of_Cards_ID[ID])).read().rstrip()
	CardName=CardName.split('"')
	CardName=CardName[5]

	if CardName.lower().find('device') !=-1: # if the wrong name is detected, we use nvidia smi and device is found instead of the card name
		Is_Nvidia_SMI_Installed=os.popen("which nvidia-smi").read()
		if Is_Nvidia_SMI_Installed!="":
			CardName=os.popen("nvidia-smi --query-gpu=gpu_name --format=csv,noheader").read()
			CardName=os.popen("cat smi.txt").read() # DEBUG
			CardName=CardName.rstrip()
			CardName=CardName.split('\n')
			CardName=CardName[Nvidia_Number]

# -------------------------------------------------

# ################ A M D ##########################

# -------------------------------------------------

	
	if Vendor.find('amd') !=-1:


		# ------------- ADD logo  -------------
		LOGO="Ati_logo.png"
		PathToLOGO="${image img/"+LOGO+" -p 5,"+str(Height_conky+55)+" }"






		# ------------- Drivers --------------------------
		Kernel_Driver=os.popen("""LC_ALL=C lspci -nnk -v -s """+str(List_Of_Cards_ID[ID])+""" | grep driver""").read() 
		if DEBUG==1:
			Kernel_Driver="Kernel driver in use: radeon"
		if Kernel_Driver!="":
			Kernel_Driver=Kernel_Driver.rstrip()
			try:
				Kernel_Driver=Kernel_Driver.split(': ')
			except:
				pass
			try:
				Kernel_Driver=Kernel_Driver[1]
			except:
				pass
		else:
			Kernel_Driver="Unknown"
		#print (Kernel_Driver)
		# 
		# essayer d'avoir le nom des écran par nvidia-settings
		# 

		List = []
		Comment="#\n# -- Cardname "+str(ID+1)+" : "+CardName+"\n#\n" 
		#CardName=Lists_Of_Cards[Card].split('product:')[1]
		CardName="${color red}${font Ubuntu-Title:size=11}"+CardName+"${font}${color}"
		#Number_Of_Cores="${font}${color}${alignr}${exec nvidia-settings -q [gpu:"+str(ID)+"]/CUDACores -t} CUDA Cores"
		#Kernel_Driver=os.popen("nvidia-settings -q 0/NvidiaKernel_Driver -t").read().rstrip()
		Kernel_Driver="#\n# -- Driver \n${goto 80}Driver :${alignr}"""+Kernel_Driver
		#Speed_Of_Fan="${goto 80}"+FanSpeed[Language]+": ${alignr}  ${exec nvidia-settings -q [fan:"+str(ID)+"]/GPUCurrentFanSpeedRPM -t} RPM"
		Resolutions="#\n# -- Resolution \n${goto 80}"+DisplayResolution[Language]+": ${alignr} "+Resolutions	
		ConnectorToDisplay="#\n# -- Connection \n${goto 80}Connector: ${alignr} "+ConnectorToDisplay
		#Screen_Detected=ScreenDisplay[Language]+": ${alignr}"+Screen_Detected

		Separator="${color}${hr 1}"

		List.append(Comment)
		List.append(CardName+"\n")	
		List.append(Kernel_Driver+"\n")
		List.append(Resolutions+"\n")
		List.append(ConnectorToDisplay+"\n")
		List.append(Display_Brand+"\n")				
		#List.append(BackgroundImage)
		#List.append(Frequency_Text+"\n")
		#List.append(Frequency_Bar+"\n")	
		#List.append(Memory_Text+"\n")
		#List.append(Memory_Bar+"\n")	
		#List.append(Temperature_Text+"\n")
		#List.append(Temperature_Bar+"\n")	
		List.append(PathToLOGO)	
		List.append(Separator+"\n")	

		Radeon_Text=''.join(List)	
		Conky_Text.append(Radeon_Text)
		Height_conky=Height_conky+90
		#${goto 80}Driver :${alignr}"""+Kernel_Driver+"""
		#${goto 80}fanspeed :${execi 5 awk '{ value += $1 } END { printf "%.0f\n", value/2.55 }' /sys/class/drm/card0/device/hwmon/hwmon0/pwm1 }%

		#GPU Usage : ${execi 5 radeontop -d- -l1 | grep -o 'gpu [0-9]\{1,3\}' | cut -c 5-7 }%

		#Memory used / Installed : ${execi 5 radeontop -d- -l1 | grep -o 'vram [0-9]\{1,3\}' | cut -c 6-8 }% / """+InstalledVram+"""









	# ----------------------------------------------------

	# ############# N V I D I A ##########################

	# -----------------------------------------------------

	elif Vendor.find('nvidia') !=-1:

		LOGO="Nvidia_logo.png"
		PathToLOGO="${image img/"+LOGO+" -p 5,"+str(Height_conky+55)+" }"
		

		List = []
		Comment="#\n# Cardname "+str(ID+1)+" : "+CardName+"\n#\n" 
		#CardName=Lists_Of_Cards[Card].split('product:')[1]
		CardName="${color red}${font Ubuntu-Title:size=11}"+CardName+"${font}${color}"
		Is_Nivida_Driver_Installed=os.popen("which nvidia-settings").read()
		if Is_Nivida_Driver_Installed=="":
			Number_Of_Cores="${font}${alignr} Nvidia drivers not installed"
		else:
			Number_Of_Cores="${font}${alignr}${exec nvidia-settings -q [gpu:"+str(Nvidia_Number)+"]/CUDACores -t} CUDA Cores"
		
		
		# ------------- kernel Drivers --------------------------
		#Kernel_Driver=os.popen("""LC_ALL=C lspci -v -s $(lspci | grep ' VGA ' | cut -d" " -f 1) | grep driver""").read() 
		Kernel_Driver=os.popen("LC_ALL=C lspci -vnnk -s "+str(List_Of_Cards_ID[Nvidia_Number])+" | grep driver").read()
		if DEBUG==1:
			Kernel_Driver="	Kernel driver in use: i915"
		#Kernel_Driver=os.popen("cat lspci-nnk.txt | grep driver").read()
		#Kernel_Driver="Kernel driver in use: 915"
		if Kernel_Driver!="":
			Kernel_Driver=Kernel_Driver.rstrip()
			try:
				Kernel_Driver=Kernel_Driver.split(': ')
			except:
				pass
			try:
				Kernel_Driver=Kernel_Driver[1]
			except:
				pass
		else:
			Kernel_Driver="Unknown"
		#print (Kernel_Driver)
		
		if Is_Nivida_Driver_Installed=="":
			Driver_Version="${voffset 10}${goto 80}Nvidia drivers not installed"
			Speed_Of_Fan="${goto 80}"+FanSpeed[Language]+": ${alignr}  Nvidia drivers not installed"

		else:
			Speed_Of_Fan="${goto 80}"+FanSpeed[Language]+": ${alignr}  ${exec nvidia-settings -q [fan:"+str(ID)+"]/GPUCurrentFanSpeedRPM -t} RPM"

			Driver_Version=os.popen("nvidia-settings -q 0/NvidiaDriverVersion -t").read().rstrip()
			Driver_Version="#\n# -- Driver \n${voffset 10}${goto 80}Driver :${alignr}"""+Kernel_Driver+" - "+Driver_Version+"\n#"

		Resolutions="# --Resolution \n${goto 80}"+DisplayResolution[Language]+": ${alignr} "+Resolutions+"\n#"	
		ConnectorToDisplay="#\n# -- Connection \n${goto 80}Connector: ${alignr} "+ConnectorToDisplay+"\n#"
		Screen_Detected="#\n# -- Screen \n"+ScreenDisplay[Language]+": ${alignr}"+All_Screens_Detected+"\n#"
		# detect Screen Resolution
		#ScreenResolution=os.popen("nvidia-settings -q ScreenPosition -t").read()
		#ScreenResolution = ScreenResolution.replace(' ','').split(',')
		#Width=ScreenResolution[2].split('=')[1].rstrip()
		#Height=ScreenResolution[3].split('=')[1].rstrip()
		#RefreshRate=os.popen("nvidia-settings -q [dpy:1]/RefreshRate -t").read().rstrip()

		

		# ----------------------
		# Frequency bar + text
		# ----------------------
		if Is_Nivida_Driver_Installed=="":
			Frequency_Text="${font}Nvidia drivers not installed"
			Frequency_Bar=""
		else:
			Maximum_Frequency=os.popen("nvidia-settings -q all | grep -w GPUCurrentClockFreqs | grep gpu:"+str(Nvidia_Number)).read().strip()
			try:
				Maximum_Frequency=Maximum_Frequency.split(',')
				Maximum_Frequency=Maximum_Frequency[1]
				Maximum_Frequency=Maximum_Frequency[:-1]
			except:
				pass
			#Get_Current_Frequency=os.popen("nvidia-settings -q [gpu:"+str(Nvidia_Number)+"]/GPUCurrentClockFreqs | grep gpu | tr ',' "'\n'" | sed -n 2p | tr -d '.'").read()
			#nvidia-settings -q [gpu:0]/GPUCurrentClockFreqs | grep gpu | tr ',' '\n' | sed -n 2p | tr -d '.'

			Frequency_Text=Frequency[Language]+"${alignr}${exec nvidia-settings -q [gpu:"+str(Nvidia_Number)+"]/GPUCurrentClockFreqs | grep gpu | tr ',' '\\n' | sed -n 2p | tr -d '.' } / "+Maximum_Frequency
			Frequency_Bar='${lua gradbar {6,'+str(Height_conky+155)+', "${nvidia memfreq }" ,3004, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}	${image img/trans-bg240.png -p 3,'+str(Height_conky+150)+' -s 314x11}'
			Frequency_Bar_List=[]
			#${lua gradbar {6, 190, "${nvidia memfreq}" ,3004, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,136 -s 314x11}
			F1="${lua gradbar {6,"+str(Height_conky+155)+", "
			F2='"${exec nvidia-settings -q [gpu:'
			F3=str(Nvidia_Number)
			F4="]/GPUCurrentClockFreqs | grep gpu | tr ',' '\\n' | sed -n 2p | tr -d '.' }"+'"'
			F5=","+Maximum_Frequency+" , 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,"	
			F6=str(Height_conky+150)
			F7=' -s 314x11}'
			Frequency_Bar_List.append(F1)
			Frequency_Bar_List.append(F2)	
			Frequency_Bar_List.append(F3)
			Frequency_Bar_List.append(F4)
			Frequency_Bar_List.append(F5)
			Frequency_Bar_List.append(F6)
			Frequency_Bar_List.append(F7)
			Frequency_Bar=''.join(Frequency_Bar_List)




		# ----------------------
		# Memory bar + text
		# ----------------------
		if Is_Nivida_Driver_Installed=="":
			Memory_Text="${font}Nvidia drivers not installed"
			Memory_Bar=""		
		else:
			Maximum_Memory=os.popen("nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory | grep gpu ").read().rstrip()
			try:
				Maximum_Memory=Maximum_Memory.split('): ')

				Maximum_Memory=Maximum_Memory[1]
				Maximum_Memory=Maximum_Memory[:-1]

			except:
				pass



			Memory_Text=Ram[Language]+"${alignr}${exec nvidia-settings -q [gpu:"+str(Nvidia_Number)+"]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:"+str(Nvidia_Number)+"]/TotalDedicatedGPUMemory -t} MiB "
			if DEBUG==1:
				Memory_Text=Ram[Language]+"${alignr}${exec nvidia-settings -q [gpu:"+str("0")+"]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:"+str("0")+"]/TotalDedicatedGPUMemory -t} MiB " # DEBUG
			Memory_Bar_List=[]
			M1="${lua gradbar {6, "+str(Height_conky+185)+" ,"
			M2='"${exec nvidia-settings -q [gpu:'
			M3=str(Nvidia_Number)
			if DEBUG==1:
				M3=str("0")		 #DEBUG
			M4=']/UsedDedicatedGPUMemory -t}"'
			M5=","+Maximum_Memory+" , 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,"
			M6=str(Height_conky+180)
			M7=' -s 314x11}'
			Memory_Bar_List.append(M1)
			Memory_Bar_List.append(M2)	
			Memory_Bar_List.append(M3)
			Memory_Bar_List.append(M4)
			Memory_Bar_List.append(M5)
			Memory_Bar_List.append(M6)
			Memory_Bar_List.append(M7)		
			Memory_Bar=''.join(Memory_Bar_List)
			#Memory_Bar="${lua gradbar {6, "+str(Height_conky+70)+" , "${exec nvidia-settings -q [gpu:"+str(Card)+ " # ]/UsedDedicatedGPUMemory -t}" ,1996, 105,2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,"+str(Height_conky+65)+" -s 314x11}"
			#Memory_Bar="${lua gradbar {6, "+str(Height_conky+70)+", "${exec nvidia-settings -q [gpu:"+str(Card)+"]/UsedDedicatedGPUMemory -t}" ,1996, 105,2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,"+str(Height_conky+65)+" -s 314x11}"
			#${lua gradbar {6, 190, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,1996 , 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,186 -s 314x11}


			#${lua gradbar {6,160, "${nvidia memfreq}" ,3004, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}	${image img/trans-bg240.png -p 3,160 -s 314x11}
			#Mémoire vive${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB${image img/trans-bg240.png -p 3,166 -s 314x11} 


			#${lua gradbar {6, 170, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,"""+TotalMemory+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,166 -s 314x11}
			#"""+Temperature[Language]+""" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C
			#${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}


			"""# detect Connetion type
			ConnectorToDisplay=os.popen("nvidia-settings -q XineramaInfoOrder -t").read().rstrip()
			if ConnectorToDisplay=="":
				ConnectorToDisplay="N/A"
			Connector_Type="${goto 80}Connector :${alignr}"+ConnectorToDisplay+"\n"
			"""
			
			# ----------------------
			# temperature bar + text
			# ----------------------
		if Is_Nivida_Driver_Installed=="":
			Temperature_Text="${font}Nvidia drivers not installed"
			Temperature_Bar=""
		else:		
			Temperature_Text=Temperature[Language]+" ${alignr} ${exec nvidia-settings -q [thermalsensor:"+str(Nvidia_Number)+"]/ThermalSensorReading -t} °C"
			Temperature_Bar_List=[]
			T1="${lua gradbar {6, "+str(Height_conky+215)+" ,"
			T2='"${exec nvidia-settings -q [thermalsensor:'
			T3=str(Nvidia_Number)
			if DEBUG==1:
				T3=str("0")		# DEBUG
			T4=']/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,'
			T5=str(Height_conky+210)
			T6=" -s 314x11}"
			Temperature_Bar_List.append(T1)
			Temperature_Bar_List.append(T2)
			Temperature_Bar_List.append(T3)	
			Temperature_Bar_List.append(T4)
			Temperature_Bar_List.append(T5)
			Temperature_Bar_List.append(T6)	
			Temperature_Bar=''.join(Temperature_Bar_List)			
			#${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}

			# ADD logo
			# PathToLOGO="${image img/"+LOGO+" -p 5,"+str(Height_conky-55)+" }"

			# separate the cards with a line
		Separator="${color}${hr 1}"



		List.append(Comment)
		List.append(CardName)	
		List.append(Number_Of_Cores+"\n")
		List.append(Driver_Version+"\n")
		List.append(Resolutions+"\n")
		List.append(ConnectorToDisplay+"\n")
		List.append(Speed_Of_Fan+"\n")
		#List.append(Screen_Detected+"\n")			
		List.append(Display_Brand+"\n")

		#List.append(BackgroundImage)
		List.append(Frequency_Text+"\n")
		List.append(Frequency_Bar+"\n")	
		List.append(Memory_Text+"\n")
		List.append(Memory_Bar+"\n")	
		List.append(Temperature_Text+"\n")
		List.append(Temperature_Bar+"\n")	
		List.append(PathToLOGO)	
		List.append(Separator+"\n")	



		Nvidia_Text=''.join(List)	
		Conky_Text.append(Nvidia_Text)
		Height_conky=Height_conky+207
		Nvidia_Number=Nvidia_Number+1
	


				#reste="""+Ram[Language]+"""${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB 
				#${lua gradbar {6, 170, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,"""+TotalMemory+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,166 -s 314x11}
				#"""+Temperature[Language]+""" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C
				#${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}


				#    CpuName=""+Cpu[Language]+" "+str(Cores+1)
			#	${color red}${font Ubuntu-Title:size=11}"""+CardName+"""${font}${color}${alignr}${exec nvidia-settings -q [gpu:0]/CUDACores -t} CUDA Cores
			#	${voffset 10}${goto 80}"""+FanSpeed[Language]+""": ${alignr}  ${exec nvidia-settings -q [fan:0]/GPUCurrentFanSpeedRPM -t} """+RPM+"""
			#	${goto 80}"""+ScreenDisplay[Language]+""" :${alignr}"""+Width+""" x """+Height+"""-"""+RefreshRate+"""
			#	${goto 80}Connector :${alignr}"""+ConnectorToDisplay+"""
			#	${goto 80}Driver :${alignr}"""+Kernel_Driver+"""
			#	"""+Frequency[Language]+"""$alignr ${nvidia memfreq} / """+Maximum_Frequency+""" Mhz
			#	${lua gradbar {6, 140, "${nvidia memfreq}" ,"""+Maximum_Frequency+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,136 -s 314x11}
			#	"""+Ram[Language]+"""${alignr}${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t} / ${exec nvidia-settings -q [gpu:0]/TotalDedicatedGPUMemory -t} MiB 
			#	${lua gradbar {6, 170, "${exec nvidia-settings -q [gpu:0]/UsedDedicatedGPUMemory -t}" ,"""+TotalMemory+""", 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,166 -s 314x11}
			#	"""+Temperature[Language]+""" ${alignr} ${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t} °C
			#	${lua gradbar {6, 200, "${exec nvidia-settings -q [thermalsensor:0]/ThermalSensorReading -t}" , 85, 105, 2, 10, 1, 0xFFFFFF, 0.25, 0x00FF00, 1, 0xFFFF00, 1, 0xFF0000, 1}}${image img/trans-bg240.png -p 3,196 -s 314x11}
			# 
			








	# -----------------------------------------------------

	# ################ I N T E L ##########################

	# ------------------------------------------------------


	elif Vendor.find('intel') !=-1:

		LOGO="Intel_HD_logo.png"
		PathToLOGO="${image img/"+LOGO+" -p 5,"+str(Height_conky+55)+" }"



		# ------------- kernel Drivers --------------------------
		#Kernel_Driver=os.popen("""LC_ALL=C lspci -v -s $(lspci | grep ' VGA ' | cut -d" " -f 1) | grep driver""").read() 
		Kernel_Driver=os.popen("LC_ALL=C lspci -vnnk -s "+str(List_Of_Cards_ID[ID])+" | grep driver").read()
		if DEBUG==1:
			Kernel_Driver="	Kernel driver in use: i915"
		#Kernel_Driver=os.popen("cat lspci-nnk.txt | grep driver").read()
		#Kernel_Driver="Kernel driver in use: 915"
		if Kernel_Driver!="":
			Kernel_Driver=Kernel_Driver.rstrip()
			try:
				Kernel_Driver=Kernel_Driver.split(': ')
			except:
				pass
			try:
				Kernel_Driver=Kernel_Driver[1]
			except:
				pass
		else:
			Kernel_Driver="Unknown"
		#print (Kernel_Driver)


		List = []
		Comment="#\n# Cardname "+str(ID+1)+" : "+CardName+"\n#\n" 
		#CardName=Lists_Of_Cards[Card].split('product:')[1]
		CardName="${color red}${font Ubuntu-Title:size=11}"+CardName+"${font}${color}"
		#Number_Of_Cores="${font}${color}${alignr}${exec nvidia-settings -q [gpu:"+str(ID)+"]/CUDACores -t} CUDA Cores"
		#Kernel_Driver=os.popen("nvidia-settings -q 0/NvidiaKernel_Driver -t").read().rstrip()
		Kernel_Driver="${goto 80}Driver :${alignr}"""+Kernel_Driver
		#Speed_Of_Fan="${goto 80}"+FanSpeed[Language]+": ${alignr}  ${exec nvidia-settings -q [fan:"+str(ID)+"]/GPUCurrentFanSpeedRPM -t} RPM"
		Resolutions="${goto 80}"+DisplayResolution[Language]+": ${alignr} "+Resolutions	
		ConnectorToDisplay="${goto 80}Connector: ${alignr} "+ConnectorToDisplay
		#Screen_Detected=ScreenDisplay[Language]+": ${alignr}"+Screen_Detected

		Separator="${color}${hr 1}"

		List.append(Comment)
		List.append(CardName+"\n")	
		List.append(Kernel_Driver+"\n")
		List.append(Resolutions+"\n")
		List.append(ConnectorToDisplay+"\n")
		List.append(Display_Brand+"\n")				
		#List.append(BackgroundImage)
		#List.append(Frequency_Text+"\n")
		#List.append(Frequency_Bar+"\n")	
		#List.append(Memory_Text+"\n")
		#List.append(Memory_Bar+"\n")	
		#List.append(Temperature_Text+"\n")
		#List.append(Temperature_Bar+"\n")	
		List.append(PathToLOGO)	
		List.append(Separator+"\n")	

		Intel_Text=''.join(List)	
		Conky_Text.append(Intel_Text)
		Height_conky=Height_conky+95

Total_Conky_Text=''.join(Conky_Text)
#total=header+txt01+"\n"+Total_Connector+Total_Conky_Text
total=header+txt01+"\n"+Total_Conky_Text
writefile( total) 
#"""+Total_Connector+"""${color red}${font Ubuntu-Title:size=11}
