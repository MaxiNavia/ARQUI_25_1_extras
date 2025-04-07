import re

def contiene_comentario(texto):
    # Dividimos el string en la parte antes de '//' y retornamos solo esa parte sin espacios extra al final
    return texto.split('//')[0].rstrip()

# Ejemplo de uso
texto = "x            3          // Se guarda en direccion 0     MOV A,3     y MOV (0),A"
resultado = contiene_comentario(texto)
print(resultado)  # "x            3"
