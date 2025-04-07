import re 
import patrones as p

def decimal_a_binario_16bits(numero):
    if numero >= 0:
        binario = format(numero, '016b')  
    else:
        binario = format((1 << 16) + numero, '016b')  

    return binario

def hexadecimal_a_binario_16bits(hexadecimal):
    # Convertir el número hexadecimal a un entero
    numero = int(hexadecimal, 16)
    # Convertir el entero a binario de 16 bits
    binario = format(numero, '016b')
    return binario

def rellenar_bits(registro):
    largo_registro = len(registro)
    if largo_registro < 16:
        cantidad_ceros = 16 - largo_registro
        for i in range(cantidad_ceros):
            registro = "0" + registro
        return registro
    else:
        return registro

def tratar_casos_formato(registro):
    registro = str(registro)

    # Caso binario (no hacemos nada)
    if re.match(r"^\d+b$", registro):
        return rellenar_bits(registro[:-1])
    # Caso decimal (convertimos a binario)
    elif re.match(r"^\d+d$", registro):
        return decimal_a_binario_16bits(int(registro[:-1]))
    elif re.match(r"^\d+$", registro):
        return decimal_a_binario_16bits(int(registro))
    # Caso hexadecimal (convertimos a binario)
    elif re.match(r"^[0-9A-F]+h$", registro):
        return hexadecimal_a_binario_16bits(registro[:-1])

def traducir_lenguaje(instruccion):
    if instruccion == "NOP":
        return "000000000000000000000000000000000000"
    
    elif instruccion == "RET":
        opcode_ciclo1 = "00000000000001011110"
        opcode_ciclo2 = "00000000000001011111"
        ceros = "0000000000000000"
        return [opcode_ciclo1 + ceros, opcode_ciclo2 + ceros]

    # Separamos la instruccion usando la funcion separar instruccion
    separado = separar_instruccion(instruccion)
    # En operacion guardamos el tipo de operacion (MOV, ADD, etc)
    # En reg uno guardamos el valor del registro 1 
    # En reg dos guardamos el valor del registro 2
    operacion = separado[0]
    reg_uno = separado[1]
    # Si solo contiene numeros
    if re.match(r"^\d+$", reg_uno):
        reg_uno = int(reg_uno)

    # Si contiene numeros entre parentesis
    elif re.match(r"^\(\d+\)$", reg_uno):
        reg_uno = int(reg_uno[1:-1])

    elif re.match(r"^\(\d+[bdh]\)$", reg_uno):
        reg_uno = reg_uno[1:-1]

    if len(separado) == 3:
        reg_dos = separado[2]
        if re.match(r"^\d+$", reg_dos):
            reg_dos = int(reg_dos)

        elif re.match(r"^\(\d+\)$", reg_dos):
            reg_dos = int(reg_dos[1:-1])
        
        elif re.match(r"^\(\d+[bdh]\)$", reg_dos):
            reg_dos = reg_dos[1:-1]
    else:
        reg_dos = None
    
    #print(f"Operacion -> {operacion}, Reg_uno -> {reg_uno}, Reg_dos -> {reg_dos}")

    # Vamos operacion por operacion decodificando en lenguaje de maquina

    # NOP
    if re.match(p.pattern_nop, instruccion):
        opcode = "00000000000000000000"
        return opcode + "0000000000000000"

    # MOV
    elif re.match(p.pattern_mov_ab, instruccion):
        opcode = "00000000000000000001"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_mov_ba, instruccion):
        opcode = "00000000000000000010"
        return opcode + "0000000000000000"

    # Esta instruccion es importante, porque manejará las instrucciones de almacenamiento de variables del segmento DATA
    # Hay que tratar los casos de formato, por ejemplo 101b, o 234d, o 135h
    elif re.match(p.pattern_mov_alit, instruccion) or re.match(p.pattern_mov_alit_especial, instruccion):
        opcode = "00000000000000000011"
        lit_a_binario = tratar_casos_formato(reg_dos)
        #lit_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_a_binario

    elif re.match(p.pattern_mov_blit, instruccion):
        opcode = "00000000000000000100"
        lit_b_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_b_binario

    ### REVISAR SI ESTA BIEN TODOS LOS DIR
    elif re.match(p.pattern_mov_adir, instruccion) or re.match(p.pattern_mov_adir_especial, instruccion):
        opcode = "00000000000000000101"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_mov_bdir, instruccion) or re.match(p.pattern_mov_bdir_especial, instruccion):
        opcode = "00000000000000000110"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    ### REVISAR ESTE 

    elif re.match(p.pattern_mov_dir_a, instruccion) or re.match(p.pattern_mov_dir_a_especial, instruccion):
        opcode = "00000000000000000111"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario


    elif re.match(p.pattern_mov_dir_b, instruccion) or re.match(p.pattern_mov_dir_b_especial, instruccion):
        opcode = "00000000000000001000"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "MOV A,(B)":
        opcode = "00000000000001000100"
        return opcode + "0000000000000000"


    elif instruccion == "MOV B,(B)":
        opcode = "00000000000001000101"
        return opcode + "0000000000000000"

    elif instruccion == "MOV (B),A":
        opcode = "00000000000001000110"
        return opcode + "0000000000000000"

    ## REVISAR (NO ESTOY SEGURO DE QUE ESTE VAYA CON EL PATTERN_MOV_PARB_LIT_ESPECIAL)
    elif re.match(p.pattern_mov_parb_lit, instruccion):
    #or re.match(p.pattern_mov_parb_lit_especial, instruccion):
        opcode = "00000000000001000111"
        return opcode + decimal_a_binario_16bits(reg_dos)
    
    # CASO MOV A, variable ---> sería un MOV A, lit, donde lit es direccion de memoria de variable
    #elif re.match(p.pattern_mov_a_variable, instruccion):
    #    opcode = "00000000000000000011"

    #elif re.match(p.pattern_mov_b_variable, instruccion):
    #    opcode = "00000000000000000100"


    # ADD
    elif re.match(p.pattern_add_ab, instruccion):
        opcode = "00000000000000001001"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_add_ba, instruccion):
        opcode = "00000000000000001010"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_add_alit, instruccion):
        opcode = "00000000000000001011"
        lit_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_a_binario

    elif re.match(p.pattern_add_blit, instruccion):
        opcode = "00000000000000001100"
        lit_b_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_b_binario

    elif re.match(p.pattern_add_adir, instruccion) or re.match(p.pattern_add_adir_especial, instruccion):
        opcode = "00000000000000001101"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario
    
    elif re.match(p.pattern_add_bdir, instruccion) or re.match(p.pattern_add_bdir_especial, instruccion):
        opcode = "00000000000000001110"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_add_dir, instruccion) or re.match(p.pattern_add_dir_especial, instruccion):
        opcode = "00000000000000001111"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "ADD A,(B)":
        opcode = "00000000000001001000"
        return opcode + "0000000000000000"

    elif instruccion == "ADD B,(B)":
        opcode = "00000000000001001001"
        return opcode + "0000000000000000"

    # SUB
    elif re.match(p.pattern_sub_ab, instruccion):
        opcode = "00000000000000010000"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_sub_ba, instruccion):
        opcode = "00000000000000010001"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_sub_alit, instruccion):
        opcode = "00000000000000010010"
        lit_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_a_binario

    elif re.match(p.pattern_sub_blit, instruccion):
        opcode = "00000000000000010011"
        lit_b_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_b_binario

    elif re.match(p.pattern_sub_adir, instruccion) or re.match(p.pattern_sub_adir_especial, instruccion):
        opcode = "00000000000000010100"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_sub_bdir, instruccion) or re.match(p.pattern_sub_bdir_especial, instruccion):
        opcode = "00000000000000010101"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_sub_dir, instruccion) or re.match(p.pattern_sub_dir_especial, instruccion):
        opcode = "00000000000000010110"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "SUB A,(B)":
        opcode = "00000000000001001010"
        return opcode + "0000000000000000"

    elif instruccion == "SUB B,(B)":
        opcode = "00000000000001001011"
        return opcode + "0000000000000000"

    # AND
    elif re.match(p.pattern_and_ab, instruccion):
        opcode = "00000000000000010111"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_and_ba, instruccion):
        opcode = "00000000000000011000"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_and_alit, instruccion):
        opcode = "00000000000000011001"
        lit_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_a_binario

    elif re.match(p.pattern_and_blit, instruccion):
        opcode = "00000000000000011010"
        lit_b_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_b_binario

    elif re.match(p.pattern_and_adir, instruccion) or re.match(p.pattern_and_adir_especial, instruccion):
        opcode = "00000000000000011011"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_and_bdir, instruccion) or re.match(p.pattern_and_bdir_especial, instruccion):
        opcode = "00000000000000011100"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_and_dir, instruccion) or re.match(p.pattern_and_dir_especial, instruccion):
        opcode = "00000000000000011101"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "AND A,(B)":
        opcode = "00000000000001001100"
        return opcode + "0000000000000000"

    elif instruccion == "AND B,(B)":
        opcode = "00000000000001001101"
        return opcode + "0000000000000000"

    # OR
    elif re.match(p.pattern_or_ab, instruccion):
        opcode = "00000000000000011110"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_or_ba, instruccion):
        opcode = "00000000000000011111"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_or_alit, instruccion):
        opcode = "00000000000000100000"
        lit_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_a_binario

    elif re.match(p.pattern_or_blit, instruccion):
        opcode = "00000000000000100001"
        lit_b_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_b_binario

    elif re.match(p.pattern_or_adir, instruccion) or re.match(p.pattern_or_adir_especial, instruccion):
        opcode = "00000000000000100010"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_or_bdir, instruccion) or re.match(p.pattern_or_bdir_especial, instruccion):
        opcode = "00000000000000100011"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_or_dir, instruccion) or re.match(p.pattern_or_dir_especial, instruccion):
        opcode = "00000000000000100100"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "OR A,(B)":
        opcode = "00000000000001001110"
        return opcode + "0000000000000000"

    elif instruccion == "OR B,(B)":
        opcode = "00000000000001001111"
        return opcode + "0000000000000000"

    # XOR
    elif re.match(p.pattern_xor_ab, instruccion):
        opcode = "00000000000000100101"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_xor_ba, instruccion):
        opcode = "00000000000000100110"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_xor_alit, instruccion):
        opcode = "00000000000000100111"
        lit_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_a_binario

    elif re.match(p.pattern_xor_blit, instruccion):
        opcode = "00000000000000101000"
        lit_b_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + lit_b_binario

    elif re.match(p.pattern_xor_adir, instruccion) or re.match(p.pattern_xor_adir_especial, instruccion):
        opcode = "00000000000000101001"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_xor_bdir, instruccion) or re.match(p.pattern_xor_bdir_especial, instruccion):
        opcode = "00000000000000101010"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario
    
    elif re.match(p.pattern_xor_dir, instruccion) or re.match(p.pattern_xor_dir_especial, instruccion):
        opcode = "00000000000000101011"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "XOR A,(B)":
        opcode = "00000000000001010000"
        return opcode + "0000000000000000"

    elif instruccion == "XOR B,(B)":
        opcode = "00000000000001010001"
        return opcode + "0000000000000000"
    
    # NOT
    elif re.match(p.pattern_not_a, instruccion):
        opcode = "00000000000000101100"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_not_ba, instruccion):
        opcode = "00000000000000101101"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_not_dir_a, instruccion) or re.match(p.pattern_not_dir_a_especial, instruccion):
        opcode = "00000000000000101110"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "NOT (B),A":
        opcode = "00000000000001010010"
        return opcode + "0000000000000000"

    # SHL 
    elif re.match(p.pattern_shl_a, instruccion):
        opcode = "00000000000000101111"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_shl_ba, instruccion):
        opcode = "00000000000000110000"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_shl_dir_a, instruccion) or re.match(p.pattern_shl_dir_a_especial, instruccion):
        opcode = "00000000000000110001"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "SHL (B),A":
        opcode = "00000000000001010011"
        return opcode + "0000000000000000"


    # SHR 
    elif re.match(p.pattern_shr_a, instruccion):
        opcode = "00000000000000110010"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_shr_ba, instruccion):
        opcode = "00000000000000110011"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_shr_dir_a, instruccion) or re.match(p.pattern_shr_dir_a_especial, instruccion):
        opcode = "00000000000000110100"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    elif instruccion == "SHR (B),A":
        opcode = "00000000000001010100"
        return opcode + "0000000000000000"

    # INC Hay que poner opcode de suma 
    elif re.match(p.pattern_inc_a, instruccion):
        opcode = "00000000000000001011" 
        return opcode + "0000000000000001" # LIT sería igual a 1

    # INC B
    elif re.match(p.pattern_inc_b, instruccion):
        opcode = "00000000000000110110" # OPCODE DE ADD B, LIT
        return opcode + "0000000000000000"

    # INC DIR (NO LO CAMBIÉ, CREO QUE ASÍ ESTA BIEN)
    ### REVISAR ESTE SI HAY QUE HACERLE LOS CAMBIOS ###
    elif re.match(p.pattern_inc_dir, instruccion) or re.match(p.pattern_inc_dir_especial, instruccion):
        opcode = "00000000000000110111"
        litdir_a_binario = tratar_casos_formato(reg_uno)
        #litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario    
    
    elif instruccion == "INC (B)":
        opcode = "00000000000001010101"
        return opcode + "0000000000000000"

    # DEC
    elif re.match(p.pattern_dec_a, instruccion):
        opcode = "00000000000000010010"
        return opcode + "0000000000000001"

    # CMP
    elif re.match(p.pattern_cmp_ab, instruccion):
        opcode = "00000000000000111001"
        return opcode + "0000000000000000"

    elif re.match(p.pattern_cmp_alit, instruccion):
        opcode = "00000000000000111010"
        litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_cmp_adir, instruccion) or re.match(p.pattern_cmp_adir_especial, instruccion):
        opcode = "00000000000000111011"
        litdir_a_binario = tratar_casos_formato(reg_dos)
        #litdir_a_binario = decimal_a_binario_16bits(reg_dos)
        return opcode + litdir_a_binario
    
    elif re.match(p.pattern_cmp_a_parb, instruccion):
        opcode = "00000000000001010110"
        return opcode + "0000000000000000"


    # JMP 
    # JMP label 
    elif re.match(p.pattern_jmp_dir, instruccion):
        opcode = "00000000000000111100"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_jeq_dir, instruccion):
        opcode = "00000000000000111101"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_jne_dir, instruccion):
        opcode = "00000000000000111110"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_jgt_dir, instruccion):
        opcode = "00000000000000111111"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_jge_dir, instruccion):
        opcode = "00000000000001000000"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_jlt_dir, instruccion):
        opcode = "00000000000001000001"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_jle_dir, instruccion):
        opcode = "00000000000001000010"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario

    elif re.match(p.pattern_jcr_dir, instruccion):
        opcode = "00000000000001000011"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
    # PUSH

    elif instruccion == "PUSH A":
        opcode = "00000000000001010111"
        return opcode + "0000000000000000"
    
    elif instruccion == "PUSH B":
        opcode = "00000000000001011000"
        return opcode + "0000000000000000"
    
    # POP 
    elif instruccion == "POP A":
        opcode_ciclo1 = "00000000000001011001"
        opcode_ciclo2 = "00000000000001011010"
        ceros = "0000000000000000"
        return [opcode_ciclo1 + ceros, opcode_ciclo2 + ceros]
    
    elif instruccion == "POP B":
        opcode_ciclo1 = "00000000000001011011"
        opcode_ciclo2 = "00000000000001011100"
        ceros = "0000000000000000"
        return [opcode_ciclo1 + ceros, opcode_ciclo2 + ceros]

    # CALL
    elif re.match(p.pattern_call, instruccion):
        opcode = "00000000000001011101"
        litdir_a_binario = decimal_a_binario_16bits(reg_uno)
        return opcode + litdir_a_binario
    
def separar_instruccion(instruccion):
    separado = instruccion.split(" ")
    registros = separado[1].split(",")
    lista = [separado[0]] + registros
    return lista

def es_label(texto):
    # Expresión regular que verifica que el texto termine en ':' pero no sea 'DATA:' ni 'CODE:'
    regex = r"^(?!DATA:|CODE:)[\w\s]+:$"
    return re.match(regex, texto) is not None

def es_instruccion_jump_label(texto):
    # Expresión regular que verifica los primeros 3 caracteres
    #regex = r"^(JMP|JEQ|JNE|JGT|JGE|JLT|JLE|JCR|CALL)"
    #regex = "^(JMP|JEQ|JNE|JGT|JGE|JLT|JLE|JCR|CALL) [A-Za-z0-9]*[A-Za-z][A-Za-z0-9]*$"

    # Acepta guion bajo 
    regex = r"^(JMP|JEQ|JNE|JGT|JGE|JLT|JLE|JCR|CALL) [A-Za-z0-9_][A-Za-z0-9_]*$"
    regex_invalido = r"^(JMP|JEQ|JNE|JGT|JGE|JLT|JLE|JCR|CALL) \d+$"
    if re.match(regex_invalido, texto):
        return False
    return re.match(regex, texto) is not None

def es_instruccion_jump(texto):
    regex = "^(JMP|JEQ|JNE|JGT|JGE|JLT|JLE|JCR) \d+$"
    return re.match(regex, texto) is not None

def es_instruccion_con_variable(texto):
    # Si es del tipo Instruccion A, (dir) y dir no tiene solo numeros, retornamos true
    if (re.match(r"^(MOV|ADD|SUB|AND|OR|XOR|CMP)\s+A,\s*\([a-zA-Z0-9]+\)$", texto)):
        return dir_nocontiene_solo_numeros(texto)
    # Si es del tipo Instruccion B, (dir)
    if (re.match(r"^(MOV|ADD|SUB|AND|OR|XOR)\s+B,\s*\([a-zA-Z0-9]+\)$", texto)):
        return dir_nocontiene_solo_numeros(texto)
    # Si es del tipo Instruccion (dir), A
    if (re.match(r"^(MOV|NOT|SHL|SHR)\s+\([a-zA-Z0-9]+\),\s*A\s*$", texto)):
        return dir_nocontiene_solo_numeros(texto)
    # Si es mov (dir),B
    if (re.match(r"^MOV\s+\([a-zA-Z0-9]+\),\s*B\s*$", texto)):
        return dir_nocontiene_solo_numeros(texto)
    # Si es Instruccion (dir)
    if (re.match(r"^(ADD|SUB|AND|OR|XOR|INC)\s+\([a-zA-Z0-9]+\)\s*$", texto)):
        return dir_nocontiene_solo_numeros(texto)
    
def dir_nocontiene_solo_numeros(ins):
    dir = obtener_contenido(ins)
    if dir == "B":
        return False
    if not dir.isdigit():
        return True
    else:
        return False

def es_comentario(texto):
    # Expresión regular que verifica si el texto comienza con //
    regex = r"^//"
    return re.match(regex, texto) is not None

def contiene_comentario(texto):
    # Verificamos si el símbolo '//' está en el texto
    if '//' in texto:
        # Si contiene '//' dividimos y tomamos la parte antes del comentario, quitando espacios finales
        return texto.split('//')[0].rstrip()
    else:
        # Si no contiene '//' devolvemos el texto original sin modificar
        return texto
    
# Sirve para tratar espacios en blanco
def normalizar_espacios(texto):
    # Normalizamos los espacios entre palabras
    texto_normalizado = " ".join(texto.split())
    
    # Eliminamos espacios alrededor de las comas
    texto_sin_espacios_comas = re.sub(r"\s*,\s*", ",", texto_normalizado)
    
    # Eliminamos espacios dentro de paréntesis
    texto_final = re.sub(r"\(\s*(.*?)\s*\)", r"(\1)", texto_sin_espacios_comas)
    
    return texto_final

def reemplazar_variable(texto, valor_variable):
    # Usamos regex para capturar cualquier cosa dentro de los paréntesis
    return re.sub(r'\(.*?\)', f'({valor_variable})', texto)


def obtener_contenido(texto):
    # Usamos regex para capturar el contenido dentro de los paréntesis
    coincidencia = re.search(r'\((.*?)\)', texto)
    if coincidencia:
        return coincidencia.group(1)  # Retorna el contenido encontrado
    return None  # Retorna None si no hay contenido en paréntesis

def obtener_indice(diccionario, clave):
    claves = list(diccionario.keys())  # Convertimos las claves a una lista
    if clave in claves:
        return claves.index(clave)  # Retornamos el índice de la clave
    return None  # Retornamos None si la clave no está en el diccionario

    
def es_instruccion_con_variable_sin_parentesis(texto):
    # Si es del tipo Instruccion A, dir y dir no tiene solo numeros, retornamos true
    if texto == "CMP A,B":
        return False
    
    if re.match(r"^(MOV|ADD|SUB|AND|OR|XOR|CMP)\s+A,\s*[a-zA-Z0-9]+$", texto):

        if re.match(r"^OR\s", texto):
            dir = texto[5:]
            if es_numerico(dir):

                return False
            elif dir == "B":
                return False
            else:

                return dir
        else:
            dir = texto[6:]
            if es_numerico(dir):
                return False
            elif dir == "B":
                return False
            else:
                return dir

    # Si es del tipo Instruccion B, dir
    elif re.match(r"^(MOV|ADD|SUB|AND|OR|XOR)\s+B,\s*[a-zA-Z0-9]+$", texto):
        if re.match(r"^OR\s", texto):
            dir = texto[5:]
            if es_numerico(dir):
                return False
            elif dir == "A":
                return False
            
            else:
                return dir
        else:
            dir = texto[6:]
            if es_numerico(dir):
                return False
            elif dir == "A":
                return False
            else:
                return dir
            
    elif re.match(r"^MOV\s+\(B\),\s*(?=.*[a-zA-Z])[a-zA-Z0-9]+$", texto):
        dir = texto[8:]
        if es_numerico(dir):
            return False
        if dir == "A" or dir == "(B)":
            return False
        else:
            return dir
    return False

def es_instruccion_con_hexadecimal_binario(texto):

    if re.match(r'^(MOV|ADD|SUB|AND|OR|XOR|CMP)\s+A\s*,\s*[0-9A-F]+h$', texto) or re.match(r'^(MOV|ADD|SUB|AND|OR|XOR)\s+B\s*,\s*[0-9A-F]+h$', texto):
        print("Instrucción válida:", texto)
        valor_hexadecimal = texto.split(",")[-1].strip()[:-1]  # Obtener el valor sin 'h'
        valor_decimal = int(valor_hexadecimal, 16)  # Convertir a decimal
        # Reemplazar el valor hexadecimal en el texto por el decimal
        texto_modificado = texto.replace(valor_hexadecimal + 'h', str(valor_decimal))
        print("TTRTT", texto_modificado)
        return texto_modificado
    
    elif re.match(r'^(MOV|ADD|SUB|AND|OR|XOR)\s+A\s*,\s*[01]+b$', texto) or re.match(r'^(MOV|ADD|SUB|AND|OR|XOR)\s+B\s*,\s*[01]+b$', texto):
        # Manejo de binario
        valor_binario = texto.split(",")[-1].strip()[:-1]  # Obtener el valor sin 'b'
        valor_decimal = int(valor_binario, 2)  # Convertir a decimal
        texto_modificado = texto.replace(valor_binario + 'b', str(valor_decimal))
        return texto_modificado
    

    else:
        return False

def es_numerico(dir):
    return dir.isdigit()


def obtener_dir(texto):
    # Verificamos el patrón para MOV dir,A
    match = re.match(r"^(MOV|NOT|SHL|SHR)\s+([a-zA-Z0-9_]+),\s*A$", texto)
    if match:
        return match.group(2)  # Retorna el valor de dir

    return None  # Retorna None si no coincide

def reemplazar_label(string1, string2, string3):
    # Reemplaza todas las ocurrencias de string2 en string1 por string3
    return string1.replace(string2, string3)