#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 22:13:17 2026

@author: antonia
"""

import numpy as np

def theta():
    u = np.random.rand() # genero n randoms entre 0 y 1 
    return np.arccos(u**(1/3))

def phi():
    return np.random.rand()* 2*np.pi
    
def vector(theta,phi): # los angulos creados anteriormente
    
    vx = np.sin(theta) * np.cos(phi)
    vy = np.sin(theta) * np.sin(phi)
    vz = np.cos(theta)
    
    return np.array([vx, vy, vz])

def energia_inicial(Emin=100, Emax=100000.0, gamma=2.7): # en Mev
    u = np.random.rand()
    a = 1 - gamma
    E0 = ((Emax**a - Emin**a)*u + Emin**a)**(1/a)
    return E0
    
def bethe_bloch(E_MeV):
    
    if E_MeV < 0.1: return 0.0
    m_mu = 105.658 #mev
    me=0.511; K=0.307075
    Z_A=0.5551; rho=1.03; I=75e-6     
    gamma = 1 + E_MeV/m_mu
    beta2 = 1 - 1/gamma**2
    Tmax  = (2*me*beta2*gamma**2)/(1+2*gamma*me/m_mu+(me/m_mu)**2)
    arg   = 2*me*beta2*gamma**2*Tmax/I**2
    if arg<=1 or beta2<=0: return 0.0
    return max(K*rho*Z_A/beta2*(0.5*np.log(arg)-beta2), 0.0)


def perdida(E0, theta, X0, dx=0.5):
    X = X0 / np.cos(theta) # distancia recorrida 
    E = E0
    x=0
    while x<X and E>0:
        E -= bethe_bloch(E)*dx
        x += dx
    return E

def generar_muon (): # energia en MeV
    E0 = energia_inicial()
    th= theta()
    ph = phi()
    v = vector(th, ph)
    X0 = 10 #cm espesor del detector ???
    
    # llegada al detector 
    L =X0/np.cos(th)
    E =  perdida(E0, th, X0) 
    # energia con la que el muon llega al detector
    E_dep =  E0-E
    
    return {
        "E0": E0,
        "theta": th,
        "phi": ph,
        "E_dep": E_dep
    }
 
 #suposicion 10.000 fotones por Mev
 #eficiencia cuantica de 0.25
 
def fotomultiplicador(E_dep, g= 10e6, s = 0.03): 
   mu_pe =  E_dep * 10000*0.25 #valor esperado de fotoelectrones
   N_pe = np.random.poisson(mu_pe) #numero real de fotoelectrones
   Q = N_pe * g  # carga acumulada en ánodo luego de multiplicación
   sigma = np.sqrt(max(N_pe,1)) * g * s * 1.602e-19
   Q = np.random.normal(Q, sigma)

   return Q
    

#s resolucion relativa del pmt
    
def tiempos(N_pe, tau=5e-9):
    return np.random.exponential(tau, N_pe)
  
def pulso(t, t0, tau=5e-9):
    x = t - t0
    return np.where(x > 0, (x/tau)*np.exp(-x/tau), 0)

# implementacion preliminar

muon = generar_muon()
