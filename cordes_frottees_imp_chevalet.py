# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 16:36:44 2026

@author: colin
"""

###############################################################################
                 # MODELE PHYSIQUE DE CORDES FROTTEES
                 
  # D'après les articles de Ollivier, Dalmont Kergomard & Weinreich, Causse
         # Point de contact entre l'archet et la corde : quelconque
                 # Ondes de torsion prises en compte
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os
from time import time
from numba import njit
import scipy.io


# PARAMETRES PHYSIQUES ET VARIABLES

T_sec = 0.1    # durée de la simulation (s)

# Paramètres physiques liés à la corde

L = 0.325                 # longueur de la corde (m)
d = 0.45e-3               # diamètre de la corde LA (m) 
R = d/2                   # rayon de la corde (m)
T = 6*9.81                # tension pour une corde de LA (N)
Area = np.pi*R**2         # section de la corde (m^2)
f0_vise = 440             # fréquence fondamentale visée (Hz)
mu = T/(2*f0_vise*L)**2   # masse linéique (kg/m)
rho = mu/Area             # masse volumique (kg/m3)
c = np.sqrt(T/mu)         # vitesse du son (m/s)
f0 = c/(2*L)              # fréquence fondamentale (Hz)
Zc = rho*c*Area           # impédance caractéristique (kg/s)
Yc = 1/Zc                 # admittance caractéristique (s/kg)
Yc_half = Yc/2 
    
# Paramètres physiques liés à l'archet

Fb = 0.2      # force de l'archet (N) -- valeur réaliste = < 5 N
vb = 0.45       # vitesse de l'archet (m/s) -- valeur réaliste < 0.5 m/s
v0 = 0.05     # paramètre de contrôle tenant compte des coeffs de viscosité dynamique et statique (m/s)
              # valeur isssue de l'article de Weinreich -- a priori ne pas le modifier
beta = 5/16   # ratio du point de contact entre la corde et l'archet


# Paramètres utiles pour la simulation

L_L = L*beta                 # longueur de la partie droite de la corde (m)
L_R = L*(1-beta)             # longueur de la partie droite de la corde (m)
T_L = 2*L_L/c                # temps de parcours d'un aller-retour sur la moitié gauche de la corde (s)
T_R = 2*L_R/c                # temps de parcours d'un aller-retour sur la moitié droite de la corde (s)
#delta_t = min(T_L, T_R)/128  # pas de temps (s)
fs = 44100
delta_t = 1/fs

# IMPORT DES DONNEES

main_path = os.path.expanduser('~') + "\Documents\M2 ATIAM\Projets et applications musicales"
os.chdir(main_path+'\File_Debut_Et_al_2010')

data = scipy.io.loadmat('CELLO_ModosXX.mat')

Nmod = int(data['Nmod'][0])
Wmod = data['Wmod'][:,0]*3
Fmod = data['Fmod'][:,0]
Zmod = data['Zmod'][:,0]
Mmod = data['Mmod'][:,0]/9


# FONCTIONS
    
# Caractéristique non-linéaire
@njit
def F(q, p=vb, Fb=Fb, v0=v0):
    """
    Caractéristique non-linéaire F telle que 
        f = F(q) = Fb * (p-q)/v0 / (1 + ((p-q)/v0)^2 )
    La pente en p=q est finie de manière à prendre en compte la torsion

    Parameters
    ----------
        q : float, vitesse transverse de la corde au point de contact avec l'archet
        p : float, vitesse de l'archet (fixe)
        Fb : float, force de l'archet
        v0 : float, paramètre de contrôle

    Returns
    -------
        f : float, force transverse appliquée sur la corde au point de contact
    """
    f = Fb * (p-q)/v0 / (1+((p-q)/v0)**2)
    return f

@njit
def F_deriv(q, p=vb, Fb=Fb, v0=v0):
    """
    Dérivée de la caractéristique non linéaire
    """
    df = -Fb/v0 * (v0**2-(p-q)**2) / (v0**2+(p-q)**2)**2
    return df

@njit
def func_Newton(q, params, Yc_half=Yc_half):
    """
    Fonction dont on veut trouver le zéro avec la méthode de Newton
    
    Parameters
    ----------
        q : float, vitesse transverse de la corde au point de contact avec l'archet
        params : array
        Yc : float, admittance caractéristique
    """
    q_iL, q_iR = params[0], params[1]
    return F(q) - 1/Yc_half*(q-q_iL-q_iR)

@njit
def func_deriv_Newton(q, params, Yc_half=Yc_half):
    """
    Dérivée de la fonction dont on veut trouver le zéro avec Newton
    """
    return F_deriv(q) - 1/Yc_half

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
    

@njit  
def Newton(func, func_deriv, params, x0, n, Yc_half=Yc_half, tol=1e-9, maxiter=1000):
    """ 
    Trouver l'abcisse m tel que func(m) = 0 par la méthode de Newton
    
    Parameters
    ----------
        func : fonction, fonction dont on cherche le zéro
        func_deriv : fonction, dérivée de la fonction func
        params : array, paramètres d'entrée de la fonction
        x0 : float, guess initial pour le zéro
        Yc : float, admittance caractéristique
        tol : float, tolérance de précision sur la valeur de l'abcisse obtenue
        maxiter : int, nombre maximal d'itérations
        
    Returns
    -------
        m : float, abcisse pour laquelle la fonction s'annule
    """
    x = x0
    for i in range(maxiter):
        f = func(x, params)
        df = func_deriv(x, params)
        
        if np.abs(df) < 1e-15:
            print("Erreur : division par 0 dans la méthode de Newton pour n =",n)
            break
        
        dx = f/df
        x = x - dx
        
        if np.abs(dx) < tol :
            return x
        
    if np.abs(dx) > tol :
        print(np.abs(dx))
        print("Erreur : la méthode de Newton n'a pas convergé pour n =",n)
        
    return x
    
@njit
def intersections(q_iL, q_iR, p, q_min, n, Yc_half=Yc_half):
    """
    Trouver les intersections entre la courbe non linéaire et la droite
    """

    inter = np.zeros((3,2))
    nb_inter = 0
    
    q_vals = np.linspace(q_min, -q_min, 100)
    params = [q_iL, q_iR]
    for i in range(1,len(q_vals)):
        if func_Newton(q_vals[i-1], params) * func_Newton(q_vals[i], params) < 0 :
            q_intersect = dichotomie(func_Newton, params, q_vals[i-1], q_vals[i], n)
            inter[nb_inter] = [q_intersect, F(q_intersect)]
            nb_inter += 1
            

    return inter, nb_inter 
    
@njit
def hysteresis(q_prev, state_prev, q_iL, q_iR, q_min, n, Yc_half=Yc_half, v0=v0, p=vb):
    """
    Trouver q et f à l'instant n en prenant en compte l'hystérésis
    Avec une dichotomie = méthode un peu plus lente mais plus robuste et précise
    """
    intersect, nb_inter = intersections(q_iL, q_iR, p, q_min, n)
    
    if nb_inter == 0 :
        print("Pas de point d'intersection trouvé pour n=",n)
    
    elif nb_inter == 1 :
        if np.abs(intersect[0,0]-p) <= v0:
            return intersect[0], 1
        else :
            return intersect[0], -1
    
    else :
        if nb_inter == 2:
            print("2 sols")
            
        # la solution n'est jamais celle du milieu
        # rester dans l'état précédent si c'est possible
        if state_prev == -1:
            return intersect[0], -1
        else :
            return intersect[-1], 1

@njit
def hysteresis2(q_prev, q_iL, q_iR, n, Yc_half=Yc_half, v0=v0, p=vb):
    """
    Trouver q et f à l'instant n en prenant en compte l'hystérésis
    Avec Newton  = méthode plus rapide mais moins précise
    """
    params = [q_iL, q_iR]
    x0 = q_prev # partir de la solution précédente pour rester dans le même régime
    q_sol = Newton(func_Newton, func_deriv_Newton, params, x0, n)
    f_sol = F(q_sol)
    
    return q_sol, f_sol

# BOUCLE TEMPORELLE
@njit
def execution(T_sec, delta_t):
    temps = np.arange(0., T_sec, delta_t)
    N = len(temps)
    state = np.zeros(N)  # -1 for slip, 1 for stick
    state[0] = -1
    
    # Initialisation
    f, q, q_iL, q_iR = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    
    D_R = int(np.rint(T_R*fs)) # temps de parcours aller-retour de la moitié droite de la corde en samples
    D_L = int(np.rint(T_L*fs))
    
    bm = 2*delta_t / Mmod
    a_m0 = (Wmod*delta_t)**2 + 4*Zmod*Wmod*delta_t + 4
    a_m1 = 2 * (Wmod**2*delta_t**2 - 4)
    a_m2 = (Wmod*delta_t)**2 - 4*Zmod*Wmod*delta_t + 4
    qo = np.zeros(N)
    qo[0] = 1
    fm = np.zeros((N,Nmod))
    qtot = np.zeros(N)
    
    # Boucle
    for n in range(1, N):
        
        # Côté tête du violon (impulsion)
        q_iR[n] = - (q_iL[n-D_R] + Yc_half*f[n-D_R])
        
        # Côté chevalet (admittance du chevalet)
        if n >= 2 :
            qi_prev2 = q_iL[n-2]
            fm_prev2 = fm[n-2,:]
            qtot_prev2 = qtot[n-2]
        else : 
            qi_prev2 = 0
            fm_prev2 = np.zeros(Nmod)
            qtot_prev2 = 0
        
        if n >= D_L :
            qo_D = 0.999*(q_iR[n-D_L] + Yc_half*f[n-D_L])
        else :
            qo_D = 0
            
        if n >= D_L+1 :
            qo_D1 = 0.999*(q_iR[n-D_L-1] + Yc_half*f[n-D_L-1])
        else :
            qo_D1 = 0
        
        if n >= D_L+2:
            qo_D2 = 0.999*(q_iR[n-D_L-2] + Yc_half*f[n-D_L-2])
        else :
            qo_D2 = 0
            
 
        gm = bm * (-qo_D - qi_prev2 +qo_D2) - a_m1*fm[n-1] - a_m2*fm_prev2
        
        q_iL[n] = (-qo_D - Zc * np.sum(gm/a_m0)) / (1 + Zc * np.sum(bm/a_m0))
        qtot[n] = q_iL[n] - qo_D

        fm[n] = (- a_m1*fm[n-1] - a_m2*fm_prev2 + bm*(qtot[n]-qtot_prev2)) / a_m0
        
        
        # Calcul de q et f à l'instant t
        # Méthode 1 : Dichotomie : plus lent mais plus précis
        [q[n], f[n]], s = hysteresis(q[n-1], state[n-1], q_iL[n], q_iR[n], q_min, n)
        state[n] = s
        # Méthode 2 : Newton : plus rapide mais moins précis
        #q[n], f[n] = hysteresis2(q[n-1], q_iL[n], q_iR[n], n)
           
        if n % 1000 == 0:
            print(f"Echantillon {n}/{N}")
    
    return temps, t_L, t_R, f, q, q_iL, q_iR, r_L, r_R
 
    
start = time()

q_vals = np.linspace(vb-100, vb+100, 10000)
f_vals = F(q_vals)
q_min = q_vals[np.argmin(np.abs(f_vals-0.01*np.max(f_vals)))]


temps, t_L, t_R, f, q, q_iL, q_iR, r_L, r_R = execution(T_sec, delta_t)
stop = time()
print("Temps d'exécution (s) :", stop-start)
    
# AFFICHAGE

#plt.close('all')

plt.figure()
plt.plot(q_vals,f_vals, 'k', lw=0.5)
plt.scatter(q, f, s=2, c='tab:red')
plt.grid()
plt.xlabel('$q$')
plt.ylabel('$f$')
plt.xlim(q_min,vb+abs(q_min))
plt.title("Parcours de la caractéristique NL")

plt.figure()
plt.title(r"$\beta =$"+str(beta)+", $F_b =$"+str(Fb)+ ", $v_b =$"+str(vb))
plt.subplot(311)
plt.plot(temps,q)
plt.ylabel(r"$q$")
plt.grid()

plt.subplot(312)
plt.plot(temps,f)
plt.ylabel(r"$f$")
plt.grid()

plt.subplot(313)
plt.plot(temps,q_iL,label=r'$q_{iL}$')
plt.plot(temps,q_iR,'--',label=r'$q_{iR}$')
plt.xlabel(r"Temps $t$ (s)")
plt.ylabel(r"$q_h$")
plt.grid()
plt.show()

#%%

main_path = os.path.expanduser('~') + "\Documents\M2 ATIAM\Projets et applications musicales"
os.chdir(main_path+'\File_Debut_Et_al_2010')

data = scipy.io.loadmat('CELLO_ModosXX.mat')

Nmod = int(data['Nmod'][0])
Wmod = data['Wmod'][:,0]
Fmod = data['Fmod'][:,0]
Zmod = data['Zmod'][:,0]
Mmod = data['Mmod'][:,0]

T_sec = 1
fs = 44100
Ts = 1/fs
temps = np.arange(0, T_sec, 1/fs)
N = len(temps)

D = int(np.rint(2*L_L/c*fs))
bm = 2*Ts / Mmod
a_m0 = (Wmod*Ts)**2 + 4*Zmod*Wmod*Ts + 4
a_m1 = 2 * (Wmod**2*Ts**2 - 4)
a_m2 = (Wmod*Ts)**2 - 4*Zmod*Wmod*Ts + 4
qo = np.zeros(N)
qo[0] = 1
qi = np.zeros(N)
fm = np.zeros((N,int(Nmod)))
qtot = np.zeros(N)

for n in range(1,N) :
    # calcul de qh à l'instant
    if n >= 2 :
        qi_prev2 = qi[n-2]
        fm_prev2 = fm[n-2,:]
        qtot_prev2 = qtot[n-2]
    else : 
        qi_prev2 = 0
        fm_prev2 = np.zeros(Nmod)
        qtot_prev2 = 0
    
    if n >= D :
        qo_D = qo[n-D]*0.999
    else :
        qo_D = 0
        
    if n >= D+1 :
        qo_D1 = qo[n-D-1]*0.999
    else :
        qo_D1 = 0
    
    if n >= D+2:
        qo_D2 = qo[n-D-2]*0.999
    else :
        qo_D2 = 0
    
    gm = bm * (-qo_D - qi_prev2 +qo_D2) - a_m1*fm[n-1] - a_m2*fm_prev2
    
    qi[n] = (-qo_D - Zc * np.sum(gm/a_m0)) / (1 + Zc * np.sum(bm/a_m0))
    qtot[n] = qi[n] - qo_D

    fm[n] = (- a_m1*fm[n-1] - a_m2*fm_prev2 + bm*(qtot[n]-qtot_prev2)) / a_m0
    
    

freq = np.linspace(0,fs, fs)
k = 2*np.pi*freq/c
z = np.exp(2j*np.pi*freq/fs)

R_e = np.fft.fft(qi,fs)
R_r = R_e * z**D
Y_r = Yc * (1+R_r) / (1-R_r)
Y_e = Yc * (1+R_e) / (1-R_e)

# théorie

W = 2 * np.pi * freq

H = np.zeros(len(W), dtype=complex)
for i in range(len(Wmod)):
    H_mod = 1j*W / (Mmod[i] * (Wmod[i]**2 - W**2 + 2j*W*Wmod[i]*Zmod[i]))
    H += H_mod

R_r2 = (H-Yc)/(H+Yc)
R_e2 = R_r2 * z**(-D)
r2 = np.fft.ifft(R_e2,fs)
Y_e2 =  Yc * (1+R_e2) / (1-R_e2)

plt.figure()
plt.plot(temps,qi)
plt.plot(temps,r2,'--')
plt.xlabel("Temps $t$ (s)")
plt.ylabel(r"$r_L(t)$")
plt.title("Fonction de réflexion côté chevalet")
plt.grid()
plt.xlim(0,0.1)

plt.figure()
plt.subplot(211)
plt.plot(freq,np.abs(R_e))
plt.plot(freq,np.abs(R_e2),'--')
plt.ylabel(r"$|R_e|$")
plt.xlim(0,fs/2)
plt.grid()
plt.subplot(212)
plt.plot(freq,np.abs(R_r))
plt.plot(freq,np.abs(R_r2),'--')
plt.ylabel(r"$|R_R|$")
plt.xlabel(r"Frequence $f$ (Hz)")
plt.xlim(0,fs/2)
plt.grid()

plt.figure()
plt.subplot(221)
plt.plot(freq, np.abs(Y_r))
plt.plot(freq,np.abs(H),'--')
plt.ylabel(r"$|Z_R|$")
plt.xlim(-1000,fs/2)
plt.grid()
plt.subplot(223)
plt.plot(freq, np.abs(Y_e))
plt.plot(freq, np.abs(Y_e2),'--')
plt.ylabel(r"$|Z_e|$")
plt.xlabel(r"Frequence $f$ (Hz)")
plt.xlim(-1000,fs/2)
plt.grid()
plt.subplot(222)
plt.plot(freq,Y_r.real)
plt.plot(freq,np.real(H),'--')
plt.ylabel(r"Re($Z_R$)")
plt.xlim(-1000,fs/2)
plt.grid()
plt.subplot(224)
plt.plot(freq,np.angle(Y_r))
plt.plot(freq,np.angle(H),'--')
plt.ylabel(r"Im($Z_R$)")
plt.xlabel(r"Frequence $f$ (Hz)")
plt.xlim(-1000,fs/2)
plt.grid()

plt.figure()
plt.semilogy(freq,np.abs(Y_r))
plt.semilogy(freq,np.abs(H),'--')
plt.grid()
plt.xlim(0,1500)
plt.xlabel("Frequence $f$ (Hz)")
plt.ylabel(r'$|Y_b|$')
plt.title("Admittance du chevalet")

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
    
wave(q, int(1/delta_t), "string_ollivier_dim5")