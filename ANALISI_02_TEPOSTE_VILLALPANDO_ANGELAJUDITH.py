# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 20:09:57 2020

@author: teposte
"""
#Importando los modulos o librerías 
import csv
import numpy as np 

#LECTURA DE ARCHIVO

#variables que usaremos         
dat_archivo=[]
Subrutas=[]
Subtransportes=[]
Subpaises_exp=[]
Subpaises_imp=[]
Sub_años=[]

total_valor_exp=0
total_valor_imp=0
#ABRIR ARCHIVO Y GUARDAR INFORMACION
archivo=open("synergy_logistics_database1.csv","r") 
lector = csv.DictReader(archivo)  # se  lee el archivo como diccionario
archivo.seek(0)
for linea in lector:
        dat_archivo.append(linea)
        
archivo.close() 
               
#CODIGO GENERAL PARA LA DETERMINACIÓN DE RUTAS, TRANSPORTES y PAISES 

for linea in dat_archivo:
    
        subruta=linea["origin"]+linea[ "destination"]
        Subrutas.append(subruta)
        
        subtransport=linea["transport_mode"]
        Subtransportes.append(subtransport)
        
        subpais_exp=linea["destination"]
        Subpaises_exp.append(subpais_exp)
        
        subpais_imp=linea["origin"]
        Subpaises_imp.append(subpais_imp)
        
        sub_año=linea["year"]
        Sub_años.append(sub_año)
        
        #Para sacar el total de valor de importaciones y exportaciones
        if linea["direction"]=="Exports":
            total_valor_exp+=int(linea["total_value"])
        elif linea["direction"]=="Imports":
            total_valor_imp+=int(linea["total_value"])
        

#Filtrado de valores repatidos

TSubaños=np.transpose(Sub_años) #Transpuesta, para generar una lista
conj_años=set(TSubaños)
Años=conj_años  #solo se renombra el conjunto de las rutas

TSubrutas=np.transpose(Subrutas) #Transpuesta, para generar una lista
conj_rutas=set(TSubrutas)
Rutas=conj_rutas  #solo se renombra el conjunto de las rutas

TSubtransportes=np.transpose(Subtransportes) 
conj_transp=set(TSubtransportes)
Transportes=conj_transp

TSubpaises_exp=np.transpose(Subpaises_exp) 
conj_paises_exp=set(TSubpaises_exp)
Paises_exp=conj_paises_exp

TSubpaises_imp=np.transpose(Subpaises_imp) 
conj_paises_imp=set(TSubpaises_imp)
Paises_imp=conj_paises_imp


val_año_e=[]
val_año_i=[]
#Pasa sacar el total de valor de importaciones y exportaciones X año

for año in Años:
    total_valor_exp_a=0
    total_valor_imp_a=0
    for linea in dat_archivo:
        if linea["direction"]=="Exports":
            #print("entro a exportaciones")
            if linea["year"]==año:
                total_valor_exp_a+=int(linea["total_value"])
        else:
            #print("entro a IMportaciones")
            if linea["year"]==año:
                total_valor_imp_a+=int(linea["total_value"])
                
        form_e=[total_valor_exp_a,año]
        
        form_i=[total_valor_imp_a,año]
    val_año_i.append(form_i)
    val_año_e.append(form_e)
    #print(año)
    #print("EXportaciones",total_valor_exp_a)
    #print("IMportaciones",total_valor_imp_a)


#print(val_año_e)
#print(val_año_i)
##############################################################
#CONSIGNA 1. MEJORES RUTAS 

#Función para calcular el top de Importaciones por año 
#k son el número de los principales que se mostraran
def ImpxYear (año,k=10,Rutas=Rutas,dat_archivo=dat_archivo):
    i=0
    imp_datos=[]
    Dat_imp=0
    for ruta in Rutas:
        #print(Dat_imp)
        valor=0
        num_imp=0.00001
        #print(ruta,ruta,ruta,ruta,ruta,ruta,ruta)
        for linea in dat_archivo:
            if int(linea["year"])==año and linea["direction"]=="Imports" and linea["origin"]+linea[ "destination"]==ruta:
                #extrayendo valores
                #print("coincidieron en ",ruta,num_imp)
                #print(valor)
                valor+=int(linea["total_value"])
                num_imp+=1
                #nomb_ruta=ruta
                #if num_imp>0:
                  #  ponde=valor/num_imp 
                #elif num_imp==0: 
                   # ponde=0        
        Dat_imp=[ruta,valor/num_imp,valor,int(num_imp)]         
        imp_datos.append(Dat_imp)
    imp_datos.sort(reverse= True, key=lambda x:x[1] )
    
    
    print("LAS RUTAS DE MEJOR DESEMPEÑO SON: \n")
    print("NOMBRE RUTA   /  PONDERACIÓN    /  VALOR DE IMPORTACIONES /  N° IMPORTACIONES ")
    while i<k:
        print(imp_datos[i][0],",",imp_datos[i][1],",",imp_datos[i][2],",",imp_datos[i][3])
        
        i+=1
    #print(imp_datos)
    return imp_datos

#Impor_año=ImpxYear(2020,200)


#Función para calcular el top de Exportaciones por año 
#k son el número de los principales que se mostraran
def ExpxYear (año,k=10,Rutas=Rutas,dat_archivo=dat_archivo):
    i=0
    exp_datos=[]
    Dat_exp=0
    for ruta in Rutas:
        valor=0
        num_exp=0.00001  # se da este valor para evitar la división entre 0
        for linea in dat_archivo:
            if int(linea["year"])==año and linea["direction"]=="Exports" and linea["origin"]+linea[ "destination"]==ruta:
                valor+=int(linea["total_value"])
                num_exp+=1    
        Dat_exp=[ruta,valor/num_exp,valor,int(num_exp)]         
        exp_datos.append(Dat_exp)
    exp_datos.sort(reverse= True, key=lambda x:x[1] )
    print("LAS RUTAS DE MEJOR DESEMPEÑO SON: \n")
    print("NOMBRE RUTA   /  PONDERACIÓN    /  VALOR DE EXPORTACIONES /  N° IMPORTACIONES ")
    while i<k:
        print(exp_datos[i][0],",",exp_datos[i][1],",",exp_datos[i][2],",",exp_datos[i][3])
        i+=1
    return exp_datos

#Expor_año=ExpxYear(2020,200)

#Función para calcular las exportaciones o importaciones totales de todos los años
def Resxtotal (n,k=10,Rutas=Rutas,dat_archivo=dat_archivo):
    if n==1:
        direc="Exports"
    else:
        direc="Imports"
    i=0
    exp_datos=[]
    Dat_exp=0
    for ruta in Rutas:
        valor=0
        num_exp=0.00001  # se da este valor para evitar la división entre 0
        for linea in dat_archivo:
            if linea["direction"]==direc and linea["origin"]+linea[ "destination"]==ruta:
                valor+=int(linea["total_value"])
                num_exp+=1    
        Dat_exp=[ruta,valor/num_exp,valor,int(num_exp)]         
        exp_datos.append(Dat_exp)
    exp_datos.sort(reverse= True, key=lambda x:x[1] )
    print("LAS RUTAS DE MEJOR DESEMPEÑO PARA 2015-2020 SON: \n")
    if direc=="Exports":
        print("NOMBRE RUTA   /  PONDERACIÓN    /  VALOR DE EXPORTACIONES /  N° EXPORTACIONES ")
    else:
        print("NOMBRE RUTA   /  PONDERACIÓN    /  VALOR DE IMPORTACIONES/  N° IMPORTACIONES ")
        
    while i<k:
        print(exp_datos[i][0],",",exp_datos[i][1],",",exp_datos[i][2],",",exp_datos[i][3])
        i+=1
    return exp_datos
  
#llamados de funciones 
#Impor_año=Resxtotal(1,200)


#########################################################################
#CONSIGNA 2. MEDIOS DE TRANSPORTE

#Función para calcular el top de Transportes por año 
#k son el número de los principales que se mostraran
def TransxYear (año,Transportes=Transportes,dat_archivo=dat_archivo):
    k=4
    i=0
    trans_datos=[]
    Dat_trans=0
    for transporte in Transportes:
        valor=0
        num_tran=0.00001
        #print(ruta,ruta,ruta,ruta,ruta,ruta,ruta)
        for linea in dat_archivo:
            if int(linea["year"])==año and linea["transport_mode"]==transporte:
                valor+=int(linea["total_value"])
                num_tran+=1      
        Dat_trans=[transporte,valor/num_tran,valor,int(num_tran)]         
        trans_datos.append(Dat_trans)
    trans_datos.sort(reverse= True, key=lambda x:x[1] )
    print("LOS TRANSPORTES CON EL MEJOR DESEMPEÑO SON: \n")
    print("MODO DE TRANSPORTE   /  PONDERACIÓN    /  VALOR DE IMPORTACIONES /  N° IMPORTACIONES ")
    while i<k:
        print(trans_datos[i][0],",",trans_datos[i][1],",",trans_datos[i][2],",",trans_datos[i][3])
        
        i+=1
    return trans_datos

#TRaor_año=TransxYear(2020)


#Función para calcular las exportaciones o importaciones totales de todos los años
def Transxtotal (n,Transportes=Transportes,dat_archivo=dat_archivo):
    k=4
    if n==1:
        direc="Exports"
    else:
        direc="Imports"
    i=0
    trans_datos=[]
    Dat_exp=0
    for transporte in Transportes:
        valor=0
        num_tran=0.00001  # se da este valor para evitar la división entre 0
        for linea in dat_archivo:
            if linea["transport_mode"]==transporte and linea["direction"]==direc:
                valor+=int(linea["total_value"])
                num_tran+=1      
        Dat_trans=[transporte,valor/num_tran,valor,int(num_tran)]         
        trans_datos.append(Dat_trans)
    trans_datos.sort(reverse= True, key=lambda x:x[1] )

    print("LOS TRANSPORTES DE MEJOR DESEMPEÑO PARA 2015-2020 SON: \n")
    if direc=="Exports":
        print("MODO DE TRANSPORTE   /  PONDERACIÓN    /  VALOR DE EXPORTACIONES /  N° EXPORTACIONES ")
    else:
        print("MODO DE TRANSPORTE   /  PONDERACIÓN    /  VALOR DE IMPORTACIONES /  N° IMPORTACIONES ")
        
    while i<k:
        print(trans_datos[i][0],",",int(trans_datos[i][1]),",",trans_datos[i][2],",",trans_datos[i][3])
        i+=1
    return trans_datos
       
#TRaor_año=TransxYear(2020)

#Transportes_2018= TransxYear(2014)

#Transportestotal_2018= Transxtotal(0)

#Introduci analisis de conjuntos de los primero 10 ver como ... mañana 





##############################################
#CONSIGNA 3. El TOP 80% PAISES.

#Función para calcular el top de Transportes por todos los años 
#k son el número de los principales que se mostraran
#Función para calcular las exportaciones o importaciones totales de todos los años
def Paises_total (n,k=0.8,Paises=Paises_exp,dat_archivo=dat_archivo,total_valor_exp=total_valor_exp,total_valor_imp=total_valor_imp):
    if n==1:
        direc="Exports"
    else:
        direc="Imports"
    i=0
    paises_datos=[]
    total_valor=0
    Dat_pais=0
    for pais in Paises:
        valor=0
        num_pais=0.00001  # se da este valor para evitar la división entre 0
        for linea in dat_archivo:
            if direc=="Exports":
                TOTAL=total_valor_exp
                #print(TOTAL)
                if linea["destination"]==pais and linea["direction"]==direc:
                    valor+=int(linea["total_value"])
                    num_pais+=1
                    total_valor+=int(linea["total_value"])
            elif direc=="Imports":
                TOTAL=total_valor_imp
                if linea["origin"]==pais and linea["direction"]==direc:
                    valor+=int(linea["total_value"])
                    num_pais+=1
                    total_valor+=int(linea["total_value"])
                    
        Dat_pais=[pais,valor,int(num_pais)]         
        paises_datos.append(Dat_pais)
    paises_datos.sort(reverse= True, key=lambda x:x[1] )
    
    
    print("LOS PAISES QUE CONTRIBUYEN CON EL",k*100,"PARA 2015-2020 SON: \n")
    if direc=="Exports":
        print("PAIS  / VALOR DE EXPORTACIONES / CONTRIBUCIÓN PORCENTUAL /  N° EXPORTACIONES ")
    else:
        print("PAIS  /  VALOR DE EXPORTACIONES / CONTRIBUCIÓN PORCENTUAL /  N° IMPORTACIONES ")
        
    porce=0
    i=0
    valorXporc=TOTAL*k
    sub_total=0#paises_datos[0][1]   #valor de importaciones o exportaciones del pais
    while int(valorXporc)>int(sub_total):
        sub_total+=paises_datos[i][1] 
        porciento=(paises_datos[i][1]*100)/TOTAL
        print(paises_datos[i][0],",",int(paises_datos[i][1]),",", porciento ,",",paises_datos[i][2])
        i+=1
        porce+=porciento
        #print(porce)
        
    print("PORCENTAJE TOTAL ENTRE LOS PAISES",porce)
    return paises_datos
#Transportestotal_2018= Paises_total(1)  
#Exports==1


#Función para calcular el top de Transportes por año 
#k son el número de los principales que se mostraran
#Función para calcular las exportaciones o importaciones totales de todos los años
def PaisesXaño (n,año=2020,k=1,Paises=Paises_exp,dat_archivo=dat_archivo,val_año_exp=val_año_e,val_año_imp=val_año_i):
    #TOTAL=0
    if n==1:
        direc="Exports"
        for year in val_año_exp:
           # print(year[1],año)
            if int(year[1])==año:
               # print("coincidio")
                TOTAL=year[0]
               # print(TOTAL)
    else:
        direc="Imports"
        for year in val_año_imp:
            #print(year[1],año)
            if int(year[1])==año:
                #print("coincidio")
                TOTAL=year[0]
               # print(TOTAL)
    i=0
    paises_datos=[]
    total_valor=0
    Dat_pais=0
    for pais in Paises:
        valor=0
        num_pais=0.00001  # se da este valor para evitar la división entre 0
        for linea in dat_archivo:
            if direc=="Exports":
                #TOTAL=val_año_exp
                #print(TOTAL)
                if  int(linea["year"])==año and linea["destination"]==pais and linea["direction"]==direc:
                    valor+=int(linea["total_value"])
                    num_pais+=1
                    total_valor+=int(linea["total_value"])
            elif direc=="Imports":
                #TOTAL=total_valor_imp
                if  int(linea["year"])==año and linea["origin"]==pais and linea["direction"]==direc:
                    valor+=int(linea["total_value"])
                    num_pais+=1
                    total_valor+=int(linea["total_value"])
                    
        Dat_pais=[pais,valor,int(num_pais)]         
        paises_datos.append(Dat_pais)
    paises_datos.sort(reverse= True, key=lambda x:x[1] )
    
    
    print("LOS PAISES QUE CONTRIBUYEN CON EL",k*100,"% PARA", año," SON: \n")
    if direc=="Exports":
        print("PAIS  / VALOR DE EXPORTACIONES / CONTRIBUCIÓN PORCENTUAL /  N° EXPORTACIONES ")
    else:
        print("PAIS  /  VALOR DE EXPORTACIONES / CONTRIBUCIÓN PORCENTUAL /  N° IMPORTACIONES ")
        
    porce=0
    i=0
    valorXporc=TOTAL*k
    sub_total=0#paises_datos[0][1]   #valor de importaciones o exportaciones del pais
    while int(valorXporc)>int(sub_total):
        sub_total+=paises_datos[i][1] 
        porciento=(paises_datos[i][1]*100)/TOTAL
        print(paises_datos[i][0],",",int(paises_datos[i][1]),",", porciento ,",",paises_datos[i][2])
        i+=1
        porce+=porciento
        #print(porce)
        
    print("PORCENTAJE TOTAL ENTRE LOS PAISES",porce)
    return paises_datos



#0 para importaciones , 1 para exportaciones
Transportes_2018= PaisesXaño (1,2020)

#Transportestotal_2018= Transxtotal(1)


