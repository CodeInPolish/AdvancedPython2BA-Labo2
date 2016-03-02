# AdvancedPython2BA-Labo2

/!\ Windows : il faut obligatoirement avoir Python dans ses variables d'environnement

Lancer ServerApp.py sur une machine qui servira de serveur 


Lancer ClientApp.py sur la machine qui veut se connecter au Chat avec la commande

"python ClientApp.py server_name server_port pseudo"

server_name = nom de la machine sur laquelle le serveur est hebergé (Ex: "DESKTOP-UPJ8DL0" chez moi)
server_port = port du serveur (5001 par défaut)
pseudo = votre pseudo (optionnel)


Mettre son pseudo

Commandes dans ClientApp.py:
	/users : liste les clients connectés
	/join user : Demander à user une connexion chat
	/accept user : Accepte la requête de demande de connexion chat avec user (une nouvelle fenêtre chat va s'ouvrir)
	/exit : Ferme la connexion entre le client et le serveur pour quitter l'appli

Commandes dans chat:
	/exit : Ferme le chat


Il manque encore plein de trucs : 
	- Le port P2P n'est pas random (il est hardcoded pour effectuer les test)
	- Pas de gestion d'erreur