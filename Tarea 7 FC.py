# -*- coding: utf-8 -*-
"""
Created on Fri May 13 08:23:20 2022

@author: Jorge
"""
import numpy as np 
import matplotlib.pyplot as plt

def calcularEnergía(estados, J):
    '''
    Esta función calcula la energía para cada configuración.
    Parameters
    ----------
    estados : Corresponde a los estados de espines de la configuración.
    J : Parámetro del cual depende la alineación de equilibrio, establece el comportamiento del material.
    Returns
    -------
    valorE : Corresponde al valor de energía para la configuración.
    '''
    energia = 0
    for i in range(0,len(estados)-1):
        estados[0] = estados[-1] #Condición de controno
        energia += estados[i]*estados[i+1]
        
    valorE=-1*energia*J
    
    return valorE
 
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

def realizarSimulacion(N, J, kT, nPasos):
    B = 1/kT #Se define el parámetro Beta
    estados = crearEstadoInicialAleatorio(N) #Se crea el estado inicial con los espines alineados de forma aleatoria
    
    estadosT = estados #Se crea la variable donde se guardan los espines
    energiaInicial = calcularEnergía(estados,J) #Se calcula la energía inicial
    energias = [energiaInicial] #Se inicializa la lista de energías con la energía inicial
    energiasCuad=[energiaInicial**2] #Se inicializa la lista de energías elevadas al cuadrado con la energía inicial
    
    n = nPasos #Se establece un parámetro n para el ciclo while
    
    
    while n > 0: #Se establece un ciclo while para hacer los cálculos para cada paso
   
       pos = np.floor(np.random.rand(1)*N).astype(int)[0] #Se escoge una posición aleatoria en la cual se cambiará la dirección del espín
       estados[pos] *= -1 #Se cambia la dirección del espín en la posición aleatoria 
       energiaActual = calcularEnergía(estados,J) #Se calcula la nueva energía después del cambio
       
       if energiaActual < energiaInicial: #Se establece la condición de energía en la cual se acepta realizar el cambio
       
           energiaInicial = energiaActual #Se realiza el cambio de energía para la siguiente iteración
           
           
           estadosT = np.row_stack((estadosT, estados)) #Se guarda la configuración de los espines
           energias.append(energiaActual) #Se guarda el valor de energía
           energiasCuad.append(energiaActual**2) #Se guarda el valor de energía elevada al cuadrado
           
       else: #Si no se cumple la condición de energía para el cambio
       
           P = np.exp(-B*(energiaActual-energiaInicial)) #Se define la probabilidad para realizar el cambio
           
           if np.random.rand(1) < P: #Mediante a un número aleatorio, se acepta el cambio
               
               energiaInicial = energiaActual #Se realiza el cambio de energía para la siguiente iteración
               
               estadosT = np.row_stack((estadosT, estados)) #Se guarda la configuración de los espines
               energias.append(energiaActual) #Se guarda el valor de energía
               energiasCuad.append(energiaActual**2) ##Se guarda el valor de energía elevada al cuadrado
               
           else: #Si no se cumple la condición anterior, se rechaza el cambio
           
               estados[pos] *= -1 #Se vuelve al estado original, pues no se acepta el cambio
               estadosT = np.row_stack((estadosT, estados)) #Se guarda la configuración de los espines
               energias.append(energiaInicial) #Se guarda el valor de energía inicial, pues no se acepta el cambio
               energiasCuad.append(energiaInicial**2) #Se guarda el valor de energía inicial elevada al cuadrado, pues no se acepta el cambio
               
       n -= 1 #Se le resta 1 una vez realizados los cálculos por cada paso
       
    arregloEnergias=np.array(energias) #Se establece el arreglo de energías
    

   
    return estadosT, arregloEnergias
    
nEspines=100
pasos=1000
J=1
T=1   

estadosT, energiasT  = realizarSimulacion(nEspines,J,T,pasos)
    
fig, ax = plt.subplots(figsize=(10,10) ,  dpi=120)
ax.set_title('Modelo Ising 1D para un kt=1')
ax.imshow(estadosT.T, 'plasma')
ax.set_xlabel('Pasos')
ax.set_ylabel('Espines')
ax.set_aspect('5')    
    
    
    