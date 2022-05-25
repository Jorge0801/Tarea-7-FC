# -*- coding: utf-8 -*-
"""
Created on Fri May 13 08:23:20 2022

@author: Jorge e Ignacio
"""
import numpy as np 
import matplotlib.pyplot as plt

def Energía(estados, J):
    '''
    Calcula la energía para cada sistema de espines.
    Parameteros
    ----------
    estados : Estados de espines de la configuración (positivo,negativo o aleatorio).
    J : Comportamiento ferromagnetico
    Devuelve
    -------
    valorE : Energía para el sistema.
    '''
    energia = 0
    for i in range(0,len(estados)-1):
        estados[0] = estados[-1] #Condición de controno
        energia += estados[i]*estados[i+1]
        
    valorEnergía=-1*energia*J
    
    return valorEnergía

def Magnetización(estados):
    '''
    Calcula magnetización del sistema.
    Parametros
    ----------
    estados : Estados de espines de la configuración (positivo,negativo o aleatorio).
    Devuelve
    -------
    magnetizacion : Retorna el valor de magnetización para el sistema
    '''
    magnetizacion = 0
    for i in range(0,len(estados)):
        estados[0] = estados[-1] #controno periódica
        magnetizacion +=estados[i]
    return np.absolute(magnetizacion)

def EstadoInicialOrdenado(N, estado):
    '''
    Crea un estado inicial con los espines del sistema incial alineados
    Parametros
    ----------
    N : Número de espines que tiene la configuración.
    estado : Corresponde a la alineación del espín.
    Devuelve
    -------
    Configuración del estado ordenado.
    '''
    return np.array([estado]*N)
 
def EstadoInicialAleatorio(N):
    '''
    Crea un estado inicial con los espines del sistema incial alineados
    Parametros
    ----------
    N : Número de espines que tiene la configuración.
    Devuelve
    -------
    estados: Configuración del estado aleatoria.
    '''
    estados = np.random.rand(1,N)[0]
    for i in range(0,len(estados)):
        if estados[i] < 0.5:
            estados[i] = -1
        else:
            estados[i] = 1
    return estados

def Simulacion(N, J, kT, nPasos):
    '''
   Simula el modelo Ising
   Parametros
   ----------
   N : Número de espines que tiene la configuración.
   J : Comportamiento farramagnetico
   kT : constante de Boltzmann tomada como 1
   nPasos : Número de pasos que tendrá la simulación.
   
   Devuelve
   -------
   estadosT : Configuración del sistema de espines para cada paso 
   arregloEnergias : Arreglo de energías.
   arregloMagnetizaciones : Arreglo de magnetizaciones.
   energiasEquilibrio : Arreglo de energías para la condición después de equilibrio.
   magnetizacionesEquilibrio : Arreglo de magnetización para la condición después de equilibrio.
   UEquilibrio : Arreglo de energías elevadas al cuadrado para la condición después de equilibrio.(Energía interna)
   '''
   
    cnt = 1/kT #Se define constante de probabilidad
    #estados = EstadoInicialAleatorio(N) #Configuracion aleatoria
    #estados = EstadoInicialOrdenado(N,1) #Configutacion positiva
    estados = EstadoInicialOrdenado(N,-1) #Configuracion negativa
    
    estadosS = estados #Se crea la variable donde se guardan los espines
    energiaInicial = Energía(estados,J) #Se calcula la energía inicial
    energias = [energiaInicial] #Lista de energías 
    UE=[energiaInicial**2] #Lista de energías para energía interna
    
    magnetizacionInicial=Magnetización(estados) #Se calcula la magnetización inicial
    magnetizaciones = [magnetizacionInicial] #Lista de magnetización
    
    n = nPasos #Se establece un parámetro n para el ciclo while
    nEquilibrio=1000 #Sistema entra en equilibrio a NPasos
    
    while n > 0: #Ciclo para recorrer n pasos en cada sistema
   
       pos = np.floor(np.random.rand(1)*N).astype(int)[0] #Posición aleatoria del sistema
       estados[pos] *= -1 #Cambia dirección 
       energiaActual = Energía(estados,J) #Calcula nueva energía
       magnetizacionActual=Magnetización(estados) #Nueva magnetización
       
       
       if energiaActual < energiaInicial: #Se evalua la condición de cambio
       
           energiaInicial = energiaActual #Se hace el cambio de energía
           magnetizacionInicial=magnetizacionActual #Cambio de magnetización 
           
           estadosS = np.row_stack((estadosS, estados)) #Guarda configuración del sistema
           energias.append(energiaActual) #Se guarda el valor de energía
           UE.append(energiaActual**2) #Se guarda energía para energía interna
           magnetizaciones.append(magnetizacionActual) #Se guarda el valor de la magnetización
           
       else: 
       
           P = np.exp(-cnt*(energiaActual-energiaInicial)) #Probabilidad de cambio 
           
           if np.random.rand(1) < P: #Número aleatorio se evalua si se acepta el cambio 
               
               energiaInicial = energiaActual 
               magnetizacionInicial=magnetizacionActual 
               
               estadosS = np.row_stack((estadosS, estados)) 
               energias.append(energiaActual) 
               UE.append(energiaActual**2) 
               magnetizaciones.append(magnetizacionActual) 
               
           else: 
           
               estados[pos] *= -1 #Se vuelve al estado original, no se acepta el cambio
               estadosS = np.row_stack((estadosS, estados)) 
               energias.append(energiaInicial) 
               UE.append(energiaInicial**2) 
               magnetizaciones.append(magnetizacionInicial) 
               
       n -= 1 
    #Se convierte en arreglos los datos obtenidos    
    arregloEnergias=np.array(energias) 
    arregloMagnetizaciones=np.array(magnetizaciones) 
    arregloUE=np.array(UE) 
    energiasEquilibrio=arregloEnergias[nEquilibrio::] 
    magnetizacionesEquilibrio=arregloMagnetizaciones[nEquilibrio::] 
    UEquilibrio=arregloUE[nEquilibrio::] 

   
    return estadosS , energiasEquilibrio , magnetizacionesEquilibrio , UEquilibrio

def PromedioSimulaciones(conjunto, ejecuciones, pasos):
    '''
    Función para reducir fluctuaciones después de nSimulaciones
    Parametros
    ----------
    conjunto : Arreglo con los datos de cada simulación
    ejecuciones : NSimulaciones
    pasos : Npasos
    Devuelve
    -------
    arregloProm : Valores promedios para cada paso 
    '''
    Prom = np.zeros (pasos) #Se inicializa un arreglo de ceros
    for valor in range(pasos): #Se hace un contador recorrer el valor en cada paso
        suma=0
        for contadorArrelo in range(ejecuciones): 
            suma += conjunto[contadorArrelo][valor] 
        Prom[valor]=suma/len(conjunto) #En cada paso se calcula el promedio respecto a todas las ejecuciones y se guarda en el arreglo
        
    return Prom

#Se hace el calculo de las soluciones analiticas para cada propiedad termodinamica
def EnergiaInternaAnalitica(J, N, kB , T):
    valorU=(-1)*J*N*np.tanh(J/(kB*T))
    return valorU

def CalorEspAnalitico(J, kB , T):
    valorC=(J/(kB*T))**2/np.cosh(J/(kB*T))**2
    return valorC

def MagnetizacionAnalitica(J, N, kB , T , B):
    valorM=(N*np.exp(J/(kB*T))*np.sinh(B/(kB*T)))/(np.sqrt(np.exp(2*J/(kB*T))*np.sinh(B/(kB*T))**2+np.exp(-2*J/(kB*T))))
    
    return valorM    

nEspines=100
pasos=1000
J=1
T=1   

estadosT , energiasEquilibrioT , magnetizacionesEquilibrioT , energiasUEquilibrioT = Simulacion(nEspines,J,T,pasos)
    
#Se grafica gráficas para observar el punto de equilibrio del sistema
#fig, ax = plt.subplots(figsize=(10,10) ,  dpi=120)
#ax.set_title('Modelo Ising 1D para un kt=1 ordenado negativo')
#ax.imshow(estadosT.T, 'plasma')
#ax.set_xlabel('Pasos')
#ax.set_ylabel('Espines')
#ax.set_aspect('5')    
    
Nsimulaciones=20 
kB=1 #

B=0.06 #Se establece un valor de campo magnetico que mejor se adaptara a la simulacion


Temperaturas = np.linspace(0,5,100) 

#Se establcen memorias para almacenar datos

listaUPromedio = []
listaMPromedioEquilibrio = []
listaU_2Promedio=[]
listaCalorEsp=[]

listaUAnalitica=[]
listaCalorEspAnalitico=[]
listaMagnetizacionAnalitica=[]

for t in Temperaturas:
    #Memoria para guardar los datos de cada simulacion
    listaEquilibrioE = []
    listaEquilibrioM = []
    listaEquilibrioUE = []
    
   
    for i in range(Nsimulaciones):
        
        resultadoEjecucion=Simulacion(nEspines, 1,t ,pasos)
        
    
        pasosEquilibrioE=len(resultadoEjecucion[1])
        listaEquilibrioE.append(resultadoEjecucion[1])
        
        pasosEquilibrioM=len(resultadoEjecucion[2])
        listaEquilibrioM.append(resultadoEjecucion[2])
        
        pasosEquilibrioUE=len(resultadoEjecucion[3])
        listaEquilibrioUE.append(resultadoEjecucion[3])
        
    
    conjuntoEquilibrioE=np.array(listaEquilibrioE)
    conjuntoEquilibrioM=np.array(listaEquilibrioM)
    conjuntoEquilibrioUE=np.array(listaEquilibrioUE)
    
    #Se reducen fluctuaciones calculando el promedio para cada temperatura para nSimulaciones
    progresoU=PromedioSimulaciones(conjuntoEquilibrioE, Nsimulaciones, pasosEquilibrioE)
    progresoEquilibrioM=PromedioSimulaciones(conjuntoEquilibrioM, Nsimulaciones, pasosEquilibrioM)
    progresoU_2=PromedioSimulaciones(conjuntoEquilibrioUE, Nsimulaciones, pasosEquilibrioUE)
    
    #Se calcula el promedio del parámetro para cada temperatura
    promUT = np.sum(progresoU)/len(progresoU)
    promMagnetizacionEquilibrioT=np.sum(progresoEquilibrioM)/len(progresoEquilibrioM)
    promUE=np.sum(progresoU_2)/len(progresoU_2)
    
    #Se calcula el calor específico utilizando los promedios de las energías correspondientes
    calorT=(1/nEspines**2)*(promUE-promUT**2)/t**2
    
    #Se calculan la energía interna, el calor específico, y la magnetización de forma analítica
    energiaIntAnalitica=EnergiaInternaAnalitica(J, nEspines, kB, t)
    calorEspAnalitico=CalorEspAnalitico(J, kB, t)
    magnetizacionAnalitica=MagnetizacionAnalitica(J, nEspines, kB, t, B)
    
    #Se guarda el valor obtenido para cada temperatura
    listaUPromedio.append(promUT)
    listaMPromedioEquilibrio.append(promMagnetizacionEquilibrioT)
    listaU_2Promedio.append(promUE)
    
    listaCalorEsp.append(calorT)
    
    listaUAnalitica.append(energiaIntAnalitica)
    listaCalorEspAnalitico.append(calorEspAnalitico)
    listaMagnetizacionAnalitica.append(magnetizacionAnalitica)

#Se grafican los resultados

# Gráfico Calor Específico Analítico y Simulación

fig3, ax3 = plt.subplots(dpi=120)

color = 'tab:red'
ax3.set_title('Modelo Ising 1D Calor Específico vs. T')
ax3.set_xlabel('kT')
ax3.set_ylabel('C analítico', color=color)
ax3.plot(Temperaturas, listaCalorEspAnalitico, color=color)
ax3.tick_params(axis='y', labelcolor=color)

ax4 = ax3.twinx()  

color = 'tab:blue'
ax4.set_ylabel('C simulación', color=color)  
ax4.plot(Temperaturas, listaCalorEsp, color=color)
ax4.tick_params(axis='y', labelcolor=color)

fig3.tight_layout()

# Gráfico Energía Interna analítica y simulación

fig5, ax5 = plt.subplots(dpi=120)

color = 'tab:red'
ax5.set_title('Modelo Ising 1D Energía Interna vs. T')
ax5.set_xlabel('kT')
ax5.set_ylabel('U analítica', color=color)
ax5.plot(Temperaturas, listaUAnalitica, color=color)
ax5.tick_params(axis='y', labelcolor=color)

ax6 = ax5.twinx()  

color = 'tab:blue'
ax6.set_ylabel('U simulación', color=color)  
ax6.plot(Temperaturas, listaUPromedio, color=color)
ax6.tick_params(axis='y', labelcolor=color)

fig5.tight_layout()

# Gráfico Magnetización analítica y simulación

fig7, ax7 = plt.subplots(dpi=120)

color = 'tab:red'
ax7.set_title('Modelo Ising 1D Magnetización vs. T')
ax7.set_xlabel('kT')
ax7.set_ylabel('M analítica', color=color)
ax7.plot(Temperaturas, listaMagnetizacionAnalitica, color=color)
ax7.tick_params(axis='y', labelcolor=color)

ax8 = ax7.twinx()  

color = 'tab:blue'
ax8.set_ylabel('M simulación', color=color)  
ax8.plot(Temperaturas, listaMPromedioEquilibrio, color=color)
ax8.tick_params(axis='y', labelcolor=color)

fig7.tight_layout()

plt.show()    
    