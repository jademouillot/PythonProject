import paho.mqtt.client as paho
from paho import mqtt
import time
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import random
import multiprocessing
import threading
import datetime

received_values_button = []
received_values_temp = []
value_button_1 = 0
value_button_2 = 0
value_temp = None
cligno_buttoncard1 = False
cligno_buttoncard2 = False
cligno_buttoncard3 = False
label = None
need_eau = False
need_light = False
need_nutrients = False
cnt=0

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
    global value_button_1
    global value_button_2
    global cligno_buttoncard1
    global cligno_buttoncard2
    global cligno_buttoncard3
    global label
    global chemin_complet
    # Décode le message JSON et extrait la valeur appropriée
    message_data = json.loads(msg.payload)
    if 'id' in message_data: #si il y a 'id' dans le message reçu alors bouton
        value_button = message_data['id']
        if value_button == 1:
            value_button_1 = value_button
            with open(chemin_complet, "a") as fichier:
                # Écrire des données à la fin du fichier
                # Obtenir l'heure actuelle
                heure_actuelle = datetime.datetime.now()

                # Formater l'heure actuelle comme une chaîne de caractères
                heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

                # ecrire dans le fichier l'heure
                fichier.write(heure_formatee + ": " + str(value_button_1) + "gave water. \n")
        elif value_button == 2:
            value_button_2 = value_button
            with open(chemin_complet, "a") as fichier:
                # Écrire des données à la fin du fichier
                # Obtenir l'heure actuelle
                heure_actuelle = datetime.datetime.now()

                # Formater l'heure actuelle comme une chaîne de caractères
                heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

                # ecrire dans le fichier l'heure
                fichier.write(heure_formatee + ": " + str(value_button_2) + "gave nutrients. \n")
        received_values_button.append(value_button) #on ajoute value_button à la liste
        print("valeur : ")
        print(received_values_button)
        print("value_button : ", value_button)
        print("cligno : ")
        #print(cligno)
        if cligno_buttoncard1 == True:
            if value_button == 1:  # si id = 1 -> on remet de l'eau
                print("dans if 1")
                message_LEDS = create_message(1, 0)  # on éteint (0) la led1 = water
                client.publish("isen15/led", message_LEDS, qos=1)
                # Ouvrir un fichier en mode ajout
                with open(chemin_complet, "a") as fichier:
                #Écrire des données à la fin du fichier
                    # Obtenir l'heure actuelle
                    heure_actuelle = datetime.datetime.now()

                    # Formater l'heure actuelle comme une chaîne de caractères
                    heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

                    #ecrire dans le fichier l'heure
                    fichier.write(heure_formatee +": " + message_LEDS + "gave water. \n")

                button1.config(bg="blue")  # on remet le bouton eau en bleu
                label = tk.Label(root, text=" Great, you gave water to your plant!")
                label.pack(padx=20, pady=20)
                root.update()
        if cligno_buttoncard2 == True:
            if value_button == 2:  # si id = 2 -> on remet de l'engrais
                message_LEDS = create_message(2, 0)  # on éteint (0) la led2 = engrais
                client.publish("isen15/led", message_LEDS, qos=1)  # eteindre la led 2
                with open(chemin_complet, "a") as fichier:
                    # Écrire des données à la fin du fichier
                    # Obtenir l'heure actuelle
                    heure_actuelle = datetime.datetime.now()

                    # Formater l'heure actuelle comme une chaîne de caractères
                    heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

                    # ecrire dans le fichier l'heure
                    fichier.write(heure_formatee + ": " + message_LEDS + "gave nutrients. \n")
                button2.config(bg="green")  # on remet le bouton engrais en vert
                label = tk.Label(root, text="Great, you gave nutrients to your plant!")
                label.pack(padx=30, pady=30)
                root.update()

        cligno_buttoncard1 = False
        cligno_buttoncard2 = False

    else: #sinon value temperature dans message
        value_temp = message_data['value']
        with open(chemin_complet, "a") as fichier:
            # Écrire des données à la fin du fichier
            # Obtenir l'heure actuelle
            heure_actuelle = datetime.datetime.now()

            # Formater l'heure actuelle comme une chaîne de caractères
            heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

            # ecrire dans le fichier l'heure
            fichier.write(heure_formatee + ": " + value_temp + "\n")
        received_values_temp.append(value_temp)


# def gestion_buttons():
#     if value_button == 1:  # si id = 1 -> on remet de l'eau
#         message_LEDS = create_message(1, 0)  # on éteint (0) la led1 = water
#         client.publish("isen15/led", message_LEDS, qos=1)
#         button1.config(bg="blue")  # on remet le bouton eau en bleu
#
#     if value_button == 2:  # si id = 2 -> on remet de l'engrais
#         message_LEDS = create_message(2, 0)  # on éteint (0) la led2 = engrais
#         client.publish("isen15/led", message_LEDS, qos=1)  # eteindre la led 2
#         button2.config(bg="green")  # on remet le bouton engrais en vert

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
    label.config(text="Button pressed !", fg="black")
    if value_temp is not None:
        label.config(text="The last temp value received is : {}".format(value_temp), fg = "black")
    else:
        label.config(text="value temp null", fg = "black")


def generate_decreasing_number_eau():
    global need_eau
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
            need_eau = True
            #eau()

def generate_decreasing_number_nutriments():   #engrais organique, normalement à renouveler tous les 6 mois mais ici simulation donc + rapide
    global need_nutrients
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
            need_nutrients = True
            #nutriments()

def generate_decreasing_number_lumiere():
    global need_light
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
            need_light = True
            #lumiere()


def show_new_window_stats():
    new_window = tk.Toplevel(root)
    new_window.title("BOTANICARE - STATISTICS")
    new_window.geometry("400x300")
    label = tk.Label(new_window, text="Statistic of the plant")
    label.pack(padx=20, pady=20)

# def show_new_window_history():
#     global chemin_complet
#     new_window = tk.Toplevel(root)
#     new_window.title("BOTANICARE - HISTORY")
#     new_window.geometry("400x300")
#     #label = tk.Label(new_window, text="History of the plant")
#     #label.pack(padx=20, pady=20)
#     label = tk.Label(root, wrap=tk.WORD)
#     label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
#     # Créer une barre de défilement verticale et l'associer au widget Text
#     scrollbar = tk.Scrollbar(root, command=label.yview)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#     label.config(yscrollcommand=scrollbar.set)
#     with open(chemin_complet, "r") as fichier:
#         # Lire le contenu du fichier
#         contenu = fichier.read()
#         # Afficher le contenu sur l'étiquette
#         label.configure(text=contenu)

def show_new_window_history():
    global chemin_complet
    new_window = tk.Toplevel(root)
    new_window.title("BOTANICARE - HISTORY")
    new_window.geometry("400x300")

    # Créer un label en haut de la fenêtre
    label_top = tk.Label(new_window, text="Historique de la plante")
    label_top.pack(pady=10)

    # Créer un widget Text pour afficher le contenu du fichier
    text_widget = tk.Text(new_window, wrap=tk.WORD)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Créer une barre de défilement verticale et l'associer au widget Text
    scrollbar = tk.Scrollbar(new_window, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    try:
        # Ouvrir le fichier en mode lecture
        with open(chemin_complet, "r") as fichier:
            # Lire le contenu du fichier
            contenu = fichier.read()
            # Afficher le contenu dans le widget Text
            text_widget.insert(tk.END, contenu)
    except FileNotFoundError:
        text_widget.insert(tk.END, "Le fichier n'existe pas.")

def toggle_color_eau(button, numbutton, substance, numled):
    global cligno_buttoncard1
    global label
    label = tk.Label(root, text="Click on Button" + str(numbutton) + "(card) to give " + substance + " to your plant!", fg = "blue")
    label.pack(padx=20, pady=20)
    if value_button_1 == 0:
        cligno_buttoncard1 = True
        print("cligno while")
        #print(cligno)
        print("dans while")
        button.config(bg="blue")
        root.update()
        print("message leds")
        message_LEDS = create_message(numled, 1)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(0.2)
        root.after(200)  # Attend 500 ms (0.5 seconde)

        button.config(bg="white")
        root.update()
        message_LEDS = create_message(numled, 0)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(0.2)
        root.after(200)  # Attend à nouveau 500 ms


    #gestion_buttons()

def toggle_color_nutrients(button, numbutton, substance, numled):
    global cligno_buttoncard2
    global label
    label = tk.Label(root, text="Click on Button" + str(numbutton) + "(card) to give " + substance + " to your plant!", fg = "green")
    label.pack(padx=30, pady=30)
    if value_button_2 == 0:
        cligno_buttoncard2 = True
        print("cligno while")
        #print(cligno)
        print("dans while")
        button.config(bg="green")
        root.update()
        message_LEDS = create_message(numled, 1)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(0.2)
        root.after(200)  # Attend 500 ms (0.5 seconde)

        button.config(bg="white")
        root.update()
        message_LEDS = create_message(numled, 0)
        client.publish("isen15/led", message_LEDS, qos=1)
        time.sleep(0.2)
        root.after(200)  # Attend à nouveau 500 ms


    #gestion_buttons()

def toggle_color_lum(button, numled):
    global need_light
    global cnt
    label = tk.Label(root, text="Careful! Your plant needs more light!", fg = "red")
    label.pack(padx=10, pady=10)
    #while True:
    button.config(bg="red")
    root.update()
    message_LEDS = create_message(numled, 1)
    client.publish("isen15/led", message_LEDS, qos=1)
    time.sleep(0.2)
    root.after(200)  # Attend 500 ms (0.5 seconde)

    button.config(bg="white")
    root.update()
    message_LEDS = create_message(numled, 0)
    client.publish("isen15/led", message_LEDS, qos=1)
    time.sleep(0.2)
    root.after(200)  # Attend à nouveau 500 ms

    cnt=cnt+0.8

    print("cnt")
    print(cnt)

    if(cnt>10):
        need_light = False
        button3.config(bg="red")  # on remet le bouton engrais en vert
        label = tk.Label(root, text="Great, you gave light to your plant!")
        label.pack(padx=40, pady=40)
        root.update()


def monitoring_plant():
        global need_eau
        global need_nutrients
        global need_light
        global chemin_complet
        global cnt
        # Create threads for each function
        # thread1 = threading.Thread(target=generate_decreasing_number_eau)
        # thread2 = threading.Thread(target=generate_decreasing_number_nutriments)
        # thread3 = threading.Thread(target=generate_decreasing_number_lumiere)
        #
        # # Start the threads
        # thread1.start()
        # thread2.start()
        # thread3.start()
        #
        # # Wait for the threads to finish
        # thread1.join()
        # thread2.join()
        # thread3.join()
        #while True :
        label.config(text="Click on the button Temperature to update it !", fg = "black")
        generate_decreasing_number_eau()
        generate_decreasing_number_nutriments()
        generate_decreasing_number_lumiere()
        while True:
            if need_eau == True:
                with open(chemin_complet, "a") as fichier:
                    # Écrire des données à la fin du fichier
                    # Obtenir l'heure actuelle
                    heure_actuelle = datetime.datetime.now()

                    # Formater l'heure actuelle comme une chaîne de caractères
                    heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

                    # ecrire dans le fichier l'heure
                    fichier.write(heure_formatee + ": " + "The plant needs water." + "\n")
                print("eau")
                toggle_color_eau(button1, 1, "water", 1)
            if need_nutrients == True:
                with open(chemin_complet, "a") as fichier:
                    # Écrire des données à la fin du fichier
                    # Obtenir l'heure actuelle
                    heure_actuelle = datetime.datetime.now()

                    # Formater l'heure actuelle comme une chaîne de caractères
                    heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

                    # ecrire dans le fichier l'heure
                    fichier.write(heure_formatee + ": " + "The plant needs nutrients." + "\n")
                print("nutrients")
                toggle_color_nutrients(button2, 2, "nutrients", 2)
            if need_light == True:
                with open(chemin_complet, "a") as fichier:
                    # Écrire des données à la fin du fichier
                    # Obtenir l'heure actuelle
                    heure_actuelle = datetime.datetime.now()

                    # Formater l'heure actuelle comme une chaîne de caractères
                    heure_formatee = heure_actuelle.strftime("%Y-%m-%d %H:%M:%S")

                    # ecrire dans le fichier l'heure
                    fichier.write(heure_formatee + ": " + "The plant needs light." + "\n")
                print("light")
                toggle_color_lum(button3, 3)

#mettre les données dans fichier et faire statistique et historique
# Spécifier un chemin complet pour créer le fichier dans un emplacement spécifique
chemin_complet = "C:\\Users\\jadem\\PycharmProjects\\TD1_DATACOMM\\historic"



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
button5 = tk.Button(frame, text="Start monitoring the plant", command = monitoring_plant, bg="orange", fg="white")  # bg pour le fond, fg pour la couleur du texte
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




#gestion des trois fonctions pour eau, nutriments, et lumiere pour les faire ensemble -> voir si on fait 4 pages différentes??
#historique avec fichier -> ce que le client fait
#statistiques : courbes : eau, temp, et lumiere
#gestion dans label

#
# def eau():
#     #si le niveau d'eau est ok (on connait le niveau d'eau nécessaire pour la plante = 15 cl)
#     #alors on éteint la LED bleue
#     #si il manque de l'eau alors LED s'allume
#
#     #sinon on clignote la LED bleue + on clignote le bouton eau sur itnerface + texte "il manque de l'eau, appuyez sur tel bouton de la carte")
#     toggle_color_eau(button1, 1, "water", 1)
#
# def nutriments():
#     #si le niveau d'eau est ok (on connait le niveau d'eau nécessaire pour la plante = 15 cl)
#     #alors on éteint la LED bleue
#     #si il manque de l'eau alors LED s'allume
#
#     #sinon on clignote la LED bleue + on clignote le bouton eau sur itnerface + texte "il manque de l'eau, appuyez sur tel bouton de la carte")
#     toggle_color_nutrients(button2, 2, "nutrients", 2)
#
#
# def lumiere():
#     #si le niveau d'eau est ok (on connait le niveau d'eau nécessaire pour la plante = 15 cl)
#     #alors on éteint la LED bleue
#     #si il manque de l'eau alors LED s'allume
#
#     #sinon on clignote la LED bleue + on clignote le bouton eau sur itnerface + texte "il manque de l'eau, appuyez sur tel bouton de la carte")
#     toggle_color_lum(button3, 3)