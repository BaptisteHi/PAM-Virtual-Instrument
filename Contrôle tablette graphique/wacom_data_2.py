import sys
import os
import time
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPointF, QRect
from PyQt5.QtGui import QPainter, QTabletEvent, QPixmap, QPen, QColor, QPainterPath, QFont 
from PyQt5.QtWidgets import QApplication, QWidget

from pythonosc import udp_client, dispatcher, osc_server

# Configuration de la communication avec Max
address_wacom = "127.0.0.1"
address_listening = address_wacom
port_wacom_send = 5048  # Port Python -> Max
port_listening = 5026   # Port Max -> Python

client_wacom = udp_client.SimpleUDPClient(address_wacom, port_wacom_send)

# Définition des adresses OSC utilisées pour communiquer avec MaxMSP
mess_x = "/x"                   # Coordonnées normalisées (entre 0 et 1)
mess_y = "/y"
mess_press = "/pressure"        # Pression du stylet
mess_is_down = "/is_down"       # État du contact (1 si le stylet touche l'écran, 0 sinon)
mess_zone = "/zone"             # Zone active (violon) (0 = Moitié Gauche/Violon, 1 = Moitié Droite/Carte)
mess_velocity = "/velocity"     #Paramètres du violon
mess_beta = "/beta"             
mess_instr = "/instr"           #Instrument actif

mess_change_beta = "/change_beta" # Reçu de Max : Change le numéro de la carte (1 à 3)
mess_change_note = "/change_note" # Reçu de Max : Change la note (1 à 12)


# Liste pour la conversion de l'index reçu (1-12) en texte pour le nom de fichier
NOTES = ['Do', 'Do#', 'Re', 'Re#', 'Mi', 'Fa', 'Fa#', 'Sol', 'Sol#', 'La', 'La#', 'Si']

# ==============================================================================
# CLASSE : OscReceiver (Thread d'écoute)
# ==============================================================================
class OscReceiver(QThread): 
    """
    Fil d'exécution parallèle (Thread) dédié à la réception des messages OSC.
    Il tourne en arrière-plan pour ne pas bloquer l'interface graphique.
    """
    # Signaux Qt permettant de communiquer avec l'interface graphique (Thread principal)
    beta_received = pyqtSignal(float)
    image_note_received = pyqtSignal(int) 

    def run(self):
        # Le dispatcher fait le tri : "Quand je reçois telle adresse, j'appelle telle fonction"
        disp = dispatcher.Dispatcher()
        disp.map(mess_change_beta, self.handle_change_beta)
        disp.map(mess_change_note, self.handle_change_note)

        # Lancement du serveur d'écoute
        try:
            server = osc_server.ThreadingOSCUDPServer((address_listening, port_listening), disp)
            print(f"Écoute OSC active sur le port {port_listening}")
            server.serve_forever()
        except Exception as e:
            print(f"Erreur serveur OSC : {e}")

    def handle_change_beta(self, unused_addr, value):
        # Convertit la valeur reçue en entier et l'envoie à la fenêtre principale
        self.beta_received.emit(float(value))

    def handle_change_note(self, unused_addr, value):
        self.image_note_received.emit(int(value))


# ==============================================================================
# CLASSE : TabletSampleWindow (Fenêtre Principale)
# ==============================================================================
class TabletSampleWindow(QWidget):
    def __init__(self, parent=None):
        super(TabletSampleWindow, self).__init__(parent)
        
        # Active la détection du stylet même lorsqu'il survole l'écran sans le toucher
        self.setAttribute(Qt.WA_TabletTracking)
        self.setWindowTitle("Interface de jeu")

        self.instrument = 1 #Si 0: violon
                            #Si 1: clarinette
        
        # --- Variables d'état du stylet ---
        self.pen_is_down = False
        self.pen_x = 0.0         # Position X brute en pixels
        self.pen_y = 0.0         # Position Y brute en pixels
        self.pen_x_norm = 0.0    # Position X normalisée (0 à 1)
        self.pen_y_norm = 0.0    # Position Y normalisée (0 à 1)
        self.pen_pressure = 0.0  # Pression
        
        self.active_y = -10. # Par défaut hors-champ
        self.activation_list = [0.,0.2265625,0.2890625,1.]  # Limites des zones d'activation des différentes cartographies selon beta
        #self.activation_threshold = 0.05
        self.current_beta = 0.0 # Mémorise la valeur envoyée par Max
        self.markers_norm_y = [3/16, 17/64, 5/16] # Ordonnées normalisées des marqueurs

        # --- Lissage des valeurs ---
        n_pond = 20 #Lissage avec les n_pond-1 valeurs précédentes

        self.velocity_list = np.zeros(n_pond-1) # vitesse violon
        self.velocity_pond = np.linspace(0,1,n_pond)**3
        self.velocity_pond /= np.sum(self.velocity_pond)

        self.press_list = np.zeros(n_pond-1)    #Force
        self.press_pond = self.velocity_pond


        # --- Variables pour le calcul de la vitesse (violon interactif) ---
        self.previous_time = 0
        self.current_time = 0
        self.prev_x_norm = 0.0
        self.velocity = 0.0
        
        # --- Variables de mémorisation de l'affichage ---
        self.last_map_x = -1.0   # Dernière position X connue sur la carte
        self.last_map_y = -1.0   # Dernière position Y connue sur la carte
        self.current_zone = 0    # 0 = Violon, 1 = Carte
        self.status_text = "En attente..."

        # Variables pour les images
        self.current_map_index = 1
        self.current_note_index = 1 
        self.current_pixmap = None

        # Chargement de l'image du violon (zone gauche)
        self.violin_pixmap = QPixmap("schema_violon.jpg")
        if self.violin_pixmap.isNull():
             print("ATTENTION: L'image du violon est introuvable.")

        # Paramétrage visuel (Police d'écriture)
        self.legend_font = QFont("Arial", 10)

        # Lancement du récepteur OSC
        self.osc_thread = OscReceiver()
        self.osc_thread.beta_received.connect(self.update_map_index)
        self.osc_thread.image_note_received.connect(self.update_note_index)
        self.osc_thread.start()

        # Charge la première image de cartographie
        self.load_image()

    def update_map_index(self, beta):  #Mise à jour de la cartographie selon la position d'excitation (violon)
        """VIOLON UNIQUEMENT : Met à jour l'index de la carte (1, 2, 3) automatiquement selon la valeur de beta choisie."""
        self.current_beta = beta
        if self.instrument ==1: #Si clarinette, on ne fait rien
            pass
        elif  beta < 0.2265625 :
            new_map_index = 1
        elif 0.2265625  <= beta < 0.2890625 :
            new_map_index = 2
        else:
            new_map_index = 3
        
        if self.instrument ==1: #Si clarinette, on ne fait rien
            pass
        elif new_map_index != self.current_map_index:
            self.current_map_index = new_map_index
            self.load_image()
        else:
            self.update() # Si la carte est la même, on met juste à jour l'écran pour le curseur

    def update_note_index(self, index): #Mise à jour de la cartographie selon la note jouée
        """
        Met à jour l'index de la note (1 à 12) si la valeur est valide.
        Si la valeur est égale à 48 (pad de gauche) -> Ouvre l'interface pour le violon.
        Si la valeur est égale à 49 (pad de droite) -> Ouvre l'interface pour la clarinette.
        """
        if 1 <= index <= 12:
            self.current_note_index = index
            self.load_image()
        elif index == -11:  #Si on appuie sur le pad de gauche, affichage de l'interface violon
            self.instrument = 0
            self.load_image()
        elif index == -10:  #si on appuie sur le pad de droite, affichage de l'interface clarinette
            self.instrument = 1
            self.load_image()

    def load_image(self):   #Charge la cartographie actuelle
        """Recompose le nom de fichier et charge la cartographie."""
        nom_note = NOTES[self.current_note_index - 1]
        if self.instrument == 0:    #Si violon
            filename = f"images_cartographie_violon/{nom_note}_{self.current_map_index}.png"
        #filename = "images_cartographie/carto_violongue.png"
        else:
            filename = f"images_cartographie_clarinette/{nom_note}.png"

        if os.path.exists(filename):
            self.current_pixmap = QPixmap(filename)
            self.status_text = f"Note : {NOTES[self.current_note_index - 1]}"
            # On définit une taille de fenêtre initiale confortable (2x la largeur de l'image)
            #self.resize(self.current_pixmap.width() * 2, self.current_pixmap.height())
        else:
            print(f"Erreur: L'image {filename} n'existe pas.")
            self.status_text = f"Erreur: {filename} introuvable"
        
        self.update() # Demande à Qt de redessiner la fenêtre

    # ==========================================================================
    # GESTION DES ÉVÉNEMENTS DU STYLET
    # ==========================================================================
    def tabletEvent(self, event):
        """Fonction appelée automatiquement à chaque micro-mouvement du stylet."""
        pos = event.posF()
        self.pen_x = pos.x()
        self.pen_y = pos.y()
        self.pen_pressure = self.press_pond[-1] * event.pressure() + np.dot(self.press_list,self.press_pond[:-1])
        self.press_list[:-1] = self.press_list[1:]
        self.press_list[-1] = self.pen_pressure

        # Récupération de la largeur et hauteur actuelles de la fenêtre
        w_half = self.width() / 2
        w = self.width()
        h = self.height()
        
        # --- CALCUL DES ZONES ET NORMALISATION ---

        ## Violon

        if self.instrument == 0:
            raw_y_norm = self.pen_y / h if h > 0 else 0.0

            if self.pen_x < w_half:
                self.current_zone = 0 # Schéma violon
                raw_x_norm = self.pen_x / w_half if w_half > 0 else 0.0
                
                # --- NOUVEAU REPÈRE POUR LA CORDE ---
                x_origine = 0.497
                y_origine_bas = 0.715 # Point qui deviendra Y = 0
                y_haut = 0.110        # Point qui deviendra Y = 1
                
                # Renormalisation
                new_x = ((raw_x_norm - x_origine) / (y_haut - y_origine_bas))
                new_y = ((raw_y_norm-y_origine_bas) / (y_haut-y_origine_bas))
                
                self.prev_x_norm = self.pen_x_norm  #On garde la valeur précédente pour le calcul de la vitesse
                self.pen_x_norm = new_x
                self.pen_y_norm = max(0.0, min(1.0, new_y))

            else:
                self.current_zone = 1 # CARTE
                self.current_time = 0
                self.previous_time = 0
                # Le comportement d'origine est conservé pour la carte de droite
                raw_x_norm = (self.pen_x - w_half) / w_half if w_half > 0 else 0.0

                # --- NOUVEAU REPÈRE POUR LA CARTE ---
                x_origine_carte = 0.152
                y_origine_carte = 0.798
                y_extrem_carte= 0.183
                x_extrem_carte = 0.798
                
                # Renormalisation
                new_x = ((raw_x_norm - x_origine_carte)  / (x_extrem_carte - x_origine_carte) * 2)
                new_y = ((raw_y_norm - y_origine_carte) / (y_extrem_carte - y_origine_carte) * 0.2 + 0.3)
                
                self.pen_x_norm = new_x
                self.pen_y_norm = new_y
                
                self.last_map_x = self.pen_x
                self.last_map_y = self.pen_y
            
            self.previous_time = self.current_time
            self.current_time = time.time()
        
        
        ##Clarinette

        elif self.instrument == 1:
            #Première normalisation
            raw_y_norm = self.pen_y / h if h > 0 else 0.0
            raw_x_norm = self.pen_x / w  if w > 0 else 0.0

            #Nouveau repère pour la carte   #A compléter avec les valeurs obtenues
            x_origine_carte_cl = 0.081
            y_origine_carte_cl = 0.862
            y_extrem_carte_cl = 0.021
            x_extrem_carte_cl = 0.536
            
            # # Renormalisation
            new_x = ((raw_x_norm - x_origine_carte_cl)  / (x_extrem_carte_cl - x_origine_carte_cl) * 0.9 + 0.05)
            new_y = ((raw_y_norm - y_origine_carte_cl) / (y_extrem_carte_cl - y_origine_carte_cl) * 0.9 + 0.05)
            # new_y = raw_y_norm
            # new_x = raw_x_norm


            self.pen_x_norm = max(0.0, min(1.0, new_x))
            self.pen_y_norm = max(0.0, min(1.0, new_y))
            
            self.last_map_x = self.pen_x
            self.last_map_y = self.pen_y


        # Détection du clic/contact
        eventType = event.type()
        if eventType == QTabletEvent.TabletPress:
            self.pen_is_down = True
        elif eventType == QTabletEvent.TabletRelease:
            self.pen_is_down = False

        # --- CALCUL DE LA VITESSE DE L'ARCHET (violon interactif) ---
        # On calcule la vitesse uniquement si le stylet est posé et qu'on est sur le schéma interactif (zone 0)
        if self.instrument == 0 and self.pen_is_down and self.current_zone == 0 and self.previous_time != 0:
            dt = self.current_time - self.previous_time
            
            if dt > 0: # Sécurité pour éviter la division par zéro
                
                self.velocity = (self.velocity_pond[-1]*(self.pen_x_norm - self.prev_x_norm) / dt + np.dot(self.velocity_list,self.velocity_pond[:-1]))
                self.velocity_list[:-1] = self.velocity_list[1:]
                self.velocity_list[-1] = self.velocity
        
        # --- ENVOI DES DONNÉES OSC VERS MAXMSP ---
        instrument_actif = 0
        if self.instrument == 0 and self.current_zone == 1:
            instrument_actif = 1
        elif self.instrument == 1:
            instrument_actif = 2
          
        if not self.pen_is_down:
            client_wacom.send_message(mess_is_down, 0)
        elif self.instrument == 0:
            client_wacom.send_message(mess_is_down, 1)
            client_wacom.send_message(mess_zone, self.current_zone)
            client_wacom.send_message(mess_x, float(self.pen_x_norm))
            client_wacom.send_message(mess_y, float(self.pen_y_norm))
            client_wacom.send_message(mess_press, float(self.pen_pressure))
            client_wacom.send_message(mess_beta,float(self.active_y))
            client_wacom.send_message(mess_velocity, float(self.velocity))
            client_wacom.send_message(mess_instr, int(instrument_actif))
        elif self.instrument == 1:
            client_wacom.send_message(mess_is_down, 1)
            client_wacom.send_message(mess_x, float(self.pen_x_norm))
            client_wacom.send_message(mess_y, float(self.pen_y_norm))
            client_wacom.send_message(mess_press, float(self.pen_pressure))
            client_wacom.send_message(mess_instr,int(instrument_actif))

        event.accept()
        self.update() # Rafraîchissement visuel

    # ==========================================================================
    # FONCTION UTILITAIRE DE DESSIN
    # ==========================================================================
    def draw_pixmap_aspect_ratio(self, painter, pixmap, target_rect):
        """
        Dessine une image (QPixmap) dans un rectangle cible (QRect) 
        en conservant strictement son ratio (sans l'écraser) et en la centrant.
        """
        if pixmap is None or pixmap.isNull():
            return
            
        # On demande à l'image de générer une copie d'elle-même redimensionnée
        # à la taille de la zone cible, en respectant formellement le ratio.
        # Qt.SmoothTransformation garantit que l'image reste nette.
        scaled_pixmap = pixmap.scaled(
            target_rect.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        #Dessin de l'interface violon
        if self.instrument == 0:
            x_offset = target_rect.x() + (target_rect.width() - scaled_pixmap.width()) // 2 #On recentre l'image de la cartographie pour laisser de la place au schéma du violon
            y_offset = target_rect.y() + (target_rect.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x_offset, y_offset, scaled_pixmap)

        else:
            painter.drawPixmap(target_rect.x(), target_rect.y(), scaled_pixmap)


    # ==========================================================================
    # MOTEUR DE DESSIN PRINCIPAL (Rafraîchit l'interface)
    # ==========================================================================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing) # Lisse les formes géométriques
        painter.setRenderHint(QPainter.SmoothPixmapTransform) # Améliore la qualité du redimensionnement d'image
        
        w_half = int(self.width() / 2)
        w = self.width()
        h = self.height()

        # === INTERFACE VIOLON ===

        if self.instrument == 0:
            # Définition des zones d'affichage logique
            rect_zone_gauche = QRect(0, 0, w_half, h)
            rect_zone_droite = QRect(w_half, 0, w_half, h)

            # 1. ZONE GAUCHE : LE VIOLON
            # On peint un fond gris clair par défaut
            painter.fillRect(rect_zone_gauche, QColor(240, 240, 240))
            
            if not self.violin_pixmap.isNull():
                # Utilisation de notre fonction pour garder le ratio du violon
                self.draw_pixmap_aspect_ratio(painter, self.violin_pixmap, rect_zone_gauche)

            # --- LOGIQUE DE LA CORDE, DES MARQUEURS ET DU CURSEUR ---
            x_origine = 0.497
            y_origine_bas = 0.715
            y_haut = 0.110
            
            # Abscisse de la corde en pixels
            pixel_x_corde = int(x_origine * w_half)

            # Détermination de l'ordonnée (Y) qui va activer les marqueurs
            
            if self.current_zone == 0 and self.pen_pressure >0:
                self.active_y = self.pen_y_norm     # C'est le stylet qui active (gauche)
            elif self.current_zone == 1:
                self.active_y = self.current_beta   # C'est MaxMSP qui active (droite)

            # Dessin des 3 marqueurs
            for i in range(len(self.markers_norm_y)):
                m_y = self.markers_norm_y[i]
                # Conversion du repère normalisé vers les pixels réels de la fenêtre
                raw_y = m_y * (y_haut - y_origine_bas) + y_origine_bas
                pixel_y = int(raw_y * h)
                
                # Vérification : Est-ce que active_y est proche de ce marqueur ?
                if self.activation_list[i] <= self.active_y < self.activation_list[i+1]:
                    # Marqueur EN SURBRILLANCE (Jaune, plus épais et plus large)
                    painter.setPen(QPen(Qt.yellow, 6)) 
                    painter.drawLine(pixel_x_corde - 20, pixel_y, pixel_x_corde + 20, pixel_y)
                else:
                    # Marqueur NORMAL (Bleu, fin)
                    painter.setPen(QPen(Qt.blue, 3)) 
                    painter.drawLine(pixel_x_corde - 10, pixel_y, pixel_x_corde + 10, pixel_y)

            # Si le stylet touche la zone gauche, on dessine l'archet (rouge)
            if self.current_zone == 0 and self.pen_pressure > 0:
                bow_length = 150
                bow_thickness = 2 + int(self.pen_pressure * 15) 
                painter.setPen(QPen(QColor(200, 0, 0, 200), bow_thickness))
                painter.drawLine(int(self.pen_x - bow_length/2), int(self.pen_y), 
                                int(self.pen_x + bow_length/2), int(self.pen_y))
                
            # Dessin du curseur animé par MaxMSP (seulement si la zone droite est active)
            if self.current_zone == 1:
                raw_ext_y = self.current_beta * (y_haut - y_origine_bas) + y_origine_bas
                pixel_ext_y = int(raw_ext_y * h)
                
                # Curseur dessiné comme un petit rectangle rouge sur la corde
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(255, 0, 0, 200))
                painter.drawRect(pixel_x_corde - 25, pixel_ext_y - 3, 50, 6)

            #---------------------------------------------------------------------------------------------

            # 2. ZONE DROITE : LA CARTOGRAPHIE
            # Fond de sécurité
            painter.fillRect(rect_zone_droite, Qt.lightGray)
            
            if self.current_pixmap:
                # Utilisation de notre fonction pour garder le ratio de la carte
                self.draw_pixmap_aspect_ratio(painter, self.current_pixmap, rect_zone_droite)

            # Dessin de la CROIX (dernière position connue sur la carte)
            if self.last_map_x > -1:
                cross_size = 20
                painter.setPen(QPen(Qt.magenta, 3)) # Épaisseur 3, couleur Magenta
                
                # Ligne horizontale
                painter.drawLine(int(self.last_map_x - cross_size/2), int(self.last_map_y),
                                int(self.last_map_x + cross_size/2), int(self.last_map_y))
                # Ligne verticale
                painter.drawLine(int(self.last_map_x), int(self.last_map_y - cross_size/2),
                                int(self.last_map_x), int(self.last_map_y + cross_size/2))


            # 3. LIGNE DE SÉPARATION CENTRALE
            painter.setOpacity(1.0)
            painter.setPen(QPen(QColor(50, 50, 50), 2))
            painter.drawLine(w_half, 0, w_half, h)

            # 4. LÉGENDE D'INFORMATIONS (Coins arrondis)
            legend_path = QPainterPath()
            legend_rect_x, legend_rect_y = 15, 15
            legend_rect_w, legend_rect_h = 300, 200
            
            # Les "15, 15" à la fin définissent le rayon de courbure des coins
            legend_path.addRoundedRect(legend_rect_x, legend_rect_y, legend_rect_w, legend_rect_h, 15, 15)
            
            painter.fillPath(legend_path, QColor(255, 255, 255, 230)) # Fond blanc transparent
            painter.setPen(QPen(QColor(100, 100, 100), 2))            # Bordure grise
            painter.drawPath(legend_path)
            
            # Texte à l'intérieur
            painter.setPen(Qt.black)
            painter.setFont(self.legend_font)
            
            nom_zone = "Violon" if self.current_zone == 0 else "Carte"
            if self.current_zone == 0:
                info = (f"Note jouée\t: {NOTES[self.current_note_index - 1]}\n\n"
                        f"Zone active\t: {nom_zone}\n"
                        f"x (normalisé)\t: {self.pen_x_norm:.3f}\n"
                        f"y (normalisé)\t: {self.pen_y_norm:.3f}\n"
                        f"Pression\t: {self.pen_pressure:.2f}\n"
                        f"Vitesse de l'archet\t: {self.velocity:.2f}")
            else:
                info = (f"Note jouée\t: {NOTES[self.current_note_index - 1]}\n\n"
                        f"Zone active\t: {nom_zone}\n"
                        f"F_b\t: {self.pen_x_norm:.3f}\n"
                        f"v_b\t: {self.pen_y_norm:.3f}\n"
                        f"Pression\t: {self.pen_pressure:.2f}")
                
            # Ajoute une petite marge (15px) à l'intérieur du rectangle pour que le texte respire
            text_rect = self.rect().adjusted(legend_rect_x + 15, legend_rect_y + 15, 0, 0)
            painter.drawText(text_rect, Qt.AlignTop | Qt.AlignLeft, info)


        # === INTERFACE CLARINETTE ===

        elif self.instrument == 1:
            # Définition de la zone d'affichage
            rect_zone = QRect(0, 0, w, h)

            painter.fillRect(rect_zone, Qt.lightGray) #Fond
            
            if self.current_pixmap:
                # Utilisation de notre fonction pour garder le ratio de la carte
                self.draw_pixmap_aspect_ratio(painter, self.current_pixmap, rect_zone)

            # Dessin de la CROIX (dernière position connue sur la carte)
            if self.last_map_x > -1:
                cross_size = 20
                painter.setPen(QPen(Qt.magenta, 3)) # Épaisseur 3, couleur Magenta
                
                # Ligne horizontale
                painter.drawLine(int(self.last_map_x - cross_size/2), int(self.last_map_y),
                                int(self.last_map_x + cross_size/2), int(self.last_map_y))
                # Ligne verticale
                painter.drawLine(int(self.last_map_x), int(self.last_map_y - cross_size/2),
                                int(self.last_map_x), int(self.last_map_y + cross_size/2))


            # 4. LÉGENDE D'INFORMATIONS (Coins arrondis)
            legend_path = QPainterPath()
            legend_rect_x, legend_rect_y = 15, 15
            legend_rect_w, legend_rect_h = 300, 200
            
            # Les "15, 15" à la fin définissent le rayon de courbure des coins
            legend_path.addRoundedRect(legend_rect_x, legend_rect_y, legend_rect_w, legend_rect_h, 15, 15)
            
            painter.fillPath(legend_path, QColor(255, 255, 255, 230)) # Fond blanc transparent
            painter.setPen(QPen(QColor(100, 100, 100), 2))            # Bordure grise
            painter.drawPath(legend_path)
            
            # Texte à l'intérieur
            painter.setPen(Qt.black)
            painter.setFont(self.legend_font)
            
            info = (f"Note jouée\t: {NOTES[self.current_note_index - 1]}\n\n"
                    f"Gamma\t: {self.pen_x_norm:.3f}\n"
                    f"Zeta\t: {self.pen_y_norm:.3f}\n"
                    f"Pression\t: {self.pen_pressure:.2f}\n")                        
                
            # Ajoute une petite marge (15px) à l'intérieur du rectangle pour que le texte respire
            text_rect = self.rect().adjusted(legend_rect_x + 15, legend_rect_y + 15, 0, 0)
            painter.drawText(text_rect, Qt.AlignTop | Qt.AlignLeft, info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TabletSampleWindow()
    window.showMaximized()
    sys.exit(app.exec_())