# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 09:20:24 2026

@author: colin
"""

###############################################################################
                    # MODELE PHYSIQUE DE CLARINETTE
                    
           # D'après l"article d'Ollivier, Dalmont, Kergomard
###############################################################################


import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os

# PARAMETRES PHYSIQUES ET VARIABLES

T_sec = 0.1           # durée simulée (s)

# Paramètres physiques

T_deg = 20             # température (°C)
T_K = 273.15 + T_deg   # température (K)
c = 20.05*np.sqrt(T_K) # vitesse du son (m/s)
rho = 1.292*273.15/T_K # masse volumique de l'air (kg/m^3)

# Paramètres d'anche et de résonateur

H = 10**(-3)           # ouverture d'anche au repos (m)
w = 1.3*10**(-2)       # largeur du canal d'anche (m)
P_M = 10*10**3         # pression de plaquage (Pa)
Ks = P_M / H           # raideur anche (Pa/m)
gamma = 0.42           # pression dans la bouche adimensionnée
P_m = gamma * P_M      # pression dans la bouche (Pa)
zeta = 0.6             # paramètre d'ouverture d'anche adimensionné
U_A = w*H*np.sqrt(2/rho*P_M)
Zc = zeta*P_M/U_A      # impédance caractéristique (kg/s)
S = rho*c/Zc           # section du résonateur (m^2)
L = 0.66               # longueur du résonateur (m)

# Paramètres utiles pour la simulation

T = 2*L/c               # temps de parcours d'un aller-retour (s)
delta_t = T/128         # pas de temps (s)



# FONCTIONS

# Fonction de réflexion 
def reflexion(t, width_T=0.1, T=T):
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
    A = np.trapz(gauss, dx=delta_t) # intégration trapézoïdale
    a = -1/A
    return a*gauss
    
    
# Caractéristique non-linéaire
def F(P, gamma=gamma, zeta=zeta, P_M=P_M, Zc=Zc):
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


def func_dicho(P, params):
    """
    Fonction dont on veut trouver le zéro par dichotomie
    
    Parameters
    ----------
        P : float, valeur de la pression dans le bec à laquelle on évalue la fonction
        params : array
    """
    qh, Zc = params[0], params[1]
    return F(P) - 1/Zc*(P-qh)


def dichotomie(func, params, a, b, tol=1e-9):
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

time = np.arange(start=0, stop=T_sec, step=delta_t)
N = len(time)

# Initialisation
U, P, qh = np.zeros(N), np.zeros(N), np.zeros(N)
r = reflexion(time)
# print(np.trapz(r,dx=delta_t))

# Boucle
for n in range(1,N):

    # calcul de qh à l'instant t
    P_reverse = P[:n][::-1]
    U_reverse = U[:n][::-1]
    qh[n] = np.sum(r[:n] * (P_reverse + Zc*U_reverse)) * delta_t
    
    
    # calcul de q et f à l'instant t
    # trouver l'intersection entre la courbe F(P) et la droite U = 1/Zc*(P-qh) par dichotomie
    P[n] = dichotomie(func_dicho, [qh[n],Zc], -P_M, P_M)
    U[n] = F(P[n])

    
# AFFICHAGE

plt.figure()
plt.subplot(311)
plt.plot(time,P)
plt.ylabel(r"$P$")
plt.grid()

plt.subplot(312)
plt.plot(time,U)
plt.ylabel(r"$U$")
plt.grid()

plt.subplot(313)
plt.plot(time,qh)
plt.xlabel(r"Temps $t$ (s)")
plt.ylabel(r"$q_h$")
plt.grid()
plt.show()

#%%

Pvals = np.linspace(-10000,8000,1000)
Uvals = np.zeros(len(Pvals))
for i in range(len(Pvals)):
    Uvals[i] = F(Pvals[i])
    
uvals = Uvals*Zc/P_M
pvals = Pvals/P_M
    
U_droite = 1/Zc * (Pvals-1)
u_droite = U_droite*Zc/P_M

plt.figure()
plt.plot(Pvals,Uvals)
plt.plot(Pvals,U_droite)
plt.grid()
plt.title("Grandeurs dimensionnées")
plt.xlim(-10000,8000)
plt.ylim(-0.4*P_M/Zc,0.4*P_M/Zc)

# plt.figure()
# plt.plot(pvals,uvals)
# plt.plot(pvals,u_droite)
# plt.grid()
# plt.title("Grandeurs adimensionnées")
# plt.xlim(-1,0.8)
# plt.ylim(-0.4,0.4)
# plt.show()

#%%

main_path = os.path.expanduser('~') + "\Documents\M2 ATIAM\Projets et applications musicales\Modele physique"
os.chdir(main_path+'\Audio')

def wave(data,fs,title):
    """
    write a wave audio file

    Parameters
    ----------
    data : 1D-array, values to be written
    fs : int, sample rate
    title : str, title of the wave file
    """
    # normalize the data to have a good amplitude in 16-bit
    amplitude = np.iinfo(np.int16).max
    data_norm = data/np.max(data)*int(amplitude/2)
    write(title+'.wav',fs,data_norm.astype(np.int16))
    
wave(P, int(128/T), "clarinette_ollivier")
    
