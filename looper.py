import datetime
from datetime import timedelta, date,datetime
import downloader
import time
import os

def countDown(seconds,motife = "para baixar dados do IBGE e NASA"):
	start1 = time.perf_counter()
	while(seconds>0):
		hour = str(seconds//3600).zfill(2)
		minutes = str((seconds%3600)//60).zfill(2)
		sec = str(seconds%60).zfill(2)
		result = hour + ":" + minutes  +":" + sec + "|" + motife
		os.system('cls' if os.name == 'nt' else 'clear')
		print(result)
		delay1 = time.perf_counter() -start1
		if(seconds<1):
			if(delay1<seconds):
				time.sleep(seconds-delay1)
			seconds = 0
		else:
			if(delay1<1):
				time.sleep(1-delay1)
			seconds = seconds -1
			start1 = time.perf_counter()

downloader.downloadTodayData(date.today())
now = datetime.now()
later = datetime(now.year,now.month,now.day+1,1,0,0)
diff = later - now
if (diff.days == 1):
	time.sleep(24*3600)
elif (later >= now):
	# print("now: " + str(now.hour) +":"+ str(now.minute)+":"+ str(now.second))
	# print("later: " + str(later.hour) +":"+ str(later.minute)+ ":"+str(later.second))
	# print("DIFF: " + str(diff.seconds) +"=>" + str(int(diff.seconds/3600)) +":"+ str(int((diff.seconds%3600)/60)) +":"+ str(int((diff.seconds%60))))
	countDown(diff.seconds)

while(True):
	downloader.downloadTodayData(date.today())
	countDown(24*3600 + 1)


