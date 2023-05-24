from funciones import mostrar_menu, cargar_csv, crear_lista_sin_repetir, listar_cantidad_marca, listar_insumos_marca, buscar_caracteristica, listar_insumos_ordenados, realizar_compras, guardar_insumos_alimentos_json, leer_insumo_json, aplicar_aumento
import os

datos_insumos = []
flag_carga = False

while True:
    os.system("cls")
    match mostrar_menu():
        case 1:
            # PUNTO 1
            if not flag_carga:
                if cargar_csv(datos_insumos, "PPLab_1\insumos.csv"):
                    print("\n¡Los insumos de la tieda de mascotas han sido cargados correctamente!")
                    flag_carga = True
            else: 
                print("\nLa carga de datos ya ha sido realizada anteriormente.")
        case 2:
            # PUNTO 2
            if flag_carga:
                marcas_sin_repetir = crear_lista_sin_repetir(datos_insumos, 'MARCA')
                listar_cantidad_marca(marcas_sin_repetir, datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 3:
            # PUNTO 3
            if flag_carga:
                marcas_sin_repetir = crear_lista_sin_repetir(datos_insumos, 'MARCA')
                listar_insumos_marca(marcas_sin_repetir, datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 4:
            # PUNTO 4
            if flag_carga:
                buscar_caracteristica(datos_insumos)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 5:
            # PUNTO 5
            if flag_carga:
                listar_insumos_ordenados(datos_insumos, 'MARCA', 'PRECIO')
            else:
                print("\nPrimero hay que cargar los datos.")
        case 6:
            # PUNTO 6
            if flag_carga:
                marcas_sin_repetir = crear_lista_sin_repetir(datos_insumos, 'MARCA')
                realizar_compras(datos_insumos, marcas_sin_repetir)
            else:
                print("\nPrimero hay que cargar los datos.")
        case 7:
            # PUNTO 7
            if flag_carga:
                guardar_insumos_alimentos_json(datos_insumos, r"PPLab_1\nombres_con_alimento.json")
            else:
                print("\nPrimero hay que cargar los datos.")
        case 8:
            # PUNTO 8
            if flag_carga:
                leer_insumo_json(r"PPLab_1\nombres_con_alimento.json")
            else:
                print("\nPrimero hay que cargar los datos.")
        case 9:
            # PUNTO 9
            if flag_carga:
                aplicar_aumento(datos_insumos, "PPLab_1\insumos.csv")
                print("\nLos precios de los insumos han sido actualizados, vuelva a carga el CSV.")
                flag_carga = False
            else:
                print("\nPrimero hay que cargar los datos.")
        case 10:
            # PUNTO 10 
            print("\nGracias por usar el programa!")
            break
    os.system("pause")