# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 16:36:44 2026

@author: colin
"""

######################################################################################
                     # MODELE PHYSIQUE DE CORDES FROTTEES
                 
              # D'après les articles de Ollivier, Dalmont Kergomard 
           # Point de contact entre l'archet et la corde : quelconque
# Fonction de réflexion construite à partir de l'admittance du chevalet (Debut et al)
#######################################################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os
from time import time
from numba import njit
import scipy.io


# PARAMETRES PHYSIQUES ET VARIABLES

T_sec = 0.5    # durée de la simulation (s)

# Paramètres physiques liés à la corde

L = 0.325                 # longueur de la corde (m) --> à faire varier pour changer la freq
d = 0.45e-3               # diamètre de la corde LA (m) 
R = d/2                   # rayon de la corde (m)
T = 6*9.81                # tension pour une corde de LA (N)
Area = np.pi*R**2         # section de la corde (m^2)
mu = 7.19595e-4           # masse linéique (kg/m)
rho = mu/Area             # masse volumique (kg/m3)
c = np.sqrt(T/mu)         # vitesse du son (m/s)
f0_th = c/(2*L)           # fréquence fondamentale attendue (Hz)
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

L_L = L*beta             # longueur de la partie droite de la corde (m)
L_R = L*(1-beta)         # longueur de la partie droite de la corde (m)
T_L = 2*L_L/c            # temps de parcours d'un aller-retour sur la moitié gauche de la corde (s)
T_R = 2*L_R/c            # temps de parcours d'un aller-retour sur la moitié droite de la corde (s)
fs = 44100               # fréquence d'échantillonage (Hz)
delta_t = 1/fs           # pas de temps (s)

# IMPORT DES DONNEES

# main_path = os.path.expanduser('~') + "\Documents\M2 ATIAM\Projets et applications musicales"
# os.chdir(main_path+'\File_Debut_Et_al_2010')

# data = scipy.io.loadmat('CELLO_ModosXX.mat')

# Nmod = int(data['Nmod'][0])
# Wmod = data['Wmod'][:,0]
# Fmod = data['Fmod'][:,0]
# Zmod = data['Zmod'][:,0]
# Mmod = data['Mmod'][:,0]

# Admittance du chevalet - Vincent Debut et al

Nmod = 88 # nombre de modes
Wmod = np.array([  457.80459813,   606.16602347,   937.60287944,  1227.64940544, # pulsations des modes
        1292.72714884,  1423.82868046,  1784.60501254,  1926.15092272,
        2315.34911731,  2395.71314077,  2544.40317242,  2787.58727589,
        2961.55910617,  3187.55592203,  3348.0717585 ,  3637.01322936,
        3743.6192178 ,  3813.80570444,  4044.19124188,  4109.7108403 ,
        4259.99763199,  4495.74130246,  4604.29717327,  4709.40807563,
        4911.42640265,  5228.78675522,  5293.38745049,  5506.52503914,
        5748.97551311,  5852.00938903,  6070.49265205,  6140.11953925,
        6355.94299717,  6469.32878753,  6656.6473557 ,  6755.13656752,
        7063.18409084,  7270.34071089,  7350.97375391,  7579.96111789,
        7751.78717505,  7977.93827914,  8431.00662791,  8999.07332034,
        9160.24292933,  9336.9912637 ,  9545.93937675,  9833.84248228,
       10384.37700582, 10580.85065019, 10723.25648642, 10923.69958442,
       11098.51755904, 11270.09806843, 11842.74810213, 12096.92842441,
       12235.97179121, 12393.36048915, 12566.25049248, 12755.356287  ,
       12925.33907501, 13082.45822727, 13205.29275186, 13393.68733982,
       13573.86985808, 13762.46813201, 13942.2558396 , 14090.90896331,
       14215.26596544, 14509.95983076, 14767.92757604, 14848.56515504,
       15008.00687824, 15203.57408935, 15394.6528056 , 15555.73917704,
       15744.62252183, 15921.55722664, 16118.35026955, 16152.23298291,
       16703.52788634, 16860.09009122, 17036.19701086, 17220.04568628,
       17351.04178645, 17524.41430744, 17680.82463166, 17926.85978027])

Fmod = np.array([  72.86186476,   96.47431897,  149.22413292,  195.38647126,
        205.74391581,  226.60937261,  284.02870921,  306.55644049,
        368.499257  ,  381.28958858,  404.95434211,  443.65829426,
        471.34677101,  507.31528137,  532.86217019,  578.84863354,
        595.81550357,  606.98602985,  643.65302695,  654.08079491,
        677.99968069,  715.51945115,  732.79665459,  749.52557427,
        781.67778961,  832.18725847,  842.46877845,  876.39067924,
        914.97787063,  931.37622128,  966.14891258,  977.23037585,
       1011.57974601, 1029.62565502, 1059.43833108, 1075.11337598,
       1124.14066202, 1157.1106621 , 1169.94380947, 1206.38828036,
       1233.73524671, 1269.72831281, 1341.83638007, 1432.24700218,
       1457.89794212, 1486.02831322, 1519.28343827, 1565.10464064,
       1652.72493141, 1683.9946831 , 1706.65927586, 1738.56078571,
       1766.38393051, 1793.69181672, 1884.83190025, 1925.28595497,
       1947.4153941 , 1972.46458337, 1999.98088201, 2030.07800397,
       2057.13160493, 2082.13789466, 2101.68761643, 2131.67154636,
       2160.3484848 , 2190.36483235, 2218.97893472, 2242.63781417,
       2262.42984577, 2309.33183113, 2350.38867295, 2363.22254225,
       2388.59848063, 2419.72396898, 2450.13509119, 2475.77278347,
       2505.83450147, 2533.99453434, 2565.31511989, 2570.7077212 ,
       2658.44903018, 2683.36667899, 2711.39496577, 2740.65539124,
       2761.50406811, 2789.09716182, 2813.99063807, 2853.14834814])

Zmod = np.array([0.02806018, 0.03084333, 0.02508868, 0.01647275, 0.0289855, # coefficients d'amortissement zeta
       0.05352241, 0.02235392, 0.01746855, 0.02548642, 0.00635098,
       0.01663475, 0.01324522, 0.01415669, 0.00340841, 0.00990157,
       0.01794775, 0.02697258, 0.00742968, 0.03227202, 0.0055932 ,
       0.00763441, 0.00739527, 0.03432816, 0.00903569, 0.01322705,
       0.01257962, 0.01198943, 0.0119133 , 0.00586819, 0.00760282,
       0.00673269, 0.01474132, 0.00853252, 0.00962712, 0.007925  ,
       0.01779052, 0.01819473, 0.00539287, 0.00366558, 0.00302975,
       0.00513375, 0.06657177, 0.00757581, 0.00265573, 0.00492994,
       0.00475768, 0.02909748, 0.00620675, 0.00313591, 0.00554923,
       0.00449006, 0.00331862, 0.00343261, 0.00545233, 0.0120341 ,
       0.00400778, 0.00494859, 0.00345198, 0.00217223, 0.00213778,
       0.00364035, 0.00632312, 0.00544423, 0.00333903, 0.00347037,
       0.00344806, 0.0057395 , 0.00760761, 0.00775131, 0.00150851,
       0.00404056, 0.00823238, 0.00316784, 0.00210596, 0.00272994,
       0.0029931 , 0.00348758, 0.00344996, 0.00168281, 0.01197384,
       0.00121528, 0.00221253, 0.00151954, 0.00311053, 0.00305237,
       0.00203544, 0.00258697, 0.00372498])

Mmod = np.array([1.79748750e+01, 3.04600824e+00, 9.81389260e+02, 2.02503484e-01, # masses modales
       1.46993879e+00, 1.28841829e+00, 3.70521551e+00, 2.65211429e+00,
       2.21439755e-01, 4.26311207e-01, 1.22402456e+00, 6.29059377e-01,
       1.37506978e-01, 1.61852196e+01, 3.58186331e-01, 3.82305003e+00,
       5.64738176e-01, 7.22966642e+00, 1.89860600e+00, 4.44797989e-01,
       5.07945623e-01, 3.09307420e-01, 8.22831558e-01, 3.48026741e-01,
       1.81168924e-01, 3.15361554e-01, 1.15635779e+00, 1.09290223e-01,
       3.09989415e-01, 3.14411969e+00, 3.23123953e-01, 9.40308038e-02,
       8.85327100e-01, 6.00336094e-01, 1.17535807e+00, 1.79307837e-01,
       1.03311117e+00, 1.69378791e+01, 8.38118985e-01, 2.58749031e+00,
       1.94356075e+00, 1.26477974e-01, 2.24812227e+00, 9.30448785e+00,
       5.00597406e+00, 1.07561238e+01, 1.52485138e+00, 6.29933702e+01,
       2.76327629e+00, 3.39844837e+00, 8.52437496e+00, 8.73899606e+00,
       5.34196876e+01, 3.17788570e+02, 2.41605518e+00, 3.15750540e+00,
       8.73136999e+00, 2.47532939e+01, 2.38016800e+01, 7.97398925e+00,
       5.53424226e+00, 4.09066836e+00, 2.80667548e+00, 2.49391712e+00,
       1.96482673e+00, 2.29333663e+00, 1.91165987e+00, 3.56257015e+00,
       3.71703127e+00, 3.95962739e+00, 1.01390854e+01, 6.81652222e+00,
       3.70618345e+01, 9.14412688e+00, 3.10323298e+00, 2.73507240e+00,
       2.75774907e+00, 7.20179810e+00, 1.21365065e+01, 4.68823532e+00,
       1.72753068e+01, 3.62914623e+00, 2.59365414e+00, 1.14876031e+00,
       1.75412353e+00, 5.35971976e+00, 1.66880236e+01, 1.33587353e+02])

# Adaptation violoncelle vers violon
# freq de résonnance principale shiftée de 200 Hz à 500 Hz

Wmod *= 3
Mmod *= 1/10

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
    f, q, q_iL, q_iR, q_oL, v = np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N)
    f_b, v_b = np.zeros(N), np.zeros(N)
    
    D_R = int(np.rint(T_R*fs)) # temps de parcours aller-retour de la moitié droite de la corde en samples
    D_L = int(np.rint(T_L*fs))
    
    bm = 2*delta_t / Mmod
    a_m0 = (Wmod*delta_t)**2 + 4*Zmod*Wmod*delta_t + 4
    a_m1 = 2 * (Wmod**2*delta_t**2 - 4)
    a_m2 = (Wmod*delta_t)**2 - 4*Zmod*Wmod*delta_t + 4
    fm = np.zeros((N,Nmod))
    qtot = np.zeros(N)
    w = np.zeros((N,Nmod))
    
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
            #qo_D = 0.999*(q_iR[n-D_L] + Yc_half*f[n-D_L])
            qo_D = 0.999*q_oL[n-D_L]
        else :
            qo_D = 0
            
        if n >= D_L+1 :
            #qo_D1 = 0.999*(q_iR[n-D_L-1] + Yc_half*f[n-D_L-1])
            qo_D1 = 0.999*q_oL[n-D_L-1]
        else :
            qo_D1 = 0
        
        if n >= D_L+2:
            #qo_D2 = 0.999*(q_iR[n-D_L-2] + Yc_half*f[n-D_L-2])
            qo_D2 = 0.999*q_oL[n-D_L-2]
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
        
        q_oL[n] = q_iR[n] + Yc_half*f[n]
        
        # pour le son à écouter
        
        v[n] = q_iL[n] + q_oL[n]
        
        if n >= 2 :
            fb_prev2 = f_b[n-2]
        else:
            fb_prev2 = 0             
                           
        if n >= D_L/2 :
            f_b[n] = 1/Yc_half * (q_oL[n-int(D_L/2)] - q_iR[n-int(D_L/2)])
        
        w[n] = 1/(a_m0) * (-a_m1*w[n-1] - a_m2*w[n-2] + bm*(f_b[n] - fb_prev2))
        v_b[n] = np.sum(w[n])
           
        if n % 1000 == 0:
            print(f"Echantillon {n}/{N}")
    
    return temps, f, q, q_iL, q_iR, v, f_b, v_b
 
    
start = time()

q_vals = np.linspace(vb-100, vb+100, 10000)
f_vals = F(q_vals)
q_min = q_vals[np.argmin(np.abs(f_vals-0.01*np.max(f_vals)))]


temps, f, q, q_iL, q_iR, v, f_b, v_b = execution(T_sec, delta_t)
stop = time()
print("Temps d'exécution (s) :", stop-start)
    
# AFFICHAGE

#plt.close('all')

main_path = os.path.expanduser('~') + "\Documents\M2 ATIAM\Projets et applications musicales\Modele physique"
os.chdir(main_path+'\Figures')

# activate latex
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "computer modern roman",
    "font.size" :13,
    "figure.dpi":100
})

plt.figure(figsize=(5,6))
plt.subplot(211)
plt.plot(temps,q)
plt.ylabel(r"$v(t)$ (m/s)")
plt.grid()
axes = plt.gca()
axes.xaxis.set_ticklabels([])
plt.xlim(0.218,0.226)

plt.subplot(212)
plt.plot(temps, f)
plt.ylabel(r"$f$ (N)")
plt.xlabel(r'Temps $t$ (s)')
plt.grid()
plt.xlim(0.218,0.226)
plt.ylim(0,0.02)

plt.savefig('violon_onde.pdf',bbox_inches='tight')

plt.figure()
plt.plot(q_vals,f_vals, 'k', lw=0.5)
plt.scatter(q, f, s=2, c='tab:red')
plt.grid()
plt.xlabel('$q$')
plt.ylabel('$f$')
plt.xlim(q_min,vb+abs(q_min))
plt.title("Parcours de la caractéristique NL")

# plt.figure()
# plt.title(r"$\beta =$"+str(beta)+", $F_b =$"+str(Fb)+ ", $v_b =$"+str(vb))
# plt.subplot(411)
# plt.plot(temps,q)
# plt.ylabel(r"$q$")
# plt.grid()

# plt.subplot(412)
# plt.plot(temps,f)
# plt.ylabel(r"$f$")
# plt.grid()

# plt.subplot(413)
# # plt.plot(temps,q_iL,label=r'$q_{iL}$')
# # plt.plot(temps,q_iR,'--',label=r'$q_{iR}$')
# # plt.xlabel(r"Temps $t$ (s)")
# # plt.ylabel(r"$q_h$")
# # plt.grid()
# plt.plot(temps, v_b)
# plt.ylabel(r'$v_b$')
# plt.grid()

# plt.subplot(414)
# plt.plot(temps,v)
# plt.ylabel(r'$f_b$')
# plt.xlabel(r'$t$')
# plt.grid()
# plt.show()

#%%

# TRACE FONCTION REFLEXION

# main_path = os.path.expanduser('~') + "\Documents\M2 ATIAM\Projets et applications musicales"
# os.chdir(main_path+'\File_Debut_Et_al_2010')

# data = scipy.io.loadmat('CELLO_ModosXX.mat')

# Nmod = int(data['Nmod'][0])
# Wmod = data['Wmod'][:,0]
# Fmod = data['Fmod'][:,0]
# Zmod = data['Zmod'][:,0]
# Mmod = data['Mmod'][:,0]

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

R_e = np.fft.fft(qi,fs) # fonction de réflexion au point de contact avec l'archet
R_r = R_e * z**D        # fonction de réflexion au chevalet
Y_r = Yc * (1+R_r) / (1-R_r)  # admittance au chevalet
Y_e = Yc * (1+R_e) / (1-R_e)  # admittance au point de contact avec l'archet

# théorie

W = 2 * np.pi * freq # pulsations

H = np.zeros(len(W), dtype=complex) # admittance au chevalet
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
    
wave(v_b, int(1/delta_t), "string_adm_bridge2_vb")