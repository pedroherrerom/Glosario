import pandas as pd
import sqlite3
from numpy import random as rd

def conectar_bd(nombre_bd='glosario.db'):
    """Conecta a la base de datos SQLite y devuelve un DataFrame con los datos"""
    try:
        conexion = sqlite3.connect(nombre_bd)
        df = pd.read_sql_query("SELECT * FROM glosario", conexion)
        conexion.close()
        return df
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def cargar_desde_csv(nombre_csv='glosariocsv.csv'):
    """Carga datos desde un archivo CSV y adapta el formato al esperado por el programa"""
    try:
        df = pd.read_csv(nombre_csv)
        
        # Asegurar columnas mínimas requeridas
        required_columns = ['traduccion_espanol', 'palabra_ingles', 'categoria']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Columna requerida '{col}' no encontrada en el CSV")
        
        return df
    except Exception as e:
        print(f"Error al cargar el archivo CSV: {e}")
        return None

def seleccionar_fuente_datos():
    """Permite al usuario seleccionar la fuente de datos"""
    while True:
        try:
            fuente = 1
            # int(input("Selecciona fuente de datos:\n1. Base de datos SQLite\n2. Archivo CSV\n= "))
            if fuente in [1, 2]:
                return fuente
            print("Por favor, introduce 1 o 2")
        except ValueError:
            print("Entrada inválida. Introduce 1 o 2")

def seleccionar_modo():
    """Permite al usuario seleccionar el modo de juego"""
    while True:
        try:
            modo = int(input("Introduce 1 para Español → Inglés \nIntroduce 0 para Inglés → Español \n= "))
            if modo in [0, 1]:
                return modo
            print("Por favor, introduce 0 o 1")
        except ValueError:
            print("Entrada inválida. Introduce 0 o 1")

def seleccionar_tipo_palabra():
    """Permite al usuario seleccionar el tipo de palabra con el que va a jugar"""
    while True:
        try:
            print("Introduce \n0 : Para jugar con todas las palabras \n1 : Para jugar solo con sustantivos \n2 : Para jugar solo con adjetivos \n3 : Para jugar solo con verbos \n4 : Para jugar solo con adverbios y conectores")
            numero = int(input(" "))
            if numero in [0,1,2,3,4]:
                lista_tipo_palabra = ["Todas","Sustantivo", "Adjetivo", "Verbo", "Adverbio"]
                tipo_palabra = lista_tipo_palabra[numero]
                print("MODO: {}".format(tipo_palabra))
                return tipo_palabra
            print("Por favor, introduce 0, 1, 2, 3 o 4 ")
        except ValueError:
            print("Entrada inválida. Introduce 0, 1, 2, 3 o 4")

def buscador_tipo_palabra(tipo_palabra, df):
    """Filtra el DataFrame según el tipo de palabra seleccionado"""
    if df is None:
        return None
        
    if tipo_palabra == "Adverbio":
        categoria = df[(df['categoria'] == 'Adverbio') | (df['categoria'] == 'Conector')]
    elif tipo_palabra == "Verbo":
        categoria = df[(df['categoria'] == 'Verbo') | (df['categoria'] == 'Verbo frasal') | (df['categoria'] == 'Expresión')]
    elif tipo_palabra == 'Todas':
        categoria = df
    else:
        categoria = df[df["categoria"] == tipo_palabra]
    
    return categoria

def eliminar_palabra(df, posicion):
    """Elimina por posición numérica (robusta a índices discontinuos)"""
    try:
        return df.drop(df.index[posicion])
    except IndexError:
        return df

def mostrar_ejemplo(df, indice):
    """Muestra el ejemplo de la palabra si lo hay"""
    ejemplo = df["ejemplo"].iloc[indice]
    if ejemplo=="":
        return None
    return ejemplo

def jugar_ronda(df, modo, indice):
    """Ejecuta una ronda del juego según el modo seleccionado"""
    if modo == 1:  # Español → Inglés
        palabra = df["traduccion_espanol"].iloc[indice]
        respuesta_correcta = df["palabra_ingles"].iloc[indice]
        direccion = "inglés"
    else:  # Inglés → Español
        palabra = df["palabra_ingles"].iloc[indice]
        respuesta_correcta = df["traduccion_espanol"].iloc[indice]
        direccion = "español"
    
    print(f"\nLa palabra es: {palabra}")
    intento = input(f"Su traducción a {direccion} es: ").strip()
    
    return intento, respuesta_correcta

def main():
    """Función principal que ejecuta el juego"""
    print("----------------------------------\nBienvenido al Juego de Vocabulario\n----------------------------------")
    
    # Seleccionar fuente de datos
    fuente = seleccionar_fuente_datos()
    
    # Cargar datos según la fuente seleccionada
    if fuente == 1:
        df = conectar_bd()
    else:
        # nombre_csv = input("Introduce el nombre del archivo CSV (o presiona Enter para 'glosariocsv.csv'): ")
        # df = cargar_desde_csv(nombre_csv if nombre_csv else 'glosariocsv.csv')
        df = cargar_desde_csv('glosariocsv.csv')
    
    if df is None or df.empty:
        print("No se pudieron cargar los datos del glosario.")
        return
    
    # Configurar juego
    puntos = 0
    modo = seleccionar_modo()
    tipo_palabra = seleccionar_tipo_palabra()
    df_filtrado = buscador_tipo_palabra(tipo_palabra, df)
    palabras_totales = len(df_filtrado)
    
    if df_filtrado is None or df_filtrado.empty:
        print("No hay palabras del tipo seleccionado.")
        return
    
    print(f"Tienes que traducir {palabras_totales} palabras")
    continuar = True
    
    # Bucle principal del juego.
    while continuar:
        if palabras_totales == 1:
            indice = 0
        else:
            indice = rd.randint(0, len(df_filtrado))
        ejemplo = mostrar_ejemplo(df_filtrado, indice)
        intento, respuesta = jugar_ronda(df_filtrado, modo, indice)        
        if intento.lower() == respuesta.lower():
            puntos += 1
            if ejemplo != None:
                print(f"EJEMPLO DE USO: {ejemplo}")
            df_filtrado = eliminar_palabra(df_filtrado, indice)
            palabras_restantes = len(df_filtrado)
            print(f"¡Correcto! +1 punto (Total: {puntos})")
            if palabras_restantes == 0:
                print(f"Enhorabuena, has traducido correctamente {palabras_totales} palabras")
                break
            print(f"Quedan {palabras_restantes} palabras de {palabras_totales}")
        else:
            print(f"Incorrecto. La respuesta correcta es: {respuesta}")
        
        # Preguntar si continuar
        opcion = input("\nPresiona Enter para continuar o cualquier otra tecla + Enter para salir: ")
        continuar = opcion == ''
    
    print(f"\nJuego terminado. \nPuntos totales: {puntos}")

if __name__ == "__main__":
    main()