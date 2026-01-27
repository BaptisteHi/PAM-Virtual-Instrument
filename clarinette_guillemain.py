# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 10:15:07 2026

@author: colin
"""

###############################################################################
                    # MODELE PHYSIQUE DE CLARINETTE
                    
      # D'après l"article de Guillemain, Kergomard et Voinier
###############################################################################


import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os

# PARAMETRES PHYSIQUES ET VARIABLES

T_sec = 1           # durée simulée (s)

# Paramètres physiques

T_deg = 20             # température (°C)
T_K = 273.15 + T_deg   # température (K)
c = 20.05*np.sqrt(T_K) # vitesse du son (m/s)
rho = 1.292*273.15/T_K # masse volumique de l'air (kg/m^3)
lv = 4e-8
lt = 5.6e-8
cp_over_cv = 1.4

# Paramètres d'anche et de résonateur

H = 1e-3               # ouverture d'anche au repos (m)
w = 1.3e-2             # largeur du canal d'anche (m)
fr = 2205              # fréquence de résonance de l'anche (Hz)
omr = 2*np.pi*fr       # pulsation de résonance de l'anche (rad/s)
qr = 0.3               # amortissement de l'anche 

P_M = 10e3             # pression de plaquage (Pa)
Ks = P_M / H           # raideur anche (Pa/m)
gamma = 0.4            # pression dans la bouche adimensionnée --> entre 1/3 et 1/2
P_m = gamma * P_M      # pression dans la bouche (Pa)
zeta = 0.4             # paramètre d'ouverture d'anche adimensionné --> entre 0.2 et 0.6

l = 0.66               # longueur du résonateur (m)
R = 7e-3               # rayon du résonateur (m)
l_corr = 0.6133*R      # longueur de correction due au rayonnement (m) (piston non encastré)
L = l+l_corr
S = np.pi*R**2         # section du résonanter (m^2)
Zc = rho*c/S           # impédance caractéristique (kg/s)
om1 = c*np.pi*1/2/L    # première pulsation de résonance du tube (rad/s)
om2 = c*np.pi*3/2/L    # deuxième

# Paramètres utiles pour la simulation


fe = 44100              # fréquence d'échantillonage (Hz)
delta_t = 1/fe          # pas de temps (s)


# FONCTIONS

D = int(np.rint(2*fe*L/c)) # délai en échantillon pour faire un aller retour dans le tube

c1 = np.cos(om1/fe)
c2 = np.cos(om2/fe)
alpha = 2/(R*c**(3/2)) * ( np.sqrt(lv) + (cp_over_cv-1)*np.sqrt(lt))
F1 = np.exp(-2*alpha*c*np.sqrt(om1/2)*L)
F2 = np.exp(-2*alpha*c*np.sqrt(om2/2)*L)
F12 = F1-F2
A1 = F1*c1
A2 = F2*c2
A12 = A1-A2

a1 = ( A12 - np.sqrt(A12**2-F12**2)) / F12
b0 = np.sqrt( 2*F1*F2*(c1-c2) * (A12-np.sqrt(A12**2-F12**2))) / F12

a_0a = fe**2/omr**2 + fe*qr/(2*omr)
b_1a = 1/a_0a
a_1a = (2*fe**2/omr**2 - 1) / a_0a
a_2a = ( fe*qr/(2*omr) - fe**2/omr**2) / a_0a
b_c0 = 1

def V(u_prev, u_delay, p_prev, p_delay, a1=a1, b0=b0):
    return - a1*u_prev - b0*u_delay + a1*p_prev - b0*p_delay

def W(x, gamma=gamma, zeta=zeta):
    heaviside = max(0, 1-gamma+x)/(1-gamma+x)
    return heaviside * zeta * (1-gamma+x)


# BOUCLE TEMPORELLE

# Initialisation
temps = np.arange(0, T_sec, delta_t)
N = len(temps)
u = np.zeros(N)        # débit à l'entrée du tube adimensionné
p = np.zeros(N)        # pression à l'entrée adimensionnée
x = np.zeros(N)        # déplacement de l'anche adimensionné 
p_ext = np.zeros(N)    # pression sortant du tube 

# Boucle
for n in range(2, N):
    x[n] = b_1a*p[n-1] + a_1a*x[n-1] + a_2a*x[n-2]
    W_n = W(x[n])
    if n >= D :
        p_delay = p[n-D]
        u_delay = u[n-D]
    else :
        p_delay = 0
        u_delay = 0
    V_n = V(u[n-1], u_delay, p[n-1], p_delay)
    u[n] = 1/2 * (gamma-V_n)/np.abs(gamma-V_n) * (-b_c0*W_n**2 + W_n*np.sqrt((b_c0*W_n)**2+4*np.abs(gamma-V_n)))
    p[n] = b_c0*u[n] + V_n
    p_ext[n] = (p[n]+u[n] - (p[n-1]+u[n-1])) / delta_t

# Variables dimensionnées
u_dim = P_M/Zc * u
p_dim = P_M * p
y_dim = H * (x-gamma)
p_ext_dim = P_M * p_ext

# AFFICHAGE

plt.figure(figsize=(8,10))
plt.subplot(411)
plt.plot(temps,u_dim)
plt.grid()
plt.ylabel(r"Débit $u_e(t)$ (m$^3$/s)")
plt.subplot(412)
plt.plot(temps,p_dim)
plt.grid()
plt.ylabel(r"Pression $p_e(t)$ (Pa)")
plt.subplot(413)
plt.plot(temps,p_ext_dim)
plt.grid()
plt.ylabel(r"Pression ext $p_{ext}(t)$ (Pa)")
plt.subplot(414)
plt.plot(temps,y_dim)
plt.plot(temps,y_dim)
plt.grid()
plt.ylabel(r"Déplacement $y(t)$")
plt.xlabel(r"Temps $t$ (s)")

#%%

# AUDIO

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
    
wave(p_dim,fe, "clarinette_guillemain_p")
wave(p_ext_dim,fe, "clarinette_guillemain_pext")


#%%

# FIGURES DE L'ARTICLE
plt.close('all')

temps = np.arange(0,1,1/fe)     # tableau d'instants temporels (s)
freq = np.arange(0, fe/2)    # tableau de fréquences (Hz)
om = 2*np.pi*freq                    # tableau de pulsations (rad/s)

k = om/c - 1j**(3/2)/2*alpha*c*om**(1/2)  # tableau de vecteurs d'ondes (1/m)


# TEMPS CONTINU

# Pertes
F = np.exp(-1j*k*L)

# Fonction de transfert de l'anche
Hr = omr**2 / (omr**2-om**2+1j*om*qr*omr)
# Réponse impulsionnelle de l'anche
xr = 2*omr/np.sqrt(4-qr**2) * np.exp(-1/2*omr*qr*temps) * np.sin(1/2*np.sqrt(4-qr**2)*omr*temps)

# Caractéristique NL
p = np.linspace(-1,1,1000)
x = p # cas de omr = infini
heaviside = np.zeros(len(p))
for i in range(len(p)):
    heaviside[i] = max(0, 1-gamma+x[i])/(1-gamma+x[i])
u = heaviside * zeta*(1-gamma+x) * (gamma-p)/np.abs(gamma-p) * np.sqrt(np.abs(gamma-p))

# Impédance d'un résonateur cylindrique
Z = 1j*np.tan(k*L)
# Réponse impulsionnelle d'un résonateur cylindrique
h = np.fft.ifft(Z,fe)

# Fonction de réflexion d'un résonateur cylindrique
Ref = -np.exp(-2*1j*k*L)
r = np.fft.ifft(Ref,fe)


# TEMPS DISCRET

om_tilde = om/fe
z = np.exp(1j*om_tilde)

# Impédance d'entrée du résonateur
Z_discret = (1-a1*z**(-1)-b0*z**(-D)) /  (1-a1*z**(-1)+b0*z**(-D))
# Réponse impulsionnelle
u_dirac = np.zeros(fe)
u_dirac[0] = 1
p_discret = np.zeros(fe)
for n in range(1,fe):
    if n >= D:
        p_delay = p_discret[n-D]
        u_delay = u_dirac[n-D]
    else:
        p_delay = 0
        u_delay = 0
    p_discret[n] = u_dirac[n] + a1*u_dirac[n-1] - b0*u_delay + a1*p_discret[n-1] - b0*p_delay

# Fonction de réflexion
R_discret = (Z_discret-1)/(Z_discret+1)
p_plus = np.zeros(fe)
p_plus[0] = 1
p_minus = np.zeros(fe)
for n in range(1,fe):
    if n >= D :
        p_plus_delay = p_plus[n-D]
    else :
        p_plus_delay = 0
    p_minus[n] = a1*p_minus[n-1] - b0*p_plus_delay


# Fonction de transfert de l'anche
Hr_discret = omr**2 / ( omr**2 + fe**2*(z-2+1/z) + fe/2*(z-1/z)*qr*omr)
# Réponse impulsionelle de l'anche
p_dirac = np.zeros(fe)
p_dirac[0] = 1
xr_discret = np.zeros(fe)
for n in range(1,fe):
    if n == 1:
        x_prev2 = 0
    else :
        x_prev2 = xr_discret[n-2]
    xr_discret[n] = b_1a*p_dirac[n-1] + a_1a*xr_discret[n-1] + a_2a*x_prev2

plt.figure()
plt.plot(freq, np.abs(F))
plt.grid()
plt.xlabel(r"Fréquence $f$ (Hz)")
plt.ylabel(r"$|F(\omega)|$")
plt.title("Filtre des pertes")

plt.figure()
plt.subplot(211)
plt.plot(freq,Hr,label='exact')
plt.plot(freq,Hr_discret,'--',label='approx')
plt.grid()
plt.legend()
plt.xlabel(r"Fréquence $f$ (Hz)")
plt.ylabel(r"$X(\omega)/P_e(\omega)$")
plt.title("Fonction de transfert de l'anche")
plt.subplot(212)
plt.plot(temps[:200],xr[:200]/np.max(xr)*np.max(xr_discret),label='exact')
plt.plot(temps[:200],xr_discret[:200],'--',label='approx')
plt.grid()
plt.legend()
plt.xlabel(r"Temps $t$ (s)")
plt.ylabel(r"$x(t)$")
plt.title("Réponse impulsionnelle de l'anche")

plt.figure()
plt.plot(p,u)
plt.grid()
plt.xlabel(r"Pression adimensionée $p_e$")
plt.ylabel(r"Débit acoustique adimensionné $u_e$")
plt.title("Caractéristique non linéaire de l'anche sans masse")

plt.figure()
plt.subplot(211)
plt.plot(freq,Z,label='exact')
plt.plot(freq,Z_discret,'--',label='approx')
plt.grid()
plt.legend()
plt.xlabel(r"Fréquence $f$ (Hz)")
plt.ylabel(r"Impédance $Z_e(\omega)$")
plt.title("Impédance d'entrée d'un résonateur cylindrique")
plt.subplot(212)
plt.plot(temps[:1100],h[:1100],label='exact')
plt.plot(temps[:1100],p_discret[:1100],'--',label='approx')
plt.grid()
plt.legend()
plt.xlabel("Temps $t$ (s)")
plt.ylabel("Réponse impulsionnelle")
plt.title("Réponse impulsionnelle d'un résonateur cylindrique")

plt.figure()
plt.subplot(211)
plt.plot(freq,Ref,label='exact')
plt.plot(freq,R_discret,'--',label='approx')
plt.grid()
plt.legend()
plt.xlabel(r"Fréquence $f$ (Hz)")
plt.ylabel(r"$R(\omega)$")
plt.title("Fonction de réflexion")
plt.subplot(212)
plt.plot(temps,r,label='exact')
plt.plot(temps,p_minus,'--',label='approx')
plt.grid()
plt.xlabel(r"Temps $t$ (s)")
plt.ylabel(r"$r(t)$")

    
