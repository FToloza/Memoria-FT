import time
from pulp import *
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


    tiempo_inicial,tiempo_final=modelo(sitios,prepilas,pilas,Krecogida,m,alpha1,alpha2,alpha3,alpha4,alpha5,alpha6,alpha7,cap,captri,CFk,CFex,CFm,Cants,Cp,Cr,Tsrk,Tspk,Trpk,Tpq,Npq)

    
    tiempo_total=tiempo_final-tiempo_inicial
    print("El tiempo es de: ",round(tiempo_total,3), "segundos.")

def modelo(sitios,prepilas,pilas,Krecogida,m,alpha1,alpha2,alpha3,alpha4,alpha5,alpha6,alpha7,cap,captri,CFk,CFex,CFm,Cants,Cp,Cr,T_sr,T_sp,T_rp,Tpq,Npq):
    tiempo_inicial=time.time()
    #Creación de Diccionarios
    Cants=dicuno(Cants)
    Cp=dicuno(Cp)
    Cr=dicuno(Cr)
    Tsrk=dicdos(T_sr)
    Tspk=dicdos(T_sp)
    Trpk=dicdos(T_rp)
    Tpq=dicdos(Tpq)
    Npq=dicdos(Npq)

    

    
    # Tuplas
    Nsitios=[s for s in range (0,int(sitios))]
    Nprepilas=[r for r in range (0,int(prepilas))]
    Npilas=[p for p in range (0,int(pilas))]

    Arcosrk=[(s,r) for s in  Nsitios for r in Nprepilas  ]
    Arcospk=[(s,p) for s in  Nsitios for p in Npilas ]
    Arcorpk=[(r,p) for r in Nprepilas for p in Npilas  ]
    Arcopq=[(p,q) for p in Npilas for q in Npilas]

    Npilas2=[p for p in range (1,int(pilas))]
    
    modelo=LpProblem("FLP",LpMinimize)

    #VARIABLES
    R=pulp.LpVariable.dicts('R',Nprepilas,lowBound=0,cat= "Binary")
    P=pulp.LpVariable.dicts('P',Npilas,lowBound=0,cat= "Binary")
    Xsr=pulp.LpVariable.dicts('Xsr',Arcosrk,lowBound=0,cat= "Binary")
    Xsp=pulp.LpVariable.dicts('Xsp',Arcospk,lowBound=0,cat= "Binary")
    Xrp=pulp.LpVariable.dicts('Xrp',Arcorpk,lowBound=0,cat= "Binary")
    Erp=pulp.LpVariable.dicts('Erp',Arcorpk,lowBound=0,cat= "Integer")
    Vrp=pulp.LpVariable.dicts('Vrp',Arcorpk,lowBound=0,cat= "Integer")
    Vp=pulp.LpVariable.dicts('Vp',Npilas,lowBound=0)

    Trp=pulp.LpVariable.dicts('Trp',Arcorpk,lowBound=0)
    Tp=pulp.LpVariable.dicts('Tp',Npilas,lowBound=0)
    
    TR=pulp.LpVariable('TR',lowBound=0)
    Zpq=pulp.LpVariable.dicts('Zpq',Arcopq,lowBound=0,cat= "Binary")
    TTp=pulp.LpVariable.dicts('TTp',Npilas,lowBound=0)
    TT=pulp.LpVariable('TT',lowBound=0)
    TEp=pulp.LpVariable.dicts('TEp',Npilas,lowBound=0)
    TE=pulp.LpVariable('TE',lowBound=0)

    #FUNCION OBJETIVO
    modelo += (lpSum(Cp[p] * P[p] for p in Npilas) + lpSum(Cr[r] * R[r] for r in Nprepilas) + lpSum(Npq[(p,q)] * Zpq[(p,q)] for p in Npilas for q in Npilas) + lpSum(CFk*TR + CFex * TE + CFm * TT  ))

    #RESTRICCIONES
    for s in Nsitios: # restriccion 1
        modelo += (lpSum(Xsr[(s,r)] for r in Nprepilas  ) + lpSum(Xsp[(s,p)] for p in Npilas) == 1)

    for r in Nprepilas: # restriccion 2
        modelo += (lpSum(Xrp[(r,p)] for p in Npilas  ) <= 1)
    
    for r in Nprepilas: # restriccion 3
        modelo += (lpSum(Xsr[(s,r)] for s in Nsitios  ) <= alpha1 * R[r])

    for p in Npilas: # restriccion 4
        modelo += (lpSum(Xsp[(s,p)] for s in Nsitios ) <= alpha2 * P[p])

    for p in Npilas: # restriccion 5
        modelo += (lpSum(Xrp[(r,p)] for r in Nprepilas ) <= alpha3 * P[p])
    

    for r in Nprepilas:# restriccion 6
        modelo += (lpSum(Xsr[(s,r)] for s in Nsitios ) <= 10000*lpSum(Xrp[(r,p)] for p in Npilas  ) )

    for r in Nprepilas: # restriccion 7
        modelo += ( lpSum(Xrp[(r,p)] for p in Npilas ) <= 10000 * lpSum(Xsr[(s,r)] for s in Nsitios ))
    
    for r in Nprepilas: #restriccion 8
        modelo += (lpSum(Cants[s] * Xsr[(s,r)]   for s in Nsitios ) == lpSum(Erp[(r,p)] for p in Npilas ))

    for r in Nprepilas: # restriccion 9
        for p in Npilas:

                modelo += (Vrp[(r,p)] >= ((1 / int(cap))*Erp[(r,p)]))

    for r in Nprepilas: # restriccion 10
        for p in Npilas:
 
                modelo +=(Vrp[(r,p)] <= alpha4 * Xrp[(r,p)] )

    for p in Npilas: #restriccion 11
        modelo +=(lpSum(Cants[s] * Xsp[(s,p)] for s in Nsitios  ) + lpSum(Erp[(r,p)] for r in Nprepilas ) == Vp[p])

    #restriccion 12
    modelo += (lpSum(Tspk[(s,p)] * Xsp[(s,p)] for s in Nsitios for p in Npilas ) + lpSum(Tsrk[(s,r)] *Xsr[(s,r)] for s in Nsitios for r in Nprepilas) + lpSum(Trpk[(r,p)] * Vrp[(r,p)] for r in Nprepilas for p in Npilas) <= TR )
 
    for p in Npilas2: #restriccion 13
        modelo +=(lpSum(Zpq[(q,p)] for q in Npilas if q != p) == P[p])

    for p in Npilas2: #restriccion 14
        modelo +=(lpSum(Zpq[(p,q)] for q in Npilas if q != p) == P[p])

    #restriccion 15
    modelo += (lpSum(Zpq[(0,p)] for p in Npilas2) == 1)

    #restriccion 16
    modelo += (lpSum(Zpq[(p,0)] for p in Npilas2) == 1)


    for p in Npilas: # restriccion 17
        modelo += (TEp[p] >= ((1 / int(captri))*Vp[p]))
    
    for p in Npilas: #restriccion 18
        modelo += (TTp[p] <= alpha6 * P[p])

    #restriccion 19
    modelo += (lpSum(TEp[p] for p in Npilas) <= TE)
   
    for p in Npilas: # restriccion 20
       for q in Npilas2:
            if p != q:
                modelo += (TTp[p] + TEp[p] + Tpq[(p,q)] - TTp[q] <= alpha7 * (1 - Zpq[(p,q)]) )

    for p in Npilas: #restriccion 21
        modelo += (TTp[p] + TEp[p] + Tpq[(p,0)] * Zpq[(p,0)] <= TT )

    #Resolver con GUROBI y con limite de una hora
    modelo.solve(GUROBI_CMD(options=[("timeLimit", 3600)]))
    
    tiempo_final=time.time()
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
    print("Datos Necesarios")
    print("")
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
    
    for i in Npilas:
      for j in Npilas:
            if i!=j:
                if Zpq[(i,j)].varValue>=0.1 and Npq[(i,j)]!=0:
                    print("Nuevo Camino")
                if Zpq[(i,j)].varValue==1 :
                    print("Desde Pila ",i+1," hacia Pila ",j+1)
                
                    
    print("")
    
    print("Tiempo Recolectora: ",TR.varValue)

    print("Tiempo Excavadora: ",TE.varValue)
    print("Tiempo Trituradora: ",TT.varValue)    
    print("")

    a=0
    for i in Npilas:
        a=a+Cp[i] * P[i].varValue
    print("CP+Pp = ",a)
    a=0
    for i in Nprepilas:
        a=a+Cr[i] * R[i].varValue
    print("CR+Rr= ",a)
    a=0
    for i in Npilas:
      for j in Npilas:
        if Zpq[(i,j)].varValue==1:
            a=a+Zpq[(i,j)].varValue*Npq[(i,j)]
    print("Zpq*Npq= ",a)

    
    
    
    print("CFk*TR = ",CFk * TR.varValue)
    print("CFex * TE = ",CFex * TE.varValue)
    print("CFm * TT = ", CFm * TT.varValue)
    print("")
    print("Z= ",value(modelo.objective))

    return tiempo_inicial,tiempo_final

main("Data 1.txt")
