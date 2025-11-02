import numpy as np
import random
import time 
import streamlit as st 

# --- 1. CONFIGURACIÓN INICIAL (Fuera de la función principal) ---
# En Streamlit, eliminamos las importaciones 'os' y 'platform' que limpian la consola.
animalesP = []
animalesD = []

# --- 2. DEFINICIÓN DE CLASES Y FUNCIONES (Iguales o ligeros ajustes) ---

# Creacion de matriz  
# La matriz será inicializada con st.cache_resource para mantener su estado.
# No la creamos aquí directamente, sino dentro de la función de inicialización.

# Clase principal
class Animal:
    def __init__(self,nombre,vida,adulto,posicionX,posicionY):
        self.nombre = nombre
        self.vida = vida
        self.adulto = adulto
        self.posicionX = posicionX
        self.posicionY = posicionY
    def __repr__(self):
        return f"{self.nombre}"
    
    # Funciones de movimiento
    def moveW(self):
        self.posicionY -= 1
    def moveA(self):
        self.posicionX -= 1
    def moveS(self):
        self.posicionY += 1
    def moveD(self):
        self.posicionX += 1
        
    # Radar: (Funciones sin cambios)
    def radarLibre(self, matriz):
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
    def radarComida(self, matriz):
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
    def radarPresa(self, matriz):
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
    def radarDepredador(self, matriz):
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
            
# Clase hija (Depredador)
class depredador(Animal):
    def matar(self, direccion, animalesP): # Recibe animalesP como argumento
        posicionPresaX = self.posicionX
        posicionPresaY = self.posicionY
        if direccion == 1:
            posicionPresaY -= 1
        elif direccion == 2:
            posicionPresaY += 1
        elif direccion == 3:
            posicionPresaX -= 1
        elif direccion == 4:
            posicionPresaX += 1
        for p in animalesP:
            if p.posicionX == posicionPresaX and p.posicionY == posicionPresaY:
                animalesP.remove(p)
                break
        self.comer(direccion)
    def reproduccionD():
        pass
        
# Segunda clase hija (Presa)
class presa(Animal):
    # Usaremos el radar de la clase padre en la simulación principal.
    def reproduccionP():
        pass

# Funcion para agregar comida
def agregarComida(matriz):        
    for i in range(4):
        y = random.randint(2,17)
        x = random.randint(2,17)
        matriz[y][x] = " *"
        matriz[y][x-1] = " *"
        matriz[y-1][x] = " *"
    return matriz

# --- 3. FUNCIONES DE INICIALIZACIÓN Y ESTADO DE STREAMLIT ---

# Inicializa la matriz, los animales y el estado SÓLO una vez
@st.cache_resource
def inicializar_simulacion():
    # Creación de matriz
    matriz = np.full((20, 20), "  ", dtype=object)
    for j in range(19):
        matriz[0][j] = "--"
        matriz[19][j] = "--"
    for i in range(19):
        matriz[i][0] = "| "
        matriz[i][19] = "| "
    
    # Creación de animales
    animalesP_init = []
    animalesD_init = []
    
    for i in range(4):
        nombre = f"P{i+1}"
        presas = presa(nombre, 10, True, random.randint(1, 6), random.randint(1, 18))
        animalesP_init.append(presas)
        
    for j in range(5):
        nombre = f"D{j+1}"
        depredadores = depredador(nombre, 10, True, random.randint(14, 18), random.randint(1, 18))
        animalesD_init.append(depredadores)
        
    # Agrega comida inicial
    matriz = agregarComida(matriz)
    
    # Inserta los animales en la matriz
    for d in animalesD_init:
        matriz[d.posicionY][d.posicionX] = d.nombre
    for p in animalesP_init:
        matriz[p.posicionY][p.posicionX] = p.nombre
        
    return matriz, animalesP_init, animalesD_init

# Función que ejecuta la lógica de un solo "tick"
def run_one_tick(matriz, animalesP, animalesD, dia):
    
    # Lógica de las Presas
    for id in animalesP:
        yaSeMovio = False
        posicionYanterior = id.posicionY
        posicionXanterior = id.posicionX
        
        # Le pasamos la matriz a los radares
        posComida = id.radarComida(matriz)
        posLibre = id.radarLibre(matriz)
        posDepredador = id.radarDepredador(matriz)

        # Prioridad 1: Evitar Depredador (Si detecta un depredador, no se mueve hacia él)
        if any(posDepredador):
            # Tu lógica original era confusa: si detecta uno, yaSeMovio = True
            # Y luego resetea la posición, lo que significa "NO TE MUEVAS".
            # Una lógica más clara para 'evitar' sería moverse a un posLibre
            # que NO esté cerca del depredador. Por simplicidad, mantendremos la tuya.
            yaSeMovio = True 

        # Prioridad 2: Buscar Comida
        if not yaSeMovio and any(posComida):
            for comida in posComida:
                if comida != 0:
                    id.comer(comida)
                    yaSeMovio = True
                    break

        # Prioridad 3: Movimiento Aleatorio
        if not yaSeMovio and any(posLibre):
            libres = [pos for pos in posLibre if pos != 0]
            if libres:
                b = random.choice(libres)
                id.moveAll(b)
                yaSeMovio = True

        # Actualiza la matriz (SÓLO si se movió o si estaba quieto)
        if yaSeMovio or True: # siempre debemos actualizar la matriz
            matriz[posicionYanterior, posicionXanterior] = "  "
            matriz[id.posicionY][id.posicionX] = id.nombre

    # Lógica de los Depredadores
    for id in animalesD:
        yaSeMovio = False
        posicionYanterior = id.posicionY
        posicionXanterior = id.posicionX

        # Le pasamos la matriz a los radares
        posAnimales = id.radarPresa(matriz)
        posComida = id.radarComida(matriz) # Opcional: Depredadores podrían comer comida.
        posLibre = id.radarLibre(matriz)

        # Prioridad 1: Cazar Presa
        if any(posAnimales):
            for animal in posAnimales:
                if animal != 0:
                    # Llama a matar y le pasa la lista global animalesP
                    id.matar(animal, animalesP) 
                    yaSeMovio = True
                    break
        
        # Prioridad 2: Buscar Comida (Si no hay presa)
        if not yaSeMovio and any(posComida):
            for comida in posComida:
                if comida != 0:
                    id.comer(comida)
                    yaSeMovio = True
                    break

        # Prioridad 3: Movimiento Aleatorio
        if not yaSeMovio and any(posLibre):
            libres = [pos for pos in posLibre if pos != 0]
            if libres:
                b = random.choice(libres)
                id.moveAll(b)
                yaSeMovio = True
        
        # Actualiza la matriz
        if yaSeMovio or True: # siempre debemos actualizar la matriz
            matriz[posicionYanterior, posicionXanterior] = "  "
            matriz[id.posicionY][id.posicionX] = id.nombre
            
    # Manejo de la comida después de los movimientos
    if not np.any(matriz == " *"):
        matriz = agregarComida(matriz)
        
    return matriz, animalesP, animalesD

# --- 4. INTERFAZ PRINCIPAL DE STREAMLIT ---

def main_streamlit():
    st.title("🌱 Simulación de Ecosistema (Presas y Depredadores)")

    # 4.1. Inicialización de State (solo si no existe)
    if 'matriz' not in st.session_state:
        st.session_state.matriz, st.session_state.animalesP, st.session_state.animalesD = inicializar_simulacion()
        st.session_state.tick = 0
        st.session_state.dia = True
        st.session_state.mensaje = "Simulación Iniciada (DÍA)"
        
    matriz = st.session_state.matriz
    animalesP = st.session_state.animalesP
    animalesD = st.session_state.animalesD
    
    # Parámetros del ciclo
    DURACION_DIA = 15
    DURACION_NOCHE = 5
    CICLO_COMPLETO = DURACION_DIA + DURACION_NOCHE
    
    # 4.2. Función del botón "Next Tick"
    def handle_tick():
        # Lógica del ciclo Día/Noche
        if st.session_state.tick == DURACION_DIA - 1:
            st.session_state.dia = False
            st.session_state.mensaje = "NOCHE INICIADA 🌙"
            st.session_state.tick = 0
            
        elif st.session_state.tick == DURACION_NOCHE - 1 and not st.session_state.dia:
            st.session_state.dia = True
            st.session_state.mensaje = "DÍA INICIADO ☀️"
            st.session_state.tick = 0

        else:
            st.session_state.tick += 1
            st.session_state.mensaje = f"{'DÍA' if st.session_state.dia else 'NOCHE'} - Tick: {st.session_state.tick + 1}"

        # Ejecutar la lógica de movimiento SOLO si es de día (como en tu código original)
        if st.session_state.dia:
            st.session_state.matriz, st.session_state.animalesP, st.session_state.animalesD = run_one_tick(
                st.session_state.matriz, st.session_state.animalesP, st.session_state.animalesD, st.session_state.dia
            )

    # 4.3. Renderización de la UI
    st.subheader(st.session_state.mensaje)
    st.info(f"Presas (P): **{len(animalesP)}** | Depredadores (D): **{len(animalesD)}**")
    
    # Botón de avance
    st.button("Avanzar 1 Tick (Ejecutar Lógica de Movimiento)", on_click=handle_tick)
    
    # Muestra la Matriz
    st.code('\n'.join(' '.join(row) for row in st.session_state.matriz))
    
    # Botón para resetear la simulación
    if st.button("Resetear Simulación", type="primary"):
        # Esto borra el caché de recursos y fuerza la reinicialización
        st.cache_resource.clear()
        # Esto borra el estado de la sesión y fuerza un re-run
        st.session_state.clear()
        st.experimental_rerun()


if __name__ == "__main__":
    main_streamlit()

def funcionFinal():
    pass