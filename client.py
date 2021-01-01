from lxml import html
from lxml import etree
from optparse import OptionParser
import requests
import socket
import time




parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", default="annuaire.txt", metavar="FILE")
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
parser.add_option("-n", "--number", dest="number",
				  help="number to check")
parser.add_option("-a", "--ip hote", dest="hote", default="localhost", 
				  help="adresse ip du serveur")


(options, args) = parser.parse_args()




hote = options.hote
port = 12800



connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))


msg_a_envoyer = b""



def nomnumero(num):
	
	url = 'https://m.facebook.com/search/top/?q='+str(num)																													#definition de l'url de recherche
	print (url)
	headers = {'User-Agent': 'Mozilla/4.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' , 'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'}
	page = requests.get(url, headers=headers)																																	#request avec requests
	path=".//*[@id='objects_container']/div[2]/div/div/a/div/div[2]/div[1]/strong/text()"																						#xpath du nom de la personne dans la page de recherche retourne
	tree = html.fromstring(page.text)																																			#pretriage de la page par lxml
	avvisi = tree.xpath(path)																																					#va chercher la valeur a pas position 'path'
	print(avvisi)
	nom = str(avvisi)[2:len(avvisi)-3]																																				#chaine du type ['"nom"'] vers nom
	print(str(nom))
	return nom







connexion_avec_serveur.send("newplage1amour".encode())
msg_recu = str(connexion_avec_serveur.recv(1024).decode())




while msg_recu != "plusdeplage":
	try:
		plage = msg_recu.split(";")
		debut = int(plage[0])
		fin = int(plage[1])
		numero = debut

		while numero <= fin:
			nomactuel = str(nomnumero(numero) + ";" + str(numero))
			msg_a_envoyer = nomactuel
			msg_a_envoyer = msg_a_envoyer.encode()
			# On envoie le message
			connexion_avec_serveur.send(msg_a_envoyer)
			print ("numero actuel: " + str(numero) + " fin dans: " + str(int(fin)-int(numero)))
			numero += 1
			time.sleep(15)


		connexion_avec_serveur.send("newplage1amour".encode())
		msg_recu = str(connexion_avec_serveur.recv(1024).decode())
	except :
		print("erreur")
		connexion_avec_serveur.send("finconnexion".encode())
		msg_recu = "plusdeplage"

print("Fermeture de la connexion")
connexion_avec_serveur.close()


