from functools import reduce
import re
import json
import os

def mostrar_menu() -> int: 
    """mostrar_menu Muestra el menú del programa

    Returns:
        int: Devuelve el numero de la opcion elegida
    """
    while True:
        os.system("cls")
        print("""                   *** MENU INSUMOS TIENDA DE MASCOTAS ***\n
        1.  Cargar datos
        2.  Listar cantidad por marca
        3.  Listar insumos por marca
        4.  Buscar insumo por característica
        5.  Listar insumos ordenados
        6.  Realizar compras
        7.  Guardar en formato JSON
        8.  Leer desde formato JSON
        9.  Actualizar precios
        10. Salir """)

        opcion = input("\nIngrese una opción: ")
        # Valido que solo entre numeros y que esté entre 1 y 10
        if re.match(r'^\d+$', opcion): 
            opcion = int(opcion)
            if opcion >= 1 and opcion <= 10:
                break
        print("\nError, opcion invalida")
        os.system("pause")
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
    # Creo una lista de caracteristicas sin repetir para luegro mostrar todas antes del input del usuario
    caracteristicas = []
    caracteristicas_separadas = [] 
    for insumo in lista_insumos:
        caracteristicas.append(insumo['CARACTERISTICAS'])

    for i in caracteristicas:
        caracteristica = i.split("~")
        caracteristicas_separadas.extend(caracteristica)

    caracteristicas_sin_repetir = list(set(caracteristicas_separadas))
    print("\nEstas son las caracteristicas disponibles:\n")
    for caracteristica in caracteristicas_sin_repetir:
        print(f"{caracteristica}") 

    # Se solicita la caracteristica y se valida
    carac_ingresada = str(input("\nPorfavor, ingrese la caracteristica que desea buscar: "))
    while carac_ingresada == '':
        carac_ingresada = str(input("\nError, no ingresó una caracteristica, reingrese: "))
    patron = re.compile(f"(^|~){carac_ingresada}(~|$)", flags= re.IGNORECASE)

    # Buscamos los insumos que coincidan con la caracteristica y lo mostramos en consola
    lista_insumos_carac = []
    for insumo in lista_insumos:
        if re.findall(patron, insumo['CARACTERISTICAS']):
            lista_insumos_carac.append(insumo)
    if lista_insumos_carac:
        print(f"\nEstos son los insumos que incluyen como caracteristica {carac_ingresada}:")
        mostrar_insumos(lista_insumos_carac)
    else: print("\nNo existen insumos con esa caracteristica.")

def listar_insumos_ordenados(lista: list, key_uno: str, key_dos: str):
    """listar_insumos_ordenados Recorre la lista de insumos y ordena con un burbujeo 
    comparando entre campos y si surge una igualidad, se compara por el segundo campo

    Args:
        lista (list): Lista destinada a ser ordenada
        key_uno (str): Primer campo en el cual se va a basar el ordenamiento
        key_dos (str): Segundo campo en el cual se va a basar el ordenamiento en caso de igualdad en el primer campo
    """   
    # Copiamos los insumos originales en una lista auxiliar
    lista_aux = [insumo.copy() for insumo in lista]
    
    # Acá cambiamos la caracteristica de cada insumo a solo la primera de cada uno y los mostramos
    for insumo in lista_aux:
        primer_caracteristica = insumo['CARACTERISTICAS'].split("~", 1)[0]
        insumo['CARACTERISTICAS'] = primer_caracteristica

    # Ordenamos la lista auxiliar
    for i in range(len(lista_aux) - 1):
        for j in range(i + 1, len(lista_aux)):
            if lista_aux[i][key_uno] > lista_aux[j][key_uno] or (lista_aux[i][key_uno] == lista_aux[j][key_uno] and float(re.sub(r'\$', '', lista_aux[i][key_dos])) < float(re.sub(r'\$', '', lista_aux[j][key_dos]))):
                aux = lista_aux[i]
                lista_aux[i] = lista_aux[j]
                lista_aux[j] = aux
    
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
    salir = 'n'

    while seguir.lower() == 's':
        # Mostramos todas las marcas sin repetir
        print("\nEstas son las marcas disponibles:\n")
        for marca in lista_marcas:
            print(f"{marca}")

        # Solicitamos y validamos la marca ingresada
        marca_ingresada = str(input("\nPorfavor, ingrese la marca que desea buscar: ")).title()
        while marca_ingresada == '':
            salir = str(input("\nNo hay ingresado ninguna marca, desea salir? s/n: ")).lower()
            if salir == 'n':
                marca_ingresada = str(input("\nReingrese una marca porfavor: ")).title()
            else:
                break
        
        # Con la funcion filter y list añadimos a la lista de insumos con la marca ingresada, comparando la marca del insumo con la ingresada
        lista_marca_ingresada = list(filter(lambda insumo: insumo['MARCA'] == marca_ingresada, lista_insumos))

        # Si se se encontraron insumos con esa marca los mostramos sino, avisamos que no hay insumos con esa marca
        if lista_marca_ingresada:
            print(f"\nEstos son los productos disponibles de {marca_ingresada}:")
            mostrar_insumos(lista_marca_ingresada)

            # Acá pedimos el ID del producto que desea el usuario y validamos que no esté vacio
            id_ingresado = str(input("\nIngrese el ID del producto que quiere: "))
            while id_ingresado == '':
                id_ingresado = str(input("\nError, no ingresó ningún ID, reingrese: "))

            # En caso de encontrar coincidencia con los datos ingresados y el producto elegido lo guardamos
            producto_elegido = list(filter(lambda insumo: insumo['MARCA'] == marca_ingresada and insumo['ID'] == id_ingresado, lista_insumos))
            
            # Si se encontró un insumo con esa marca y ID seguimos pidiendo datos, sino avisamos que no existe ese ID para la marca ingresada
            if producto_elegido:
                # El producto que se eligió es el primero de la lista
                producto_elegido = producto_elegido[0]

                # Pedimos la cantidad del insumo que desea el usuario y validamos que no sea negativo ni que ingrese una cadena vacia
                cantidad_ingresada = str(input("\nIngrese la cantidad del producto que desea comprar: "))
                while cantidad_ingresada == '' or int(cantidad_ingresada) < 1:
                    cantidad_ingresada = str(input("\nError, cantidad invalida, reingrese: "))
                cantidad_ingresada = int(cantidad_ingresada)

                # Agregamos a las listas el producto y la cantidad para luego poder mostrarlos en el .TXT
                productos_elegidos.append(producto_elegido)
                cantidad_elegidos.append(cantidad_ingresada)

                # Sacamos el "$" para evitar problemas y calculas el subtotal del producto ingresado, agregamos el subtotal a la lista de subtotales
                precio = float(re.sub(r'\$', '', producto_elegido['PRECIO']))
                subtotal = precio * cantidad_ingresada
                subtotales.append(subtotal)

                # Flag para identificar que se realizó la compra
                hay_compra = True
            else: 
                print(f"\nNo existe el ID {id_ingresado} para la marca {marca_ingresada}")

        else:
            if salir != 's': 
                print(f"\nNo hay insumos para la marca {marca_ingresada}")

        # En caso de que el usuario decida salir antes de tiempo por ingresar un dato erroneamente 
        if salir == 's':
            break
        
        # En caso de que se haga realizado la primer compra, se le pregunta al usuario si desea seguir comprando, validamos el ingreso 
        seguir = str(input("\nDesea seguir comprando? s/n: ")).lower()
        while seguir != 's' and seguir != 'n':
            seguir = str(input("\nRespuesta invalida, desea seguir comprando? s/n: ")).lower()

    # En caso de que haya una compra, calculamos su total y escribimos los datos en el .TXT
    if hay_compra:
        # Total de toda la compra
        total = reduce(lambda ant, sig: ant + sig, subtotales)
        print(f"\nEl total de la compra es de: ${total}")

        # Abrimos el archivo para luego escribir todos los insumos que compró
        with open("PPLab_1\compra.txt", "w") as file:
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
        
    # Abrimos el archivo .JSON
    with open(archivo, "w", encoding= 'utf-8') as file:
        # Filtramos aquellos insumos que tengas en el nombre 'Alimento'
        lista_filtrada = list(filter(lambda insumo: re.findall('Alimento', insumo['NOMBRE']), lista_insumos))
        #Escribimos los insumos en el archivo
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
    """aplicar_aumento Se encarga de actualizar los precios de una lista aumentandolos en un 8.4% y escribiendo los nuevos insumos en el archivo .csv

    Args:
        lista_insumos (list): Lista de los insumos con datos solicitados a ser actualizados
        archivo (str): Dirección del archivo .csv que contiene los datos de los insumos
    """    
    # Funcion lambda que sirve para quitarle el simbolo '$' y se le agrega el 8.4%, luego volvemos a colocarle el simbolo
    precio_actualizado = lambda insumo: "${:.2f}".format(round(float(re.sub(r'\$', '', insumo['PRECIO'])) * 1.084, 2))

    # Agreamos a una lista de insumos nueva los insumos con el campo 'PRECIO' actualizado
    insumos_actualizados = [{campo: valor if campo != "PRECIO" else precio_actualizado(insumo) for campo, valor in insumo.items()} for insumo in lista_insumos]
    
    # Abrimos el archivo CSV
    with open(archivo, "w", encoding= 'utf-8') as file:
        campos = ["ID","NOMBRE","MARCA","PRECIO","CARACTERISTICAS"]
        
        # Se escribe como primera linea los campos
        file.write(','.join(campos) + '\n')

        # Se crea una lista llamada valores que representa en cadena los valores de cada insumo separados por ','
        valores = [','.join(str(valor) for valor in insumo.values()) for insumo in insumos_actualizados]

        # Coloca '\n' al final de cada linea
        file.write('\n'.join(valores))

        # Se encarga de limpiar la lista de insumos antigua para luego actualizarla entrando a la opcion 1 del menú de nuevo
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