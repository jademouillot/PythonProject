import paho.mqtt.client as paho
from paho import mqtt
import time
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

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

def create_message():
    message = {
        "id": 3,
        "state": 1
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

# Définir la taille de la police pour le titre
titre_font = ("Helvetica", 20)

# Créer un widget Label pour afficher le titre
titre_label = tk.Label(root, text="BOTANICARE", font=titre_font)

# Ajouter le titre à la fenêtre
titre_label.pack(pady=20)


# Charger l'image depuis un fichier (par exemple, "image.png")
#image_path = "chemin/vers/votre/image/image.png"  # Remplacez "chemin/vers/votre/image/image.png" par le chemin de votre image
#image = tk.PhotoImage(file=image_path)

# Créer un widget Label pour afficher l'image
image_label = tk.Label(root, image=image)

# Ajouter l'image à la fenêtre
image_label.pack(pady=10)

# Création d'une étiquette pour afficher les messages
label = tk.Label(root, text="")
label.pack(padx=20, pady=20)

# Création d'un cadre pour organiser les éléments
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)
client.subscribe("isen15/temp", qos=1)

# Création d'un bouton avec le fond bleu
button1 = tk.Button(frame, text="Eau", command=temp, bg="blue", fg="white")  # bg pour le fond, fg pour la couleur du texte
# Création de plusieurs boutons et les placer dans une grille
button1.grid(row=0, column=0, padx=10, pady=10)


# Création d'un bouton avec le fond vert
button2 = tk.Button(frame, text="Nutriments", command=temp, bg="green", fg="white")  # bg pour le fond, fg pour la couleur du texte
# Création de plusieurs boutons et les placer dans une grille
button2.grid(row=0, column=1, padx=10, pady=10)

# Création d'un bouton avec le fond rouge
button3 = tk.Button(frame, text="Lumière", command=temp, bg="red", fg="white")  # bg pour le fond, fg pour la couleur du texte
# Création de plusieurs boutons et les placer dans une grille
button3.grid(row=1, column=0, padx=10, pady=10)


button4 = tk.Button(frame, text="Température", command=show_message)
button4.grid(row=1, column=1, padx=10, pady=10)

# Boucle principale d'exécution
root.mainloop()

try:
    while True:

        # Calcul de la moyenne des valeurs reçues
        print("debut avant creation message")
        message_LEDS = create_message()
        print("avant publish")
        client.publish("isen15/led", message_LEDS, qos=1)
        print("apres message")

        time.sleep(0.5)

        if value_button is not None:
            print("La dernière valeur reçue est:", value_button)
        else:
            print("value_button null")

        #print("le bouton avec l'id", received_values[-1], "est appuyé")
        print("received values", received_values)

        time.sleep(0.5)

        message_temp = create_message_temp()

        client.publish("isen15/getTemp",message_temp, qos=1)

        if value_temp is not None:
            print("La dernière valeur temp reçue est:", value_temp)
        else:
            print("value temp null")

        # Attente de 3 secondes avant d'envoyer le prochain message
        time.sleep(3)

        #client.subscribe("valeur", qos=1)

except KeyboardInterrupt:
    # Arrêt de la boucle de publication en cas d'interruption du clavier (Ctrl+C)
    pass

client.loop_stop()

#client.loop_forever()