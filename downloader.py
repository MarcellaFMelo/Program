import datetime
from datetime import timedelta, date
import wget
import time
import os
from zipfile import ZipFile
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

allStationsIBGE = ["alma","alar","amco","amcr","amte","amua","aplj","apma","babj","babr","bail","bait","bapa","batf","bavc","braz","ceeu","cefe","eft","cesb","chpi","coru","cruz","cuib","each","eesc","gogy","goja","gour","gva1","ifsc","ilha","imbt","impz","itai","jamg","maba","mabs","mgbh","mgin","mgjf","mgjp","mgla","mgmc","mgmt","mgrp","mgto","mgub","mgv1","msaq","msbl","msdr","msjr","msmj","msmn","msnv","mspm","mspp","mtca","mtga","mtit","mtji","mtla","mtle","mtsc","mtsr","naus","paar","pait","pasm","pbcg","pbjp","pbpt","peaf","pepe","perc","picr","pisr","pitn","poal","poli","ppte","prgu","prma","prur","riob","rjcg","rjni","rjva","rnmo","rnna","roji","rosa","rsal","rscl","rspe","rspf","rssl","salu","savo","scaq","scca","scch","scfl","scla","seaj","sjrp","sjsp","smar","spar","spbo","spbp","spc1","spdr","spfe","spfr","spja","spli","spor","sps1","sptu","ssa1","togu","topl","uba1","ufpr","vico"]
# allStationsIBGE = ["alma"]
driver = None

def initSoup():
	global driver
	profile = webdriver.FirefoxProfile()
	profile.set_preference('browser.download.folderList', 2) # custom location
	profile.set_preference('browser.download.manager.showWhenStarting', False)
	profile.set_preference('browser.download.dir', os.getcwd())
	profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
	profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-compress')
	driver = webdriver.Firefox(profile)
	driver.get("https://urs.earthdata.nasa.gov")
	usernameInput = driver.find_element_by_id("username")
	usernameInput.send_keys("scrapperWorker1")
	passwordInput = driver.find_element_by_id("password")
	passwordInput.send_keys("Qwertyuiop123")
	loginButton = driver.find_element_by_class_name("eui-btn--round")
	loginButton.click()
	time.sleep(2)
	driver.get("https://cddis.nasa.gov/archive/gnss/products/")
	delay = 60 # seconds
	try:
		myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'parDirText')))
	except TimeoutException:
		print("Site indisponível")
	time.sleep(5)


def downloadNASA(URL,filename,place):
	driver.execute_script("window.open('"+ URL +"');")
	time.sleep(5)
	if (len(driver.window_handles)<=1):
		time.sleep(10)
		#after Download
		downloadPath = os.getcwd()
		downloadPath =  downloadPath + "/" + filename
		os.replace(downloadPath, place + "/" + filename)
	else:
		driver.switch_to.window(driver.window_handles[1])
		driver.close()
		driver.switch_to.window(driver.window_handles[0])

def calculateGPSWeek(selectedDate):
	epoch = date(1980, 1, 6)
	epochMonday = epoch - timedelta(((epoch.weekday()+1)%7)) 
	todayMonday = selectedDate - timedelta(((selectedDate.weekday()+1)%7))
	noWeeks = ((todayMonday - epochMonday).days) // 7
	return int(noWeeks)

def daterange(start_date, end_date):
	for n in range(int((end_date - start_date).days)):
		yield start_date + timedelta(n)

def downloadMinimalYear(minimalYear,todayDate):
	todayDateStr = str(todayDate.day).zfill(2) +"/"+str(todayDate.month).zfill(2) +"/"+ str(todayDate.year)
	print("downloadMinimalYear")
	print("01/01/"+str(minimalYear)+" - "+ todayDateStr)
	pastDate = datetime.date(minimalYear,1,1)
	downloadRangeYear(pastDate,todayDate)

def downloadTodayData(todayDate):
	# todayDateStr = str(todayDate.day).zfill(2) +"/"+str(todayDate.month).zfill(2) +"/"+ str(todayDate.year)
	# print("downloadTodayData")
	# print(todayDateStr)
	downloadRangeYear(todayDate,todayDate)

def downloadRangeYear(pastDate,todayDate):
	initSoup()
	pastDate = pastDate - timedelta(1)
	pastDateStr = str(pastDate.day).zfill(2) +"/"+str(pastDate.month).zfill(2) +"/"+ str(pastDate.year)
	if(pastDate == todayDate - timedelta(1)):
		print("Download de ontem: "+ pastDateStr)
	else:
		todayDateStr = str(todayDate.day).zfill(2) +"/"+str(todayDate.month).zfill(2) +"/"+ str(todayDate.year)
		print("Download de Periodo: "+ pastDateStr + " - " + todayDateStr)
	if(not os.path.exists('Data')):
		try:
			os.mkdir("Data")
		except OSError:
			print ("Creation of the directory %s failed" % path)
			return
	rootPath = os.getcwd() + "/Data"
	for iterateDate in daterange(pastDate,todayDate):
		dateOfYear = iterateDate.timetuple().tm_yday
		weekGPS = calculateGPSWeek(iterateDate)
		dateOfWeek = (iterateDate.weekday() + 1) %7
		iterateYearPath = rootPath +"/"+str(iterateDate.year)
		iterateMonthPath = iterateYearPath +"/"+str(iterateDate.month).zfill(2)
		iterateDayPath = iterateMonthPath +"/"+str(iterateDate.day).zfill(2)
		nasaPath = iterateDayPath +"/NASA"
		ibgePath = iterateDayPath +"/IBGE"
		if(not os.path.exists(iterateYearPath)):
			try:
				os.mkdir(iterateYearPath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return
		if(not os.path.exists(iterateMonthPath)):
			try:
				os.mkdir(iterateMonthPath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return
		if(not os.path.exists(iterateDayPath)):
			try:
				os.mkdir(iterateDayPath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return
		if(not os.path.exists(nasaPath)):
			try:
				os.mkdir(nasaPath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return		
		if(not os.path.exists(ibgePath)):
			try:
				os.mkdir(ibgePath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return
		#download via wget by ibge
		for station in allStationsIBGE:
			stationPath = ibgePath + "/" + station
			if(not os.path.exists(stationPath)):
				try:
					os.mkdir(stationPath)
				except OSError:
					print ("Creation of the directory %s failed" % path)
					return
			downloadIBGEurl = "https://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/" + \
								str(iterateDate.year)+"/" + str(dateOfYear).zfill(3) +"/" + station + str(dateOfYear).zfill(3) + "1.zip"
			try:
				# print(downloadIBGEurl)
				# print(stationPath)
				# input()
				wget.download(downloadIBGEurl,stationPath)
				filename = station + str(dateOfYear).zfill(3) + "1.zip"
				# with ZipFile(filename, 'r') as zipObj:
				# 	# Extract all the contents of zip file in current directory
				# 	zipObj.extractall()
			except:
				pass
		#download NASA
		IGSpath = nasaPath + "/igs"
		if(not os.path.exists(IGSpath)):
			try:
				os.mkdir(IGSpath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return
		IGLpath = nasaPath + "/igl"
		if(not os.path.exists(IGLpath)):
			try:
				os.mkdir(IGLpath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return
		IGRpath = nasaPath + "/igr"
		if(not os.path.exists(IGRpath)):
			try:
				os.mkdir(IGRpath)
			except OSError:
				print ("Creation of the directory %s failed" % path)
				return
		filename = "igs" + str(weekGPS) + str(dateOfWeek) + ".sp3.Z"
		downloadNASAurlIGS ="https://cddis.nasa.gov/archive/gnss/products/"+ str(weekGPS) +"/" + filename
		try:
			# print(downloadNASAurlIGS)
			# input()
			downloadNASA(downloadNASAurlIGS,filename,IGSpath)
		except:
			pass
		filename = "igl" + str(weekGPS) + str(dateOfWeek) + ".sp3.Z"
		downloadNASAurlIGL ="https://cddis.nasa.gov/archive/gnss/products/"+ str(weekGPS) +"/" + filename
		try:
			# print(downloadNASAurlIGL)
			# input()
			downloadNASA(downloadNASAurlIGL,filename,IGLpath)
		except:
			pass
		filename = "igr" + str(weekGPS) + str(dateOfWeek) + ".sp3.Z"
		downloadNASAurlIGR ="https://cddis.nasa.gov/archive/gnss/products/"+ str(weekGPS) +"/" + filename
		try:
			downloadNASA(downloadNASAurlIGR,filename,IGRpath)
		except:
			pass
	driver.close()

if __name__ == "__main__":
	allStationsIBGE =[]
	downloadRangeYear(date.today() - timedelta(7),date.today())
	
