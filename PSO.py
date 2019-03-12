# -*- coding: utf-8 -*-
"""PSO_jul_06_2018.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/0B_ElSkvqhSW4VkJUTzQzY21jV1hMSjZ1dUlPaXFGdEtSNFdF
"""

import numpy as np

#FOBJ Gera vetorialmente os valores com a funcao objetivo escalar

def FOBJ(X,Fun):
    rows = X.shape[0] # Numero de linhas da matriz X[n,m]. If Y has n rows and m columns, then Y.shape is (n,m) . So Y.shape[0] is n.
    fobj=np.zeros(rows)
    for i in range(rows):
        fobj[i]=Fun(X[i,]) # X é um vetor com i linhas de partículas e todas as colunas
    return fobj

#Enxame retorna a populacao aleatoria com todos valores entre MIN e MAX
def Enxame(PAR,NPAR,MAX,MIN): #a PAR não necessário
    x=np.zeros((NPAR, len(MAX)))
    for j in range(len(MAX)):
        for i in range(NPAR):
            x[i,j]=MIN[j]+(MAX[j]-MIN[j])*np.random.random()
    return x


#VE rotina velocidade utilizada na correcao das particulas
#nesta versao do programa fazemos a adequacao restricao de VELOCIDADE: 30% do limite

def VE(X,VEL,FOBEST,PBEST,W,C1,C2,MAX,MIN):
    rows = X.shape[0]
    cols = X.shape[1]
    VEL=np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            R1=np.random.random()
            R2=np.random.random()
            VELOCIDADE=W*VEL[i,j]+C1*R1*(PBEST[i,j]-X[i,j])+C2*R2*(FOBEST[j]-X[i,j])
            if(VELOCIDADE> MAX[j]):
                VELOCIDADE=0.5*MAX[j]
            if(VELOCIDADE<MIN[j]):
                VELOCIDADE=0.5*MIN[j]
            VEL[i,j]=np.copy(VELOCIDADE)
            X[i,j]=X[i,j]+VEL[i,j]
            if(X[i,j]>MAX[j]):
                X[i,j]=MAX[j]
            if(X[i,j]<MIN[j]):
                X[i,j]=MIN[j]
    return X, VEL

#PART atualiza PBEST (melhor de cada particula)
def PART(x,xnew,Fun): # x é o vetor anterior de PBEST
    rows = x.shape[0]
#    cols  = x.shape[1] #a não necessário
    YCAL=FOBJ(x,Fun)
    NEW=FOBJ(xnew,Fun) #xnew vem da rotina velocidade!!!!
    for i in range(rows):
        if(YCAL[i]>NEW[i]):
            x[i,]=np.copy(xnew[i,]) 
    PBEST=np.copy(x)
    return PBEST

def PSO(W,C1,C2,NPAR,ITE,PAR,MAX,MIN,Fun,x):
    #rows = x.shape[0]
    #cols  = x.shape[1]
#    x=Enxame(PAR,NPAR,MAX,MIN)# gera populacao inicial aleatoria
    PBEST=np.copy(x) # inicialmente eh aleatorio
    YCAL=FOBJ(x,Fun) # estima a funcao nos valores aleatorios
    best=np.argmin(YCAL)
    GBEST=PBEST[best] # melhor global: isto primeira interacao
    FOBEST=YCAL[best]
    VEL=Enxame(PAR,NPAR,MAX,MIN) # velocidades define aleatoria no primeiro uso

    for i in range(ITE):
        xnew,VEL=VE(VEL,x,GBEST,PBEST,W,C1,C2,MAX,MIN)# nova atualizacao de x utilizando as velocidades
        PBEST=PART(PBEST,xnew,Fun) #atualizcao de PBEST (sempre atualiza com a nova busca)
        #YCAL=FOBJ(xnew,Fun)
        YCAL=FOBJ(PBEST,Fun)
        new=np.argmin(YCAL) #índice do Ycal min
        NEW=YCAL[new]
        if(NEW<FOBEST):
            GBEST=xnew[new]
            FOBEST=NEW
#        if((i%25)==0):
#            print("i=",i,"---",NEW,"\n") #add última iteração 
        if i==ITE-1: #Coletar X e Y ordenados da ultima iteração
#            y=FOBJ(xnew,Fun)
#            XY = np.c_[xnew,y] #concatena x e y em 2 colunas
            XY= np.c_[PBEST,YCAL] #concatena x e y em 2 colunas            
            XYsorted = XY[XY[:,-1].argsort()] #Ordena a partir da last col(Y) for all row
            BEST_XY_PSO=np.append(GBEST,FOBEST)
    return GBEST,FOBEST,XYsorted,BEST_XY_PSO



######################################MAIN
import Function 
############################### FUNÇÃO
'''
Fun=Function.Rosenbrock
MAX=[20,20] # MAXIMO DE CADA PARAMETRO
MIN=[-30,-30] # MINIMO DE CADA PARAMETRO
'''
'''
F_Name='Shubert'
Fun=Function.Shubert
MAX=[10,10] # MAXIMO DE CADA PARAMETRO
MIN=[-10,-10] # MINIMO DE CADA PARAMETRO
'''
'''
Fun=Function.Schwefel
MAX=[500,500] # MAXIMO DE CADA PARAMETRO
MIN=[-300,-300] # MINIMO DE CADA PARAMETRO
'''

'''
############################### DADOS DE ENTRADA 
W=0.75
C1=2
C2=2

NPAR=50 #PARTICULAS
ITE=200 #ITERACOES
PAR=len(MAX) #NUM DE PARAMETROS A SER OTIMIZADOS

############################## RESOLUÇÃO E IMPRESSÃO
X=Enxame(PAR,NPAR,MAX,MIN) # inicializa partículas

GBEST,FOBEST,XYsorted,BEST_XY_PSO =PSO(W,C1,C2,NPAR,ITE,PAR,MAX,MIN,Fun,X)

print('\n','Ótimo=',FOBEST)
print('\n','XBEST=',GBEST)
#print(x)
#print(ynew)

'''


