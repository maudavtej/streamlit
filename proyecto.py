import numpy as np
import random
import time 
import os 
import platform
animalesP=[]
animalesD=[]
#Fucnion para limpiar pantalla
def limpiarPantalla():
    comando = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(comando)
#Creacion de matriz  
matriz = np.full((20, 20), "  ", dtype=object)
j = 1
for j in range(19):
    matriz[0][j] = "--"
    matriz[19][j] = "--"
for i  in range(19):
    matriz[i][0] = "| "
    matriz[i][19] = "| "
#Calse principal
class Animal:
    def __init__(self,nombre,vida,adulto,posicionX,posicionY):
        self.nombre = nombre
        self.vida = vida
        self.adulto = adulto
        self.posicionX = posicionX
        self.posicionY = posicionY
    def __repr__(self):
        return f"{self.nombre}"
    #Funciones de movimiento
    def moveW(self):
        self.posicionY -= 1
    def moveA(self):
        self.posicionX -= 1
    def moveS(self):
        self.posicionY += 1
    def moveD(self):
        self.posicionX += 1
        #Radar:
    def radarLibre(self):
        direccionesLibres = [0,0,0,0]
        clean = "  "
        if 1 <= self.posicionY - 1 <= 18 and matriz[self.posicionY - 1,self.posicionX] == clean: 
            direccionesLibres[0] = 1
        if 1 <= self.posicionY + 1 <= 18 and matriz[self.posicionY + 1,self.posicionX] == clean:
            direccionesLibres[1] = 2
        if 1 <= self.posicionX - 1 <= 18 and matriz[self.posicionY,self.posicionX - 1] == clean:
            direccionesLibres[2] = 3
        if 1 <= self.posicionX + 1 <= 18 and matriz[self.posicionY,self.posicionX + 1] == clean: 
            direccionesLibres[3] = 4
        return direccionesLibres
    def radarComida(self):
        direccionesComida = [0,0,0,0]
        comida = " *"
        if 1 <= self.posicionY - 1 <= 18 and matriz[self.posicionY - 1,self.posicionX] == comida: 
            direccionesComida[0] = 1
        if 1 <= self.posicionY + 1 <= 18 and matriz[self.posicionY + 1,self.posicionX] == comida:
            direccionesComida[1] = 2
        if 1 <= self.posicionX - 1 <= 18 and matriz[self.posicionY,self.posicionX - 1] == comida:
            direccionesComida[2] = 3
        if 1 <= self.posicionX + 1 <= 18 and matriz[self.posicionY,self.posicionX + 1] == comida: 
            direccionesComida[3] = 4
        return direccionesComida
    def radarPresa(self):
        direccionesAnimales = [0,0,0,0]
        if 1 <= self.posicionY - 1 <= 18 and matriz[self.posicionY - 1,self.posicionX].startswith("P"): 
            direccionesAnimales[0] = 1 #Arriba
        if 1 <= self.posicionY + 1 <= 18 and matriz[self.posicionY + 1,self.posicionX].startswith("P"):
            direccionesAnimales[1] = 2 #Abajo
        if 1 <= self.posicionX - 1 <= 18 and matriz[self.posicionY,self.posicionX - 1].startswith("P"):
            direccionesAnimales[2] = 3 #Izquierda
        if 1 <= self.posicionX +1 <= 18 and matriz[self.posicionY,self.posicionX + 1].startswith("P"): 
            direccionesAnimales[3] = 4 #Derecha
        return direccionesAnimales
    def radarDepredador(self):
        direccionesAnimales = [0,0,0,0]
        if 1 <= self.posicionY - 1 <= 18 and matriz[self.posicionY - 1,self.posicionX].startswith("D"): 
            direccionesAnimales[0] = 1 #Arriba
        if 1 <= self.posicionY + 1 <= 18 and matriz[self.posicionY + 1,self.posicionX].startswith("D"):
            direccionesAnimales[1] = 2 #Abajo
        if 1 <= self.posicionX - 1 <= 18 and matriz[self.posicionY,self.posicionX - 1].startswith("D"):
            direccionesAnimales[2] = 3 #Izquierda
        if 1 <= self.posicionX +1 <= 18 and matriz[self.posicionY,self.posicionX + 1].startswith("D"): 
            direccionesAnimales[3] = 4 #Derecha
        return direccionesAnimales
    def comer(self, a):
        if a == 1:
            self.moveW()
        if a == 2:
            self.moveS()        
        if a == 3:
            self.moveA()
        if a == 4:
            self.moveD()
    def moveAll(self, b):
        if b == 1:
            self.moveW()
        if b == 2:
            self.moveS()
        if b == 3:
            self.moveA()
        if b == 4:
            self.moveD()
#Clase hija 
class depredador(Animal):
    def matar(self,direccion):
        posicionPresaX = self.posicionX
        posicionPresaY = self.posicionY
        if direccion == 1:
            posicionPresaY - 1
        elif direccion == 2:
            posicionPresaY +1
        elif direccion == 3:
            posicionPresaX - 1
        elif direccion == 4:
            posicionPresaX +1
        for p in animalesP:
            if p.posicionX == posicionPresaX and p.posicionY == posicionPresaY:
                animalesP.remove(p)
                break
        self.comer(direccion)
    def reproduccionD():
        pass
#Segunda clase hija
class presa(Animal):
    def radarDepredador(self):
        direccionesAnimales = [0,0,0,0]
        limY, limX = matriz.shape
        if self.posicionY > 0 and matriz[self.posicionY - 1,self.posicionX].startswith("D"): 
            direccionesAnimales[0] = 1
        if self.posicionY < limY -1 and matriz[self.posicionY + 1,self.posicionX].startswith("D"):
            direccionesAnimales[1] = 2
        if self.posicionX > 0 and matriz[self.posicionY,self.posicionX - 1].startswith("D"):
            direccionesAnimales[2] = 3
        if self.posicionX < limX -1 and matriz[self.posicionY,self.posicionX + 1].startswith("D"): 
            direccionesAnimales[3] = 4
        return direccionesAnimales
    def reproduccionP():
        pass

#Creamos animales
for i in range(4):
    nombre = f"P{i+1}"
    vida = 10
    adulto = True
    vida = 10
    posicionX = random.randint(1,6)
    posicionY = random.randint(1,18)
    presas = presa(nombre,vida,adulto,posicionX,posicionY)
    animalesP.append(presas)
for j in range (5):
    nombre = f"D{j+1}"
    vida = 10
    adulto = True
    posicionX = random.randint(14,18)
    posicionY = random.randint(1,18)
    depredadores = depredador(nombre,vida,adulto,posicionX,posicionY)
    animalesD.append(depredadores) 
#Funcion para agregar comida
def agregarComida():        
    for i in range(4):#Se agregan tres grupos de comida 
        y = random.randint(2,17)
        x = random.randint(2,17)
        matriz[y][x] = " *"
        matriz[y][x-1] = " *"
        matriz[y-1][x] = " *"
def main(animalesD, animalesP):
    duracionDia = 15 #Aqui decimos cuantos tiks dura el dia 
    duracionNoche = 5 
    diaCompleto=duracionDia+duracionNoche
    #Aqui la noche solo dura 5 tiks pero como ya transcurrieron 10 tiks se le tienen q sumar
    dia = True
    agregarComida()
    #Se insertan a los primeros depredadores y presas
    for d in animalesD:
        matriz[d.posicionY][d.posicionX] = d.nombre
    for p in animalesP:
        matriz[p.posicionY][p.posicionX] = p.nombre
    i = 0
    while True:
        i+=1
        dia = True
        #Primero evalua si es de dia o de noche 
        if i == duracionDia:
            dia = False
            print("NOCHE INICIADA")
            time.sleep(4)
            i=0
        else:
            if i == diaCompleto:
                dia = True 
                print("DÍA INICIADO...")
                time.sleep(1)
                i=0
            if not np.any(matriz == " *"):
                agregarComida()
        if dia == True:
            #presa
            for id in animalesP:
                yaSeMovio = False
                posicionYanterior = id.posicionY
                posicionXanterior = id.posicionX
                posComida = id.radarComida()
                posLibre = id.radarLibre()
                posDepredador = id.radarDepredador()
                if yaSeMovio == False:
                    if posDepredador == [0,0,0,0]:
                        yaSeMovio = False
                    else:
                        for depredador in posDepredador:
                            if depredador != 0 :
                                id.posicionY = posicionYanterior
                                id.posicionX = posicionXanterior
                                break
                            yaSeMovio = True        
                if yaSeMovio == False:
                    if posComida == [0,0,0,0]:
                        yaSeMovio = False
                    else:
                        for comida in posComida:
                            if comida != 0:
                                id.comer(comida)
                                break
                            yaSeMovio = True
                if yaSeMovio == False:
                    if posLibre == [0,0,0,0]:
                        yaSeMovio = False
                    else:                        
                        libres = [] 
                        for posiciones in posLibre:
                            if posiciones != 0:
                                libres.append(posiciones)              
                        if libres:
                            b = random.choice(libres)
                            id.moveAll(b)   
                matriz[posicionYanterior,posicionXanterior] = "  "
                matriz[id.posicionY][id.posicionX] = id.nombre
            #depredador
            for id in animalesD:
                yaSeMovio = False
                posicionYanterior = id.posicionY
                posicionXanterior = id.posicionX
                posComida = id.radarComida()
                posAnimales = id.radarPresa()
                posLibre = id.radarLibre()
                if yaSeMovio == False:
                    if posAnimales == [0,0,0,0]:
                        yaSeMovio = False 
                    else:
                        for animal in posAnimales:
                            if animal != 0:
                                id.matar(animal)
                                break
                        yaSeMovio = True
                if yaSeMovio == False:
                    if posComida == [0,0,0,0]:
                        yaSeMovio = False
                    else:
                        for comida in posComida:
                            if comida != 0:
                                id.comer(comida)
                                break
                            yaSeMovio = True
                if yaSeMovio == False:
                    if posLibre == [0,0,0,0]:
                        yaSeMovio = False
                    else:
                        libres = [] 
                        for posiciones in posLibre:
                            if posiciones != 0:
                                libres.append(posiciones)              
                        if libres:
                            b = random.choice(libres)
                            id.moveAll(b) 
                matriz[posicionYanterior,posicionXanterior] = "  "
                matriz[id.posicionY][id.posicionX] = id.nombre
        print('\n'.join(' '.join(row) for row in matriz))
        limpiarPantalla()
        time.sleep(1)
        if i == 100:
            break    
main(animalesD, animalesP)