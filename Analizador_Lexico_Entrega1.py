import ply.lex as lex
import re
import codecs
import os
import sys

#PASO 1- DEFINO LOS TOKENS
tokens = (
    'ID','STRINGD','INTEGER','FLOATD','MINUS','PLUS','MULT','DIVIDE','REST','ASSIGN'
    ,'NE','LT','LTE','GT','GTE','EQUAL','LBRA','RBRA','COMMA','ENDL'
    ,'OP_BRA','CL_BRA','COLON','OP_BRC','CL_BRC'
)
#PASO 2- DEFINO LAS PALABRAS RESERVADAS
reserved = {
'if'     :'IF',
'else'   :'ELSE',
'while'  :'WHILE',
'and'    :'AND',
'or'     :'OR',
'write'  :'WRITE',
'read'   :'READ',
'DECVAR' :'DECVAR',
'ENDDEC' :'ENDDEC',
'between':'BETWEEN',
'take'   :'TAKE',
'INT'    :'INT',
'FLOAT'  :'FLOAT',
'STRING' :'STRING',
}
#PASO 3 ESPECIFICO QUE VALOR ES CADA TOKEN 
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIVIDE = r'\/'
t_REST = r'\%'
t_ASSIGN = r'\:\='
t_NE = r'\!\='
t_LT = r'\<'
t_LTE = r'\<\='
t_GT = r'\>'
t_GTE = r'\>\='
t_EQUAL = r'\='
t_LBRA = r'\('
t_RBRA = r'\)'
t_COMMA = r'\,'
t_ENDL = r'\;'
t_OP_BRA = r'\{'
t_CL_BRA = r'\}'
t_OP_BRC = r'\['
t_CL_BRC = r'\]'
t_COLON= r'\:'

def t_FLOATD(t):
    r'[0-9]*\.[0-9]+'
    t.value = float(t.value)
    if( t.value >(3.4028237*(10^38))  or t.value <(1.175494*(10^-38)) ):
        t.lexer.skip(1)
        print(
         '''
         Error Léxico:
            Linea: '%f'
            Tipo: El caracter ingresado no se encuentra dentro de los limite de un float32
         '''%t.lexer.lineno)           
        return None    

    return t 
    
def t_INTEGER(t):
    r'-?[0-9]+'
    t.value = int(t.value)
    if( t.value >32767 or t.value <-32767):
        t.lexer.skip(1)
        print(
         '''
         Error Léxico:
            Linea: '%d'
            Tipo: El caracter ingresado no se encuentra dentro de los limite de un entero
         '''%t.lexer.lineno)           
        return None    
    return t

def t_STRINGD(t):
    r'\"[A-Za-z0-9 ]*\"'
    t.value = str(t.value)
    if(len(t.value)>30):
        t.lexer.skip(1)
        print("La cadena ingresada '%s' supera el máximo de caracteres permitido" %t.value)
        return None  
    return t 

def t_ID(t):
    r'[A-Za-z].[A-Za-z0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

t_ignore = ' \t ' #Ignora espacios y tabulaciones

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) #Le suma al lexer los enters para el error



def t_error(t):
    print("El caracter ingresado '%s' no es valido" %t.value[0])
    t.lexer.skip(1)    

# Comentario simple // ...
def t_comentario(t):
    r'\-\/[\w\s]*\/\-\n'
    t.lexer.lineno += 1

#PASO 4: Añado la lista de reservados a los tokens
tokens = list(tokens) + list(reserved.values())
t_IF = r'if'
t_ELSE = r'else'
t_WHILE= r'while'
t_AND = r'and'
t_OR=  r'or'
t_WRITE = r'write'
t_READ = r'read'
t_DECVAR = r'decvar'
t_ENDDEC = r'enddec'
t_BETWEEN = r'between'
t_TAKE = r'take'
t_INT = r'int'
t_FLOAT = r'float'
t_STRING = r'string'

#PASO 5: Crear el Lexer

# resultado del analisis
resultado_lexema = []

def testLexer(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos) )
        resultado_lexema.append(estado)
    return resultado_lexema


 # instanciamos el analizador lexico
analizador = lex.lex()

if __name__ == '__main__':
    while True:
        data = input("ingrese: ")
        testLexer(data)
        print(resultado_lexema)    