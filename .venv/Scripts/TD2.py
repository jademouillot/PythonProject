import paho.mqtt.client as paho
from paho import mqtt
import time
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import random
import multiprocessing

received_values = []
value_button = None
value_temp = None

def show_message():
    messagebox.showinfo("Info", "Bonjour, ceci est un message d'information !")

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(client, userdata, mid, properties=None):
    print("Message Published: " + str(mid))

def on_message(client, userdata, msg):
    global value_temp
    global value_button
    # Décode le message JSON et extrait la valeur appropriée
    message_data = json.loads(msg.payload)
    if 'id' in message_data:
        value_button = message_data['id']
        received_values.append(value_button)
    else:
        value_temp = message_data['value']
        received_values.append(value_temp)

def calculate_average():
    if received_values:
        average = sum(received_values) / len(received_values)
        print("Moyenne des valeurs reçues:", average)
    else:
        print("Aucune valeur reçue pour calculer la moyenne.")

def create_message(a,b):
    message = {
        "id": a,
        "state": b
    }
    return json.dumps(message)

def create_message_temp():
    message = {
        "request":1
    }
    return json.dumps(message)

def temp():
    message_temp = create_message_temp()

    client.publish("isen15/getTemp", message_temp, qos=1)
    label.config(text="Bouton cliqué!", fg="blue")
    if value_temp is not None:
        label.config(text="La dernière valeur temp reçue est: {}".format(value_temp))
    else:
        label.config(text="value temp null")

def generate_decreasing_number_eau():
    max_value = 15
    min_value = 7

    # Attente initiale de 2 secondes
    #time.sleep(2)

    # Boucle de génération de nombres décroissants
    while max_value >= min_value:
        print("Current value:", max_value)
        time.sleep(1)  # Attendre 1 seconde avant de décrémenter
        max_value -= 1  # Décrémenter la valeur maximale

        # Appeler une fonction lorsque la valeur atteint 10
        if max_value == min_value:
            print("Reached minimum value, calling a function...")
            eau()

def generate_decreasing_number_nutriments():   #engrais organique, normalement à renouveler tous les 6 mois mais ici simulation donc + rapide
    max_value = 40
    #min_value = 20 #prof!!
    min_value = 30

    # Attente initiale de 2 secondes
    #time.sleep(2)

    # Boucle de génération de nombres décroissants
    while max_value >= min_value:
        print("Current value:", max_value)
        time.sleep(1)# Attendre 1 seconde avant de décrémenter
        max_value -= 2  # Décrémenter la valeur maximale

        # Appeler une fonction lorsque la valeur atteint 10
        if max_value == min_value:
            print("Reached minimum value, calling a function...")
            nutriments()

def generate_decreasing_number_lumiere():
    max_value = 10000  #a l'ombre
    min_value = 4000

    # Attente initiale de 2 secondes
    #time.sleep(2)

    # Boucle de génération de nombres décroissants
    while max_value >= min_value:
        print("Current value:", max_value)
        time.sleep(1)  # Attendre 1 seconde avant de décrémenter
        max_value -= 1000  # Décrémenter la valeur maximale

        # Appeler une fonction lorsque la valeur atteint 10
        if max_value == min_value:
            print("Reached minimum value, calling a function...")
            lumiere()

def eau():
    #si le niveau d'eau est ok (on connait le niveau d'eau nécessaire pour la plante = 15 cl)
    #alors on éteint la LED bleue
    #si il manque de l'eau alors LED s'allume

    #sinon on clignote la LED bleue + on clignote le bouton eau sur itnerface + texte "il manque de l'eau, appuyez sur tel bouton de la carte")
    toggle_color(button1, 1, "water", 1)

def nutriments():
    #si le niveau d'eau est ok (on connait le niveau d'eau nécessaire pour la plante = 15 cl)
    #alors on éteint la LED bleue
    #si il manque de l'eau alors LED s'allume

    #sinon on clignote la LED bleue + on clignote le bouton eau sur itnerface + texte "il manque de l'eau, appuyez sur tel bouton de la carte")
    toggle_color(button2, 2, "nutrients", 2)


def lumiere():
    #si le niveau d'eau est ok (on connait le niveau d'eau nécessaire pour la plante = 15 cl)
    #alors on éteint la LED bleue
    #si il manque de l'eau alors LED s'allume

    #sinon on clignote la LED bleue + on clignote le bouton eau sur itnerface + texte "il manque de l'eau, appuyez sur tel bouton de la carte")
    toggle_color_lum(button3, 3)

def show_new_window_stats():
    new_window = tk.Toplevel(root)
    new_window.title("BOTANICARE - STATISTICS")
    new_window.geometry("400x300")
    label = tk.Label(new_window, text="Statistic of the plant")
    label.pack(padx=20, pady=20)

def show_new_window_history():
    new_window = tk.Toplevel(root)
    new_window.title("BOTANICARE - HISTORY")
    new_window.geometry("400x300")
    label = tk.Label(new_window, text="History of the plant")
    label.pack(padx=20, pady=20)

def toggle_color(button, numbutton, substance, numled):
    label = tk.Label(root, text="Click on Button" + str(numbutton) + "(card) to give " + substance + " to your plant!")
    if substance=="water":
        label.pack(padx=20, pady=20)
    else:
        label.pack(padx=30, pady=30)
    while True:
        if substance == "water":
            button.config(bg="blue")
        else:
            button.config(bg="green")
        root.update()
        message_LEDS = create_message(numled, 1)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(1)
        root.after(500)  # Attend 500 ms (0.5 seconde)

        button.config(bg="white")
        root.update()
        message_LEDS = create_message(numled, 0)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(1)
        root.after(500)  # Attend à nouveau 500 ms

def toggle_color_lum(button, numled):
    label = tk.Label(root, text="Careful! Your plant needs more light!")
    label.pack(padx=10, pady=10)
    while True:
        button.config(bg="red")
        root.update()
        message_LEDS = create_message(numled, 1)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(1)
        root.after(500)  # Attend 500 ms (0.5 seconde)

        button.config(bg="white")
        root.update()
        message_LEDS = create_message(numled, 0)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(1)
        root.after(500)  # Attend à nouveau 500 ms

def monitoring_plant():
    # Créer des processus pour chaque fonction
    #processus1 = multiprocessing.Process(target=generate_decreasing_number_eau)
    #processus2 = multiprocessing.Process(target=generate_decreasing_number_nutriments)
    #processus3 = multiprocessing.Process(target=generate_decreasing_number_lumiere)
    #
    # # Démarrer les processus
    #processus1.start()
    #processus2.start()
    #processus3.start()
    #
    # # Attendre que les processus se terminent
    #processus1.join()
    #processus2.join()
    #processus3.join()

    generate_decreasing_number_eau()
    generate_decreasing_number_nutriments()
    generate_decreasing_number_lumiere()

client = paho.Client(paho.CallbackAPIVersion.VERSION1,"")

client.on_connect = on_connect

client.on_subscribe = on_subscribe

client.on_publish = on_publish

client.on_message = on_message

#client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

#client.username_pw_set("jadekarin", "Password2024-")

client.connect("broker.hivemq.com", 1883)

client.subscribe("isen15/button", qos=1)

client.subscribe("isen15/temp", qos=1)

client.loop_start()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Botanicare")
root.geometry("500x600")  # Définir la taille de la fenêtre principale (largeur x hauteur)

menu_bar = tk.Menu(root)

# Création du menu "File" avec deux options
file_menu = tk.Menu(menu_bar, tearoff=0)

# Ajout d'une étiquette personnalisée avec une largeur fixe
label_statistics = tk.Label(root, text="Statistics", width=20, anchor="w") #changer la taille des boutons?
file_menu.add_command(label="Statistics", command=show_new_window_stats, compound="left", image=None)

# Ajout d'une étiquette personnalisée avec une largeur fixe
label_history = tk.Label(root, text="History", width=20, anchor="w")
file_menu.add_command(label="History", command=show_new_window_history, compound="left", image=None)

file_menu.add_separator()

# Ajout d'une étiquette personnalisée avec une largeur fixe
label_exit = tk.Label(root, text="Exit", width=20, anchor="w")
file_menu.add_command(label="Exit", command=root.quit, compound="left", image=None)

menu_bar.add_cascade(label="Pages", menu=file_menu)

root.config(menu=menu_bar)

# Définir la taille de la police pour le titre
titre_font = ("Helvetica", 20)

# Créer un widget Label pour afficher le titre
titre_label = tk.Label(root, text="BOTANICARE", font=titre_font)

# Ajouter le titre à la fenêtre
titre_label.pack(pady=20)

# Charger l'image depuis un fichier (par exemple, "image.png")
image_path = "C:\\Users\\jadem\\PycharmProjects\\TD1_DATACOMM\\image.png"
image = tk.PhotoImage(file=image_path)

image = image.subsample(2, 2)  # Facteur de sous-échantillonnage : 2 dans chaque dimension

# Créer un widget Label pour afficher l'image
image_label = tk.Label(root, image=image)

# Ajouter l'image à la fenêtre
image_label.pack(pady=10)

# Création d'un cadre pour organiser les éléments
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)
client.subscribe("isen15/temp", qos=1)

# Création d'un bouton avec le fond bleu
button1 = tk.Button(frame, text="Water", bg="blue", fg="white")  # bg pour le fond, fg pour la couleur du texte
# Création de plusieurs boutons et les placer dans une grille
button1.grid(row=1, column=0, padx=10, pady=10)

# Création d'un bouton avec le fond vert
button2 = tk.Button(frame, text="Nutrients", bg="green", fg="white")  # bg pour le fond, fg pour la couleur du texte
# Création de plusieurs boutons et les placer dans une grille
button2.grid(row=1, column=1, padx=10, pady=10)

# Création d'un bouton avec le fond rouge
button3 = tk.Button(frame, text="Light", bg="red", fg="white")  # bg pour le fond, fg pour la couleur du texte
# Création de plusieurs boutons et les placer dans une grille
button3.grid(row=2, column=0, padx=10, pady=10)

button4 = tk.Button(frame, text="Temperature", command=temp)
button4.grid(row=2, column=1, padx=10, pady=10)

# Création d'un bouton avec le fond bleu
button5 = tk.Button(frame, text="Start monitoring the plant", command = monitoring_plant, bg="blue", fg="white")  # bg pour le fond, fg pour la couleur du texte
# Création de plusieurs boutons et les placer dans une grille
button5.grid(row=0, column=0, padx=10, pady=10)

# Création d'une étiquette pour afficher les messages
label = tk.Label(root, text="")
label.pack(padx=20, pady=20)

# #generate_decreasing_number()
#
# # Boucle principale d'exécution
#
#
#
# try:
#     while True:
#
#         # Calcul de la moyenne des valeurs reçues
#         print("debut avant creation message")
#         message_LEDS = create_message()
#         print("avant publish")
#         client.publish("isen15/led", message_LEDS, qos=1)
#         print("apres message")
#
#         time.sleep(0.5)
#
#         if value_button is not None:
#             print("La dernière valeur reçue est:", value_button)
#         else:
#             print("value_button null")
#
#         #print("le bouton avec l'id", received_values[-1], "est appuyé")
#         print("received values", received_values)
#
#         time.sleep(0.5)
#
#         message_temp = create_message_temp()
#
#         client.publish("isen15/getTemp",message_temp, qos=1)
#
#         if value_temp is not None:
#             print("La dernière valeur temp reçue est:", value_temp)
#         else:
#             print("value temp null")
#
#         # Attente de 3 secondes avant d'envoyer le prochain message
#         time.sleep(3)
#
#         #client.subscribe("valeur", qos=1)
#
# except KeyboardInterrupt:
#     # Arrêt de la boucle de publication en cas d'interruption du clavier (Ctrl+C)
#     pass
#
# client.loop_stop()

root.mainloop()

#client.loop_forever()

#au debut besoin de rien -> pas de led allumée, bonnes conditions et seulemnt apres que ça peut changer

#temperature/lumiere
#si temp baisse -> lum baisse

#voir pour faire les 3 fonctions en meme temps
#fait normalement -> a tester

#boutons
#lancer le programme generate
#attendre appui bouton
#recommencer programme generate
#...

#mettre les données dans fichier et faire statistique et historique
# Spécifier un chemin complet pour créer le fichier dans un emplacement spécifique
#chemin_complet = "/chemin/vers/votre/emplacement/donnees.txt"

# Ouvrir un fichier en mode ajout
#with open(chemin_complet, "a") as fichier:
    # Écrire des données à la fin du fichier
    #fichier.write("Ceci est une nouvelle ligne ajoutée.\n")
    #fichier.write("Voici une autre nouvelle ligne ajoutée.\n")