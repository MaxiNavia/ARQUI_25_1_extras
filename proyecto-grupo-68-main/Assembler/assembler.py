import sys
from iic2343 import Basys3
import funciones as f


file_name = sys.argv[1]

content = []
with open(file_name) as assembly:
    for linea in assembly:
        linea = linea.strip()
        if not f.es_comentario(linea) and linea != "": # Ignoramos Comentarios y lineas vacias
            # Si es que la linea contiene un comentario, limpiamos el comentario, por ejemplo: MOV A,3 \\ HOLI ---> MOV A,3
            linea = f.contiene_comentario(linea)
            content.append(f.normalizar_espacios(linea))

print("TODO EL CONTENIDO DEL ASSEMBLY --->", content)

# Obtenemos los labes del codigo
labels = list(filter(f.es_label, content))
print("LABELS DEL ASSEMBLY --->", labels, len(labels))

# Creamos un diccionario cuya llave sea el label y valor sea la direccion
content_sin_data_label = [elemento for elemento in content if elemento not in ("DATA:", "CODE:")]
dict_direccion_label = {}
print("TODO EL CONTENIDO DEL ASSEMBLY SIN DATA: NI CODE: --->", content_sin_data_label)

# Usamos enumerate para obtener el índice y el valor
indice = 0
for valor in content_sin_data_label:
    if valor[:3] == "POP" or valor[:3] == "RET":
        indice += 2
    elif valor in labels:
        dict_direccion_label[valor] = indice
        #print(valor, indice)

    else:
        #print(valor, indice)

        indice += 1

#print("DICT. LLAVE LABEL VALOR DIRECCION --->", dict_direccion_label)

# Separamos en DATA y CODE. 
if "DATA:" in content:
    posicion_data = content.index("DATA:")
else:
    posicion_data = None

posicion_code = content.index("CODE:")

if posicion_data is not None:
    DATA = content[posicion_data + 1:posicion_code]
    for clave in dict_direccion_label: # Agregado 1 noviembre
        dict_direccion_label[clave] -= len(DATA)
    print("DICT. LLAVE LABEL VALOR DIRECCION SI HAY DATA: --->", dict_direccion_label)

CODE = content[posicion_code + 1:]

# QUITAMOS LABELS (NO LOS QUEREMOS PROCESAR, NO SON INSTRUCCIONES)
CODE = [elemento for elemento in CODE if elemento not in labels]
#print("SECCION CODE SIN LABELS --->", CODE)

if posicion_data is not None:
    instrucciones_data = []
    dict_variables = {}
    contador_memoria = 0
    # Creamos un diccionario cuya sea el nombre de la variable definida en segmento DATA, y valor sea el valor que contiene
    # Esto ayudará para aceptar instrucciones del tipo MOV A,(var1)
    for linea in DATA:
        # Obtenemos variable y valor
        variable_valor = linea.split(" ")
        if len(variable_valor) == 1:
            variable = None
            valor = variable_valor[0]
            # Pasamos altiro a binario 
            #valor = f.tratar_casos_formato(valor)
        else:
            variable = variable_valor[0]
            valor = variable_valor[1]
            #valor = f.tratar_casos_formato(valor)
            dict_variables[variable] = valor 

        instrucciones_data.append(f"MOV A,{valor}")
        instrucciones_data.append(f"MOV ({contador_memoria}),A")
        contador_memoria += 1
    #print("DICT LLAVE VARIABLE VALOR VALOR QUE CONTIENE", dict_variables)
    print("INSTRUCCIONES DATA", instrucciones_data)

# Obtenemos todas las instrucciones, las de DATA y las de CODE
if posicion_data is not None:
    instrucciones = instrucciones_data + CODE
else:
    instrucciones_data = []
    instrucciones = CODE


instance = Basys3()

instance.begin()

i = 0
print("\nCODIGO DE MAQUINA:")
for instruccion in instrucciones:
    # Si la instruccion es de tipo salto, JMPs o CALL
    if f.es_instruccion_jump_label(instruccion):
        # Reescribimos instuccion de esta forma: JMP label ---> JMP direccion_label
        if instruccion[:4] == "CALL":
            direccion = dict_direccion_label[instruccion[5:] + ":"] 

            print("label", instruccion[5:] + ":", "direccion", direccion)

            if posicion_data is not None:  # Agregué esto 1 noviembre
                direccion = dict_direccion_label[instruccion[5:] + ":"] + len(instrucciones_data) # Agregué esto 1 noviembre
                print("label", instruccion[5:] + ":", "direccion", direccion)

            instruccion = instruccion[0:5] + str(direccion)
            print(instruccion)
        else:
            direccion = dict_direccion_label[instruccion[4:] + ":"] 
            if posicion_data is not None:  # Agregué esto 1 noviembre
                direccion = dict_direccion_label[instruccion[4:] + ":"] + len(instrucciones_data) # Agregué esto 1 noviembre
            instruccion = instruccion[0:4] + str(direccion)

    # Si es un jump con numero nomas, como por ejemplo: JMP 5
    elif f.es_instruccion_jump(instruccion):
        if posicion_data is not None:
            direccion = int(instruccion[4:]) + len(instrucciones_data)
            instruccion = instruccion[:3] + " " + str(direccion)

    # Tratar casos MOV A, (nombre_var) A = MEM[nombre_var]
    elif f.es_instruccion_con_variable(instruccion):
        nombre_var = f.obtener_contenido(instruccion)
        if nombre_var in dict_variables:
            indice = f.obtener_indice(dict_variables, nombre_var)
            #instruccion = f.reemplazar_variable(instruccion, dict_variables[nombre_var])
            instruccion = f.reemplazar_variable(instruccion, indice)

        else:
            "Nombre de variable no encontrada."  

    # Tratar casos MOV A, nombre_var, y transformar a MOV A, lit, donde lit es la direccion de memoria de 
       

    # OJOOOOO: and i >= len(instrucciones_data): AL AGREGAR ESO NO FUNCIONAN LOS DE LA ETAPA 1
    # ARREGLAR

    elif f.es_instruccion_con_variable_sin_parentesis(instruccion) != False and i >= len(instrucciones_data):
        if f.es_instruccion_con_hexadecimal_binario(instruccion) != False:
            print("CONVERTIMOS EL HEXADECIMAL", instruccion)
            instruccion = f.es_instruccion_con_hexadecimal_binario(instruccion)

        else:
            print("ACAAAA", instruccion)
            nombre_var = f.es_instruccion_con_variable_sin_parentesis(instruccion)

            #if nombre_var in dict_direccion_label:
            if nombre_var in dict_variables:
                direccion = str(list(dict_variables.keys()).index(nombre_var))
            ## ESTO PUEDE ESTAR MAL
            ## LO HAGO PARA LAS INSTRUCCIONES CMP A, nombre_label
            ### REVISARRRRR ###3
            elif nombre_var + ":" in labels: 
                direccion = str(dict_direccion_label[nombre_var + ":"])
                if posicion_data is not None:
                    direccion = str(dict_direccion_label[nombre_var + ":"] + len(instrucciones_data))
            print(instruccion, nombre_var, direccion)
            instruccion = f.reemplazar_label(instruccion, nombre_var, direccion)
            #print(instruccion)

    codigo_maquina = f.traducir_lenguaje(instruccion)

    # Si el codigo maquina es de tipo lista, estamos antes una instruccion POP 
    # La lista contiene cada codigo de maquina para cada ciclo 
    ### VERIFICAR CORRECTO FUNCIONAMIENTO ###
    if isinstance(codigo_maquina, list):
        for codigo in codigo_maquina:
            print(i, codigo, instruccion)
            inst_to_int = int(codigo, 2) # Se interpreta toda la instruccion como un numero entero
            inst_to_bytes = inst_to_int.to_bytes(5, "big") # Se interpreta el numero en 5 bytes, es importante que sea de este largo
            instance.write(i, bytearray(inst_to_bytes))
            i += 1

    else:
        print(i, codigo_maquina, instruccion)

        inst_to_int = int(codigo_maquina, 2) # Se interpreta toda la instruccion como un numero entero
        inst_to_bytes = inst_to_int.to_bytes(5, "big") # Se interpreta el numero en 5 bytes, es importante que sea de este largo
        instance.write(i, bytearray(inst_to_bytes))
        i += 1

instance.end()

