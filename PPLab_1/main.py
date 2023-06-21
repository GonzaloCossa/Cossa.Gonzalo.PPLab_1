from funciones import *
import os

datos_insumos = []
# Estas listas vacias son para guardas compras realizadas anteriormente
productos_elegidos = []
cantidad_elegidos = []
subtotales = []
# Flags para el ingreso de los puntos
flag_carga = False
flag_carga_archivo_json = False

while True:
    os.system("cls")
    match mostrar_menu():
        case 1:
            # PUNTO 1                                      Carga Archivo CSV
            if not flag_carga:
                if cargar_csv(datos_insumos):
                    print("\n¡Los insumos de la tieda de mascotas han sido cargados correctamente!\n")
                    flag_carga = True
            else: 
                print("\nLa carga de datos ya ha sido realizada anteriormente.")
        case 2:
            # PUNTO 2                                  Listar Cantidad por Marca
            if flag_carga:
                marcas_sin_repetir = crear_lista_sin_repetir(datos_insumos, 'MARCA')
                listar_cantidad_marca(marcas_sin_repetir, datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 3:
            # PUNTO 3                                  Listar Insumos por Marca
            if flag_carga:
                marcas_sin_repetir = crear_lista_sin_repetir(datos_insumos, 'MARCA')
                listar_insumos_marca(marcas_sin_repetir, datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 4:
            # PUNTO 4                              Buscar Insumo por Caracteristica
            if flag_carga:
                buscar_caracteristica(datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 5:
            # PUNTO 5                                  Listar Insumos Ordenados
            if flag_carga:
                listar_insumos_ordenados(datos_insumos, 'MARCA', 'PRECIO')
            else:
                print("\nPrimero hay que cargar los datos.")
        case 6:
            # PUNTO 6                                      Realizar Compras
            if flag_carga:
                productos_sin_repetir = crear_lista_sin_repetir(datos_insumos, 'NOMBRE')
                realizar_compras(datos_insumos, productos_sin_repetir, productos_elegidos, cantidad_elegidos, subtotales)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 7:
            # PUNTO 7                   Guardar Insumos Con "Alimento" en el Nombre en Formato JSON
            if flag_carga:
                guardar_insumos_alimentos_json(datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 8:
            # PUNTO 8                                      Leer Archivo JSON
                leer_insumo_json()
        case 9:
            # PUNTO 9                          Aplicar el Aumento del 8.4% a Los Insumos
            if flag_carga:
                aplicar_aumento(datos_insumos, "insumos.csv")
                print("\nLos precios de los insumos han sido actualizados, vuelva a carga el CSV.")
                flag_carga = False
            else:
                print("\nPrimero hay que cargar los datos.")
        case 10:
            # PUNTO 10                                     Nueva Alta Insumo
            if flag_carga:
                alta_insumo(datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 11:
            # PUNTO 11                       Guardar los Nuevos Insumos y los Actualizados
            if flag_carga:
                guardar_segun_exportacion(datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 12:
            # PUNTO 12                              Mostrar Stock Por Marca Ingresada
            if flag_carga:
                marcas_sin_repetir = crear_lista_sin_repetir(datos_insumos, 'MARCA')
                stock_por_marca(datos_insumos, marcas_sin_repetir)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 13:
            # PUNTO 13                                    Imprimir Bajo Stock
            if flag_carga:
                imprimir_bajo_stock(datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 14:
            # PUNTO 14                                           SALIDA
            print("\nGracias por usar el programa!")
            break
    os.system("pause")