from functools import reduce
import random, re, json, os

def mostrar_menu() -> int: 
    """mostrar_menu Muestra el menú del programa

    Returns:
        int: Devuelve el numero de la opcion elegida
    """
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
    10. Agregar nuevo producto
    11. Guardar nuevos productos
    12. Stock por Marca
    13. Imprimir Bajo Stock
    14. Salir """)

    while True:
        try:
            opcion = int(input("\nIngrese una opción: "))
            if opcion > 0 and opcion <= 14:
                return opcion
        except ValueError:
            print("\nIngrese una opcion valida.")

def cargar_csv(lista: list) -> int:
    """cargar_csv cargar_csv Se encarga de leer las filas del archivo ingresado por el usuario convirtiendolas en diccionarios 
    y separarando los datos y campos, lo termina guardando en una lista de diccionarios 

    Args:
        lista (list): Lista destino donde se guadará la lista de diccionarios

    Returns:
        int: Retorna una variable todoOk = 1 si los datos se cargaron correctamente y todoOk = 0 si no se cargó correctamente
    """    
    todoOk = 0  
    
    archivo = input("\nIngrese el nombre del archivo .CSV que desea leer (sin extensión): ")
    try:
        with open(archivo + ".csv", "r", encoding= 'utf-8') as file:
            campos = file.readline().strip().split(',')
            for linea in file:
                valores = linea.strip().split(",")
                item = {}
                for i in range(len(campos)):
                    item[campos[i]] = valores[i]
                
                # Creamos un nuevo campo llamado STOCK y le asignamos un numero random entre 0 y 10 incluidos
                item['STOCK'] = list(map(lambda x: random.randint(0, 10), [0]))[0] # Acá agrego un nuevo campo al insumo
                lista.append(item)
        if lista: 
            todoOk = 1
        return todoOk
    except FileNotFoundError:
        print("\nError, el archivo " + archivo + " no existe.")

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
    print("------------------------------------------")
    print("|    MARCA                   |  CANTIDAD |")
    print("------------------------------------------")
    for marca in lista_marcas:
        cant_por_marca = len(list(filter(lambda insumo: insumo['MARCA'] == marca, lista_insumos)))
        print(f"|    {marca:23s} |     {cant_por_marca:1d}     |")
        print("------------------------------------------")

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

def realizar_compras(lista_insumos: list, lista_productos: list, productos_elegidos: list, cantidad_elegidos: list, subtotales: list) -> None:
    """realizar_compras Se encarga de realizar las compras que solicite el usuario, mostrando marcas, solicitando un id y luego validando, 
    guarda la compra en compra.txt 

    Args:
        lista_insumos (list): Lista de los insumos disponibles
        lista_productos (list): Lista de los productos disponibles 
        productos_elegidos (list): Lista de los productos elegidos en compras previamente realizadas
        cantidad_elegidos (list): Cantidad de los productos elegidos en compras previamente realizadas
        subtotales (list): Lista con los subtotales de los productos elegidos en compras previamente realizadas
    """  
    producto_elegido = {}
    subtotal = 0.0
    hay_compra = False
    seguir = 's'
    salir = 'n'

    while seguir.lower() == 's':
        # Mostramos todas las marcas sin repetir
        print("\nEstas son los productos disponibles:\n")
        for producto in lista_productos:
            print(f"{producto}")

        # Solicitamos y validamos la marca ingresada
        nombre_ingresado = str(input("\nPorfavor, ingrese el nombre del producto que desea buscar: "))
        while nombre_ingresado == '':
            salir = str(input("\nNo ingresó el nombre del producto, desea salir? s/n: ")).lower()
            if salir == 'n':
                nombre_ingresado = str(input("\nReingrese un nombre porfavor: "))
            else:
                break
        
        # Con la funcion filter y list añadimos a la lista de insumos con la marca ingresada, comparando la marca del insumo con la ingresada
        lista_nombre_ingresado = list(filter(lambda insumo: insumo['NOMBRE'] == nombre_ingresado, lista_insumos))

        # Si se se encontraron insumos con esa marca los mostramos sino, avisamos que no hay insumos con esa marca
        if lista_nombre_ingresado:
            print(f"\nEstos son las marcas disponibles de {nombre_ingresado}:")
            mostrar_insumos(lista_nombre_ingresado)

            # Acá pedimos el ID del producto que desea el usuario y validamos que no esté vacio
            while True:
                try:
                    id_ingresado = int(input("\nIngrese el ID del producto que quiere: "))
                    if id_ingresado < 0 or id_ingresado > int(lista_insumos[-1]['ID']):
                        print(f"\nNo existe el ID {id_ingresado} para el producto {nombre_ingresado}")
                    else:
                        id_ingresado = str(id_ingresado)
                        break
                except ValueError:
                    print("\nError, ingresó un ID invalido.")

            # En caso de encontrar coincidencia con los datos ingresados y el producto elegido lo guardamos
            producto_elegido = next(filter(lambda insumo: insumo['NOMBRE'] == nombre_ingresado and insumo['ID'] == id_ingresado, lista_insumos))
            
            # Si se encontró un insumo con esa marca y ID seguimos pidiendo datos, sino avisamos que no existe ese ID para la marca ingresada
            if producto_elegido and producto_elegido['STOCK'] > 0:

                # Pedimos la cantidad del insumo que desea el usuario y validamos que no sea negativo ni que ingrese una cadena vacia
                cantidad_ingresada = input("\nIngrese la cantidad del producto que desea comprar: ")
                while not cantidad_ingresada.isdigit() or int(cantidad_ingresada) < 1:
                    print("\nError, cantidad inválida. Ingrese un número entero positivo mayor a cero.")
                    cantidad_ingresada = input("\nIngrese la cantidad del producto que desea comprar: ")
                cantidad_ingresada = int(cantidad_ingresada)

                if cantidad_ingresada <= producto_elegido['STOCK']:
                    producto_elegido['STOCK'] -= cantidad_ingresada
                else:
                    print("\nNo hay stock suficiente, intente comprar una cantidad menor.\n")
                    os.system("pause")
                    continue

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
                print("\nNo hay stock del insumo elegido.")

        else:
            if salir != 's': 
                print(f"\nNo hay marcas para el producto {nombre_ingresado}")

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
        total = round(reduce(lambda ant, sig: ant + sig, subtotales), 2)
        print(f"\nEl total de la compra es de: ${total}\n")

        # Abrimos el archivo para luego escribir todos los insumos que compró
        with open("compra.txt", "w") as file:
            file.write("FACTURA DE COMPRA\n\n")
            file.write("Cantidad   Producto                           Marca                    Subtotal   \n")
            file.write("---------------------------------------------------------------------------------\n")

            # Ahora escribo las nuevas compras
            for i in range(len(productos_elegidos)):
                insumo = productos_elegidos[i]
                cantidad = cantidad_elegidos[i]
                subtotal = subtotales[i]
                file.write(f"{cantidad:^8d}   {insumo['NOMBRE']:34s} {insumo['MARCA']:24s} ${subtotal:.2f}\n")
                file.write("---------------------------------------------------------------------------------\n")
            file.write(f"El total de la compra es de: ${total}")
    else:
        print("\nNo se realizaron compras debido a la falta de stock o un error inesperado.\n")

def guardar_insumos_alimentos_json(lista_insumos: list) -> None:
    """guardar_insumos_alimentos_json Se encarga de escribir en un archivo .json solicitado al usuario, todos aquellos insumos filtrados que contengan en su nombre
    la cadena "Alimento"

    Args:
        lista_insumos (list): Lista de los insumos dispobles
    """

    archivo = input("\nIngrese el nombre del archivo .JSON donde desea guardar los insumos (sin extension): ")

    # Abrimos el archivo .JSON
    with open(archivo + ".json", "w", encoding= 'utf-8') as file:
        # Filtramos aquellos insumos que tengas en el nombre 'Alimento'
        lista_filtrada = list(filter(lambda insumo: re.findall('Alimento', insumo['NOMBRE']), lista_insumos))
        #Escribimos los insumos en el archivo
        json.dump(lista_filtrada, file, ensure_ascii=False, indent=4)

def leer_insumo_json() -> None:
    """leer_insumo_json Se encarga de leer el archivo .json solicitado al usuario y muestra sus insumos
    """    

    archivo = input("\nIngrese el nombre del archivo .JSON que desea leer (sin extension): ")

    try:
        with open(archivo + ".json", "r", encoding= 'utf-8') as file:
            lista = json.load(file)
            mostrar_insumos(lista)
    except FileNotFoundError:
        print("\nError, el archivo " + archivo + " no existe.\n")


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

def alta_insumo(lista_insumos: list) -> None:
    """alta_insumo Permite el agregado de un nuevo insumo creado por el usuario con un ID autoincremental

    Args:
        lista_insumos (list): Lista de insumos a la cual se le va a agregar el nuevo insumo creado
    """    
    marcas = []
    caracteristicas_ingresadas = []
    seguir = 's'

    with open("marcas.txt", "r", encoding= 'utf-8') as file:
        for linea in file:
            marca = linea.strip()
            marcas.append(marca)

    print("\nEstas son las marcas disponibles:\n")
    for marca in marcas:
        print(f"{marca}")
    
    marca_ingresada = str(input("\nPorfavor, ingrese la marca: ")).title()
    while marca_ingresada == '' or marca_ingresada not in marcas:
        marca_ingresada = str(input("\nReingrese una marca porfavor: ")).title()

    nuevo_id = str(int(lista_insumos[-1]['ID']) + 1)

    nombre_ingresado = str(input("\nIngrese el nombre del producto que quiere: "))
    while nombre_ingresado == '' or re.search(r'\d', nombre_ingresado):
        nombre_ingresado = str(input("\nError, nombre invalido, reingrese: "))

    while True: 
        try:
            precio_ingresado = float(input("Ingrese el precio del producto: "))
        except ValueError:
            print("Debe ingresar un precio, tiene que ser numerico.")
            continue
        else:
            break

    while seguir == 's' and len(caracteristicas_ingresadas) < 3:
        caracteristica_ingresada = str(input("\nIngrese una caracteristica para el producto: "))
        while caracteristica_ingresada == '':
            caracteristica_ingresada = str(input("\nIngrese una caracteristica valida para el producto: "))
            
        caracteristicas_ingresadas.append(caracteristica_ingresada)

        if len(caracteristicas_ingresadas) >= 3:
            break

        while True:
            seguir = input("\nDesea seguir agregando caracteristicas? s/n: ").lower()
            if seguir == 's' or seguir == 'n':
                break
        
    caracteristicas_unidas = "~".join(caracteristicas_ingresadas)
    
    precio_ingresado = "${:.2f}".format(precio_ingresado)
    nuevo_insumo = {'ID': nuevo_id, 'NOMBRE': nombre_ingresado, 'MARCA': marca_ingresada, 'PRECIO': precio_ingresado, 'CARACTERISTICAS': caracteristicas_unidas}

    lista_insumos.append(nuevo_insumo)

def guardar_segun_exportacion(lista_insumos: list) -> None:
    """Guarda a eleccion del usuario, en un archivo json o un archivo csv la lista de insumos que le pasamos por parametro, con un nombre elegido por el usuario

    Args:
        lista_insumos (list): lista de diccionarios 
    """    
    while True:
        formato_exportacion = input("En que tipo de archivo desea guardar los insumos? (CSV o JSON): ").lower()
        if formato_exportacion == 'json' or formato_exportacion == 'csv':
            break

    nombre_archivo = input("Ingrese el nombre del archivo (sin la extension): ")
    
    if formato_exportacion == "json":
        with open(nombre_archivo + "." + formato_exportacion, "w", encoding= "UTF-8") as file:
            json.dump(lista_insumos, file, indent= 2)

    else:
        with open(nombre_archivo + "." + formato_exportacion, "w", encoding= "UTF-8") as file:
            file.write("ID,NOMBRE,MARCA,PRECIO,CARACTERISTICAS")
            for insumo in lista_insumos:
                file.write(f"\n{insumo['ID']},{insumo['NOMBRE']},{insumo['MARCA']},{insumo['PRECIO']},{insumo['CARACTERISTICAS']}")

def stock_por_marca(lista_insumos: list, lista_marcas: list) -> None:
    """stock_por_marca Se encarga de solicitar una marca al usuario y calcula y muestra cuanto stock tiene ese insumo

    Args:
        lista_insumos (list): Lista de diccionarios 
        lista_marcas (list): Lista de las marcas disponibles sin repetir
    """    
    # Mostramos las marcas disponibles
    print("\nEstas son las marcas disponibles:\n")
    for marca in lista_marcas:
        print(f"{marca}")

    # Solicitamos y validamos la marca ingresada
    marca_ingresada = str(input("\nPorfavor, ingrese la marca que desea buscar: "))
    while marca_ingresada == '' or marca_ingresada not in lista_marcas:                
        marca_ingresada = str(input("\nError, ingresó una marca invalida, reingrese una marca porfavor: "))

    # Calculamos el stock de la marca ingresada
    productos_marca = list(filter(lambda insumo: insumo['MARCA'] == marca_ingresada, lista_insumos))
    stock_total = sum(int(insumo['STOCK']) for insumo in productos_marca)
    print(f"\nEl stock total de los productos de la marca {marca_ingresada} es: {stock_total}")

def imprimir_bajo_stock(lista_insumos: list) -> None:
    """imprimir_bajo_stock Se encarga de recorrer la lista de insumos y escribir en un archivo CSV un listado con el nombre de producto y 
    el stock de aquellos productos que tengan 2 o menos unidades de stock.

    Args:
        lista_insumos (list): Lista de insumos a recorrer
    """    
    archivo = input("\nIngrese el nombre del archivo .CSV donde desea guardar los insumos con bajo stock (sin extensión): ")
    while archivo == '' or os.path.exists(archivo + '.csv'):
        archivo = input("\nError, el archivo ya existe o ingresó un nombre del archivo .CSV valido (sin extensión): ")
    insumos_bajo_stock = filter(lambda insumo: int(insumo['STOCK']) <= 2, lista_insumos)

    with open(archivo + ".csv", "w", encoding= 'utf-8') as file:
        file.write("PRODUCTO,STOCK")
        for insumo in insumos_bajo_stock:
            file.write(f"\n{insumo['NOMBRE']},{insumo['STOCK']}")
    print("\nEl archivo " + archivo + ".csv se ha creado exitosamente con los productos de bajo stock.")

def mostrar_insumo(insumo: dict) -> None:
    """mostrar_insumo Se encarga de mostrar los valores de un insumo especifico

    Args:
        insumo (dict): Insumo pedido para mostrar
    """    
    print(f"| {(insumo['ID']):2s} | {insumo['NOMBRE']:34s} | {insumo['MARCA']:24s}| {insumo['PRECIO']:8s} |  {insumo['CARACTERISTICAS']:88s}|")

def mostrar_insumos(lista: list) -> None:
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