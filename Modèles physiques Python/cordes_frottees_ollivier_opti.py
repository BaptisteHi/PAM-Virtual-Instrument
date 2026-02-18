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


# Paramètres physiques liés au violon 

# Valeurs numériques de Schelleng, The violin as a circuit, 1963
f_T1 = 500             # fréquence de résonance du premier mode de table T1 (Hz)
S = 1.76e8*10**(-3)# raideur effective du corps du violon (N/m)
M = 17.8e-3      # masse effective du corps du violon (kg)
print("Amplitude bridge :",Yc**(-1)/(S*M)**(1/2))

# Paramètres utiles pour la simulation

L_L = L*beta                 # longueur de la partie droite de la corde (m)
L_R = L*(1-beta)             # longueur de la partie droite de la corde (m)
T_L = 2*L_L/c                # temps de parcours d'un aller-retour sur la moitié gauche de la corde (s)
T_R = 2*L_R/c                # temps de parcours d'un aller-retour sur la moitié droite de la corde (s)
delta_t = min(T_L, T_R)/128  # pas de temps (s)



# FONCTIONS

# Fonctions de réflexion 
@njit
def reflexion_left(t, width_T=0.039, T=T_L, Yc=Yc, S=S, M=M, Q=30, f_T1=500):
    """
    Fonction de réflexion r(t), de la forme gaussienne :
        r(t) = a * exp[-b(t-T)^2]
    Prise en compte des réflexions multiples du chevalet par une queue décroissante de la forme
        r(t) = Y^(-1)*(SM)^(-1/2) * Re(exp((jw-w/2Q)(t-T_L)))

    Parameters
    ----------
        t : array, instants temporels >= 0 (s)
        width_T : float, largeur à mi-hauteur en proportion de T (en %)
        T : float, temps de parcours aller-retour (s)
        amp : float, amplitude des réflexions multiples =  Y^(-1)*(SM)^(-1/2)
            avec Y admittance caract"ristique transverse (=2*Zc)
            et S, M la raideur et la masse effectives du chevalet
        Q : float, facteur de qualité du chevalet
        w_b : float, pulsation de résonance du chevalet
        
    Returns
    -------
        r : array, valeurs de la fonction de réflexion 
    """
    # pulse principale
    b = 4 * np.log(2) / (width_T*T)**2
    r = np.exp(-b * (t-T)**2)
    
    # réflexions multiples du chevalet
    w_T1 = 2*np.pi*f_T1
    sigma = np.sqrt(1/(2*b)) # écart-type de la gaussienne
    T_start = T + 3*sigma    
    istart = int(T_start/delta_t)
    amp =  Yc**(-1)/(S*M)**(1/2)
    r[istart:] =amp*np.real(np.exp((1j*w_T1-w_T1/(2*Q))*(t[istart:]-T)))
    
    A = np.sum(r) #np.trapz(r, dx=delta_t) # intégration trapézoïdale
    a = -1/A
    r = a*r
    
    return r

@njit
def reflexion_right(t, width_T=0.039, T=T_R):
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
    A = np.sum(gauss) #np.trapz(gauss, dx=delta_t) # intégration trapézoïdale
    a = -1/A
    return a*gauss
    
    
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
    
    q_vals = np.linspace(q_min, p+v0, 100)
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
        print("Pas de point d'intersection trouvé")
    
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
    
    # Calcul des fonctions de réflexion sur toute leur longueur
    Lwin_L = int(5 * T_L / delta_t)
    Lwin_R = int(5 * T_R / delta_t)
    print(Lwin_R)
    t_L = np.arange(0, Lwin_L) * delta_t
    t_R = np.arange(0, Lwin_R) * delta_t
    
    r_L = reflexion_left(t_L)
    r_R = reflexion_right(t_R)
    
    r_L_reverse = r_L[::-1].copy()
    r_R_reverse = r_R[::-1].copy()
    
    # Initialisation des buffers circulaires (ondes sortantes)
    outgoing_hist_left = np.zeros(Lwin_L)
    outgoing_hist_right = np.zeros(Lwin_R)
    
    
    # Boucle
    for n in range(1, N):
        
        # Convolution avec les buffers circulaires 
        q_iL[n] = np.dot(r_L_reverse, outgoing_hist_left) #* delta_t
        q_iR[n] = np.dot(r_R_reverse, outgoing_hist_right) #* delta_t
        
        # Calcul de q et f à l'instant t
        # Méthode 1 : Dichotomie : plus lent mais plus précis
        [q[n], f[n]], s = hysteresis(q[n-1], state[n-1], q_iL[n], q_iR[n], q_min, n)
        state[n] = s
        # Méthode 2 : Newton : plus rapide mais moins précis
        # q[n], f[n] = hysteresis2(q[n-1], q_iL[n], q_iR[n], n)
        
        # Mise à jour des buffers circulaires (rotation + ajout)
        w_new_left = q_iR[n] + Yc_half * f[n]
        w_new_right = q_iL[n] + Yc_half * f[n]
        
        # Rotation des buffers 
        outgoing_hist_left[:-1] = outgoing_hist_left[1:]
        outgoing_hist_left[-1] = w_new_left
        
        outgoing_hist_right[:-1] = outgoing_hist_right[1:]
        outgoing_hist_right[-1] = w_new_right
        
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
plt.plot(t_L,r_L,label='left')
plt.plot(t_R,r_R,'--',label='right')
plt.grid()
plt.legend()
plt.xlabel(r"$t$ (s)")
plt.ylabel(r"$r_L(t)$")
plt.title(r"Fonctions de réflexion")
plt.show()

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

# Plot de la fonction non linéaire et de son intersection avec la droite (qh quelqconque)
qvals = np.linspace(-4,5,1000)
fvals = np.zeros(len(qvals))
for i in range(len(fvals)):
    fvals[i] = F(qvals[i])
    
#fdroite = 1/Zc * (qvals-1)

plt.figure()
plt.plot(qvals,fvals)
#plt.plot(qvals,fdroite)
plt.grid()

# Plot de la fonction de rélexion
Lwin_L = int(5 * T_L / delta_t)
Lwin_R = int(5 * T_R / delta_t)
t_L = np.arange(0, Lwin_L) * delta_t
t_R = np.arange(0, Lwin_R) * delta_t

r_L = reflexion_left(t_L)
r_R = reflexion_right(t_R)
plt.figure()
plt.plot(t_L,r_L,label='left')
plt.plot(t_R,r_R,'--',label='right')
plt.grid()
plt.legend()
plt.xlabel(r"$t$ (s)")
plt.ylabel(r"$r_L(t)$")
plt.title(r"Fonction de réflexion côté chevalet $r_L(t)$")
plt.show()

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