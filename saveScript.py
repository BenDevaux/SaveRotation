"""
Auteur : Benjamin Devaux
Version : 1.0
Date : 13/12/2021
Script de sauvegarde du serveur wordpress. Dump BDD, phpFiles, apache.

Codes retours :
0 : L action s est bien deroulee
1 : Le fichier de configuration n'existe pas
2 : Il manque une section ou une variable dans le fichier de configuration
3 : Dump non realise
4 : Archive non realisee
5 : Fichier pas envoye en FTP
6 : Script de rotation non effectue

Fichier de configuration par defaut : scriptConf.ini
"""

import os
import sys
import time
import datetime
import dateutil.relativedelta
import logging
from ftplib import FTP
import ConfigParser

#Definition des variables
dumpFilePath = 'dumpBDD.sql'
logFilePath = "saveLog.log"
confFilePath = "scriptConf.ini"

#Toutes les informations a verifier dans le fichier de conf sont recuperees
section1 = 'BDD'
section2 = 'SAVE'
section3 = 'FTP'
section4 = 'MSG'

confVar1 = ['user', 'mdp', 'name']
confVar2 = ['apache', 'wordpress']
confVar3 = ['host', 'user', 'mdp', 'maxFilesNumber']
confVar4 = ['MSG1', 'MSG2' ,'MSG3', 'MSG4', 'MSG5', 'MSG6', 'MSG7', 'MSG8', 'MSG9']

sectionList = [section1, section2, section3, section4]
confVarList = [confVar1, confVar2, confVar3, confVar4]


#LOG
logging.basicConfig(filename=logFilePath, format='%(asctime)s %(levelname)s : %(message)s', encoding='utf-8', level=logging.DEBUG)

#Verification du nombre d'argument pour assigner un fichier de configuration
if len(sys.argv) > 1:
	configFile = str(sys.argv[1])
else:
	configFile = confFilePath

#Verification que le fichier de configuration existe
if os.path.isfile(configFile) is False:
	print("le fichier de conf n'existe pas")
	logging.error("le fichier de configuration n'existe pas")
	sys.exit(1)

#Utilisation du fichier de configuration
config = ConfigParser.ConfigParser()
config.read(configFile)

#Creation d'une fonction de verification du contenu du fichier de configuration
def checkConfig(section, confVar):
	if config.has_section(section) is False:
		logging.error("la section %s n'existe pas dans le fichier de configuration %s"%(section, configFile))
		sys.exit(2)
	for variable in confVar:
		if config.has_option(section, variable) is False:
			logging.error("la variable %s n'existe pas dans la section %s du fichier de configuration %s"%(variable, section, configFile))
			sys.exit(2)




#Utilisation de la fonction de verification du contenu du fichier de configuration
for section, variable in zip(sectionList, confVarList):
	checkConfig(section, variable)
logging.info("Les informations sont bien presentes dans le fichier de configuration")

#Les informations du fichier de conf sont mises dans des variables
BDDuser = config.get('BDD', 'user')
BDDmdp = config.get('BDD', 'mdp')
BDDname = config.get('BDD', 'name')

apacheFiles = config.get('SAVE', 'apache')
wpFiles = config.get('SAVE', 'wordpress')

ftpHost = config.get('FTP', 'host')
ftpUser = config.get('FTP', 'user')
ftpMdp = config.get('FTP', 'mdp')

#Creation du dump de la BDD
logging.info(config.get('MSG', 'MSG1'))
dumpBDD = os.system("mysqldump -u%s  -p%s %s > %s"%(BDDuser, BDDmdp, BDDname, dumpFilePath))

#Verification de la bonne realisation du dump
exitCode = os.WEXITSTATUS(dumpBDD)

#Si le dump ne se realise pas, le script s'arrete
if int(exitCode) > 0:
	logging.error(config.get('MSG', 'MSG2'))
	sys.exit(3)

logging.info(config.get('MSG', 'MSG3'))
#Creation d'une archive
timestr = time.strftime("%Y%m%d")
logging.info(config.get('MSG', 'MSG4') + timestr) 
archiveTar = os.system("tar zcvf %s.tar.gz %s %s %s " %(timestr,apacheFiles,wpFiles,dumpFilePath))
secTest = os.WEXITSTATUS(archiveTar)

if int(secTest) > 0:
	logging.error(config.get('MSG', 'MSG5'))
	sys.exit(4)
logging.info(config.get('MSG', 'MSG6'))

#Connexion FTP
ftp = FTP(ftpHost, ftpUser, ftpMdp)
ftp.cwd('files')

#Envoie du fichier en FTP
logging.info(config.get('MSG', 'MSG7'))
f = open('%s.tar.gz'%timestr, 'rb')
storFile = ftp.storbinary('STOR %s.tar.gz'%timestr, f)
f.close()

if storFile == "226 Transfer complete.":
	logging.info(config.get('MSG','MSG8'))
	rotationScript = 'python rotationScript.py ' + configFile
	execRotaScript = os.system(rotationScript)
	execTest = os.WEXITSTATUS(execRotaScript)
	if int(execTest) > 0:
		logging.error("le script de rotation ne s'est pas correctement execute")
		sys.exit(6)
	else:
		logging.info("La sauvegarde s'est bien deroulee")
		sys.exit(0)
else:
	logging.error(config.get('MSG', 'MSG9'))
	sys.exit(5)
