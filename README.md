# SaveRotation

Script de sauvegarde et rotation de sauvegarde réalisé dans le cadre du projet n°9 de ma formation Administrateur Infrastructure et Cloud

# Lancement du script
Ce script prend pour premier argument un fichier de configuration. Ce fichier doit respecter les sections présentes dans le fichier de configuration exemple. Si aucun argument n'est donné le script se lancera avec le fichier de configuration exemple.

# Fichier de configuration

Ce fichier de configuration doit contenir certaines données afin que le script s'exécute correctement. Dans le cas où une donnée venait à manquer le script ne s'exécutera pas et renverra une message d'erreur personnalisé indiquant la section ou la variable manquante.

Ce fichier de configuration a besoin des données suivantes :

[BDD]

user = 

mdp =

name =


[SAVE]

apache = 

wordpress =

[FTP]

host =

user =

mdp =

mawFilesNumber=

[MSG]

MSG1 =

MSG2 =

MSG3 =

MSG4 =

MSG5 =

MSG6 =

MSG7 =

MSG8 =

MSG9 = 


# Script de sauvegarde 
Ce script va créer un dump de la base de donnée renseignée dans le fichier de configuration puis l'envoyer via FTP. Une fois le fichier envoyé le script de rotation se lance.

# Script de rotation
Le but du script de rotation de sauvegarde est d'empêcher une surcharge de fichier sur le serveur de sauvegarde. Les fichiers de sauvegardes ayant pour nom leur date de création le script de rotation va comparer cette date à la date du jour. Le script va ensuite compter le nombre de fichiers de sauvegarde présents dans le dossier. Si ce nombre est supérieur au nombre de fichiers maximum défini dans le fichier de configuration (maxFilesNumber) ET que le fichier le plus ancien date de plus d'un mois alors ce dernier sera supprimé afin de libérer de la place.
Cette méthode permet de garder quelques sauvegardes en cas de rollback à une date donnée nécessaire tout en empêchant d'être surchargé de fichiers de sauvegarde. 
