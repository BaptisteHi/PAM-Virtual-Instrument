import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QTabletEvent, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel

from time import sleep
from pythonosc import udp_client
import time

adress_wacom = "127.0.0.1"
port_wacom = 5012
client_wacom = udp_client.SimpleUDPClient(adress_wacom, port_wacom)
mess_x = "/x"
mess_y = "/y"
mess_press = "/pressure"
mess_is_down = "/is_down"

class TabletSampleWindow(QWidget):
    def __init__(self, parent=None):
        super(TabletSampleWindow, self).__init__(parent)
        # Amélioration 1 : Active le suivi même sans toucher la surface
        self.setAttribute(Qt.WA_TabletTracking) 
        
        self.pen_is_down = False
        self.pen_x = 0.0
        self.pen_y = 0.0
        self.pen_pressure = 0.0
        self.text = "Approchez le stylet..."
        
        self.setWindowTitle("Wacom Tablet Test")

        label = QLabel(self)
        pixmap = QPixmap("./notebooks/wacom/carto_test_wacom.jpeg")
        label.setPixmap(pixmap)
        #self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

    def tabletEvent(self, event):
        # Amélioration 2 & 3 : Utilisation de posF() pour la précision sub-pixel et coordonnées locales
        pos = event.posF()
        self.pen_x = pos.x()
        self.pen_y = pos.y()
        self.pen_pressure = event.pressure()

        # Envoi des positions et de la pression vers Max


        eventType = event.type()
        
        if eventType == QTabletEvent.TabletPress:
            self.pen_is_down = True
            self.text = "Click!"
        elif eventType == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            self.text = "Relachement"
        elif eventType == QTabletEvent.TabletMove:
            self.text = "Mouvement"
        
        if self.pen_is_down == False:
            client_wacom.send_message(mess_is_down, 0)
        else:
            client_wacom.send_message(mess_is_down, 1)
            client_wacom.send_message(mess_x, self.pen_x)
            client_wacom.send_message(mess_y, self.pen_y)
            client_wacom.send_message(mess_press, self.pen_pressure)

        # Force la mise à jour de l'affichage
        event.accept()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        # Affichage des données brutes
        info = (f"État: {self.text}\n"
                f"X: {self.pen_x:.2f}\n"
                f"Y: {self.pen_y:.2f}\n"
                f"Pression: {self.pen_pressure:.4f} / 1.0\n"
                f"Contact: {'OUI' if self.pen_is_down else 'NON'}")
        
        painter.drawText(self.rect().adjusted(10, 10, -10, -10), Qt.AlignTop | Qt.AlignLeft, info)
        
        # Visualisation de la pression (cercle qui grossit)
        radius = 10 + (self.pen_pressure * 50)
        painter.drawEllipse(int(self.pen_x - radius), int(self.pen_y - radius), int(radius * 2), int(radius * 2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TabletSampleWindow()
    window.show()
    sys.exit(app.exec_())