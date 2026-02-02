#%%

from time import sleep
from pythonosc import udp_client
import threading
import queue
import time
import numpy as np
from pythonosc import dispatcher, osc_server
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os

#%%
# ++++++++++++++++++++++++++++++++++++++ #
#         ENVOI DE MESSAGE               #
# ++++++++++++++++++++++++++++++++++++++ #

# Cellule permettant d'initialiser les paramètres du modèle
adress_param ="127.0.0.1"
port_param = 5248
client_param = udp_client.SimpleUDPClient(adress_param, port_param)

def initialize_parameters(default_vb = 0.1,
                            default_Fb = 1.5,
                            default_v0 = 0.06,
                            default_L = 0.325,
                            default_f0_vise = 440.0,
                            default_w_ratio = 0.03,
                            default_x = 0.12,
                            default_tension = 58.86,
                            default_f_T1 = 500.0,
                            default_Q = 30.0,
                            default_S = 17600.0,
                            default_M = 0.0178):
    
    mess_vb = "/vb"
    mess_Fb = "/Fb"
    mess_v0 = "/v0"
    mess_L = "/L"
    mess_f0_vise = "/f0_vise"
    mess_w_ratio = "/w_ratio"
    mess_x = "/x"
    mess_tension = "/tension"
    mess_f_T1 = "/f_T1"
    mess_Q = "/Q"
    mess_S = "/S"
    mess_M = "/M"

    client_param.send_message(mess_vb, default_vb)
    client_param.send_message(mess_Fb, default_Fb)
    client_param.send_message(mess_v0, default_v0)
    client_param.send_message(mess_L, default_L)
    client_param.send_message(mess_f0_vise, default_f0_vise)
    client_param.send_message(mess_w_ratio, default_w_ratio)
    client_param.send_message(mess_x, default_x)
    client_param.send_message(mess_tension, default_tension)
    client_param.send_message(mess_f_T1, default_f_T1)
    client_param.send_message(mess_Q, default_Q)
    client_param.send_message(mess_S, default_S)
    client_param.send_message(mess_M, default_M)


#%%
# ++++++++++++++++++++++++++++++++++++++ #
#        RECEPTION DES SIGNAUX           #
# ++++++++++++++++++++++++++++++++++++++ #

# cellule permettant de lancer une simulation et de récupérer le signal généré
IP = "127.0.0.1"
PORT_SEND = 5682


is_recording = False

# --- CLIENT D'ENVOI ---
client = udp_client.SimpleUDPClient(IP, PORT_SEND)

def run_simu(n_samples, mode=0):
    """
    mode 0 : Transitoire (immédiat)
    mode 1 : Permanent (attente de 1s)
    """
    global is_recording
    os.remove(".\MAXMSP\simu.wav")
    
    print(f"\n--- Démarrage Simulation : Mode {'Permanent' if mode==1 else 'Transitoire'} ---")

    is_recording = True 

    # On reset Max (Bang de start)
    client.send_message("/sim/start", 1.0) 
    sleep(0.5)
    initialize_parameters()
    
    if mode == 1: # Régime Permanent
        print("... Stabilisation du filtre (1s) ...")
        time.sleep(1.0) 
        # Après 1s, on demande le flux
        client.send_message("/sim/trigger_buffer", 1)
    else: # Transitoire
        # On demande le flux immédiatement (ou juste après le start)
        client.send_message("/sim/trigger_buffer", 1)
    
    time.sleep(1.5)
    is_recording = False
    client.send_message("/sim/trigger_buffer", 0)
    sleep(3.0)
    fs, simu = wavfile.read(".\MAXMSP\simu.wav")
    
    return np.array(simu[:n_samples])


#%%
data_transitoire = run_simu(n_samples=10000, mode=0)
data_permanent = run_simu(n_samples=10000, mode=1)

print(f"\nRésultat final :")
print(f"Shape Transitoire : {data_transitoire.shape}")
print(f"Shape Permanent : {data_permanent.shape}")

plt.subplot(2,1,1)
plt.title("Transitoire")
plt.plot(data_transitoire)
plt.subplot(2,1,2)
plt.title("Permanent")
plt.plot(data_permanent)
plt.tight_layout()
plt.show()