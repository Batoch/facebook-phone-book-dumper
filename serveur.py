import socket
import select

hote = ''
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True
clients_connectes = []
with open("annuaire.txt", "r") as fichier:
	annuaire=fichier.read()
	fichier.close()



plage = [int(annuaire[len(annuaire)-10:len(annuaire)]),699999999]		#pose probleme, on a des trous dans l'annuaire
print(plage)

while serveur_lance:
	print("nombre de clients: " + str(len(clients_connectes)))
	# On va vérifier que de nouveaux clients ne demandent pas à se connecter
	# Pour cela, on écoute la connexion_principale en lecture
	# On attend maximum 10ms
	connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.01)

	for connexion in connexions_demandees:
		connexion_avec_client, infos_connexion = connexion.accept()
		# On ajoute le socket connecté à la liste des clients
		clients_connectes.append(connexion_avec_client)
    
	# Maintenant, on écoute la liste des clients connectés
	# Les clients renvoyés par select sont ceux devant être lus (recv)
	# On attend 50ms maximum
	# On enferme l'appel à select.select dans un bloc try
	# En effet, si la liste de clients connectés est vide, une exception
	# Peut être levée
	clients_a_lire = []
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
	except select.error:
		pass
	else:
		# On parcourt la liste des clients à lire
		for client in clients_a_lire:
			# Client est de type socket
			msg_recu = client.recv(1024)
			msg_recu = msg_recu.decode()
			if msg_recu == "newplage1amour":
				print("demande de nouvelle plage")
				if plage[1]-plage[0] > 0:
					plageaffecte = str(plage[0]) + ";" + str(int(plage[0]) + 100)
					plage[0] = plage[0] + 100												#incrementation de la plage
					client.send(plageaffecte.encode())
					print("affecte: " + plageaffecte)
				else:
					print("travail fini!!!")
					client.send("plusdeplage".encode())

			else:
				if msg_recu == "finconnexion":
					connexion_avec_client_deco = client.getpeername()
					client.close()
					for i in range(len(clients_connectes)):
						if str(clients_connectes[i])[16:22] == "closed":
							clients_connectes[i]="0"
							clients_connectes.remove("0")


				else:
					print("arrive de nouveaux numero: {}".format(msg_recu))
					with open("annuaire.txt", "a") as fichier:
						fichier.write(msg_recu + "\n")











print("Fermeture des connexions")
for client in clients_connectes:
    client.close()

connexion_principale.close()