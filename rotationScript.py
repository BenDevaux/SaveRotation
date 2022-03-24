"""
Auteur : Benjamin Devaux
Version : 1.0
Date : 13/12/2021

Script de rotation de sauvegarde (est lance par le script saveScript.py)

Codes retours :
0 : Script execute avec succes
1 : Le fichier de configuration n'existe pas

"""

from ftplib import FTP
from dateutil import parser
import sys
import time
import datetime
import dateutil.relativedelta
import logging
import ConfigParser
import os

#Definition des variables

logFilePath = "saveLog.log"
ftpDir = 'files'

#LOG
logging.basicConfig(filename=logFilePath, format='%(asctime)s %(levelname)s : %(message)s', encodeing='utf-8', level=logging.DEBUG)


if len(sys.argv) != 2:
	logging.error("Le fichier de configuration n'a pas ete defini")
	sys.exit(1)

configFile = str(sys.argv[1])

if os.path.isfile(configFile) is False:
	logging.error("le fichier de configuration n'existe pas")
	sys.exit(1)

config = ConfigParser.ConfigParser()
config.read(configFile)


#Configuration
ftpHost = config.get('FTP', 'host')
ftpUser = config.get('FTP', 'user')
ftpMdp = config.get('FTP', 'mdp')
maxFilesNumber = config.get('FTP', 'maxFilesNumber')

ftp = FTP(ftpHost, ftpUser, ftpMdp)
ftp.cwd(ftpDir)

filesList = ftp.nlst("/%s/"%ftpDir)
filesNumber = len(filesList)

#Calcul de la date de suppression des archives
timestr = time.strftime("%Y%m%d")
actualTime = datetime.datetime.strptime(timestr, "%Y%m%d")
rmTime = actualTime - dateutil.relativedelta.relativedelta(months=1)


for filename in filesList:
	filesFTP = ftp.nlst("/%s"%ftpDir)
	filesNumber = len(filesFTP)
	creationDate = filename[7:15]
	creationDate = parser.parse(creationDate)

	if creationDate < rmTime and filesNumber > maxFilesNumber:
		ftp.delete(filename)
		logging.info("Suppression du fichier %s" %filename)
	else:
		logging.info("Fichier %s non supprime" %filename)
logging.info("La rotation des sauvegarde s'est bien effectuee")
sys.exit(0)
