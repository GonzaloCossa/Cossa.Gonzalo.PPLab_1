from functools import reduce
import re
import json

def mostrar_menu() -> int: 
    """mostrar_menu Muestra el menú del programa

    Returns:
        int: Devuelve el numero de la opcion elegida
    """
    print("""                   *** MENU INSUMOS TIENDA DE MASCOTAS ***\n
    01. Cargar datos
    02. Listar cantidad por marca
    03. Listar insumos por marca
    04. Buscar insumo por característica
    05. Listar insumos ordenados
    06. Realizar compras
    07. Guardar en formato JSON
    08. Leer desde formato JSON
    09. Actualizar precios
    10. Salir """)
    opcion = int(input("\n    Ingrese una opción: "))
    return opcion

def cargar_csv(lista: list, archivo: str) -> int:
    """cargar_csv cargar_csv Se encarga de leer las filas del archivo convirtiendolas en diccionarios 
    y separarando los datos y campos, lo termina guardando en una lista de diccionarios 

    Args:
        lista (list): Lista destino donde se guadará la lista de diccionarios
        archivo (str): Dirección donde se encuentra el archivo que se tiene que leer

    Returns:
        int: Retorna una variable todoOk = 1 si los datos se cargaron correctamente y todoOk = 0 si no se cargó correctamente
    """    
    todoOk = 0  
    with open(archivo, "r", encoding= 'utf-8') as file:
        campos = file.readline().strip().split(',')
        for linea in file:
            valores = linea.strip().split(",")
            item = {}
            for i in range(len(campos)):
                item[campos[i]] = valores[i]
            lista.append(item)
    if lista: 
        todoOk = 1
    return todoOk

def crear_lista_sin_repetir(lista: list, campo: str) -> list:
    """crear_lista_sin_repetir Crea una lista la cual contiene sin repetir los valores de un campo elegido

    Args:
        lista (list): Lista donde se va a guardar la lista final de valores sin repetir
        campo (str): Campo a eleccion del cual se buscar hacer la lista

    Returns:
        list: Devuelve la lista con los valores sin repetir
    """    
    lista_destino = list(set(map(lambda x: x[campo], lista)))
    return lista_destino

def listar_cantidad_marca(lista_marcas: list, lista_insumos: list) -> None:
    """listar_cantidad_marca Recorre la lista pasada por parametro y a su vez la lista de insumo 
    comparando que sea la misma en cada caso y la mostramos

    Args:
        lista_marcas (list): Lista con todas las marcas disponibles
        lista_insumos (list): Lista con todos los insumos disponibles
    """    
    print("--------------------------------------------------------------------")
    for marca in lista_marcas:
        cant_por_marca = len(list(filter(lambda insumo: insumo['MARCA'] == marca, lista_insumos)))
        print(f"La marca es: {marca} y su cantidad de insumos es: {cant_por_marca}")
        print("--------------------------------------------------------------------")

def listar_insumos_marca(lista_marcas: list, lista_insumos: list) -> None:
    """listar_insumos_marca Recorremos la lista de marcas y mostramos el nombre y precio los insumos que pertenecen a ella

    Args:
        lista_marcas (list): Lista con todas las marcas disponibles
        lista_insumos (list): Lista con todos los insumos disponibles
    """    
    for marca in lista_marcas:
        print(f"MARCA: {marca}")
        print("--------------------------------------------------------------------")
        insumos_filtrados = filter(lambda insumo: insumo['MARCA'] == marca, lista_insumos)
        for insumo in insumos_filtrados:
            print(f"Nombre: {insumo['NOMBRE']:34s} Precio: {insumo['PRECIO']:8s}")
        print("--------------------------------------------------------------------\n")

def buscar_caracteristica(lista_insumos: list) -> None:
    """buscar_caracteristica Pedimos una caracteristica por input, luego buscamos como patron esa caracteristica e imprimimos las coincidencias 

    Args:
        lista_insumos (list): Lista de los insumos disponibles
    """    
    patron = str(input("Porfavor, ingrese la caracteristica que desea buscar: "))
    lista_insumos_carac = []
    for insumo in lista_insumos:
        if re.findall(patron, insumo['CARACTERISTICAS']):
            lista_insumos_carac.append(insumo)
    if lista_insumos_carac:
        mostrar_insumos(lista_insumos_carac)
    else: print("No existen insumos con esa caracteristica.")

def listar_insumos_ordenados(lista: list, key_uno: str, key_dos: str):
    """listar_insumos_ordenados Recorre la lista de insumos y ordena con un burbujeo 
    comparando entre campos y si surge una igualidad, se compara por el segundo campo

    Args:
        lista (list): Lista destinada a ser ordenada
        key_uno (str): Primer campo en el cual se va a basar el ordenamiento
        key_dos (str): Segundo campo en el cual se va a basar el ordenamiento en caso de igualdad en el primer campo
    """    
    lista_aux = lista
    for i in range(len(lista_aux) - 1):
        for j in range(i + 1, len(lista_aux)):
            if((((lista_aux[i][key_uno] == lista_aux[j][key_uno] and lista_aux[i][key_dos] < lista_aux[j][key_dos]) or lista_aux[i][key_uno] > lista_aux[j][key_uno]))):
                    aux = lista_aux[i]
                    lista_aux[i] = lista_aux[j]
                    lista_aux[j] = aux
    
    for insumo in lista_aux:
        texto_encontrado = insumo['CARACTERISTICAS'].split("~", 1)[0]
        insumo['CARACTERISTICAS'] = texto_encontrado
    mostrar_insumos(lista_aux)

def realizar_compras(lista_insumos: list, lista_marcas: list) -> None:
    """realizar_compras Se encarga de realizar las compras que solicite el usuario, mostrando marcas, solicitando un id y luego validando, 
    guarda la compra en compra.txt 

    Args:
        lista_insumos (list): Lista de los insumos disponibles
        lista_marcas (list): Lista de las marcas disponibles 
    """    
    cantidad_elegidos = []
    productos_elegidos = []
    producto_elegido = []
    subtotales = []
    subtotal = 0.0
    hay_compra = False
    seguir = 's'

    while seguir.lower() == 's':
        print("\nEstas son las marcas disponibles:\n")
        for marca in lista_marcas:
            print(f"{marca}")
        marca_ingresada = str(input("\nPorfavor, ingrese la marca que desea buscar: ")).capitalize()
        lista_marca_ingresada = list(filter(lambda insumo: insumo['MARCA'] == marca_ingresada, lista_insumos))

        if lista_marca_ingresada:
            print(f"\nEstos son los productos disponibles de {marca_ingresada}:")
            mostrar_insumos(lista_marca_ingresada)

            id_ingresado = str(input("\nIngrese el ID del producto que quiere: "))
            producto_elegido = list(filter(lambda insumo: insumo['MARCA'] == marca_ingresada and insumo['ID'] == id_ingresado, lista_insumos))
            
            if producto_elegido:
                producto_elegido = producto_elegido[0]
                cantidad_ingresada = int(input("\nIngrese la cantidad del producto que desea comprar: "))
                while cantidad_ingresada < 1:
                    cantidad_ingresada = input("\nError, cantidad invalida, reingrese: ")
                productos_elegidos.append(producto_elegido)
                cantidad_elegidos.append(cantidad_ingresada)
                subtotal = float(re.sub(r'[^\d.]', '', producto_elegido['PRECIO'])) * cantidad_ingresada
                subtotales.append(subtotal)
                hay_compra = True
            else: 
                print(f"\nNo existe el ID {id_ingresado} para la marca {marca_ingresada}")

        else: print(f"\nNo hay insumos para la marca {marca_ingresada}")

        seguir = input("\nDesea seguir comprando? s/n: ")

    if hay_compra:
        total = reduce(lambda ant, sig: ant + sig, subtotales)
        print(f"\nEl total de la compra es de: ${total}")
        with open("PPLab1\compra.txt", "w") as file:
            file.write("FACTURA DE COMPRA\n\n")
            file.write("Cantidad   Producto                           Marca                    Subtotal   \n")
            file.write("---------------------------------------------------------------------------------\n")
            for i in range(len(productos_elegidos)):
                insumo = productos_elegidos[i]
                cantidad = cantidad_elegidos[i]
                subtotal = subtotales[i]
                file.write(f"{cantidad:^8d}   {insumo['NOMBRE']:34s} {insumo['MARCA']:24s} ${subtotal:.2f}\n")
                file.write("---------------------------------------------------------------------------------\n")
            file.write(f"El total de la compra es de: ${total}")

def guardar_insumos_alimentos_json(lista_insumos: list, archivo: str) -> None:
    """guardar_insumos_alimentos_json Se encarga de escribir en un archivo .json todos aquellos insumos filtrados que contengan en su nombre
    la cadena "Alimento"

    Args:
        lista_insumos (list): Lista de los insumos dispobles
        archivo (str): Dirección del archivo donde se van a guardar los insumos filtrados
    """    
    with open(archivo, "w", encoding= 'utf-8') as file:
        lista_filtrada = list(filter(lambda insumo: re.findall('Alimento', insumo['NOMBRE']), lista_insumos))
        json.dump(lista_filtrada, file, ensure_ascii=False, indent=4)

def leer_insumo_json(archivo: str) -> None:
    """leer_insumo_json Se encarga de leer el archivo .json en cuestión y muestra sus insumos

    Args:
        archivo (str): Dirección del archivo donde se van a leer los insumos filtrados
    """    
    with open(archivo, "r", encoding= 'utf-8') as file:
        lista = json.load(file)
        mostrar_insumos(lista)

def aplicar_aumento(lista_insumos: list, archivo: str) -> None:
    with open(archivo, "w", encoding= 'utf-8') as file:
        precio_actualizado = lambda insumo: "${:.2f}".format(round(float(re.sub(r'\$', '', insumo['PRECIO'])) * 1.084, 2))
        insumos_actualizados = list(map(lambda insumo: {campo: valor if campo != "PRECIO" else precio_actualizado(insumo) for campo, valor in insumo.items()}, lista_insumos))
        campos = ["ID","NOMBRE","MARCA","PRECIO","CARACTERISTICAS"]
        file.write(",".join(campos) + "\n")
        lines = [','.join(str(valor) for valor in insumo.values()) for insumo in insumos_actualizados]
        file.write('\n'.join(lines))
        lista_insumos.clear()

def mostrar_insumo(insumo: dict):
    """mostrar_insumo Se encarga de mostrar los valores de un insumo especifico

    Args:
        insumo (dict): Insumo pedido para mostrar
    """    
    print(f"| {(insumo['ID']):2s} | {insumo['NOMBRE']:34s} | {insumo['MARCA']:24s}| {insumo['PRECIO']:8s} |  {insumo['CARACTERISTICAS']:88s}|")

def mostrar_insumos(lista: list):
    """mostrar_insumos Se encarga de mostrar los valores de una lista de insumos especificos

    Args:
        lista (list): Lista de insumos que se van a mostrar
    """    
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print(f"| ID | NOMBRE                             | MARCA                   | PRECIO   |  CARACTERISTICAS                                                                         |")
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for insumo in lista:
        mostrar_insumo(insumo)
        print("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------")