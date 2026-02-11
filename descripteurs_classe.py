"""
@Lalie
Le fichier contenant les descripteurs 

Commande utile :
from descripteurs_classe import Classifieur_son, Classifieur_justesse

Comment les utiliser ?
 - définir un signal de pression P
 - pour la justesse, entrer la longueur L et le rayon a avec la méthode .set_f_ref(L,a)

 - Pour obtenir la valeur du descripteur : utiliser la méthode .descripteur(P) 
 - Pour obtenir un label (0 ou 1) : utiliser la méthode .classify(P) 

 - changer les seuils : .set_seuil(eps)
 - obtenir la fréquence à partir d'un signal de pression : Classifieur_justesse.get_pitch(P)
"""

import numpy as np

class Classifieur_son:
    
    def __init__(self, eps1 = 10**(-2)):
        self.eps1 = eps1
    
    def set_seuil(self, eps):
        self.eps1 = eps
    
    def descripteur(self, P) :
        """
        Renvoie la valeur de la pression moyennée sur le dernier tiers des échantillons
        """ 
        N = len(P)
        N_tiers = N // 3
        P_tiers = P[2*N_tiers:]
        return np.mean(P_tiers)
    
    def classify(self, P) :
        """
        Renvoie 0 si les paramètres ne permettent pas de produire un son, 1 sinon.  
        """
        D_son = self.descripteur(P)
        c = -1
        if D_son > self.eps1 : 
            c = 1 
        return c
    
class Classifieur_justesse():

    def __init__(self, eps2 = 5, fs=44100*2, fmin = 50, fmax = 2e4, L_sec = 0.1, H = 4):
        self.eps2 = eps2 # l'écart maximal en cents à la note de référence. Par défaut : 5 cents
        # params fft
        self.fs = fs
        self.L_sec = L_sec
        self.L_n = int(L_sec*self.fs)
        self.Nfft = 4*self.nextpow2(self.L_n)
        # params produit spectral
        self.H = H
        self.fmin = fmin
        self.fmax = fmax

    def set_f_ref(self, L, a, c = 343) : 
            self.f_ref = c/(4*(L+0.6133*a))
            return self.f_ref
    
    def set_seuil(self, eps):
        """
         eps: écart maximal en cents
        """
        self.eps2 = eps 

    def nextpow2(self, i):
        n = 1
        while n < i:
            n *= 2
        return n
    
    def get_spectre(self, x):
        sig = x[:self.L_n]*np.hamming(self.L_n)
        fftFreq_hz_v = np.abs(np.fft.fftfreq(self.Nfft, d=1/self.fs))
        fftAmpl_v = np.abs(np.fft.fft(sig, self.Nfft))
        return fftFreq_hz_v, fftAmpl_v

    def get_pitch(self, P):
        fftFreq_hz_v, fftAmpl_v = self.get_spectre(P)
        R = int(self.Nfft/(2*self.H) + 1)
        spAmpl_v = np.ones(R)
        spFreq_hz_v = fftFreq_hz_v[:R]
        for h in range(self.H) :
          X = fftAmpl_v[::h+1] 
          spAmpl_v = spAmpl_v*X[:R]
        Nmin = int(self.fmin*self.Nfft/self.fs)
        Nmax = min(R,int(self.fmax*self.Nfft/self.fs))
        i_max = np.argmax(spAmpl_v[Nmin:Nmax]) + Nmin
        f0_hz = spFreq_hz_v[i_max]
        return f0_hz

    def descripteur(self, P):
        f_act = self.get_pitch(P)
        D_note = 1200*np.log2(f_act/self.f_ref)
        return D_note
    
    def classify(self,P):
        """
        Renvoie 0 si la note n'est pas juste, 1 sinon.  
        """
        c = -1
        D_note  = self.descripteur(P)
        if np.abs(D_note) < self.eps2 :
            c = 1
        return c