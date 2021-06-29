from pulp import *
import time
def valor(inicio,ini): #devuelve el numero entero del string y la posicion del espacio para poder sacar los valores qe desee en una linea
    a=inicio.find("\t", ini+1)
    num=float(inicio[ini+1:a])
    return num,a

def valorn(inicio): #devuelve el numero entero del string y la posicion del espacio para poder sacar los valores qe desee en una linea
    a=inicio.find("\n")
    
    num=float(inicio[0:a])
    return num

def igual(inicio):
    posi=inicio.find("=")
    posc=inicio.find(";")
    a=float(inicio[posi+1:posc])
    return a

def lector2(f):
    vector=[]
    i=f.readline()
    inicio=f.readline()
    while inicio[0:1]!= "]":
        vector.append(valorn(inicio))
        inicio=f.readline()
    return vector
def lectorhs(f):
    vector=[]
    inicio=f.readline()
    while inicio[0:1]!= "]":
        vector.append(valorn(inicio))
        inicio=f.readline()
    return vector
def lector3(f):
    
    matriz=[]
    i=f.readline()
    inicio=f.readline()
    while inicio[0:1]!= "]":
        vector=[]
        numero,pos=valor(inicio,-1)
        vector.append(numero)
        while pos!=-1:
            numero,pos=valor(inicio,pos)
            vector.append(numero)
        matriz.append(vector)    
        inicio=f.readline()
    return matriz
def dicuno(a):
    dic = dict()
    cont=0
    for i in a:
        dic[cont]=i
        cont+=1
    return dic

def dicdos(b):
    dic2 = dict()
    for i in range(len(b)):
        for j in range(len(b[i])):
            dic2 [i,j]= b[i][j]
    return dic2

def imprimir(ma):
    for i in range (len(ma)):
        print(ma[i])
    return

def lector(texto):
    cont=1
    vaux=[]
    f=open(texto,"r")
    inicio=f.readline()
    
    while inicio[0:2] != "hs":
        a=igual(inicio)
        vaux.append(a)
        inicio=f.readline()
    
    Cants=lectorhs(f)
    Cp=lector2(f)
    Cr=lector2(f)

    Tsrk=lector3(f)
    Tspk=lector3(f)
    Trpk=lector3(f)
    Tpq=lector3(f)
    Npq=lector3(f)
   
    f.close()
    return vaux,Cants,Cp,Cr,Tsrk,Tspk,Trpk,Tpq,Npq

def main (texto):
    while True:
        try:
            print("")
            print("Si desea resolver con el modelo sin la Variación ingrese 0")
            print("Si desea resolver con el modelo con la Variación ingrese 1")
            verificador =int(input())
            if verificador ==1 or verificador == 0:
                break
        except:
            print("")
            print("Oops no has ingresado un numero, ingrese un numero porfavor.")
    
    vaux,Cants,Cp,Cr,Tsrk,Tspk,Trpk,Tpq,Npq=lector(texto)
    
    sitios=vaux[0]
    prepilas=vaux[1] 
    pilas=vaux[2]
    Krecogida=vaux[3]
    m=vaux[4]
    alpha1=vaux[5]
    alpha2=vaux[6]
    alpha3=vaux[7]
    alpha4=vaux[8]
    alpha5=vaux[9]
    alpha6=vaux[10]
    alpha7=vaux[11]
    cap=vaux[12]
    captri=vaux[13]
    CFk=vaux[14]
    CFex=vaux[15]
    CFm=vaux[16]


    #print(alpha1)

    
    #imprimir(Tpq)

    Pilas,Volumen,Z_FLP,tiempo_inicial_FLP,tiempo_final_FLP=modelo_FLP(sitios,prepilas,pilas,alpha1,alpha2,alpha3,alpha4,alpha5,alpha6,alpha7,cap,CFk,Cants,Cp,Cr,Tsrk,Tspk,Trpk,verificador)
    Z_TSP,tiempo_inicial_TSP,tiempo_final_TSP=modelo_TSP(Pilas,Volumen,Tpq,Npq,captri,CFex,CFm,alpha6,alpha7)
    
    tiempo_total_FLP=tiempo_final_FLP-tiempo_inicial_FLP
    print("")
    print("El tiempo utilizado en el FLP es de: ",round(tiempo_total_FLP,3), "segundos.")
    tiempo_total_TSP=tiempo_final_TSP-tiempo_inicial_TSP
    print("El tiempo utilizado en el TSP es de: ",round(tiempo_total_TSP,3), "segundos.")
    print("El tiempo total utilizado es de: ",round(tiempo_total_TSP+tiempo_total_FLP,3), "segundos.")
    print("El costo total es de : ", Z_FLP + Z_TSP )
    print("")
    print("----------------------------------------")




def modelo_FLP(sitios,prepilas,pilas,alpha1,alpha2,alpha3,alpha4,alpha5,alpha6,alpha7,cap,CFk,Cants,Cp,Cr,T_sr,T_sp,T_rp,verificador):

    tiempo_inicial_FLP=time.time()
    


    Cants=dicuno(Cants)
    Cp=dicuno(Cp)
    Cr=dicuno(Cr)
    T_sr=dicdos(T_sr)
    T_sp=dicdos(T_sp)
    T_rp=dicdos(T_rp)

    

    Nsitios=[s for s in range (0,int(sitios))]
    Nprepilas=[r for r in range (0,int(prepilas))]
    Npilas=[p for p in range (0,int(pilas))]
    
    Arcosr=[(s,r) for s in  Nsitios for r in Nprepilas ]
    Arcosp=[(s,p) for s in  Nsitios for p in Npilas ]
    Arcorp=[(r,p) for r in Nprepilas for p in Npilas ]
    solver = GUROBI_CMD(options=[("timeLimit", 3600)])
    
    
    modelo_FLP=LpProblem("FLP",LpMinimize)
    

    #variables
    
    R=pulp.LpVariable.dicts('R',Nprepilas,lowBound=0,cat= "Binary")
    P=pulp.LpVariable.dicts('P',Npilas,lowBound=0,cat= "Binary")
    Xsr=pulp.LpVariable.dicts('Xsr',Arcosr,lowBound=0,cat= "Binary")
    Xsp=pulp.LpVariable.dicts('Xsp',Arcosp,lowBound=0,cat= "Binary")
    Xrp=pulp.LpVariable.dicts('Xrp',Arcorp,lowBound=0,cat= "Binary")
    Erp=pulp.LpVariable.dicts('Erp',Arcorp,lowBound=0,cat= "Integer")
    Vrp=pulp.LpVariable.dicts('Vrp',Arcorp,lowBound=0,cat= "Integer")
    Vp=pulp.LpVariable.dicts('Vp',Npilas,lowBound=0)
    TR=pulp.LpVariable('TR',lowBound=0)

    #objetivo
    modelo_FLP += (lpSum(Cp[p] * P[p] for p in Npilas) + lpSum(Cr[r] * R[r] for r in Nprepilas) + CFk*TR)

    #RESTRICCIONES
    for s in Nsitios: # restriccion 1
        modelo_FLP += (lpSum(Xsr[(s,r)] for r in Nprepilas ) + lpSum(Xsp[(s,p)] for p in Npilas ) == 1)

    for r in Nprepilas: # restriccion 2
        modelo_FLP += (lpSum(Xrp[(r,p)] for p in Npilas  ) <= 1)
    
    for r in Nprepilas: # restriccion 3
        modelo_FLP += (lpSum(Xsr[(s,r)] for s in Nsitios  ) <= alpha1 * R[r])

    for p in Npilas: # restriccion 4
        modelo_FLP += (lpSum(Xsp[(s,p)] for s in Nsitios  ) <= alpha2 * P[p])

    for p in Npilas: # restriccion 5
        modelo_FLP += (lpSum(Xrp[(r,p)] for r in Nprepilas ) <= alpha3 * P[p])

    if verificador ==0 :
        for r in Nprepilas: # restriccion 6
            modelo_FLP += (lpSum(Xsr[(s,r)] for s in Nsitios ) - lpSum(Xrp[(r,p)] for p in Npilas ) == 0)

    if verificador ==1 :
        for r in Nprepilas:
            modelo_FLP += (lpSum(Xsr[(s,r)] for s in Nsitios ) <= 10000*lpSum(Xrp[(r,p)] for p in Npilas ) )

        for r in Nprepilas:
            modelo_FLP += ( lpSum(Xrp[(r,p)] for p in Npilas ) <= 10000 * lpSum(Xsr[(s,r)] for s in Nsitios ))

    #restriccion 7
    for r in Nprepilas:
        modelo_FLP += (lpSum(Cants[s] * Xsr[(s,r)]  for s in Nsitios ) == lpSum(Erp[(r,p)] for p in Npilas))


    for r in Nprepilas: # restriccion 8 
        for p in Npilas:
            
            modelo_FLP += (Vrp[(r,p)] >= ((1 / int(cap))*Erp[(r,p)]))

    for r in Nprepilas: # restriccion 9 
        for p in Npilas:
            
            modelo_FLP += (Vrp[(r,p)] <= alpha4 * Xrp[(r,p)] )

    for p in Npilas: #restriccion 10
        modelo_FLP += (lpSum(Cants[s] * Xsp[(s,p)] for s in Nsitios  ) + lpSum(Erp[(r,p)] for r in Nprepilas) == Vp[p])

    #restriccion 11
    modelo_FLP += (lpSum(T_sp[(s,p)] * Xsp[(s,p)] for s in Nsitios for p in Npilas ) + lpSum(T_sr[(s,r)] *Xsr[(s,r)] for s in Nsitios for r in Nprepilas) + lpSum(T_rp[(r,p)] * Vrp[(r,p)] for r in Nprepilas for p in Npilas) == TR )
       
    result = modelo_FLP.solve(solver)

    Pilas=[]
    Volumen=[]

    
    tiempo_final_FLP=time.time()
    for i in Npilas:
        Pilas.append(P[i].varValue) 
    for i in Npilas:
        Volumen.append(Vp[i].varValue) 
    print("----------------------------------------")
    
    print("FLP")
    print("")
    print("Pilas Localizadas: ")
    for i in Npilas:
        if P[i].varValue == 1:
            print(i+1,end =" ")
    print("")
    print("Prepilas Localizadas: ")
    for i in Nprepilas:
        if R[i].varValue == 1:
            print(i+1,end =" ")
    print("")
    print("")
    print("Datos Necesarios")
    for i in Nsitios:
        for j in Npilas:
            
            if Xsp[(i,j)].varValue == 1:
                print("desde sitio",i+1,"hacia pila", j+1 )
    print("")
    for i in Nsitios:
        for j in Nprepilas:
            
            if Xsr[(i,j)].varValue == 1:
                print("desde sitio",i+1,"hacia prepila", j+1 )
    print("")
    for i in Nprepilas:
        for j in Npilas:
            
            if Xrp[(i,j)].varValue == 1:
                print("desde prepila",i+1,"hacia pila", j+1 )

    print("")
    a=0
    for i in Npilas:
        a=a+Cp[i] * P[i].varValue
    print("CP+Pp = ",a)
    a=0
    for i in Nprepilas:
        a=a+Cr[i] * R[i].varValue
    print("CR+Rr= ",a)

    
    print("CFk*TR = ",CFk*TR.varValue )
    print("")
    print("Tiempo Recolectora: ",TR.varValue)
    print("")
    print("Z=", value(modelo_FLP.objective))
    print("")
    print("----------------------------------------")
    Z_FLP=value(modelo_FLP.objective) 
    
    return Pilas,Volumen,Z_FLP,tiempo_inicial_FLP,tiempo_final_FLP

def modelo_TSP(Pilas,Volumen,Tpq,Npq,captri,CFex,CFm,alpha6,alpha7):

    tiempo_inicial_TSP=time.time()


    Pilas=dicuno(Pilas)
    Volumen=dicuno(Volumen)
    T_pq=dicdos(Tpq)
    Npq=dicdos(Npq)

    Npilas=[p for p in range (0,len(Pilas))]
    Npilas2=[p for p in range (1,len(Pilas))]
    Arcopq=[(p,q) for p in Npilas for q in Npilas]
    solver = GUROBI_CMD(options=[("timeLimit", 3600)])
    modelo_TSP=LpProblem("TSP",LpMinimize)

    #Variables

    Zpq=pulp.LpVariable.dicts('Zpq',Arcopq,lowBound=0,cat= "Binary")
    TTp=pulp.LpVariable.dicts('TTp',Npilas,lowBound=0)
    TT=pulp.LpVariable('TT',lowBound=0)
    TEp=pulp.LpVariable.dicts('TEp',Npilas,lowBound=0)
    TE=pulp.LpVariable('TE',lowBound=0)

    #Funcion Objetivo

    modelo_TSP += (lpSum(Npq[(p,q)] * Zpq[(p,q)] for p in Npilas for q in Npilas) + CFex * TE + CFm * TT )
    

    #RESTRICCIONES
    for p in Npilas2: #restriccion 1
        modelo_TSP += (lpSum(Zpq[(q,p)] for q in Npilas if q != p) == Pilas[p])

    for p in Npilas2: #restriccion 2
        modelo_TSP += (lpSum(Zpq[(p,q)] for q in Npilas if q != p) == Pilas[p])

    #restriccion 3
    modelo_TSP += (lpSum(Zpq[(0,p)] for p in Npilas2) == 1)

    #restriccion 4
    modelo_TSP += (lpSum(Zpq[(p,0)] for p in Npilas2) == 1)

    for p in Npilas: # restriccion 5
        modelo_TSP +=  (TEp[p] >= ( Volumen[p] / int(captri) ))
    
    for p in Npilas: #restriccion 6
        modelo_TSP +=  (TTp[p] <= alpha6 * Pilas[p])

    #restriccion 7
    modelo_TSP += (lpSum(TEp[p] for p in Npilas) <= TE)

    for p in Npilas: # restriccion 8
       for q in Npilas2:
            if p != q:
                modelo_TSP += (TTp[p] + TEp[p] + T_pq[(p,q)] - TTp[q] <= alpha7 * (1 - Zpq[(p,q)]) )

    for p in Npilas: #restriccion 9
        modelo_TSP += (TTp[p] + TEp[p] + T_pq[(p,0)] * Zpq[(p,0)] <= TT )
    


    result = modelo_TSP.solve(solver)
    #modelo_TSP.solve(pulp.PULP_CBC_CMD(maxSeconds=100))
    tiempo_final_TSP=time.time()
    Z_TSP=value(modelo_TSP.objective)
    print("----------------------------------------")
    
    print("TSP")

    print("")
    for i in Npilas:
      for j in Npilas:
            if Zpq[(i,j)].varValue==1 :
                print(i+1,j+1 ,Zpq[(i,j)].varValue)
            if Zpq[(i,j)].varValue==1 and Npq[(i,j)]!=0:
                print("desde ",i+1 ,"hacia ", j+1)    
    print("")

    print("Tiempo Excavadora: ",TE.varValue)
    print("Tiempo Trituradora: ",TT.varValue)    

    a=0
    for i in Npilas:
      for j in Npilas:
        if Zpq[(i,j)].varValue==1:
            a=a+Zpq[(i,j)].varValue*Npq[(i,j)]
    print("")
    print("Zpq*Npq= ",a)
    print("CFex * TE = ",CFex * TE.varValue)
    print("CFm * TT = ", CFm * TT.varValue)
    print("")
    print("Z= ",value(modelo_TSP.objective))
    print("")
    print("----------------------------------------")

    return Z_TSP,tiempo_inicial_TSP,tiempo_final_TSP


main("Data 1.txt")
