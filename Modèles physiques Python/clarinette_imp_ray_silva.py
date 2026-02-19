# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 16:19:48 2026

@author: colin
"""

###############################################################################
                    # MODELE PHYSIQUE DE CLARINETTE
                    
           # D'après l"article d'Ollivier, Dalmont, Kergomard
      # Fonction de réflexion d'après Guillemain, Kergomard, Voinier
###############################################################################


import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os
from time import time
from numba import njit

# PARAMETRES PHYSIQUES ET VARIABLES

T_sec = 1         # durée simulée (s)

# Paramètres physiques

T_deg = 20             # température (°C)
T_K = 273.15 + T_deg   # température (K)
c = 20.05*np.sqrt(T_K) # vitesse du son (m/s)
rho = 1.292*273.15/T_K # masse volumique de l'air (kg/m^3)
lv = 4e-8
lt = 5.6e-8
cp_over_cv = 1.402

# Paramètres d'anche et de résonateur

gamma = 0.38           # pression dans la bouche adimensionnée --> entre 1/3 et 1/2
zeta = 0.4            # paramètre d'ouverture d'anche adimensionné --> entre 0.2 et 0.6

H = 10**(-3)           # ouverture d'anche au repos (m)
w = 1.3*10**(-2)       # largeur du canal d'anche (m)
P_M = 10*10**3         # pression de plaquage (Pa)
Ks = P_M / H           # raideur anche (Pa/m)
P_m = gamma * P_M      # pression dans la bouche (Pa)
U_A = w*H*np.sqrt(2/rho*P_M)
Zc = zeta*P_M/U_A      # impédance caractéristique (kg/s)
S = rho*c/Zc           # section du résonateur (m^2)
R = np.sqrt(S/np.pi)   # rayon du résonateur (m)
L = 0.58               # longueur du résonateur (m)
alpha = 2/(R*c**(3/2)) * ( np.sqrt(lv) + (cp_over_cv-1)*np.sqrt(lt))

# Paramètres utiles pour la simulation

T = 2*L/c               # temps de parcours d'un aller-retour (s)
#delta_t = T/128         # pas de temps (s)
#fs = int(np.rint(1/delta_t)) # fréquence d'échantillonage
fs = 44100*2
delta_t = 1/fs

# FONCTIONS

# Caractéristique non-linéaire
@njit
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

@njit
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

@njit
def dichotomie(func, params, a, b, n, tol=1e-9):
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

D = int(np.rint(2*L/c * fs))
beta = 2*R/(c/fs)
n1 = 0.167
d1 = 1.393
d2 = 0.457

@njit
def execution(T_sec, delta_t):

    temps = np.arange(0, T_sec, delta_t)
    N = len(temps)
    
    # Initialisation
    U, P, P_ext, qh = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    
    # Boucle
    for n in range(1,N):
    
        # calcul de qh à l'instant
        if n >= 2 :
            qh_prev2 = qh[n-2]
        else : 
            qh_prev2 = 0
        
        if n >= D :
            q0_D = P[n-D] + Zc*U[n-D]
        else :
            q0_D = 0
            
        if n >= D+1 :
            q0_D1 = P[n-D-1] + Zc*U[n-D-1]
        else :
            q0_D1 = 0
        
        if n >= D+2:
            q0_D2 = P[n-D-2] + Zc*U[n-D-2]
        else :
            q0_D2 = 0
            
        qh[n] = -2*(1-d2*beta**2)*qh[n-1] - (1 - d1*beta + d2*beta**2)*qh_prev2 \
            - (1+n1*beta)*q0_D - 2*q0_D1 - (1-n1*beta)*q0_D2
        qh[n] /= (1 + d1*beta + d2*beta**2)
        
        # calcul de q et f à l'instant t
        # trouver l'intersection entre la courbe F(P) et la droite U = 1/Zc*(P-qh) par dichotomie
        P[n] = dichotomie(func_dicho, [qh[n],Zc], -P_M, P_M, n)
        U[n] = F(P[n])
        P_ext[n] = (P[n]+U[n] - (P[n-1]+U[n-1])) / delta_t
        
    return temps, U, P, P_ext, qh
     

start = time()
temps, U, P, P_ext, qh = execution(T_sec, delta_t)
stop = time()
print("Temps d'exécution (s) :", stop-start)
    
# AFFICHAGE

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

#%%

# TRACE FONCTION DE REFLEXION

T_sec = 1
fs = 44100*2
temps = np.arange(0, T_sec, 1/fs)
N = len(temps)

D = int(np.rint(2*L/c * fs))
beta = 2*R/(c/fs)
n1 = 0.167
d1 = 1.393
d2 = 0.457

q0 = np.zeros(N)
q0[0] = 1 # impulsion
qi = np.zeros(N)

for n in range(1,N):

    # calcul de qh à l'instant
    if n >= 2 :
        qi_prev2 = qi[n-2]
    else : 
        qi_prev2 = 0
    
    if n >= D :
        q0_D = q0[n-D]
    else :
        q0_D = 0
        
    if n >= D+1 :
        q0_D1 = q0[n-D-1]
    else :
        q0_D1 = 0
    
    if n >= D+2:
        q0_D2 = q0[n-D-2]
    else :
        q0_D2 = 0
        
    qi[n] = -2*(1-d2*beta**2)*qi[n-1] - (1 - d1*beta + d2*beta**2)*qi_prev2 \
        - (1+n1*beta)*q0_D - 2*q0_D1 - (1-n1*beta)*q0_D2
    qi[n] /= (1 + d1*beta + d2*beta**2)
    # print(qi[n])

# # fonction de réflexion théorique (pertes mais pas de rayonnement) --Chaigne
# r_th = np.zeros(N)
# x = 2*L
# B = 1.044/R * np.sqrt(2*lv/c)
# D2 = B*x/2
# r_th[D+1:] = D2/np.sqrt(np.pi) * np.exp(-D2**2/(temps[D+1:]-x/c))/(temps[D+1:]-x/c)**(3/2) * np.exp(-1.080*x*lv/R**2)
# r_th /= np.max(np.abs(r_th))

freq = np.linspace(0,fs, fs)
k = 2*np.pi*freq/c
z = np.exp(2j*np.pi*freq/fs)

R_e = np.fft.fft(qi,fs)
R_r = R_e * z**D
Z_r = Zc * (1+R_r) / (1-R_r)
Z_e = Zc * (1+R_e) / (1-R_e)

R_r3 = (1 + n1*1j*k*R) / (1 + d1*1j*k*R + d2*(1j*k*R)**2)
R_r2 = ((1+n1*beta)+2*z**(-1)+(1-n1*beta)*z**(-2))/((1+d1*beta+d2*beta**2)+2*(1-d2*beta**2)*z**(-1)+(1-d1*beta+d2*beta**2)*z**(-2))
R_e2 = R_r2 * z**(-D)
Z_r2 = Zc * (1+R_r2) / (1-R_r2+1e-14)
Z_r3 = Zc * (1+R_r3) / (1-R_r3+1e-14)
Z_e2 = Zc * (1+R_e2) / (1-R_e2)
r2 = np.fft.ifft(R_r2,fs)

plt.figure()
plt.plot(temps,qi)
plt.xlabel("$t$ (s)")
plt.ylabel("$r(t)$")
plt.title("Fonction de réflexion")
plt.xlim(0.002,0.006)
plt.grid()

plt.figure()
plt.subplot(211)
plt.plot(freq,np.abs(R_e))
#plt.plot(freq,np.abs(R_e2),'--')
plt.ylabel(r"$|R_e|$")
plt.xlim(0,fs/2)
plt.grid()
plt.subplot(212)
plt.plot(freq,np.abs(R_r))
#plt.plot(freq,np.abs(R_r2),'--')
#plt.plot(freq,np.abs(R_r3),'--')
plt.ylabel(r"$|R_R|$")
plt.xlabel(r"Frequence $f$ (Hz)")
plt.xlim(0,fs/2)
plt.grid()

plt.figure()
plt.subplot(221)
plt.plot(freq, np.abs(Z_r))
#plt.plot(freq, np.abs(Z_r2),'--')
#plt.plot(freq, np.abs(Z_r3),'--')
plt.ylabel(r"$|Z_R|$")
plt.xlim(-1000,fs/2)
plt.grid()
plt.subplot(223)
plt.plot(freq, np.abs(Z_e))
#plt.plot(freq, np.abs(Z_e2),'--')
plt.ylabel(r"$|Z_e|$")
plt.xlabel(r"Frequence $f$ (Hz)")
plt.xlim(-1000,fs/2)
plt.grid()
plt.subplot(222)
plt.plot(freq,Z_r.real)
#plt.plot(freq, np.real(Z_r2),'--')
plt.ylabel(r"Re($Z_R$)")
plt.xlim(-1000,fs/2)
plt.grid()
plt.subplot(224)
plt.plot(freq,np.angle(Z_r))
#plt.plot(freq, np.angle(Z_r2),'--')
plt.ylabel(r"Im($Z_R$)")
plt.xlabel(r"Frequence $f$ (Hz)")
plt.xlim(-1000,fs/2)
plt.grid()

#%%

# EXPORT AUDIO

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
    write(title+'.mp3',fs,data_norm.astype(np.int16))
    
wave(P, fs, "clarinette_silva_g0.38_z0.4")
    
