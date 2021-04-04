import datetime
import downloader
import os

exitFlag = False
minimalYear = 2010
todayDate =  datetime.date.today()
todayDateStr = str(todayDate.day).zfill(2) +"/"+str(todayDate.month).zfill(2) +"/"+ str(todayDate.year)
state = 0

def mainMenu():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("=== Downloads das observações GNSS das estações da RBMC e das efemérides precisas do IGS ===\n")
	print("[1]-Baixar dados desde 01/01/" + str(minimalYear))
	print("[2]-Baixar dados desde uma data específica")
	print("[3]-Baixar dados de hoje - " +todayDateStr)
	print("[4]-Sair \n")
	choice = input("Favor digitar o número da opção desejada: ")
	if not choice.isnumeric() or int(choice)< 1 or int(choice)>4:
		choice = 0
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Opção Inválida, favor tentar novamente.")
		input("Pressione enter para continuar.")
	else:
		choice = int(choice)
	return choice

def minimalYearMenu():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Certeza que voce deseja baixar todos os dados desde 01/01/"+ str(minimalYear) + "?")
	choice = input("Sim(S) ou Não(N): ")
	if ("S" in choice.upper()):
		downloader.downloadMinimalYear(minimalYear,todayDate)
	elif ("N" in choice.upper()):
		pass
	else:
		input("Opção invalida.")
		input("Pressione enter para continuar.")

def rangeYearMenu():
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Favor informar a data no formato dd/mm/aaaa. Ex: 31/01/2020")
	dateSrt = input()
	dateSplit = dateSrt.split("/")
	if(len(dateSplit) != 3):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Data não reconhecida, favor seguir a formatação informada. Ex: 17/05/2014")
		input("Pressione enter para continuar.")
	else:
		day = int(dateSplit[0])
		month = int(dateSplit[1])
		year = int(dateSplit[2])
		try:
			date = datetime.date(year,month,day)
			if(date < datetime.date(int(minimalYear),1,1)):
				os.system('cls' if os.name == 'nt' else 'clear')
				print("Data informada é menor do que o limite - 01/01/" + str(minimalYear))
				input("Pressione enter para continuar.")
			elif(date>todayDate):
				os.system('cls' if os.name == 'nt' else 'clear')
				print("Data informada é posterior a data de hoje")
				input("Pressione enter para continuar.")
			else:
				downloader.downloadRangeYear(date,todayDate)
		except:
			os.system('cls' if os.name == 'nt' else 'clear')
			print("Data invalida.")
			input("Pressione enter para continuar.")

while(not exitFlag):
	if (state == 0):
		choice = mainMenu()
		state = choice
	elif(state == 1):
		minimalYearMenu()
		state = 0
	elif(state == 2):
		rangeYearMenu()
		state = 0
	elif(state == 3):
		downloader.downloadTodayData(todayDate)
		state = 0
	elif(state == 4):
		os.system('cls' if os.name == 'nt' else 'clear')
		exitFlag = True
	else:
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Erro no menu")
		exitFlag = True
