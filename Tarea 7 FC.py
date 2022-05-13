# -*- coding: utf-8 -*-
"""
Created on Fri May 13 08:23:20 2022

@author: Jorge
"""
import numpy as np 
nEspines = 20
J = 1
Kb = 1
pasos = 1000
 
def crearEstadoInicialAleatorio(N):
    '''
    Esta función crea un estado inicial aleatorio.
    Parameters
    ----------
    N : Número de espines que tiene la configuración.
    Returns
    -------
    estados: Corresponde a la configuración de espines creada.
    '''
    estados = np.random.rand(1,N)[0]
    for i in range(0,len(estados)):
        if estados[i] < 0.5:
            estados[i] = -1
        else:
            estados[i] = 1
    return estados

def crearEstadoInicialOrdenado(N, estado):
    '''
    Esta función crea un estado inicial con todos los espines de la configuración incial alineados
    Parameters
    ----------
    N : Número de espines que tiene la configuración.
    estado : Corresponde a la alineación del espín.
    Returns
    -------
    Retorna la configuración de estados alineada.
    '''
    return np.array([estado]*N)

