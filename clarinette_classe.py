

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os
from time import time
from numba import njit

class Clarinette_DelayLine: 

    def __init__(self, L = 0.66, dur = 0.1, temperature = 20, w = 1.3e-2, H = 1e-3, P_M = 1e4):
        self.dur = dur                           # durée simulée (s)
        # paramètres physiques
        self.temperature = 273.15 + temperature  # température (K)
        self.c = 20.05*np.sqrt(temperature)      # vitesse du son (m/s)
        self.rho = 1.292*273.15/temperature      # masse volumique de l'air (kg/m^3)
        # paramètres instrument
        self.H = H                       # ouverture d'anche au repos (m)
        self.w = w                       # largeur du canal d'anche (m)
        self.P_M = P_M                   # pression de plaquage (Pa)
        self.Ks = P_M / H                # raideur anche (Pa/m)
        self.U_A = w*H*np.sqrt(2/self.rho*P_M)
        self.L = L                       # longueur du résonateur (m)
        # Paramètres utiles pour la simulation
        self.T = 2*L/self.c                   # temps de parcours d'un aller-retour (s)
        self.delta_t = self.T/128        # pas de temps (s)

    def params_controle_musicien(self, gamma, zeta) : 
        self.gamma = gamma                    # pression dans la bouche adimensionnée --> entre 1/3 et 1/2
        self.zeta = zeta                      # paramètre d'ouverture d'anche adimensionné --> entre 0.2 et 0.6
        self.P_m = gamma * self.P_M           # pression dans la bouche (Pa)
        self.Zc = zeta*self.P_M/self.U_A      # impédance caractéristique (kg/s)
        self.S = self.rho*self.c/self.Zc           # section du résonateur (m^2)

        # AFFICHAGE

    def affiche_result(self):        
        start = time()
        temps, U, P, qh, r = self.execution(self.dur, self.delta_t)
        stop = time()
        print("Temps d'exécution (s) :", stop-start)
            
        plt.figure()
        plt.subplot(311)
        plt.plot(temps,P)
        plt.ylabel(r"$P$ (Pa)")
        plt.grid()

        plt.subplot(312)
        plt.plot(temps,U)
        plt.ylabel(r"$U$ (m$^3$/s)")
        plt.grid()

        plt.subplot(313)
        plt.plot(temps,qh)
        plt.xlabel(r"Temps $t$ (s)")
        plt.ylabel(r"$q_h$")
        plt.grid()
        plt.show()

    # FONCTIONS

    # Fonction de réflexion 
    def reflexion(self, t, T, width_T=0.1):
        """
        Fonction de réflexion r(t), de la forme gaussienne :
            r(t) = a * exp[-b(t-T)^2]

        Parameters
        ----------
            t : float ou array, instant temporel >= 0 (s)
            width_T : float, largeur à mi-hauteur en proportion de T (en %)
            T : float, temps de parcours aller-retour (s)
            
        Returns
        -------
            float ou array, valeur de la fonction de réflexion en t
        """
        b = 4 * np.log(2) / (width_T*T)**2
        gauss = np.exp(-b * (t-T)**2)
        A = np.trapz(gauss, dx = self.delta_t) # intégration trapézoïdale
        a = -1/A
        return a*gauss
        
        
    # Caractéristique non-linéaire
    def F(self, P, gamma, zeta, P_M, Zc):
        """
        Caractéristique non-linéaire F telle que u = F(P_m-p)

        Parameters
        ----------
            P : float, pression dans le bec (Pa)
            gamma : float, pression dans la bouche adimensionnée
            zeta : float, paramètre d'ouverture d'anche adimensionné
            P_M : float, pression de plaquage
            Zc : float, impédance caractéristique
        Returns
        -------
            U : float, débit volumique dans le bec
        """
        p = P/P_M # pression adimensionnée
        if np.abs(gamma-p) <= 1:
            u = zeta * (1+p-gamma) * np.sqrt(np.abs(gamma-p)) * (gamma-p)/np.abs(gamma-p) # débit adimensionné
        else :
            u = 0
        U = u*P_M/Zc # débit dimensionné
        return U

    def func_dicho(self, P, params):
        """
        Fonction dont on veut trouver le zéro par dichotomie
        
        Parameters
        ----------
            P : float, valeur de la pression dans le bec à laquelle on évalue la fonction
            params : array
        """
        qh, Zc = params[0], params[1]
        return self.F(P, self.gamma, self.zeta, self.P_M, self.Zc) - 1/Zc*(P-qh)

    def dichotomie(self, func, params, a, b, n, tol=1e-9):
        """ 
        Trouver l'abcisse m tel que func(m) = 0 par dichotomie
        
        Parameters
        ----------
            func : fonction, fonction dont on cherche l'annulation
            params : array, paramètres d'entrée de la fonction
            a : float, borne minimale de l'intervalle de recherche
            b : float, borne maximale de l'intervalle de recherche
            tol : float, tolérance de précision sur la valeur de l'abcisse obtenue
            
        Returns
        -------
            m : float, abcisse pour laquelle la fonction s'annule
        """
        
        if func(a,params)*func(b,params) > 0:
            print("Mauvais choix des bornes de l'intervalle, n=",n)
        else :
            m = (a+b)/2
            
            while np.abs(a-b) > tol:
                if func(m,params) == 0.:
                    return m
                elif func(a,params)*func(m,params) > 0:
                    a = m
                else :
                    b = m
                m = (a+b)/2
                
            return m
        

    # BOUCLE TEMPORELLE
    def execution(self, T_sec, delta_t):

        temps = np.arange(0, T_sec, delta_t)
        N = len(temps)
        
        # Initialisation
        U, P, qh = np.zeros(N), np.zeros(N), np.zeros(N)
        
        # Calcul des fonctions de réflexion 
        Lwin = int(5 * self.T / delta_t)
        t_win = np.arange(0, Lwin) * delta_t
        r = self.reflexion(t_win, T = self.T)
        r_reverse = r[::-1].copy()
        
        # Initialisation du buffer circulaire 
        outgoing_hist = np.zeros(Lwin)
        
        # Boucle
        for n in range(1,N):
        
            # calcul de qh à l'instant t
            qh[n] = np.dot(r_reverse, outgoing_hist) * delta_t
            
            # calcul de q et f à l'instant t
            # trouver l'intersection entre la courbe F(P) et la droite U = 1/Zc*(P-qh) par dichotomie
            P[n] = self.dichotomie(self.func_dicho, [qh[n],self.Zc], -self.P_M, self.P_M, n)
            U[n] = self.F(P[n], self.gamma, self.zeta, self.P_M, self.Zc)
            
        
            # Mise à jour du buffer circulaire (rotation + ajout)
            w_new = P[n] + self.Zc * U[n]
            # Rotation des buffers 
            outgoing_hist[:-1] = outgoing_hist[1:]
            outgoing_hist[-1] = w_new
            
        return temps, U, P, qh, r


# Test 

# clar = Clarinette_DelayLine()
# clar.params_controle_musicien(0.42, 0.6)
# clar.affiche_result()